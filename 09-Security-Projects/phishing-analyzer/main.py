#!/usr/bin/env python3
"""
Phishing Email Analyzer - Strumento Educativo per l'Analisi delle Email
========================================================================

⚠️  DISCLAIMER IMPORTANTE:
Questo strumento è creato esclusivamente a scopo EDUCATIVO e DIFENSIVO.
Aiuta a identificare e comprendere le email di phishing per proteggersi.

Autore: Progetto educativo
Versione: 1.0.0
Licenza: Educational Use Only
"""

import click
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich import print as rprint
import email
from email import policy
from email.parser import BytesParser

# Aggiungi il path del progetto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzers import (
    HeaderAnalyzer,
    LinkAnalyzer,
    SenderAnalyzer,
    ContentAnalyzer
)
from utils import (
    DNSChecker,
    RiskCalculator,
    format_risk_report,
    explain_spf,
    explain_dmarc,
    explain_dkim
)

console = Console()


def print_banner():
    """Mostra il banner dell'applicazione"""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║          [bold cyan]PHISHING EMAIL ANALYZER[/bold cyan]                             ║
║          [dim]Strumento Educativo per l'Analisi delle Email[/dim]           ║
║                                                                    ║
║          ⚠️  USO EDUCATIVO E DIFENSIVO ⚠️                             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    console.print(banner)


def print_disclaimer():
    """Stampa il disclaimer legale"""
    disclaimer = """
[yellow bold]DISCLAIMER LEGALE[/yellow bold]

Questo strumento è creato esclusivamente a scopo [bold green]EDUCATIVO[/bold green] e
[bold green]DIFENSIVO[/bold green]. L'obiettivo è insegnare a:

  ✓ Identificare le email di phishing
  ✓ Comprendere le tecniche di attacco
  ✓ Proteggersi dalle minacce email
  ✓ Migliorare la consapevolezza della sicurezza

[yellow bold]NON UTILIZZARE per:[/yellow bold]
  ✗ Inviare email di phishing
  ✗ Testare senza autorizzazione
  ✗ Qualsiasi attività illegale

L'utente è il solo responsabile dell'uso di questo strumento.
"""
    console.print(Panel(disclaimer, title="[bold red]⚠️  DISCLAIMER", border_style="red"))


def load_email_file(file_path: str) -> email.message.Message:
    """Carica un file .eml e restituisce l'oggetto email"""
    try:
        with open(file_path, 'rb') as f:
            parser = BytesParser(policy=policy.default)
            email_message = parser.parse(f)
        return email_message
    except FileNotFoundError:
        console.print(f"[red]Errore: File non trovato: {file_path}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Errore nel caricamento della email: {e}[/red]")
        sys.exit(1)


def analyze_email(email_message: email.message.Message) -> dict:
    """
    Esegue l'analisi completa della email

    Args:
        email_message: Oggetto email.message.EmailMessage

    Returns:
        Dict con tutti i risultati dell'analisi
    """
    console.print("\n[bold cyan]🔍 Inizio analisi email...[/bold cyan]")

    results = {}

    # 1. Analizza Header
    console.print("  • Analisi header SPF/DKIM/DMARC...")
    header_analyzer = HeaderAnalyzer()
    results['headers'] = header_analyzer.analyze_headers(email_message)

    # Verifica anche SPF/DMARC del dominio mittente
    sender_analyzer = SenderAnalyzer()
    sender_info = sender_analyzer.analyze_sender(email_message)
    results['sender'] = sender_info

    if sender_info.get('domain'):
        console.print("  • Verifica DNS del dominio...")
        dns_checker = DNSChecker()
        results['sender_spf'] = dns_checker.check_spf(sender_info['domain'])
        results['sender_dmarc'] = dns_checker.check_dmarc(sender_info['domain'])

    # 2. Analizza Link
    console.print("  • Analisi dei link...")
    link_analyzer = LinkAnalyzer()

    # Estrai contenuto testuale
    text_content = extract_text_content(email_message)
    html_content = extract_html_content(email_message)

    results['links'] = link_analyzer.analyze_email_links(text_content, html_content)

    # 3. Analizza Contenuto
    console.print("  • Analisi del contenuto...")
    content_analyzer = ContentAnalyzer()
    results['content'] = content_analyzer.analyze_content(email_message)

    # 4. Calcola Rischio
    console.print("  • Calcolo del rischio...")
    risk_calculator = RiskCalculator()

    # Prepara i dati per il calcolo del rischio
    risk_data = {
        'spf': results.get('sender_spf', {}),
        'dkim': results.get('headers', {}).get('dkim', {}),
        'dmarc': results.get('sender_dmarc', {}),
        'sender': sender_info,
        'links': results.get('links', {}),
        'content': results.get('content', {}),
        'attachments': results.get('content', {}).get('attachments', {})
    }

    results['risk'] = risk_calculator.calculate_risk_score(risk_data)

    return results


