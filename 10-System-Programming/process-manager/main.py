#!/usr/bin/env python3
"""
Process Manager - Educational System Programming Tool

Questo programma è uno strumento educativo per imparare la gestione dei processi.
Simila a top/htop ma progettato per l'apprendimento.

Autore: Progetto educativo System Programming
Linguaggio: Python 3.10+
Dipendenze: psutil, rich, click, PyYAML

Concetti educativi trattati:
- PID (Process ID): Identificatore univoco del processo
- Process Hierarchy: Gerarchia padre-figlio
- Signals: IPC (Inter-Process Communication)
- /proc filesystem (Linux): Filesystem virtuale con info processi
- Memory Management: RSS, VMS, swap
- CPU Scheduling: Time slicing, priorities
"""

import sys
import time
import signal
import argparse
from pathlib import Path
from typing import Optional, List

# Import dei moduli personalizzati
from process import ProcessManager, ProcessInfo
from tree import ProcessTreeBuilder, ProcessTreeRenderer
from filter import ProcessFilter, ProcessSearcher
from sort import ProcessSorter, TopNProcesses
from killer import ProcessKiller, TerminateMethod, TerminationResult

# Tenta di importare Rich per UI avanzata
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.tree import Tree as RichTree
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Nota: Installa 'rich' per una UI avanzata: pip install rich")


