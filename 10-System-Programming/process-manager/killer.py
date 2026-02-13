"""
Killer Module - Terminazione dei processi

Questo modulo fornisce funzionalità per terminare processi in modo sicuro,
con supporto per diversi segnali e conferme.

Concetti educativi:
- Signals: Meccanismo di comunicazione inter-processo (IPC)
- SIGTERM: Termination signal (15) - permette cleanup graceful
- SIGKILL: Kill signal (9) - terminazione immediata forzata
- Process Lifecycle: Stati di terminazione e zombie process
- Permission Checks: UID/GID per verificare permessi di terminazione

AVVERTENZA: Terminare processi di sistema può causare instabilità!
"""

import os
import signal
import psutil
import time
from typing import Optional, List
from enum import Enum

from process import ProcessInfo, ProcessManager


class TerminateMethod(Enum):
    """Metodi di terminazione dei processi"""
    SIGTERM = "SIGTERM (15) - Termination request"
    SIGKILL = "SIGKILL (9) - Immediate termination"
    SIGINT = "SIGINT (2) - Interrupt (Ctrl+C)"
    SIGSTOP = "SIGSTOP (19) - Stop/pause process"
    SIGCONT = "SIGCONT (18) - Continue stopped process"


class TerminationResult(Enum):
    """Risultati dell'operazione di terminazione"""
    SUCCESS = "Processo terminato con successo"
    ALREADY_DEAD = "Il processo era già terminato"
    ACCESS_DENIED = "Permesso negato (richiede root/sudo)"
    NOT_FOUND = "Processo non trovato"
    ZOMBIE = "Processo zombie (già terminato)"
    FAILED = "Terminazione fallita"


