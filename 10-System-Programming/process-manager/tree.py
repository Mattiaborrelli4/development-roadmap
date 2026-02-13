"""
Tree Module - Visualizzazione gerarchica dei processi

Questo modulo fornisce funzionalità per visualizzare i processi in una
struttura ad albero, mostrando le relazioni padre-figlio.

Concetti educativi:
- Process Hierarchy: I processi formano un albero con radice in init/PID 1
- Parent-Child: fork() crea un figlio che eredita dal padre
- Orphan Process: Processo il cui padre è terminato (adottato da init)
- Zombie Process: Processo terminato ma ancora nella tabella dei processi
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from process import ProcessInfo, ProcessManager


@dataclass
class TreeNode:
    """Nodo dell'albero dei processi"""
    process: ProcessInfo
    children: List['TreeNode']
    depth: int = 0

    def add_child(self, child: 'TreeNode'):
        """Aggiunge un nodo figlio"""
        child.depth = self.depth + 1
        self.children.append(child)


class ProcessTreeBuilder:
    """
    Costruisce l'albero gerarchico dei processi.

    Il processo init/systemd (PID 1) è la radice dell'albero.
    Ogni altro processo è un discendente di init.
    """

    def __init__(self):
        """Inizializza il builder dell'albero"""
        self.manager = ProcessManager()
        self.process_map: Dict[int, TreeNode] = {}
        self.root_nodes: List[TreeNode] = []

    def build_tree(self, processes: List[ProcessInfo]) -> List[TreeNode]:
        """
        Costruisce l'albero dei processi dalla lista piatta.

        Args:
            processes: Lista di ProcessInfo

        Returns:
            Lista di nodi radice (alberi)

        Algoritmo:
        1. Crea una mappa PID -> TreeNode per tutti i processi
        2. Per ogni processo, trova il padre e aggiungi se stesso come figlio
        3. I processi senza padre (o padre non trovato) diventano radici
        """
        self.process_map = {}
        self.root_nodes = []

        # Fase 1: Crea i nodi
        for proc in processes:
            self.process_map[proc.pid] = TreeNode(process=proc, children=[])

        # Fase 2: Costruisci la gerarchia
        for proc in processes:
            node = self.process_map[proc.pid]

            # Cerca il padre
            if proc.ppid in self.process_map:
                # Padre trovato, aggiungi come figlio
                parent_node = self.process_map[proc.ppid]
                parent_node.add_child(node)
            else:
                # Padre non trovato (processo radice o orfano)
                self.root_nodes.append(node)

        # Ordina le radici per PID
        self.root_nodes.sort(key=lambda n: n.process.pid)

        return self.root_nodes

    def build_subtree(self, root_pid: int) -> Optional[TreeNode]:
        """
        Costruisce un sottoalbero partendo da un PID specifico.

        Args:
            root_pid: PID della radice del sottoalbero

        Returns:
            TreeNode radice del sottoalbero, o None se non trovato
        """
        root_process = self.manager.get_process_by_pid(root_pid)
        if not root_process:
            return None

        # Ottieni tutti i processi per costruire la mappa
        all_processes = self.manager.get_all_processes()

        # Crea mappa per ricerca veloce
        proc_map = {p.pid: p for p in all_processes}

        # Funzione ricorsiva per costruire l'albero
        def build_node(pid: int, depth: int = 0) -> Optional[TreeNode]:
            if pid not in proc_map:
                return None

            proc = proc_map[pid]
            node = TreeNode(process=proc, children=[], depth=depth)

            # Trovi i figli diretti
            for p in all_processes:
                if p.ppid == pid:
                    child_node = build_node(p.pid, depth + 1)
                    if child_node:
                        node.add_child(child_node)

            # Ordina i figli per PID
            node.children.sort(key=lambda n: n.process.pid)

            return node

        return build_node(root_pid)

    def get_tree_stats(self, root: TreeNode) -> Dict:
        """
        Calcola statistiche sull'albero dei processi.

        Args:
            root: Nodo radice dell'albero

        Returns:
            Dizionario con statistiche (numero nodi, profondità max, etc.)
        """
        def count_nodes(node: TreeNode) -> int:
            """Conta ricorsivamente i nodi"""
            count = 1
            for child in node.children:
                count += count_nodes(child)
            return count

        def max_depth(node: TreeNode) -> int:
            """Calcola la profondità massima"""
            if not node.children:
                return node.depth
            return max(max_depth(child) for child in node.children)

        def count_leaves(node: TreeNode) -> int:
            """Conta i nodi foglia (senza figli)"""
            if not node.children:
                return 1
            return sum(count_leaves(child) for child in node.children)

        return {
            'total_nodes': count_nodes(root),
            'max_depth': max_depth(root),
            'leaf_count': count_leaves(root),
            'direct_children': len(root.children)
        }