class ProcessManagerUI:
    """
    Interfaccia utente principale per il Process Manager.

    Fornisce un'interfaccia a linee di comando per tutte le funzionalità.
    """

    def __init__(self):
        """Inizializza l'interfaccia"""
        self.manager = ProcessManager()
        self.filter = ProcessFilter()
        self.sorter = ProcessSorter()
        self.killer = ProcessKiller(require_confirmation=True)
        self.searcher = ProcessSearcher()
        self.top_selector = TopNProcesses()

        # Configurazione console
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def list_processes(self,
                      sort_by: str = 'cpu',
                      filter_name: Optional[str] = None,
                      limit: int = 20,
                      show_all: bool = False):
        """
        Lista i processi con ordinamento e filtri.

        Args:
            sort_by: Campo di ordinamento
            filter_name: Filtro per nome
            limit: Numero massimo di processi
            show_all: Se True, mostra tutti i processi
        """
        # Ottieni processi
        processes = self.manager.get_all_processes()

        # Applica filtro
        if filter_name:
            processes = self.filter.by_name(processes, filter_name)
            print(f"\n🔍 Filtrando per nome: '{filter_name}'")
            print(f"   Trovati {len(processes)} processi\n")

        # Ordina
        processes = self.sorter.sort(processes, sort_by, reverse=True)

        # Limita
        if not show_all:
            processes = processes[:limit]

        # Mostra statistiche
        stats = self.manager.get_system_stats()
        print(f"💻 Statistiche di sistema:")
        print(f"   CPU: {stats['cpu_percent']:.1f}% ({stats['cpu_count']} cores)")
        print(f"   Memory: {stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB ({stats['memory']['percent']}%)")
        print(f"   Processi totali: {stats['process_count']}\n")

        # Intestazione tabella
        if RICH_AVAILABLE:
            self._list_processes_rich(processes, sort_by)
        else:
            self._list_processes_plain(processes, sort_by)

    def _list_processes_rich(self, processes: List[ProcessInfo], sort_by: str):
        """Mostra processi con Rich"""
        table = Table(title=f"Processi (ordinati per {sort_by})")
        table.add_column("PID", style="cyan", justify="right")
        table.add_column("Nome", style="green")
        table.add_column("CPU %", justify="right")
        table.add_column("Mem MB", justify="right")
        table.add_column("Stato", style="yellow")
        table.add_column("Thread", justify="right")

        for p in processes:
            # Colora CPU in base al valore
            cpu_style = "red" if p.cpu_percent > 50 else "yellow" if p.cpu_percent > 20 else "white"
            mem_style = "red" if p.memory_mb > 1000 else "yellow" if p.memory_mb > 500 else "white"

            table.add_row(
                str(p.pid),
                p.name[:20],
                f"[{cpu_style}]{p.cpu_percent:.1f}%[/]",
                f"[{mem_style}]{p.memory_mb:.1f}[/]",
                p.status,
                str(p.num_threads)
            )

        self.console.print(table)
        print(f"\nMostrati {len(processes)} processi")

    def _list_processes_plain(self, processes: List[ProcessInfo], sort_by: str):
        """Mostra processi in testo plain"""
        print(f"{'PID':>6} {'Nome':<25} {'CPU %':>7} {'Mem MB':>8} {'Stato':<8} {'Thread':>6}")
        print("-" * 70)

        for p in processes:
            # Colori ANSI
            cpu_color = "\033[31m" if p.cpu_percent > 50 else "\033[33m" if p.cpu_percent > 20 else "\033[0m"
            mem_color = "\033[31m" if p.memory_mb > 1000 else "\033[33m" if p.memory_mb > 500 else "\033[0m"
            reset = "\033[0m"

            print(f"{p.pid:>6} {p.name[:25]:<25} "
                  f"{cpu_color}{p.cpu_percent:>6.1f}%{reset} "
                  f"{mem_color}{p.memory_mb:>7.1f}{reset} "
                  f"{p.status:<8} "
                  f"{p.num_threads:>6}")

        print(f"\nMostrati {len(processes)} processi")

    def show_tree(self, root_pid: Optional[int] = None, max_depth: int = -1):
        """
        Mostra l'albero dei processi.

        Args:
            root_pid: PID della radice (None = albero completo)
            max_depth: Profondità massima
        """
        builder = ProcessTreeBuilder()
        renderer = ProcessTreeRenderer(use_unicode=True)

        if root_pid:
            # Sottoalbero
            print(f"\n🌳 Albero processi (radice: PID {root_pid})\n")
            root = builder.build_subtree(root_pid)
            if not root:
                print(f"Processo {root_pid} non trovato")
                return

            tree_str = renderer.render(root, show_pid=True, show_cpu=True, show_memory=True, max_depth=max_depth)
            print(tree_str)

            stats = builder.get_tree_stats(root)
            print(f"\n📊 Statistiche:")
            print(f"   Totale processi: {stats['total_nodes']}")
            print(f"   Profondità massima: {stats['max_depth']}")
            print(f"   Processi foglia: {stats['leaf_count']}")
        else:
            # Albero completo
            print(f"\n🌳 Albero completo dei processi\n")
            all_processes = self.manager.get_all_processes()

            # Limita per leggibilità
            if len(all_processes) > 100:
                print(f"⚠️  Ci sono {len(all_processes)} processi. Mostrando i primi 100.\n")
                all_processes = all_processes[:100]

            roots = builder.build_tree(all_processes)
            print(f"Alberi trovati: {len(roots)}\n")

            for i, root in enumerate(roots[:5], 1):  # Max 5 alberi
                print(f"--- Albero {i} ---")
                tree_str = renderer.render_compact(root)
                # Limita profondità per display
                lines = tree_str.split('\n')
                if len(lines) > 20:
                    tree_str = '\n'.join(lines[:20]) + f"\n... ({len(lines) - 20} altre righe)"
                print(tree_str)
                print()

    def watch_processes(self, interval: int = 2, sort_by: str = 'cpu'):
        """
        Modalità watch con auto-refresh.

        Args:
            interval: Secondi tra refresh
            sort_by: Campo di ordinamento
        """
        print(f"\n🔄 Modalità Watch (refresh ogni {interval}s, ordinato per {sort_by})")
        print("   Premi Ctrl+C per uscire\n")

        try:
            iteration = 0
            while True:
                iteration += 1

                # Clear screen (multipiattaforma)
                if sys.platform == "win32":
                    os.system('cls')
                else:
                    print("\033[2J\033[H", end="")

                print(f"⏱️  Iterazione {iteration} - {time.strftime('%H:%M:%S')}")
                print()

                # Lista processi
                self.list_processes(sort_by=sort_by, limit=15, show_all=False)

                # Attendi
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n✅ Watch terminato")

    def search_processes(self, query: str, case_sensitive: bool = False):
        """
        Cerca processi.

        Args:
            query: Termine di ricerca
            case_sensitive: Ricerca case-sensitive
        """
        print(f"\n🔍 Ricerca: '{query}'\n")

        results = self.searcher.search(query, search_name=True, case_sensitive=case_sensitive)

        if not results:
            print("Nessun risultato trovato")
            return

        print(f"Trovati {len(results)} processi:\n")

        # Ordina per nome
        results = self.sorter.sort(results, 'name', reverse=False)

        # Mostra risultati
        if RICH_AVAILABLE:
            self._list_processes_rich(results, 'name')
        else:
            self._list_processes_plain(results, 'name')

    def kill_process(self, pid: int,
                    method: str = 'sigterm',
                    force: bool = False):
        """
        Termina un processo.

        Args:
            pid: PID del processo
            method: Metodo di terminazione
            force: Forza terminazione senza conferma
        """
        # Mappa metodo stringa -> enum
        method_map = {
            'sigterm': TerminateMethod.SIGTERM,
            'sigkill': TerminateMethod.SIGKILL,
            'sigint': TerminateMethod.SIGINT,
            'sigstop': TerminateMethod.SIGSTOP,
        }

        terminate_method = method_map.get(method.lower(), TerminateMethod.SIGTERM)

        print(f"\n⚡ Terminazione processo {pid} (metodo: {method.upper()})\n")

        result = self.killer.kill_by_pid(pid, terminate_method, force)

        # Mostra risultato
        result_emoji = {
            TerminationResult.SUCCESS: "✅",
            TerminationResult.ALREADY_DEAD: "💀",
            TerminationResult.ACCESS_DENIED: "🔒",
            TerminationResult.NOT_FOUND: "❓",
            TerminationResult.ZOMBIE: "🧟",
            TerminationResult.FAILED: "❌"
        }

        emoji = result_emoji.get(result, "❓")
        print(f"{emoji} {result.value}")

    def show_details(self, pid: int):
        """
        Mostra dettagli estesi di un processo.

        Args:
            pid: PID del processo
        """
        print(f"\n📋 Dettagli processo {pid}\n")

        details = self.manager.get_process_details(pid)

        if not details:
            print("Processo non trovato")
            return

        if 'error' in details:
            print(f"Errore: {details['error']}")
            return

        # Info base
        print("📌 Informazioni Base:")
        print(f"   PID: {details['basic']['pid']}")
        print(f"   Nome: {details['basic']['name']}")
        print(f"   Eseguibile: {details['basic']['exe']}")
        print(f"   Directory: {details['basic']['cwd']}")
        print(f"   Stato: {details['basic']['status']}")
        print(f"   Cmdline: {' '.join(details['basic']['cmdline']) if details['basic']['cmdline'] else 'N/A'}")

        # Info utente
        print("\n👤 Contesto Utente:")
        print(f"   Username: {details['user']['username']}")
        print(f"   UID: {details['user']['uids']['real']}")

        # Info memoria
        print("\n💾 Memoria:")
        print(f"   RSS: {details['memory']['rss_mb']:.1f} MB")
        print(f"   VMS: {details['memory']['vms_mb']:.1f} MB")
        print(f"   Percent: {details['memory']['percent']:.1f}%")

        # Info thread
        print("\n🧵 Thread:")
        print(f"   Totale: {details['threads']['num_threads']}")

        # File aperti
        print(f"\n📂 File Aperti ({len(details['files'])}):")
        for f in details['files'][:10]:
            if isinstance(f, str):
                print(f"   {f}")
            else:
                print(f"   FD {f['fd']}: {f['path']}")
        if len(details['files']) > 10:
            print(f"   ... e altri {len(details['files']) - 10}")

        # Connessioni
        print(f"\n🌐 Connessioni ({len(details['connections'])}):")
        for c in details['connections'][:10]:
            if isinstance(c, str):
                print(f"   {c}")
            else:
                addr = c['local_address']
                remote = c['remote_address'] if c['remote_address'] != 'N/A' else 'N/A'
                print(f"   {addr} -> {remote} ({c['status']})")
        if len(details['connections']) > 10:
            print(f"   ... e altre {len(details['connections']) - 10}")

    def show_stats(self):
        """Mostra statistiche di sistema"""
        print("\n📊 Statistiche di Sistema\n")

        stats = self.manager.get_system_stats()

        # CPU
        print("💻 CPU:")
        print(f"   Utilizzo: {stats['cpu_percent']:.1f}%")
        print(f"   Core: {stats['cpu_count']}")

        # Memoria
        print("\n💾 Memoria:")
        mem = stats['memory']
        print(f"   Totale: {mem['total_gb']:.1f} GB")
        print(f"   Usata: {mem['used_gb']:.1f} GB ({mem['percent']}%)")
        print(f"   Disponibile: {mem['available_gb']:.1f} GB")

        # Swap
        swap = stats['swap']
        if swap['total_gb'] > 0:
            print("\n💿 Swap:")
            print(f"   Totale: {swap['total_gb']:.1f} GB")
            print(f"   Usato: {swap['used_gb']:.1f} GB ({swap['percent']}%)")

        # Processi
        print(f"\n📋 Processi: {stats['process_count']} totali")

        # Top processi
        processes = self.manager.get_all_processes()
        print("\n🔥 Top 5 CPU:")
        for p in self.top_selector.top_by_cpu(processes, 5):
            print(f"   {p.name:<25} CPU: {p.cpu_percent:5.1f}%")

        print("\n🐘 Top 5 Memoria:")
        for p in self.top_selector.top_by_memory(processes, 5):
            print(f"   {p.name:<25} MEM: {p.memory_mb:6.1f} MB")


