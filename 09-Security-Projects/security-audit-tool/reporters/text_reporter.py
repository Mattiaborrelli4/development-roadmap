"""
Text Reporter Module
Genera report in formato testuale/console
"""

from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint


class TextReporter:
    """Generatore di report testuali."""

    def __init__(self):
        self.console = Console()

    def generate(self, findings: List[Dict], verbose: bool = False) -> None:
        """
        Genera il report testuale.

        Args:
            findings: Lista di vulnerabilità trovate
            verbose: Mostra dettagli aggiuntivi
        """
        if not findings:
            self._print_no_findings()
            return

        # Ordina per severità
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        findings.sort(key=lambda x: severity_order.get(x.get('severity', 'LOW'), 4))

        # Intestazione
        self._print_header(len(findings))

        # Raggruppa per severità
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_findings = [f for f in findings if f.get('severity') == severity]
            if severity_findings:
                self._print_severity_section(severity, severity_findings, verbose)

        # Statistiche finali
        self._print_statistics(findings)

        # Disclaimer
        self._print_disclaimer()

    def _print_no_findings(self):
        """Stampa messaggio quando non ci sono vulnerabilità."""
        self.console.print("\n" + "="*80, style="bold")
        self.console.print("[bold green]✓ NESSUNA VULNERABILITÀ TROVATA[/bold green]\n")
        self.console.print("Non sono state rilevate vulnerabilità di sicurezza nel codice analizzato.")
        self.console.print("\n[yellow]💡 Nota:[/yellow] Questo non garantisce che il codice sia completamente sicuro.")
        self.console.print("Una revisione manuale umana è sempre raccomandata.")
        self.console.print()

    def _print_header(self, total_findings: int):
        """Stampa l'intestazione del report."""
        self.console.print("\n" + "="*80, style="bold")
        self.console.print(f"[bold cyan]🔍 RISULTATI AUDIT DI SICUREZZA[/bold cyan]")
        self.console.print(f"[bold]Vulnerabilità trovate: {total_findings}[/bold]")
        self.console.print()

    def _print_severity_section(self, severity: str, findings: List[Dict], verbose: bool):
        """Stampa una sezione per livello di severità."""
        # Colore per severità
        colors = {
            'CRITICAL': 'red',
            'HIGH': 'orange1',
            'MEDIUM': 'yellow',
            'LOW': 'blue'
        }
        color = colors.get(severity, 'white')

        # Titolo sezione
        self.console.print(f"[bold {color}]═══ {severity} ({len(findings)}) ═══[/bold {color}]")
        self.console.print()

        # Tabella risultati
        table = Table(show_header=True, header_style=f"bold {color}", show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Tipo", style="cyan", width=20)
        table.add_column("File", style="green")
        table.add_column("Riga", style="yellow", width=5)
        table.add_column("Codice", style="dim")

        for i, finding in enumerate(findings, 1):
            table.add_row(
                str(i),
                finding.get('type', 'unknown').replace('_', ' ').title(),
                finding.get('file', 'unknown')[:60],
                str(finding.get('line', '?')),
                finding.get('code', '')[:50]
            )

        self.console.print(table)
        self.console.print()

        # Dettagli se verbose
        if verbose:
            for i, finding in enumerate(findings, 1):
                self._print_finding_details(finding, i)

    def _print_finding_details(self, finding: Dict, index: int):
        """Stampa dettagli di una vulnerabilità."""
        severity = finding.get('severity', 'UNKNOWN')
        color = {
            'CRITICAL': 'red',
            'HIGH': 'orange1',
            'MEDIUM': 'yellow',
            'LOW': 'blue'
        }.get(severity, 'white')

        # Panel
        panel_content = f"""
[bold cyan]Tipo:[/bold cyan] {finding.get('type', 'unknown').replace('_', ' ').title()}
[bold cyan]Titolo:[/bold cyan] {finding.get('title', 'Nessun titolo')}
[bold cyan]CWE:[/bold cyan] {finding.get('cwe', 'N/A')}

[bold]Descrizione:[/bold]
{finding.get('description', 'Nessuna descrizione')}

[bold]File:[/bold] {finding.get('file', 'unknown')}
[bold]Riga:[/bold] {finding.get('line', '?')}

[bold]Codice:[/bold]
{finding.get('code', 'N/A')}

[bold]Pattern:[/bold] {finding.get('pattern_matched', 'N/A')}

[bold yellow]💡 Raccomandazione:[/bold yellow]
{finding.get('recommendation', 'Nessuna raccomandazione disponibile')}
"""

        if finding.get('references'):
            panel_content += f"\n[bold]📚 Riferimenti:[/bold]\n"
            for ref in finding.get('references', []):
                panel_content += f"  • {ref}\n"

        self.console.print(Panel(
            panel_content,
            title=f"[{color}]Vulnerabilità #{index}[/{color}]",
            border_style=color,
            padding=(1, 2)
        ))
        self.console.print()

    def _print_statistics(self, findings: List[Dict]):
        """Stampa statistiche delle vulnerabilità."""
        # Conta per tipo
        type_counts = {}
        for finding in findings:
            ftype = finding.get('type', 'unknown')
            type_counts[ftype] = type_counts.get(ftype, 0) + 1

        # Conta per severità
        severity_counts = {}
        for finding in findings:
            sev = finding.get('severity', 'UNKNOWN')
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        # Tabella statistiche
        self.console.print("[bold]📊 STATISTICHE[/bold]\n")

        # Per tipo
        table_type = Table(title="Vulnerabilità per Tipo", show_header=True)
        table_type.add_column("Tipo", style="cyan")
        table_type.add_column("Conteggio", justify="right", style="bold")

        for ftype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            table_type.add_row(ftype.replace('_', ' ').title(), str(count))

        self.console.print(table_type)
        self.console.print()

    def _print_disclaimer(self):
        """Stampa il disclaimer finale."""
        disclaimer = """
[yellow]⚠️  DISCLAIMER IMPORTANTE ⚠️[/yellow]

I risultati forniti da questo strumento sono [bold]indicativi[/bold] e non sostituiscono
un penetration test professionale o una revisione umana approfondita.

[bold]Ricorda di:[/bold]
• Verificare manualmente ogni vulnerabilità rilevata
• Considerare il contesto di utilizzo del codice
• Testare eventuali fix in un ambiente di test
• Mantenere aggiornate le dipendenze

Questo strumento è creato per scopi [bold]EDUCATIVI e DIFENSIVI[/bold].
Utilizzare solo su codice di propria proprietà o con esplicito permesso.
        """
        self.console.print(Panel(disclaimer, border_style="yellow"))
        self.console.print()