def extract_text_content(email_message: email.message.Message) -> str:
    """Estrae il contenuto testuale"""
    text_content = ''
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset() or 'utf-8'
                try:
                    text_content += part.get_payload(decode=True).decode(charset, errors='ignore')
                except:
                    pass
    elif email_message.get_content_type() == 'text/plain':
        charset = email_message.get_content_charset() or 'utf-8'
        try:
            text_content = email_message.get_payload(decode=True).decode(charset, errors='ignore')
        except:
            pass
    return text_content


def extract_html_content(email_message: email.message.Message) -> str:
    """Estrae il contenuto HTML"""
    html_content = ''
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/html':
                charset = part.get_content_charset() or 'utf-8'
                try:
                    html_content += part.get_payload(decode=True).decode(charset, errors='ignore')
                except:
                    pass
    return html_content


def print_analysis_report(results: dict):
    """Stampa il report completo dell'analisi"""
    console.print("\n")

    # Report del rischio
    console.print(Panel(format_risk_report(results['risk']), title="[bold red]⚠️  VALUTAZIONE DEL RISCHIO", border_style="red"))

    # Report mittente
    from analyzers.sender import SenderAnalyzer
    sender_analyzer = SenderAnalyzer()
    if results.get('sender'):
        console.print(Panel(
            sender_analyzer.format_sender_report(results['sender']),
            title="👤 ANALISI MITTENTE",
            border_style="cyan"
        ))

    # Report header
    headers = results.get('headers', {})
    if headers:
        console.print("\n[bold]📧 ANALISI HEADER DI SICUREZZA[/bold]")
        console.print("─" * 60)

        spf = headers.get('spf', {})
        spf_status = spf.get('status', 'none')
        spf_emoji = "✅" if spf_status == 'pass' else "🔴" if spf_status == 'fail' else "⚠️"
        console.print(f"{spf_emoji} SPF: {spf.get('details', 'N/A')}")

        dkim = headers.get('dkim', {})
        dkim_valid = dkim.get('valid')
        if dkim_valid is True:
            console.print("✅ DKIM: Firma valida")
        elif dkim_valid is False:
            console.print("🔴 DKIM: Firma non valida")
        else:
            console.print("⚠️  DKIM: Nessuna firma")

        dmarc = headers.get('dmarc', {})
        dmarc_status = dmarc.get('status', 'none')
        dmarc_emoji = "✅" if dmarc_status == 'pass' else "⚠️"
        console.print(f"{dmarc_emoji} DMARC: {dmarc.get('details', 'N/A')}")

    # Report link
    from analyzers.links import LinkAnalyzer
    link_analyzer = LinkAnalyzer()
    if results.get('links'):
        console.print(Panel(
            link_analyzer.format_link_report(results['links']),
            title="🔗 ANALISI LINK",
            border_style="blue"
        ))

    # Report contenuto
    from analyzers.content import ContentAnalyzer
    content_analyzer = ContentAnalyzer()
    if results.get('content'):
        console.print(Panel(
            content_analyzer.format_content_report(results['content']),
            title="📄 ANALISI CONTENUTO",
            border_style="yellow"
        ))


