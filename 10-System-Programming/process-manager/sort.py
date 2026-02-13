"""
Sort Module - Ordinamento dei processi

Questo modulo fornisce funzionalità per ordinare i processi
in base a vari criteri.

Concetti educativi:
- Sorting Algorithms: Algoritmi di ordinamento
- Key Functions: Funzioni di chiave per l'ordinamento
- Stable Sort: Ordinamento stabile (mantiene l'ordine originale per chiavi uguali)
- Lambda Functions: Funzioni anonime per chiavi di ordinamento
"""

from typing import List, Callable, Optional
from process import ProcessInfo
import operator


class ProcessSorter:
    """
    Classe per l'ordinamento dei processi.

    Supporta ordinamento per vari criteri e direzioni.
    """

    def __init__(self):
        """Inizializza il sorter"""
        self.sort_fields = {
            'pid': self._by_pid,
            'name': self._by_name,
            'cpu': self._by_cpu,
            'memory': self._by_memory,
            'threads': self._by_threads,
            'status': self._by_status,
            'ppid': self._by_ppid,
        }

    def sort(self, processes: List[ProcessInfo],
            field: str = 'cpu',
            reverse: bool = True) -> List[ProcessInfo]:
        """
        Ordina i processi per un campo specifico.

        Args:
            processes: Lista di ProcessInfo
            field: Campo di ordinamento ('pid', 'name', 'cpu', 'memory', etc.)
            reverse: Se True, ordine decrescente

        Returns:
            Lista ordinata di ProcessInfo

        Concetto: Python's sorted() usa Timsort (O(n log n) nel caso peggiore)
        """
        if field not in self.sort_fields:
            raise ValueError(f"Campo di ordinamento non valido: {field}. "
                           f"Campi validi: {list(self.sort_fields.keys())}")

        # Ordina usando la funzione key appropriata
        return sorted(processes, key=self.sort_fields[field], reverse=reverse)

    def sort_multiple(self, processes: List[ProcessInfo],
                     fields: List[tuple]) -> List[ProcessInfo]:
        """
        Ordina i processi per molteplici campi (in ordine di priorità).

        Args:
            processes: Lista di ProcessInfo
            fields: Lista di tuple (campo, reverse)

        Returns:
            Lista ordinata

        Concetto: Multi-key sorting (ordinamento a più livelli)
        Esempio: Ordina per CPU (decrescente), poi per nome (alfabetico)
        """
        result = processes[:]

        # Applica ordinamenti in ordine inverso di priorità
        # (l'ultimo ordinamento ha la priorità più alta)
        for field, reverse in reversed(fields):
            if field not in self.sort_fields:
                continue
            result = sorted(result, key=self.sort_fields[field], reverse=reverse)

        return result

    def custom_sort(self, processes: List[ProcessInfo],
                   key_func: Callable[[ProcessInfo], any],
                   reverse: bool = True) -> List[ProcessInfo]:
        """
        Ordina con una funzione di chiave personalizzata.

        Args:
            processes: Lista di ProcessInfo
            key_func: Funzione che mappa ProcessInfo a un valore confrontabile
            reverse: Se True, ordine decrescente

        Returns:
            Lista ordinata

        Concetto: Higher-order function per ordinamento flessibile
        """
        return sorted(processes, key=key_func, reverse=reverse)

    # Funzioni di chiave per ogni campo
    def _by_pid(self, proc: ProcessInfo) -> int:
        """Chiave per PID"""
        return proc.pid

    def _by_name(self, proc: ProcessInfo) -> str:
        """Chiave per nome (case-insensitive)"""
        return proc.name.lower()

    def _by_cpu(self, proc: ProcessInfo) -> float:
        """Chiave per utilizzo CPU"""
        return proc.cpu_percent

    def _by_memory(self, proc: ProcessInfo) -> float:
        """Chiave per utilizzo memoria"""
        return proc.memory_mb

    def _by_threads(self, proc: ProcessInfo) -> int:
        """Chiave per numero di thread"""
        return proc.num_threads

    def _by_status(self, proc: ProcessInfo) -> str:
        """Chiave per stato"""
        return proc.status

    def _by_ppid(self, proc: ProcessInfo) -> int:
        """Chiave per PID del padre"""
        return proc.ppid


class TopNProcesses:
    """
    Selettore per i top N processi in base a criteri specifici.

    Utile per identificare i processi più "pesanti" o attivi.
    """

    def __init__(self):
        """Inizializza il selettore"""
        self.sorter = ProcessSorter()

    def top_by_cpu(self, processes: List[ProcessInfo],
                   n: int = 10) -> List[ProcessInfo]:
        """
        Restituisce i top N processi per utilizzo CPU.

        Args:
            processes: Lista di ProcessInfo
            n: Numero di processi da restituire

        Returns:
            Top N processi
        """
        sorted_procs = self.sorter.sort(processes, 'cpu', reverse=True)
        return sorted_procs[:n]

    def top_by_memory(self, processes: List[ProcessInfo],
                     n: int = 10) -> List[ProcessInfo]:
        """
        Restituisce i top N processi per utilizzo memoria.

        Args:
            processes: Lista di ProcessInfo
            n: Numero di processi da restituire

        Returns:
            Top N processi
        """
        sorted_procs = self.sorter.sort(processes, 'memory', reverse=True)
        return sorted_procs[:n]

    def top_by_threads(self, processes: List[ProcessInfo],
                      n: int = 10) -> List[ProcessInfo]:
        """
        Restituisce i top N processi per numero di thread.

        Args:
            processes: Lista di ProcessInfo
            n: Numero di processi da restituire

        Returns:
            Top N processi
        """
        sorted_procs = self.sorter.sort(processes, 'threads', reverse=True)
        return sorted_procs[:n]


