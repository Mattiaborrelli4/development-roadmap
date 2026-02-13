"""
Process Module - Gestione dei processi per il Process Manager

Questo modulo fornisce funzioni per ottenere informazioni sui processi,
inclusi PID, nome, utilizzo CPU, memoria e dettagli aggiuntivi.

Concetti educativi:
- PID (Process ID): Identificatore univoco del processo
- PPID (Parent PID): Identificatore del processo padre
- CPU Percent: Percentuale di utilizzo della CPU
- Memory Percent: Percentuale di memoria utilizzata
- Process State: Stati del processo (running, sleeping, etc.)
"""

import psutil
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessInfo:
    """Classe dati per le informazioni del processo"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    ppid: int
    num_threads: int
    create_time: float

    def to_dict(self) -> Dict:
        """Converte in dizionario per facile accesso"""
        return {
            'pid': self.pid,
            'name': self.name,
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_mb': self.memory_mb,
            'status': self.status,
            'ppid': self.ppid,
            'num_threads': self.num_threads,
            'create_time': self.create_time
        }


class ProcessManager:
    """
    Gestore principale per le operazioni sui processi.

    Fornisce metodi per listare, filtrare e ottenere dettagli sui processi.
    """

    def __init__(self):
        """Inizializza il ProcessManager"""
        self.cached_processes: Dict[int, ProcessInfo] = {}

    def get_all_processes(self, cache: bool = False) -> List[ProcessInfo]:
        """
        Ottiene tutti i processi in esecuzione.

        Args:
            cache: Se True, usa la cache se disponibile

        Returns:
            Lista di ProcessInfo

        Concetto: psutil.process_iter() itera su tutti i processi attivi
        Nota: Alcuni processi potrebbero terminare durante l'iterazione
        """
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent',
                                         'status', 'ppid', 'num_threads', 'create_time']):
            try:
                # Ottieni le info base del processo
                pinfo = proc.info

                # Calcola memoria in MB
                memory_mb = proc.memory_info().rss / (1024 * 1024)

                # Crea oggetto ProcessInfo
                process = ProcessInfo(
                    pid=pinfo['pid'],
                    name=pinfo['name'],
                    cpu_percent=pinfo['cpu_percent'] or 0.0,
                    memory_percent=pinfo['memory_percent'] or 0.0,
                    memory_mb=memory_mb,
                    status=pinfo['status'],
                    ppid=pinfo['ppid'],
                    num_threads=pinfo['num_threads'],
                    create_time=pinfo['create_time']
                )

                processes.append(process)
                self.cached_processes[process.pid] = process

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Il processo potrebbe terminare durante l'iterazione
                continue

        return processes

    def get_process_by_pid(self, pid: int) -> Optional[ProcessInfo]:
        """
        Ottiene informazioni su un processo specifico dato il suo PID.

        Args:
            pid: Process ID

        Returns:
            ProcessInfo se trovato, None altrimenti

        Concetto: Ogni processo ha un PID univoco assegnato dal kernel
        """
        try:
            proc = psutil.Process(pid)

            memory_mb = proc.memory_info().rss / (1024 * 1024)

            return ProcessInfo(
                pid=proc.pid,
                name=proc.name(),
                cpu_percent=proc.cpu_percent(),
                memory_percent=proc.memory_percent(),
                memory_mb=memory_mb,
                status=proc.status(),
                ppid=proc.ppid(),
                num_threads=proc.num_threads(),
                create_time=proc.create_time()
            )

        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied:
            return None

    def get_process_details(self, pid: int) -> Optional[Dict]:
        """
        Ottiene dettagli estesi su un processo:
        - File aperti
        - Connessioni di rete
        - Thread attivi
        - Contesto utente

        Args:
            pid: Process ID

        Returns:
            Dizionario con dettagli estesi

        Concetti educativi:
        - File Descriptors: Ogni processo ha una tabella di file aperti
        - Socket Connections: Connessioni TCP/UDP attive
        - User Context: UID, GID, permessi del processo
        """
        try:
            proc = psutil.Process(pid)

            details = {
                'basic': {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'exe': proc.exe() if proc.exe() else 'N/A',
                    'cwd': proc.cwd() if proc.cwd() else 'N/A',
                    'cmdline': proc.cmdline(),
                    'status': proc.status(),
                },
                'user': {
                    'username': proc.username(),
                    'uids': proc.uids()._asdict(),
                    'gids': proc.gids()._asdict(),
                },
                'timing': {
                    'create_time': datetime.fromtimestamp(proc.create_time()).isoformat(),
                    'cpu_times': proc.cpu_times()._asdict(),
                },
                'memory': {
                    'rss_mb': proc.memory_info().rss / (1024 * 1024),
                    'vms_mb': proc.memory_info().vms / (1024 * 1024),
                    'percent': proc.memory_percent(),
                },
                'threads': {
                    'num_threads': proc.num_threads(),
                    'threads': [t.id for t in proc.threads()] if hasattr(proc, 'threads') else []
                },
                'files': [],
                'connections': []
            }

            # Ottieni file aperti (richiede permessi)
            try:
                details['files'] = [
                    {'fd': f.fd, 'path': f.path}
                    for f in proc.open_files()
                ]
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                details['files'] = ['Access denied or process terminated']

            # Ottieni connessioni di rete
            try:
                details['connections'] = [
                    {
                        'type': c.type,
                        'local_address': c.laddr,
                        'remote_address': c.raddr if c.raddr else 'N/A',
                        'status': c.status
                    }
                    for c in proc.connections()
                ]
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                details['connections'] = ['Access denied or process terminated']

            return details

        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied:
            return {'error': 'Access denied - insufficient permissions'}

    def search_processes(self, search_term: str) -> List[ProcessInfo]:
        """
        Cerca processi per nome.

        Args:
            search_term: Termine di ricerca (case-insensitive)

        Returns:
            Lista di ProcessInfo che corrispondono
        """
        all_processes = self.get_all_processes()
        search_lower = search_term.lower()

        return [
            proc for proc in all_processes
            if search_lower in proc.name.lower()
        ]

    def sort_processes(self, processes: List[ProcessInfo],
                      sort_by: str = 'cpu') -> List[ProcessInfo]:
        """
        Ordina i processi in base al criterio specificato.

        Args:
            processes: Lista di ProcessInfo
            sort_by: Criterio di ordinamento ('cpu', 'memory', 'pid', 'name')

        Returns:
            Lista ordinata di ProcessInfo
        """
        reverse = True  # Decrescente per default

        if sort_by == 'cpu':
            return sorted(processes, key=lambda p: p.cpu_percent, reverse=reverse)
        elif sort_by == 'memory':
            return sorted(processes, key=lambda p: p.memory_mb, reverse=reverse)
        elif sort_by == 'pid':
            return sorted(processes, key=lambda p: p.pid, reverse=False)
        elif sort_by == 'name':
            return sorted(processes, key=lambda p: p.name.lower(), reverse=False)
        else:
            return processes

    def get_process_children(self, pid: int) -> List[ProcessInfo]:
        """
        Ottiene i processi figli di un dato processo.

        Args:
            pid: PID del processo padre

        Returns:
            Lista di ProcessInfo figli

        Concetto: I processi formano una gerarchia ad albero
        - init/systemd è il processo radice (PID 1)
        - Ogni processo ha un processo padre (tranne init)
        - fork() crea un processo figlio
        """
        try:
            proc = psutil.Process(pid)
            children = []

            for child in proc.children(recursive=False):
                try:
                    memory_mb = child.memory_info().rss / (1024 * 1024)
                    child_info = ProcessInfo(
                        pid=child.pid,
                        name=child.name(),
                        cpu_percent=child.cpu_percent(),
                        memory_percent=child.memory_percent(),
                        memory_mb=memory_mb,
                        status=child.status(),
                        ppid=child.ppid(),
                        num_threads=child.num_threads(),
                        create_time=child.create_time()
                    )
                    children.append(child_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return children

        except psutil.NoSuchProcess:
            return []
        except psutil.AccessDenied:
            return []

    def get_process_count(self) -> int:
        """
        Ottiene il numero totale di processi in esecuzione.

        Returns:
            Numero di processi
        """
        return len(psutil.pids())

    def get_system_stats(self) -> Dict:
        """
        Ottiene statistiche di sistema generali.

        Returns:
            Dizionario con statistiche CPU, memoria, etc.

        Concetti:
        - CPU Load: Carico medio del sistema (1, 5, 15 min)
        - Memory Info: RAM totale, usata, disponibile
        - Swap Info: Memoria virtuale su disco
        """
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'cpu_count': psutil.cpu_count(),
            'memory': {
                'total_gb': psutil.virtual_memory().total / (1024**3),
                'available_gb': psutil.virtual_memory().available / (1024**3),
                'used_gb': psutil.virtual_memory().used / (1024**3),
                'percent': psutil.virtual_memory().percent
            },
            'swap': {
                'total_gb': psutil.swap_memory().total / (1024**3),
                'used_gb': psutil.swap_memory().used / (1024**3),
                'percent': psutil.swap_memory().percent
            },
            'process_count': self.get_process_count()
        }


# Funzioni helper per compatibilità
def get_all_processes() -> List[ProcessInfo]:
    """Funzione helper per ottenere tutti i processi"""
    manager = ProcessManager()
    return manager.get_all_processes()


def get_process_by_pid(pid: int) -> Optional[ProcessInfo]:
    """Funzione helper per ottenere un processo per PID"""
    manager = ProcessManager()
    return manager.get_process_by_pid(pid)


if __name__ == '__main__':
    # Test del modulo
    print("=== Test Process Module ===\n")

    manager = ProcessManager()

    # Test: Ottieni tutti i processi
    print(f"Numero totale di processi: {manager.get_process_count()}\n")

    # Test: Ottieni primi 10 processi
    processes = manager.get_all_processes()
    print("Primi 10 processi:")
    for proc in processes[:10]:
        print(f"  PID {proc.pid:>6}: {proc.name:<25} CPU: {proc.cpu_percent:>5.1f}% "
              f"MEM: {proc.memory_mb:>6.1f}MB")

    # Test: Statistiche di sistema
    print("\nStatistiche di sistema:")
    stats = manager.get_system_stats()
    print(f"  CPU: {stats['cpu_percent']}% ({stats['cpu_count']} cores)")
    print(f"  Memory: {stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB "
          f"({stats['memory']['percent']}%)")

    print("\n✓ Module test completed!")