class ProcessTreeRenderer:
    """
    Renderer per la visualizzazione dell'albero dei processi.

    Crea una rappresentazione testuale con caratteri ASCII/Unicode
    per mostrare le relazioni padre-figlio.
    """

    def __init__(self, use_unicode: bool = True):
        """
        Inizializza il renderer.

        Args:
            use_unicode: Se True, usa caratteri Unicode per l'albero
        """
        self.use_unicode = use_unicode

        if use_unicode:
            # Caratteri Unicode per l'albero
            self.chars = {
                'vertical': '│',
                'branch': '├─',
                'last': '└─',
                'indent': '  ',
                'blank': ' '
            }
        else:
            # Caratteri ASCII compatibili
            self.chars = {
                'vertical': '|',
                'branch': '|-',
                'last': '`-',
                'indent': '  ',
                'blank': ' '
            }

    def render(self, root: TreeNode,
               show_pid: bool = True,
               show_cpu: bool = True,
               show_memory: bool = True,
               max_depth: int = -1) -> str:
        """
        Renderizza l'albero come stringa.

        Args:
            root: Nodo radice
            show_pid: Mostra PID
            show_cpu: Mostra utilizzo CPU
            show_memory: Mostra utilizzo memoria
            max_depth: Profondità massima (-1 = illimitata)

        Returns:
            Stringa rappresentante l'albero
        """
        lines = []

        def render_node(node: TreeNode, prefix: str = '', is_last: bool = True):
            if max_depth >= 0 and node.depth > max_depth:
                return

            # Crea il prefisso per il nodo corrente
            connector = self.chars['last'] if is_last else self.chars['branch']
            line = f"{prefix}{connector} "

            # Aggiungi info processo
            line += self._format_process(node.process, show_pid, show_cpu, show_memory)
            lines.append(line)

            # Prepara prefisso per i figli
            new_prefix = prefix
            if is_last:
                new_prefix += self.chars['indent'] + ' '
            else:
                new_prefix += self.chars['vertical'] + ' '

            # Renderizza i figli
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                render_node(child, new_prefix, is_last_child)

        # Renderizza la radice
        root_line = self._format_process(root.process, show_pid, show_cpu, show_memory)
        lines.append(root_line)

        # Renderizza i figli della radice
        for i, child in enumerate(root.children):
            is_last_child = (i == len(root.children) - 1)
            render_node(child, '', is_last_child)

        return '\n'.join(lines)

    def _format_process(self, proc: ProcessInfo,
                       show_pid: bool,
                       show_cpu: bool,
                       show_memory: bool) -> str:
        """Formatta un processo per la visualizzazione"""
        parts = [proc.name]

        if show_pid:
            parts.append(f"[{proc.pid}]")

        if show_cpu:
            parts.append(f"CPU:{proc.cpu_percent:4.1f}%")

        if show_memory:
            parts.append(f"MEM:{proc.memory_mb:5.1f}MB")

        return ' '.join(parts)

    def render_compact(self, root: TreeNode) -> str:
        """
        Renderizza l'albero in formato compatto (solo nomi e PIDs).

        Args:
            root: Nodo radice

        Returns:
            Stringa compatta
        """
        lines = []

        def render_node(node: TreeNode, prefix: str = '', is_last: bool = True):
            connector = self.chars['last'] if is_last else self.chars['branch']
            line = f"{prefix}{connector} {node.process.name} ({node.process.pid})"
            lines.append(line)

            new_prefix = prefix + (self.chars['indent'] + ' ' if is_last else self.chars['vertical'] + ' ')

            for i, child in enumerate(node.children):
                is_last_child = (i == len(child.children) - 1)
                render_node(child, new_prefix, is_last_child)

        # Radice
        lines.append(f"{root.process.name} ({root.process.pid})")

        for i, child in enumerate(root.children):
            is_last_child = (i == len(root.children) - 1)
            render_node(child, '', is_last_child)

        return '\n'.join(lines)


def print_process_tree(root_pid: Optional[int] = None,
                       show_pid: bool = True,
                       show_cpu: bool = True,
                       show_memory: bool = True,
                       max_depth: int = -1):
    """
    Funzione helper per stampare l'albero dei processi.

    Args:
        root_pid: PID della radice (None = albero completo)
        show_pid: Mostra PID
        show_cpu: Mostra CPU
        show_memory: Mostra memoria
        max_depth: Profondità massima
    """
    manager = ProcessManager()
    builder = ProcessTreeBuilder()
    renderer = ProcessTreeRenderer(use_unicode=True)

    if root_pid:
        # Sottoalbero
        root = builder.build_subtree(root_pid)
        if not root:
            print(f"Processo con PID {root_pid} non trovato")
            return

        tree_str = renderer.render(root, show_pid, show_cpu, show_memory, max_depth)
        print(tree_str)

        stats = builder.get_tree_stats(root)
        print(f"\nStatistiche sottoalbero:")
        print(f"  Totale processi: {stats['total_nodes']}")
        print(f"  Profondità massima: {stats['max_depth']}")
        print(f"  Processi foglia: {stats['leaf_count']}")

    else:
        # Albero completo
        all_processes = manager.get_all_processes()
        roots = builder.build_tree(all_processes)

        print(f"Albero dei processi ({len(all_processes)} processi totali)\n")

        for root in roots:
            tree_str = renderer.render(root, show_pid, show_cpu, show_memory, max_depth)
            print(tree_str)
            print()


if __name__ == '__main__':
    # Test del modulo
    print("=== Test Tree Module ===\n")

    # Test: Albero completo (prime 50 processi)
    manager = ProcessManager()
    processes = manager.get_all_processes()[:50]

    builder = ProcessTreeBuilder()
    renderer = ProcessTreeRenderer()

    roots = builder.build_tree(processes)

    print(f"Albero dei processi (primi 50 processi)\n")
    for root in roots[:3]:  # Mostra solo prime 3 radici
        print(renderer.render_compact(root))
        print()

    # Test: Statistiche
    if roots:
        stats = builder.get_tree_stats(roots[0])
        print(f"\nStatistiche prima radice:")
        print(f"  Totale nodi: {stats['total_nodes']}")
        print(f"  Profondità max: {stats['max_depth']}")
        print(f"  Figli diretti: {stats['direct_children']}")

    print("\n✓ Module test completed!")