# CLI Commands
@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Phishing Email Analyzer - Strumento Educativo

    ⚠️  USO EDUCATIVO E DIFENSIVO ⚠️

    Questo strumento aiuta a identificare e comprendere le email di phishing.
    """
    print_banner()
    print_disclaimer()


@cli.command()
@click.argument('email_file', type=click.Path(exists=True))
@click.option('--json', 'output_json', is_flag=True, help='Output in formato JSON')
def analyze(email_file, output_json):
    """
    Analizza un file email (.eml)

    Esempio: python main.py analyze email_phishing.eml
    """
    console.print(f"\n[bold cyan]📂 Caricamento file: {email_file}[/bold cyan]")

    # Carica la email
    email_message = load_email_file(email_file)

    # Mostra informazioni base
    from_header = email_message.get('From', 'N/A')
    subject = email_message.get('Subject', 'N/A')
    console.print(f"  Da: {from_header}")
    console.print(f"  Oggetto: {subject}")

    # Esegui analisi
    results = analyze_email(email_message)

    # Stampa report
    print_analysis_report(results)

    # Messaggio finale
    console.print("\n[bold green]✅ Analisi completata![/bold green]")
    console.print("\n[dim]Ricorda: Se hai dubbi, contatta sempre l'azienda tramite canali ufficiali.[/dim]")


@cli.command()
def stdin():
    """
    Leggi una email dallo standard input

    Esempio: cat email.eml | python main.py analyze --stdin
    """
    import sys

    console.print("\n[bold cyan]📂 Lettura email da stdin...[/bold cyan]")

    # Leggi da stdin
    email_content = sys.stdin.buffer.read()
    parser = BytesParser(policy=policy.default)
    email_message = parser.parsebytes(email_content)

    # Mostra informazioni base
    from_header = email_message.get('From', 'N/A')
    subject = email_message.get('Subject', 'N/A')
    console.print(f"  Da: {from_header}")
    console.print(f"  Oggetto: {subject}")

    # Esegui analisi
    results = analyze_email(email_message)

    # Stampa report
    print_analysis_report(results)


@cli.command()
def explain_spf_cmd():
    """Spiega cos'è l'SPF (Sender Policy Framework)"""
    console.print(explain_spf())


@cli.command()
def explain_dmarc_cmd():
    """Spiega cos'è DMARC (Domain-based Message Authentication)"""
    console.print(explain_dmarc())


@cli.command()
def explain_dkim_cmd():
    """Spiega cos'è DKIM (DomainKeys Identified Mail)"""
    console.print(explain_dkim())


@cli.command()
@click.argument('urls', nargs=-1, required=True)
def check_links(urls):
    """
    Controlla uno o più URL per indicatori sospetti

    Esempio: python main.py check-links https://example.com https://suspicious.com
    """
    from analyzers.links import check_url

    console.print("\n[bold cyan]🔍 Analisi URL[/bold cyan]\n")

    for url in urls:
        console.print(f"[bold]URL: {url}[/bold]")

        result = check_url(url)

        if result.get('suspicious'):
            console.print(f"  [red]⚠️  SOSPETTO - Punteggio: {result['risk_score']}/100[/red]")

            checks = result.get('checks', {})
            issues = []

            if not checks.get('https'):
                issues.append("❌ Non usa HTTPS")
            if checks.get('ip_address'):
                issues.append("❌ Usa indirizzo IP")
            if checks.get('suspicious_tld'):
                issues.append(f"⚠️  TLD sospetto: {checks.get('tld')}")
            if checks.get('shortened'):
                issues.append("⚠️  URL accorziato")
            if checks.get('misspelled'):
                issues.append("❌ Dominio con refuso")
            if checks.get('special_chars'):
                issues.append("❌ Caratteri speciali")
            if checks.get('lookalike_chars'):
                issues.append("❌ Caratteri lookalike")

            for issue in issues:
                console.print(f"  {issue}")
        else:
            console.print("  [green]✅ Nessun indicatore sospetto[/green]")

        console.print()


@cli.command()
@click.argument('domain')
def check_domain(domain):
    """
    Controlla la configurazione DNS di un dominio

    Esempio: python main.py check-domain example.com
    """
    console.print(f"\n[bold cyan]🔍 Analisi DNS: {domain}[/bold cyan]\n")

    dns_checker = DNSChecker()

    # SPF
    console.print("[bold]SPF (Sender Policy Framework)[/bold]")
    spf_result = dns_checker.check_spf(domain)
    console.print(f"  Status: {spf_result['status']}")
    if spf_result.get('record'):
        console.print(f"  Record: {spf_result['record']}")
    console.print(f"  {spf_result['details']}\n")

    # DMARC
    console.print("[bold]DMARC[/bold]")
    dmarc_result = dns_checker.check_dmarc(domain)
    console.print(f"  Status: {dmarc_result['status']}")
    if dmarc_result.get('policy'):
        console.print(f"  Policy: {dmarc_result['policy']}")
    if dmarc_result.get('record'):
        console.print(f"  Record: {dmarc_result['record']}")
    console.print(f"  {dmarc_result['details']}\n")

    # MX
    console.print("[bold]MX (Mail Exchange)[/bold]")
    mx_records = dns_checker.get_mx_records(domain)
    if mx_records:
        for mx in mx_records:
            console.print(f"  • {mx['exchange']} (priorità: {mx['preference']})")
    else:
        console.print("  Nessun record MX trovato")


