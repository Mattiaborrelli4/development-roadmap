#!/usr/bin/env python3
"""
Security Audit Tool - Strumento di Analisi di Sicurezza Educativo/Difensivo
Versione 1.0.0

⚠️  DISCLAIMER IMPORTANTE ⚠️
Questo strumento è creato ESCLUSIVAMENTe per scopi EDUCATIVI e DIFENSIVI.
- Utilizzare solo su codice di tua proprietà o con esplicito permesso
- Non utilizzare per scopi offensivi o illegali
- Rispettare le leggi locali e i termini di servizio
- L'autore non è responsabile per usi impropri

Scopo: Aiutare gli sviluppatori a identificare e correggere vulnerabilità
nel proprio codice per migliorare la sicurezza delle applicazioni.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import click
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from datetime import datetime

# Aggiungi il percorso del progetto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from parsers.code_reader import CodeReader
from parsers.ast_parser import ASTParser
from analyzers.sql_injection import SQLInjectionAnalyzer
from analyzers.xss_detector import XSSAnalyzer
from analyzers.credentials import CredentialsAnalyzer
from analyzers.dependencies import DependenciesAnalyzer
from analyzers.crypto import CryptoAnalyzer
from analyzers.validation import ValidationAnalyzer
from reporters.html_reporter import HTMLReporter
from reporters.text_reporter import TextReporter

console = Console()


def print_banner():
    """Stampa il banner iniziale dello strumento."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🔒 SECURITY AUDIT TOOL v1.0.0 🔒                      ║
    ║        Strumento di Analisi di Sicurezza                    ║
    ║        Scopo: EDUCATIVO / DIFENSIVO                         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))
    console.print("\n⚠️  [bold red]DISCLAIMER IMPORTANTE[/bold red] ⚠️\n", style="bold")
    console.print("Questo strumento è creato ESCLUSIVAMENTe per scopi EDUCATIVI e DIFENSIVI.\n"
                  "Utilizzare solo su codice di tua proprietà o con esplicito permesso.\n"
                  "Non utilizzare per scopi offensivi o illegali.\n")
    console.print("="*80, style="dim")
    console.print()


def load_patterns(config_path: str = None) -> Dict[str, Any]:
    """Carica i pattern di vulnerabilità dal file YAML."""
    if config_path is None:
        config_path = project_root / "config" / "patterns.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        console.print(f"[red]❌ Errore: File di configurazione non trovato: {config_path}[/red]")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_target_path(target_path: str) -> Path:
    """Valida che il percorso target esista e sia accessibile."""
    path = Path(target_path).resolve()

    if not path.exists():
        console.print(f"[red]❌ Errore: Il percorso specificato non esiste: {target_path}[/red]")
        console.print(f"[yellow]💡 Suggerimento: Verifica che il percorso sia corretto.[/yellow]")
        sys.exit(1)

    # Verifica che sia un codice che l'utente ha il permesso di analizzare
    console.print(f"[cyan]🔍 Analizzando: {path}[/cyan]")
    return path