class ProcessKiller:
    """
    Gestore per la terminazione dei processi.

    Fornisce metodi sicuri per terminare processi con conferme e logging.
    """

    def __init__(self, require_confirmation: bool = True):
        """
        Inizializza il ProcessKiller.

        Args:
            require_confirmation: Se True, richiede conferma prima di terminare
        """
        self.require_confirmation = require_confirmation
        self.manager = ProcessManager()

    def kill_by_pid(self, pid: int,
                   method: TerminateMethod = TerminateMethod.SIGTERM,
                   force: bool = False) -> TerminationResult:
        """
        Termina un processo per PID.

        Args:
            pid: PID del processo
            method: Metodo di terminazione
            force: Se True, salta la conferma

        Returns:
            TerminationResult

        Concetti:
        - SIGTERM: Permette al processo di fare cleanup prima di terminare
        - SIGKILL: Termina immediatamente senza cleanup (usa con cautela!)
        """
        # Verifica se il processo esiste
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return TerminationResult.NOT_FOUND

        # Ottieni info per la conferma
        proc_info = self.manager.get_process_by_pid(pid)

        if not force and self.require_confirmation:
            print(f"\n⚠️  Sei sicuro di voler terminare questo processo?")
            print(f"   PID: {pid}")
            print(f"   Nome: {proc_info.name if proc_info else 'N/A'}")
            print(f"   CPU: {proc_info.cpu_percent if proc_info else 0:.1f}%")
            print(f"   Memoria: {proc_info.memory_mb if proc_info else 0:.1f} MB")
            print(f"   Metodo: {method.value}")

            response = input("\n   Terminare? (s/N): ").strip().lower()
            if response not in ['s', 'si', 'y', 'yes']:
                print("   ❌ Operazione annullata")
                return TerminationResult.FAILED

        # Esegui la terminazione
        return self._terminate(proc, method)

    def kill_by_name(self, name: str,
                     method: TerminateMethod = TerminateMethod.SIGTERM,
                     kill_all: bool = False,
                     force: bool = False) -> List[tuple]:
        """
        Termina processi per nome.

        Args:
            name: Nome del processo
            method: Metodo di terminazione
            kill_all: Se True, termina tutte le istanze
            force: Se True, salta le conferme

        Returns:
            Lista di tuple (pid, result)

        Concetto: Può esserci più di un processo con lo stesso nome
        """
        processes = self.manager.search_processes(name)

        if not processes:
            print(f"Nessun processo trovato con nome: {name}")
            return []

        if not kill_all and len(processes) > 1:
            print(f"Trovati {len(processes)} processi con nome '{name}':")
            for i, p in enumerate(processes[:10], 1):
                print(f"  [{i}] PID {p.pid}: CPU {p.cpu_percent:.1f}%, MEM {p.memory_mb:.1f} MB")

            choice = input(f"\nQuale processo terminare? (1-{min(len(processes), 10)}, o 'all' per tutti): ")
            if choice.lower() == 'all':
                kill_all = True
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(processes):
                        processes = [processes[idx]]
                    else:
                        print("Scelta non valida")
                        return []
                except ValueError:
                    print("Scelta non valida")
                    return []

        results = []
        for proc in processes:
            result = self.kill_by_pid(proc.pid, method, force)
            results.append((proc.pid, result))

        return results

    def kill_tree(self, root_pid: int,
                  method: TerminateMethod = TerminateMethod.SIGTERM,
                  force: bool = False) -> List[tuple]:
        """
        Termina un albero di processi (padre e tutti i figli).

        Args:
            root_pid: PID del processo radice
            method: Metodo di terminazione
            force: Se True, salta le conferme

        Returns:
            Lista di tuple (pid, result)

        Concetto: Quando termini un processo, i figli possono diventare orfani
        - Terminare prima i figli previene zombie processes
        - Oppure terminare il padre e lasciare che init adotti i figli
        """
        try:
            root_proc = psutil.Process(root_pid)
        except psutil.NoSuchProcess:
            print(f"Processo {root_pid} non trovato")
            return []

        # Ottieni tutti i discendenti
        try:
            descendants = root_proc.children(recursive=True)
        except psutil.NoSuchProcess:
            descendants = []

        # Ordina: prima i discendenti, poi la radice
        pids_to_kill = [p.pid for p in descendants] + [root_pid]

        if not force and self.require_confirmation:
            print(f"\n⚠️  Terminazione albero processi: {len(pids_to_kill)} processi")
            print(f"   PID radice: {root_pid}")
            print(f"   Discendenti: {len(descendants)}")
            response = input("\n   Continuare? (s/N): ").strip().lower()
            if response not in ['s', 'si', 'y', 'yes']:
                print("   ❌ Operazione annullata")
                return []

        results = []
        for pid in pids_to_kill:
            result = self._terminate_by_pid(pid, method)
            results.append((pid, result))

        return results

    def _terminate(self, proc: psutil.Process,
                  method: TerminateMethod) -> TerminationResult:
        """
        Termina un processo usando il metodo specificato.

        Args:
            proc: Oggetto Process psutil
            method: Metodo di terminazione

        Returns:
            TerminationResult
        """
        try:
            # Controlla lo stato del processo
            if proc.status() == psutil.STATUS_ZOMBIE:
                return TerminationResult.ZOMBIE

            # Mappa il metodo al signal appropriato
            signal_map = {
                TerminateMethod.SIGTERM: signal.SIGTERM,
                TerminateMethod.SIGKILL: signal.SIGKILL,
                TerminateMethod.SIGINT: signal.SIGINT,
                TerminateMethod.SIGSTOP: signal.SIGSTOP,
                TerminateMethod.SIGCONT: signal.SIGCONT,
            }

            sig = signal_map.get(method)

            if method == TerminateMethod.SIGKILL:
                # SIGKILL: Terminazione immediata
                proc.kill()
            elif method == TerminateMethod.SIGSTOP:
                # SIGSTOP: Metti in pausa
                proc.send_signal(sig)
            elif method == TerminateMethod.SIGCONT:
                # SIGCONT: Riprendi
                proc.send_signal(sig)
            else:
                # SIGTERM/SIGINT: Richiesta di terminazione
                proc.send_signal(sig)

                # Aspetta che termini (max 5 secondi)
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    # Ancora in esecuzione, prova con SIGKILL
                    print(f"   ⚠️  Processo non risponde, uso SIGKILL...")
                    proc.kill()
                    proc.wait(timeout=2)

            return TerminationResult.SUCCESS

        except psutil.AccessDenied:
            return TerminationResult.ACCESS_DENIED
        except psutil.NoSuchProcess:
            return TerminationResult.ALREADY_DEAD
        except Exception as e:
            print(f"   ❌ Errore: {e}")
            return TerminationResult.FAILED

    def _terminate_by_pid(self, pid: int,
                         method: TerminateMethod) -> TerminationResult:
        """Termina un processo per PID (wrapper interno)"""
        try:
            proc = psutil.Process(pid)
            return self._terminate(proc, method)
        except psutil.NoSuchProcess:
            return TerminationResult.NOT_FOUND

    def safe_kill_list(self, pids: List[int],
                      method: TerminateMethod = TerminateMethod.SIGTERM,
                      force: bool = False) -> dict:
        """
        Termina una lista di PID con controlli di sicurezza.

        Args:
            pids: Lista di PID
            method: Metodo di terminazione
            force: Se True, salta le conferme

        Returns:
            Dizionario con risultati

        Concetto: Safety checks per evitare di terminare processi critici
        """
        dangerous_pids = [1, 2]  # init/systemd, kthreadd
        safe_pids = []

        for pid in pids:
            if pid in dangerous_pids:
                print(f"⚠️  SKIP: PID {pid} è un processo di sistema critico!")
                continue
            safe_pids.append(pid)

        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }

        for pid in safe_pids:
            result = self.kill_by_pid(pid, method, force)
            if result == TerminationResult.SUCCESS:
                results['success'].append((pid, result))
            elif result == TerminationResult.ACCESS_DENIED:
                results['failed'].append((pid, result))
            else:
                results['skipped'].append((pid, result))

        return results


def print_termination_result(result: TerminationResult) -> None:
    """Stampa il risultato della terminazione con emoji appropriate"""
    emoji_map = {
        TerminationResult.SUCCESS: "✅",
        TerminationResult.ALREADY_DEAD: "💀",
        TerminationResult.ACCESS_DENIED: "🔒",
        TerminationResult.NOT_FOUND: "❓",
        TerminationResult.ZOMBIE: "🧟",
        TerminationResult.FAILED: "❌"
    }

    emoji = emoji_map.get(result, "❓")
    print(f"   {emoji} {result.value}")


# Funzioni helper per compatibilità
def kill_process(pid: int, force: bool = False) -> TerminationResult:
    """Funzione helper per terminare un processo"""
    killer = ProcessKiller(require_confirmation=not force)
    return killer.kill_by_pid(pid, TerminateMethod.SIGTERM, force)


if __name__ == '__main__':
    # Test del modulo (ATTENZIONE: è un test reale!)
    print("=== Test Killer Module ===\n")
    print("⚠️  ATTENZIONE: Questo modulo terminerebbe processi reali!")
    print("✓ Modulo caricato correttamente (nessun processo terminato)\n")

    # Mostra i metodi disponibili
    print("Metodi di terminazione disponibili:")
    for method in TerminateMethod:
        print(f"  - {method.value}")

    print("\n✓ Module test completed (safe mode)!")