@cli.command()
def learn():
    """Mostra una guida educativa sul phishing"""
    guide = """
╔════════════════════════════════════════════════════════════════════╗
║              [bold cyan]GUIDA EDUCATIVA SUL PHISHING[/bold cyan]                     ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  [bold yellow]COS'È IL PHISHING?[/bold yellow]                                            ║
║                                                                    ║
║  Il phishing è un tipo di attacco in cui i criminali si spacciano  ║
║  per entità affidabili (banche, aziende, servizi) per rubare:      ║
║  • Password e credenziali                                          ║
║  • Informazioni finanziarie                                        ║
║  • Dati personali                                                  ║
║  • Accesso agli account                                            ║
║                                                                    ║
║  [bold yellow]COME FUNZIONA?[/bold yellow]                                              ║
║                                                                    ║
║  1. L'attaccante invia email fraudolente che sembrano legittime   ║
║  2. La email crea urgenza o preoccupazione                         ║
║  3. Chiede di cliccare un link o aprire un allegato               ║
║  4. Il link porta a un sito falso che ruba i dati                 ║
║  5. Oppure l'allegato installa malware                             ║
║                                                                    ║
║  [bold red]SEGNALI DI PHISHING[/bold red]                                            ║
║                                                                    ║
║  🔴 [bold]Urgenza e Pressione[/bold]                                             ║
║     "Entro 24 ore o il conto verrà chiuso!"                       ║
║     "Azione immediata richiesta!"                                 ║
║                                                                    ║
║  🔴 [bold]Richiesta di Credenziali[/bold]                                        ║
║     "Conferma la tua password"                                     ║
║     "Aggiorna le tue informazioni"                                ║
║     ⚠️  LE AZIENDE NON CHIEDONO MAI PASSWORD VIA EMAIL!            ║
║                                                                    ║
║  🔴 [bold]Link Sospetti[/bold]                                                   ║
║     URL con refusi (paypa1.com invece di paypal.com)              ║
║     Uso di indirizzi IP invece di domini                          ║
║     TLD insolite (.xyz, .top, .zip)                                ║
║                                                                    ║
║  🔴 [bold]Allegati Pericolosi[/bold]                                              ║
║     File .exe, .scr, .bat, .zip                                    ║
║     Doppie estensioni (file.pdf.exe)                               ║
║                                                                    ║
║  [bold green]COME PROTEGGERSI[/bold green]                                              ║
║                                                                    ║
║  ✅ Verifica SEMPRE l'indirizzo del mittente                      ║
║  ✅ Passa il mouse sui link senza cliccare                         ║
║  ✅ Non fidarti delle email che creano urgenza                     ║
║  ✅ Verifica con l'azienda tramite canali ufficiali                ║
║  ✅ Attiva l'autenticazione a due fattori (2FA)                   ║
║  ✅ Mantieni aggiornato il software e l'antivirus                 ║
║  ✅ Usa password forti e diverse per ogni servizio                 ║
║                                                                    ║
║  [bold cyan]SE RICEVI UNA EMAIL SOSPETTA[/bold cyan]                               ║
║                                                                    ║
║  1. [yellow]NON[/yellow] cliccare sui link                                    ║
║  2. [yellow]NON[/yellow] aprire gli allegati                                   ║
║  3. [yellow]NON[/yellow] rispondere alla email                                   ║
║  4. Segnala come spam/phishing                                    ║
║  5. Contatta l'azienda tramite il sito ufficiale                  ║
║                                                                    ║
║  [bold]COME SEGNALE PHISHING:[/bold]                                            ║
║  • Gmail: Segnala come Phishing                                    ║
║  • Outlook: Segnala come Phishing                                  ║
║  • Poste: Inoltra a ante@poste.it                                  ║
║  • Banche: Usa il servizio di segnalazione della banca             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """
    console.print(guide)


if __name__ == '__main__':
    cli()