def filter_by_severity(findings: List[Dict], severity_levels: str) -> List[Dict]:
    """Filtra i risultati per livello di severità."""
    if not severity_levels:
        return findings

    allowed = [s.strip().upper() for s in severity_levels.split(',')]
    return [f for f in findings if f.get('severity', '').upper() in allowed]


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Security Audit Tool - Strumento di Analisi di Sicurezza

    Strumento EDUCATIVO/DIFENSIVO per identificare vulnerabilità comuni
    nel codice sorgente. Aiuta gli sviluppatori a scrivere codice più sicuro.
    """
    pass


@cli.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.option('--report', '-r', type=click.Path(), help='Percorso del file report (HTML)')
@click.option('--severity', '-s', type=str, help='Filtra per severità (es: high,critical)')
@click.option('--output', '-o', type=click.Choice(['text', 'html', 'both']), default='text',
              help='Formato output (default: text)')
@click.option('--config', '-c', type=click.Path(), help='Percorso file config YAML personalizzato')
@click.option('--verbose', '-v', is_flag=True, help='Output dettagliato')
def audit(target_path: str, report: Optional[str], severity: Optional[str],
          output: str, config: Optional[str], verbose: bool):
    """
    Esegue un audit di sicurezza sul codice sorgente.

    TARGET_PATH: Percorso del file o directory da analizzare

    Esempi:
      python main.py audit ./myproject
      python main.py audit ./myproject --report security_report.html
      python main.py audit ./myproject --severity critical,high
      python main.py audit ./myproject --output both --report report.html
    """
    print_banner()

    # Valida percorso target
    console.print(f"\n[bold cyan]📂 Target:[/bold cyan] {target_path}")
    console.print(f"[bold cyan]📊 Output:[/bold cyan] {output.upper()}")
    if severity:
        console.print(f"[bold cyan]🎯 Severità:[/bold cyan] {severity}")
    console.print()

    target = validate_target_path(target_path)

    # Carica pattern di vulnerabilità
    patterns = load_patterns(config)

    # Inizializza componenti
    console.print("[bold blue]⚙️  Inizializzazione componenti...[/bold blue]")
    code_reader = CodeReader(target)
    ast_parser = ASTParser()

    # Inizializza analyzer
    analyzers = {
        'sql_injection': SQLInjectionAnalyzer(patterns.get('sql_injection', {})),
        'xss': XSSAnalyzer(patterns.get('xss', {})),
        'credentials': CredentialsAnalyzer(patterns.get('hardcoded_credentials', {})),
        'dependencies': DependenciesAnalyzer(patterns.get('dependencies', {})),
        'crypto': CryptoAnalyzer(patterns.get('weak_crypto', {})),
        'validation': ValidationAnalyzer(patterns.get('input_validation', {}))
    }

    # Leggi i file di codice
    with console.status("[bold green]📂 Scansionando file di codice...", spinner="dots"):
        code_files = code_reader.scan_files()

    if not code_files:
        console.print("[yellow]⚠️  Nessun file di codice trovato da analizzare.[/yellow]")
        sys.exit(0)

    console.print(f"[green]✓ Trovati {len(code_files)} file da analizzare[/green]")
    console.print()

    # Esegui analisi con progress bar
    all_findings = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        # Analizza SQL Injection
        task = progress.add_task("[cyan]🔍 Analizzando SQL Injection...", total=None)
        findings = analyzers['sql_injection'].analyze(code_files)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] SQL Injection: {len(findings)} vulnerabilità trovate")

        # Analizza XSS
        task = progress.add_task("[cyan]🔍 Analizzando XSS...", total=None)
        findings = analyzers['xss'].analyze(code_files)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] XSS: {len(findings)} vulnerabilità trovate")

        # Analizza Credenziali Hardcoded
        task = progress.add_task("[cyan]🔍 Analizzando credenziali hardcoded...", total=None)
        findings = analyzers['credentials'].analyze(code_files)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] Credenziali: {len(findings)} vulnerabilità trovate")

        # Analizza Dipendenze
        task = progress.add_task("[cyan]🔍 Analizzando dipendenze...", total=None)
        findings = analyzers['dependencies'].analyze(target)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] Dipendenze: {len(findings)} vulnerabilità trovate")

        # Analizza Crittografia
        task = progress.add_task("[cyan]🔍 Analizzando crittografia...", total=None)
        findings = analyzers['crypto'].analyze(code_files)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] Crittografia: {len(findings)} vulnerabilità trovate")

        # Analizza Validazione Input
        task = progress.add_task("[cyan]🔍 Analizzando validazione input...", total=None)
        findings = analyzers['validation'].analyze(code_files)
        all_findings.extend(findings)
        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] Validazione: {len(findings)} vulnerabilità trovate")

    console.print()

    # Filtra per severità se richiesto
    if severity:
        all_findings = filter_by_severity(all_findings, severity)
        console.print(f"[cyan]🎯 Filtrato per severità: {severity}[/cyan]")
        console.print()

    # Genera report
    console.print("[bold blue]📋 Generazione report...[/bold blue]\n")

    if output in ['text', 'both']:
        text_reporter = TextReporter()
        text_reporter.generate(all_findings, verbose=verbose)

    report_path = None
    if output in ['html', 'both']:
        report_path = report or f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html_reporter = HTMLReporter()
        html_reporter.generate(all_findings, report_path, target)
        console.print(f"[green]✓ Report HTML salvato: {report_path}[/green]")

    # Riepilogo finale
    console.print("\n" + "="*80, style="bold")
    console.print("[bold cyan]📊 RIEPILOGO AUDIT[/bold cyan]\n")

    # Statistiche per severità
    severity_counts = {}
    for finding in all_findings:
        sev = finding.get('severity', 'UNKNOWN').upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # Crea tabella riepilogo
    table = Table(title="Vulnerabilità per Severità", show_header=True, header_style="bold")
    table.add_column("Severità", style="cyan")
    table.add_column("Conteggio", justify="right", style="bold")

    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']
    for sev in severity_order:
        count = severity_counts.get(sev, 0)
        color = {
            'CRITICAL': 'red',
            'HIGH': 'orange1',
            'MEDIUM': 'yellow',
            'LOW': 'blue',
            'UNKNOWN': 'dim'
        }.get(sev, 'white')
        table.add_row(f"[{color}]{sev}[/{color}]", str(count))

    console.print(table)
    console.print()

    # Consigli finali
    if severity_counts.get('CRITICAL', 0) > 0:
        console.print("[red]⚠️  Trovate vulnerabilità CRITICHE! Rileggere e correggere immediatamente.[/red]")
    elif severity_counts.get('HIGH', 0) > 0:
        console.print("[orange1]⚠️  Trovate vulnerabilità HIGH! Valutare la priorità delle correzioni.[/orange1]")
    else:
        console.print("[green]✓ Nessuna vulnerabilità critica rilevata.[/green]")

    console.print("\n[bold cyan]💡 Ricorda:[/bold cyan] Questi risultati sono indicativi. Una revisione manuale "
                  "umana è sempre raccomandata per confermare le vulnerabilità.")
    console.print()

    # Exit code basato sulla severità
    if severity_counts.get('CRITICAL', 0) > 0:
        sys.exit(2)
    elif severity_counts.get('HIGH', 0) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command()
def patterns():
    """Mostra tutti i pattern di vulnerabilità supportati."""
    patterns = load_patterns()

    console.print("\n[bold cyan]📚 Pattern di Vulnerabilità Supportati[/bold cyan]\n")

    for vuln_type, config in patterns.items():
        if vuln_type in ['version', 'last_updated']:
            continue

        severity = config.get('severity', 'UNKNOWN')
        cwe = config.get('cwe', 'N/A')
        description = config.get('description', 'Nessuna descrizione')

        # Colore basato sulla severità
        color = {
            'CRITICAL': 'red',
            'HIGH': 'orange1',
            'MEDIUM': 'yellow',
            'LOW': 'blue'
        }.get(severity, 'white')

        console.print(Panel(
            f"[bold]{vuln_type.upper().replace('_', ' ')}[/bold]\n\n"
            f"[{color}]Severità: {severity}[/{color}]\n"
            f"CWE: {cwe}\n"
            f"Descrizione: {description}",
            border_style=color
        ))
        console.print()


@cli.command()
@click.argument('target_path', type=click.Path(exists=True))
def info(target_path: str):
    """Mostra informazioni sul progetto target."""
    print_banner()

    target = Path(target_path).resolve()
    console.print(f"\n[bold cyan]📂 Analisi Progetto: {target}[/bold cyan]\n")

    code_reader = CodeReader(target)
    files = code_reader.scan_files()

    if not files:
        console.print("[yellow]⚠️  Nessun file di codice trovato.[/yellow]")
        return

    # Statistiche sui file
    extensions = {}
    total_lines = 0

    for file_info in files:
        ext = file_info['extension']
        extensions[ext] = extensions.get(ext, 0) + 1
        total_lines += file_info.get('line_count', 0)

    # Mostra statistiche
    console.print(f"[bold]File totali:[/bold] {len(files)}")
    console.print(f"[bold]Linee di codice:[/bold] {total_lines:,}")
    console.print()

    # Tabella linguaggi
    table = Table(title="Linguaggi Rilevati", show_header=True)
    table.add_column("Estensione", style="cyan")
    table.add_column("File", justify="right")

    for ext, count in sorted(extensions.items()):
        table.add_row(ext, str(count))

    console.print(table)
    console.print()


@cli.command()
def disclaimer():
    """Mostra il disclaimer legale completo."""
    console.print(Panel("""
