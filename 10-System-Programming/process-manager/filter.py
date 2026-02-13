"""
Filter Module - Filtraggio e ricerca dei processi

Questo modulo fornisce funzionalità avanzate per filtrare e cercare
processi in base a vari criteri.

Concetti educativi:
- Predicate Filtering: Funzioni che restituiscono True/False per ogni elemento
- Lambda Functions: Funzioni anonime per filtraggio dinamico
- List Comprehensions: Sintassi Python per trasformare e filtrare liste
"""

import re
from typing import List, Callable, Optional
from process import ProcessInfo, ProcessManager


class ProcessFilter:
    """
    Classe per il filtraggio dei processi.

    Supporta vari criteri di filtro e combinazioni logiche (AND, OR, NOT).
    """

    def __init__(self):
        """Inizializza il filtro"""
        self.manager = ProcessManager()

    def by_name(self, processes: List[ProcessInfo],
                name_pattern: str,
                case_sensitive: bool = False) -> List[ProcessInfo]:
        """
        Filtra processi per nome.

        Args:
            processes: Lista di ProcessInfo
            name_pattern: Pattern di ricerca nel nome
            case_sensitive: Se True, ricerca case-sensitive

        Returns:
            Lista filtrata di ProcessInfo

        Concetto: Pattern matching su stringhe
        """
        if not case_sensitive:
            name_pattern = name_pattern.lower()
            return [p for p in processes if name_pattern in p.name.lower()]
        return [p for p in processes if name_pattern in p.name]

    def by_name_regex(self, processes: List[ProcessInfo],
                     pattern: str,
                     case_sensitive: bool = False) -> List[ProcessInfo]:
        """
        Filtra processi usando espressioni regolari.

        Args:
            processes: Lista di ProcessInfo
            pattern: Pattern regex
            case_sensitive: Se True, matching case-sensitive

        Returns:
            Lista filtrata

        Concetto: Regular Expressions per pattern complessi
        Esempio: "chrome.*helper" trova processi con "chrome" seguito da "helper"
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)

        return [p for p in processes if regex.search(p.name)]

    def by_pid(self, processes: List[ProcessInfo],
               pid: Optional[int] = None,
               pid_range: Optional[tuple] = None) -> List[ProcessInfo]:
        """
        Filtra processi per PID.

        Args:
            processes: Lista di ProcessInfo
            pid: PID specifico
            pid_range: Tupla (min_pid, max_pid) per range

        Returns:
            Lista filtrata
        """
        if pid is not None:
            return [p for p in processes if p.pid == pid]
        if pid_range is not None:
            min_pid, max_pid = pid_range
            return [p for p in processes if min_pid <= p.pid <= max_pid]
        return processes

    def by_cpu(self, processes: List[ProcessInfo],
              min_cpu: float = 0.0,
              max_cpu: float = 100.0) -> List[ProcessInfo]:
        """
        Filtra processi per utilizzo CPU.

        Args:
            processes: Lista di ProcessInfo
            min_cpu: Percentuale minima CPU
            max_cpu: Percentuale massima CPU

        Returns:
            Lista filtrata
        """
        return [p for p in processes if min_cpu <= p.cpu_percent <= max_cpu]

    def by_memory(self, processes: List[ProcessInfo],
                 min_memory: float = 0.0,
                 max_memory: float = float('inf')) -> List[ProcessInfo]:
        """
        Filtra processi per utilizzo memoria.

        Args:
            processes: Lista di ProcessInfo
            min_memory: Memoria minima in MB
            max_memory: Memoria massima in MB

        Returns:
            Lista filtrata
        """
        return [p for p in processes if min_memory <= p.memory_mb <= max_memory]

    def by_status(self, processes: List[ProcessInfo],
                 status: str) -> List[ProcessInfo]:
        """
        Filtra processi per stato.

        Args:
            processes: Lista di ProcessInfo
            status: Stato del processo (running, sleeping, etc.)

        Returns:
            Lista filtrata

        Stati comuni:
        - R: Running
        - S: Sleeping (interruptible)
        - D: Disk sleep (uninterruptible)
        - Z: Zombie
        - T: Traced/Stopped
        """
        return [p for p in processes if p.status == status]

    def by_parent(self, processes: List[ProcessInfo],
                 ppid: int) -> List[ProcessInfo]:
        """
        Filtra processi che hanno un determinato padre.

        Args:
            processes: Lista di ProcessInfo
            ppid: PID del processo padre

        Returns:
            Lista di processi figli

        Concetto: Relazione padre-figlio nella gerarchia dei processi
        """
        return [p for p in processes if p.ppid == ppid]

    def by_threads(self, processes: List[ProcessInfo],
                  min_threads: int = 0,
                  max_threads: int = float('inf')) -> List[ProcessInfo]:
        """
        Filtra processi per numero di thread.

        Args:
            processes: Lista di ProcessInfo
            min_threads: Numero minimo di thread
            max_threads: Numero massimo di thread

        Returns:
            Lista filtrata
        """
        return [p for p in processes if min_threads <= p.num_threads <= max_threads]

    def multi_filter(self, processes: List[ProcessInfo],
                    filters: List[Callable[[ProcessInfo], bool]],
                    logic: str = 'AND') -> List[ProcessInfo]:
        """
        Applica molteplici filtri con logica AND/OR.

        Args:
            processes: Lista di ProcessInfo
            filters: Lista di funzioni predicate
            logic: 'AND' (tutti i filtri) o 'OR' (almeno un filtro)

        Returns:
            Lista filtrata

        Concetto: Composizione di predicati logici
        """
        if logic == 'AND':
            # Tutti i filtri devono essere soddisfatti
            return [p for p in processes if all(f(p) for f in filters)]
        elif logic == 'OR':
            # Almeno un filtro deve essere soddisfatto
            return [p for p in processes if any(f(p) for f in filters)]
        else:
            return processes

    def custom(self, processes: List[ProcessInfo],
              predicate: Callable[[ProcessInfo], bool]) -> List[ProcessInfo]:
        """
        Filtra con una funzione personalizzata.

        Args:
            processes: Lista di ProcessInfo
            predicate: Funzione che prende ProcessInfo e restituisce bool

        Returns:
            Lista filtrata

        Concetto: Higher-order functions (funzioni che accettano funzioni)
        """
        return [p for p in processes if predicate(p)]


class ProcessSearcher:
    """
    Classe per la ricerca avanzata di processi.

    Combina più criteri di ricerca e fornisce un'interfaccia fluente.
    """

    def __init__(self):
        """Inizializza il searcher"""
        self.manager = ProcessManager()
        self.filter = ProcessFilter()
        self._processes: Optional[List[ProcessInfo]] = None

    def load_all(self) -> 'ProcessSearcher':
        """Carica tutti i processi"""
        self._processes = self.manager.get_all_processes()
        return self

    def search(self, query: str,
               search_name: bool = True,
               case_sensitive: bool = False) -> List[ProcessInfo]:
        """
        Ricerca processi con query generica.

        Args:
            query: Termine di ricerca
            search_name: Se True cerca nel nome
            case_sensitive: Se True, ricerca case-sensitive

        Returns:
            Lista di ProcessInfo che corrispondono
        """
        if self._processes is None:
            self.load_all()

        if search_name:
            return self.filter.by_name(self._processes, query, case_sensitive)
        return []

    def advanced_search(self,
                       name: Optional[str] = None,
                       min_cpu: Optional[float] = None,
                       max_cpu: Optional[float] = None,
                       min_memory: Optional[float] = None,
                       max_memory: Optional[float] = None,
                       status: Optional[str] = None,
                       ppid: Optional[int] = None) -> List[ProcessInfo]:
        """
        Ricerca avanzata con molteplici criteri.

        Args:
            name: Filtro nome
            min_cpu: CPU minima
            max_cpu: CPU massima
            min_memory: Memoria minima (MB)
            max_memory: Memoria massima (MB)
            status: Filtro stato
            ppid: Filtro processo padre

        Returns:
            Lista filtrata

        Concetto: Query builder pattern per costruire query complesse
        """
        if self._processes is None:
            self.load_all()

        result = self._processes

        # Applica i filtri in sequenza
        if name:
            result = self.filter.by_name(result, name)
        if min_cpu is not None or max_cpu is not None:
            min_cpu = min_cpu if min_cpu is not None else 0.0
            max_cpu = max_cpu if max_cpu is not None else 100.0
            result = self.filter.by_cpu(result, min_cpu, max_cpu)
        if min_memory is not None or max_memory is not None:
            min_memory = min_memory if min_memory is not None else 0.0
            max_memory = max_memory if max_memory is not None else float('inf')
            result = self.filter.by_memory(result, min_memory, max_memory)
        if status:
            result = self.filter.by_status(result, status)
        if ppid:
            result = self.filter.by_parent(result, ppid)

        return result


def highlight_match(text: str, pattern: str,
                   case_sensitive: bool = False) -> str:
    """
    Evidenzia il pattern nel testo (per display colorato).

    Args:
        text: Testo originale
        pattern: Pattern da evidenziare
        case_sensitive: Se True, case-sensitive

    Returns:
        Testo con codici ANSI per l'evidenziazione

    Concetto: ANSI escape codes per colore nel terminale
    """
    if not case_sensitive:
        text_lower = text.lower()
        pattern_lower = pattern.lower()

        # Trova tutte le occorrenze
        result = []
        i = 0
        while i < len(text):
            idx = text_lower.find(pattern_lower, i)
            if idx == -1:
                result.append(text[i:])
                break
            result.append(text[i:idx])
            # Aggiungi codice ANSI per evidenziazione (giallo su nero)
            result.append('\033[33m\033[1m')
            result.append(text[idx:idx + len(pattern)])
            result.append('\033[0m')  # Reset
            i = idx + len(pattern)

        return ''.join(result)
    else:
        # Case-sensitive
        idx = text.find(pattern)
        if idx == -1:
            return text

        return (text[:idx] +
                '\033[33m\033[1m' +
                text[idx:idx + len(pattern)] +
                '\033[0m' +
                text[idx + len(pattern):])


if __name__ == '__main__':
    # Test del modulo
    print("=== Test Filter Module ===\n")

    manager = ProcessManager()
    filter_obj = ProcessFilter()
    searcher = ProcessSearcher()

    processes = manager.get_all_processes()

    # Test 1: Filtro per nome
    print("Test 1: Filtro per nome (python)")
    python_procs = filter_obj.by_name(processes, 'python')
    print(f"  Trovati {len(python_procs)} processi Python")
    for p in python_procs[:5]:
        print(f"    - {p.name} (PID {p.pid})")

    # Test 2: Filtro per CPU
    print("\nTest 2: Filtro per CPU (> 0.5%)")
    cpu_procs = filter_obj.by_cpu(processes, min_cpu=0.5)
    print(f"  Trovati {len(cpu_procs)} processi con CPU > 0.5%")
    for p in sorted(cpu_procs, key=lambda x: x.cpu_percent, reverse=True)[:5]:
        print(f"    - {p.name}: {p.cpu_percent:.1f}%")

    # Test 3: Filtro per memoria
    print("\nTest 3: Filtro per memoria (> 100 MB)")
    mem_procs = filter_obj.by_memory(processes, min_memory=100)
    print(f"  Trovati {len(mem_procs)} processi con > 100 MB")
    for p in sorted(mem_procs, key=lambda x: x.memory_mb, reverse=True)[:5]:
        print(f"    - {p.name}: {p.memory_mb:.1f} MB")

    # Test 4: Ricerca avanzata
    print("\nTest 4: Ricerca avanzata (nome: *sys*, CPU > 0%)")
    results = searcher.advanced_search(name='sys', min_cpu=0.0)
    print(f"  Trovati {len(results)} processi")
    for p in results[:5]:
        print(f"    - {p.name} (PID {p.pid}): CPU {p.cpu_percent:.1f}%")

    # Test 5: Filtro multi-condizione
    print("\nTest 5: Multi-filtro (CPU > 0 E Memoria > 50 MB)")
    filters = [
        lambda p: p.cpu_percent > 0,
        lambda p: p.memory_mb > 50
    ]
    multi_results = filter_obj.multi_filter(processes, filters, logic='AND')
    print(f"  Trovati {len(multi_results)} processi")
    for p in sorted(multi_results, key=lambda x: x.memory_mb, reverse=True)[:5]:
        print(f"    - {p.name}: CPU {p.cpu_percent:.1f}%, MEM {p.memory_mb:.1f} MB")

    # Test 6: Evidenziazione
    print("\nTest 6: Evidenziazione pattern")
    test_text = "python3.9 -m my_script.py"
    highlighted = highlight_match(test_text, 'py')
    print(f"  Originale: {test_text}")
    print(f"  Evidenziato: {highlighted}")

    print("\n✓ Module test completed!")