class ProcessGrouper:
    """
    Raggruppa processi per vari criteri.

    Utile per analisi aggregate (es. memoria totale per applicazione).
    """

    def __init__(self):
        """Inizializza il grouper"""

    def group_by_name(self, processes: List[ProcessInfo]) -> dict:
        """
        Raggruppa processi per nome.

        Args:
            processes: Lista di ProcessInfo

        Returns:
            Dizionario {nome: [processi]}

        Concetto: Grouping/Aggregation per analisi statistica
        """
        groups = {}
        for proc in processes:
            if proc.name not in groups:
                groups[proc.name] = []
            groups[proc.name].append(proc)
        return groups

    def group_by_status(self, processes: List[ProcessInfo]) -> dict:
        """
        Raggruppa processi per stato.

        Args:
            processes: Lista di ProcessInfo

        Returns:
            Dizionario {status: [processi]}
        """
        groups = {}
        for proc in processes:
            if proc.status not in groups:
                groups[proc.status] = []
            groups[proc.status].append(proc)
        return groups

    def aggregate_by_name(self, processes: List[ProcessInfo]) -> List[dict]:
        """
        Aggrega statistiche per nome di processo.

        Args:
            processes: Lista di ProcessInfo

        Returns:
            Lista di dizionari con statistiche aggregate

        Concetto: Map-Reduce pattern (aggregazione dati)
        """
        groups = self.group_by_name(processes)

        result = []
        for name, procs in groups.items():
            total_cpu = sum(p.cpu_percent for p in procs)
            total_memory = sum(p.memory_mb for p in procs)
            total_threads = sum(p.num_threads for p in procs)

            result.append({
                'name': name,
                'count': len(procs),
                'total_cpu': total_cpu,
                'total_memory_mb': total_memory,
                'avg_cpu': total_cpu / len(procs),
                'avg_memory_mb': total_memory / len(procs),
                'total_threads': total_threads
            })

        # Ordina per memoria totale
        result.sort(key=lambda x: x['total_memory_mb'], reverse=True)
        return result


def get_sort_menu() -> str:
    """
    Restituisce il menu delle opzioni di ordinamento.

    Returns:
        Stringa con le opzioni disponibili
    """
    return """
Opzioni di ordinamento:
  [1] PID           - Identificatore del processo
  [2] Name          - Nome del processo (A-Z)
  [3] CPU           - Utilizzo CPU (alto-basso)
  [4] Memory        - Utilizzo memoria (alto-basso)
  [5] Threads       - Numero di thread
  [6] Status        - Stato del processo

  [a] Ascending     - Ordine crescente
  [d] Descending    - Ordine decrescente (default)
"""


if __name__ == '__main__':
    # Test del modulo
    from process import ProcessManager

    print("=== Test Sort Module ===\n")

    manager = ProcessManager()
    sorter = ProcessSorter()
    top_selector = TopNProcesses()
    grouper = ProcessGrouper()

    processes = manager.get_all_processes()

    # Test 1: Ordinamento per CPU
    print("Test 1: Ordinamento per CPU (top 10)")
    top_cpu = sorter.sort(processes, 'cpu', reverse=True)[:10]
    print(f"{'PID':>6} {'Nome':<25} {'CPU %':>7} {'Mem MB':>8}")
    print("-" * 52)
    for p in top_cpu:
        print(f"{p.pid:>6} {p.name:<25} {p.cpu_percent:>6.1f}% {p.memory_mb:>7.1f}")

    # Test 2: Ordinamento per memoria
    print("\nTest 2: Ordinamento per Memoria (top 10)")
    top_mem = sorter.sort(processes, 'memory', reverse=True)[:10]
    print(f"{'PID':>6} {'Nome':<25} {'CPU %':>7} {'Mem MB':>8}")
    print("-" * 52)
    for p in top_mem:
        print(f"{p.pid:>6} {p.name:<25} {p.cpu_percent:>6.1f}% {p.memory_mb:>7.1f}")

    # Test 3: Ordinamento multi-campo
    print("\nTest 3: Ordinamento multi-campo (CPU poi Nome)")
    multi_sorted = sorter.sort_multiple(processes, [('cpu', True), ('name', False)])
    print(f"{'PID':>6} {'Nome':<25} {'CPU %':>7}")
    print("-" * 42)
    for p in multi_sorted[:10]:
        print(f"{p.pid:>6} {p.name:<25} {p.cpu_percent:>6.1f}%")

    # Test 4: Top N selector
    print("\nTest 4: Top 5 per Thread")
    top_threads = top_selector.top_by_threads(processes, 5)
    print(f"{'PID':>6} {'Nome':<25} {'Thread':>7}")
    print("-" * 42)
    for p in top_threads:
        print(f"{p.pid:>6} {p.name:<25} {p.num_threads:>7}")

    # Test 5: Raggruppamento
    print("\nTest 5: Raggruppamento per nome (top 5)")
    aggregated = grouper.aggregate_by_name(processes)[:5]
    print(f"{'Nome':<25} {'Count':>5} {'CPU tot':>8} {'Mem tot':>9}")
    print("-" * 51)
    for agg in aggregated:
        print(f"{agg['name']:<25} {agg['count']:>5} {agg['total_cpu']:>7.1f}% {agg['total_memory_mb']:>8.1f} MB")

    # Test 6: Raggruppamento per stato
    print("\nTest 6: Raggruppamento per stato")
    status_groups = grouper.group_by_status(processes)
    print(f"{'Stato':<10} {'Count':>7}")
    print("-" * 19)
    for status, procs in sorted(status_groups.items()):
        print(f"{status:<10} {len(procs):>7}")

    print("\n✓ Module test completed!")