def main():
    """Funzione principale"""
    parser = argparse.ArgumentParser(
        description='Process Manager - Educational System Programming Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s list                    Lista tutti i processi
  %(prog)s list --sort memory       Ordina per memoria
  %(prog)s list --filter chrome     Filtra per nome
  %(prog)s tree                    Mostra albero processi
  %(prog)s tree --pid 1234         Mostra sottoalbero
  %(prog)s watch                   Modalità auto-refresh
  %(prog)s search python           Cerca processi
  %(prog)s kill 1234               Termina processo
  %(prog)s details 1234            Mostra dettagli
  %(prog)s stats                   Statistiche di sistema

Concetti educativi:
- PID: Process ID, identificatore univoco
- Signals: Meccanismo IPC per controllo processi
- /proc fs: Filesystem virtuale Linux con info processi
- Process Hierarchy: Gerarchia padre-figlio
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Comando da eseguire')

    # Comando: list
    list_parser = subparsers.add_parser('list', help='Lista processi')
    list_parser.add_argument('--sort', choices=['pid', 'name', 'cpu', 'memory', 'threads'],
                           default='cpu', help='Campo ordinamento')
    list_parser.add_argument('--filter', help='Filtra per nome')
    list_parser.add_argument('--limit', type=int, default=20, help='Limite processi')
    list_parser.add_argument('--all', action='store_true', help='Mostra tutti')

    # Comando: tree
    tree_parser = subparsers.add_parser('tree', help='Mostra albero processi')
    tree_parser.add_argument('--pid', type=int, help='PID radice sottoalbero')
    tree_parser.add_argument('--depth', type=int, default=-1, help='Profondità massima')

    # Comando: watch
    watch_parser = subparsers.add_parser('watch', help='Modalità auto-refresh')
    watch_parser.add_argument('--interval', type=int, default=2, help='Secondi tra refresh')
    watch_parser.add_argument('--sort', choices=['pid', 'name', 'cpu', 'memory'],
                            default='cpu', help='Campo ordinamento')

    # Comando: search
    search_parser = subparsers.add_parser('search', help='Cerca processi')
    search_parser.add_argument('query', help='Termine ricerca')
    search_parser.add_argument('--case-sensitive', action='store_true',
                            help='Ricerca case-sensitive')

    # Comando: kill
    kill_parser = subparsers.add_parser('kill', help='Termina processo')
    kill_parser.add_argument('pid', type=int, help='PID processo')
    kill_parser.add_argument('--method', choices=['sigterm', 'sigkill', 'sigint'],
                           default='sigterm', help='Metodo terminazione')
    kill_parser.add_argument('--force', action='store_true',
                           help='Forza senza conferma')

    # Comando: details
    details_parser = subparsers.add_parser('details', help='Mostra dettagli processo')
    details_parser.add_argument('pid', type=int, help='PID processo')

    # Comando: stats
    stats_parser = subparsers.add_parser('stats', help='Statistiche sistema')

    args = parser.parse_args()

    # Nessun comando fornito
    if not args.command:
        parser.print_help()
        return 0

    # Esegui comando
    ui = ProcessManagerUI()

    try:
        if args.command == 'list':
            ui.list_processes(
                sort_by=args.sort,
                filter_name=args.filter,
                limit=args.limit,
                show_all=args.all
            )

        elif args.command == 'tree':
            ui.show_tree(root_pid=args.pid, max_depth=args.depth)

        elif args.command == 'watch':
            ui.watch_processes(interval=args.interval, sort_by=args.sort)

        elif args.command == 'search':
            ui.search_processes(args.query, args.case_sensitive)

        elif args.command == 'kill':
            ui.kill_process(args.pid, args.method, args.force)

        elif args.command == 'details':
            ui.show_details(args.pid)

        elif args.command == 'stats':
            ui.show_stats()

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Operazione interrotta")
        return 130
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