[bold red]⚠️  DISCLAIMER LEGALE ⚠️[/bold red]

[bold]1. SCOPO EDUCATIVO/DIFENSIVO[/bold]
Questo strumento è creato ESCLUSIVAMENTe per scopi educativi e difensivi.
Aiuta gli sviluppatori a identificare e correggere vulnerabilità nel proprio
codice.

[bold]2. UTILIZCO AUTORIZZATO[/bold]
- Utilizzare SOLO su codice di tua proprietà
- Utilizzare SOLO con esplicito permesso scritto del proprietario
- NON utilizzare su sistemi di terze parti senza autorizzazione

[bold]3. RESPONSABILITÀ[/bold]
L'autore di questo strumento NON è responsabile per:
- Usi impropri o illegali di questo software
- Danni diretti o indiretti causati dall'utilizzo
- Violazioni di leggi o regolamenti

[bold]4. CONFORMITÀ LEGALE[/bold]
L'utente è responsabile di:
- Rispettare tutte le leggi locali e internazionali
- Ottenere le autorizzazioni necessarie prima delle scansioni
- Utilizzare i risultati in modo etico e legale

[bold]5. LIMITAZIONI[/bold]
Questo strumento:
- Non garantisce la rilevazione di tutte le vulnerabilità
- Fornisce risultati indicativi che richiedono verifica umana
- Non sostituisce un penetration test professionale

[bold]6. CONSENSO[/bold]
Utilizzando questo strumento, accetti di:
- Aderire a questi termini
- Assumerti la piena responsabilità del tuo utilizzo
- Utilizzare il software esclusivamente per scopi legali

Per domande o chiarimenti, contattare lo sviluppatore.
""", title="TERMINI DI UTILIZZO", border_style="red bold"))


if __name__ == '__main__':
    cli()
