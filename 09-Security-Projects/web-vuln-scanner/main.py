"""
Web Vulnerability Scanner - Main Entry Point
Educational and Defensive Security Tool

⚠️ LEGAL DISCLAIMER:
This tool is for EDUCATIONAL and DEFENSIVE purposes ONLY.
Only scan YOUR OWN applications or applications you have EXPLICIT WRITTEN PERMISSION to test.
Unauthorized security testing is ILLEGAL.
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
import click
from rich.console import Console
from rich.progress import Progress
import aiohttp

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scanners.crawler import WebCrawler
from scanners.sql_injection import SQLiScanner
from scanners.xss_scanner import XSSScanner
from scanners.auth_scanner import AuthScanner
from scanners.config_scanner import ConfigScanner
from reporters.report_generator import ReportGenerator


console = Console()


class PermissionChecker:
    """Checks for explicit permission to scan"""

    @staticmethod
    def verify_permission(permission_file: str = None) -> bool:
        """
        Verify that user has permission to scan target

        Args:
            permission_file: Path to permission file

        Returns:
            True if permission verified
        """
        if permission_file:
            try:
                with open(permission_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for required fields
                required = ['I,', 'have explicit permission', 'Target:', 'Date:', 'Signature:']

                if all(field in content for field in required):
                    console.print("[✓] Permission file verified", style="green")
                    return True
                else:
                    console.print("[✗] Invalid permission file format", style="red")
                    return False

            except FileNotFoundError:
                console.print(f"[!] Permission file not found: {permission_file}", style="red")
                return False

        # Interactive confirmation
        console.print("\n" + "="*60, style="yellow")
        console.print("⚠️  LEGAL DISCLAIMER", style="bold red")
        console.print("="*60, style="yellow")
        console.print("\nThis scanner is for EDUCATIONAL and DEFENSIVE purposes ONLY.")
        console.print("By using this tool, you confirm that:")
        console.print("  1. You own the target application OR")
        console.print("  2. You have EXPLICIT WRITTEN PERMISSION to test it")
        console.print("\nUnauthorized security testing is ILLEGAL.")
        console.print("You are responsible for ensuring you have proper authorization.")
        console.print("="*60 + "\n", style="yellow")

        response = console.input("[bold yellow]Do you have permission to scan this target? (yes/no): ").lower()

        if response == 'yes':
            console.print("[✓] Permission acknowledged", style="green")
            return True
        else:
            console.print("[✗] Scanning aborted. No permission.", style="red")
            return False


class WebVulnScanner:
    """Main vulnerability scanner class"""

    def __init__(self, target_url: str, config: Dict[str, Any] = None):
        """
        Initialize scanner

        Args:
            target_url: Target URL to scan
            config: Scanner configuration
        """
        self.target_url = target_url
        self.config = config or {}
        self.findings = []
        self.scan_info = {}

    async def scan(self, checks: List[str] = None,
                   max_pages: int = 50) -> List[Dict[str, Any]]:
        """
        Run vulnerability scan

        Args:
            checks: List of checks to run (sqli, xss, auth, config)
            max_pages: Maximum pages to crawl

        Returns:
            List of findings
        """
        if not checks:
            checks = ['sqli', 'xss', 'auth', 'config']

        start_time = time.time()

        console.print(f"\n[*] Starting scan of: {self.target_url}", style="blue")
        console.print(f"[*] Checks enabled: {', '.join(checks)}", style="blue")

        all_findings = []

        async with aiohttp.ClientSession() as session:
            # Phase 1: Crawl website
            console.print("\n[*] Phase 1: Crawling website...", style="cyan")
            crawler = WebCrawler(
                base_url=self.target_url,
                max_pages=max_pages,
                max_depth=3,
                delay=0.2,
                respect_robots=True
            )

            crawl_results = await crawler.crawl()

            console.print(f"[+] Crawled {crawl_results['total_pages']} page(s)", style="green")
            console.print(f"[+] Found {crawl_results['total_forms']} form(s)", style="green")

            self.scan_info = {
                'target': self.target_url,
                'pages_scanned': crawl_results['total_pages'],
                'forms_tested': len(crawl_results['forms']),
                'checks_performed': checks
            }

            # Phase 2: Test forms
            console.print("\n[*] Phase 2: Testing for vulnerabilities...", style="cyan")

            if 'sqli' in checks and crawl_results['forms']:
                console.print("\n[*] Testing for SQL Injection...", style="yellow")
                sqli_scanner = SQLiScanner()

                for form in crawl_results['forms']:
                    findings = await sqli_scanner.scan_form(form, session, self.target_url)
                    all_findings.extend(findings)

                # Also test URL parameters
                for url in crawl_results['visited_urls'][:10]:  # Limit to 10 URLs
                    if '?' in url:
                        findings = await sqli_scanner.scan_url(url, session)
                        all_findings.extend(findings)

            if 'xss' in checks and crawl_results['forms']:
                console.print("\n[*] Testing for XSS...", style="yellow")
                xss_scanner = XSSScanner()

                for form in crawl_results['forms']:
                    findings = await xss_scanner.scan_form(form, session, self.target_url)
                    all_findings.extend(findings)

                # Also test URL parameters
                for url in crawl_results['visited_urls'][:10]:
                    if '?' in url:
                        findings = await xss_scanner.scan_url(url, session)
                        all_findings.extend(findings)

            if 'auth' in checks:
                console.print("\n[*] Testing Authentication...", style="yellow")
                auth_scanner = AuthScanner()
                findings = await auth_scanner.scan(self.target_url, session, crawl_results)
                all_findings.extend(findings)

            if 'config' in checks:
                console.print("\n[*] Testing Security Configuration...", style="yellow")
                config_scanner = ConfigScanner()
                findings = await config_scanner.scan(self.target_url, session)
                all_findings.extend(findings)

        # Calculate duration
        duration = time.time() - start_time
        self.scan_info['duration'] = f"{duration:.2f} seconds"

        self.findings = all_findings

        # Print summary
        console.print(f"\n[+] Scan completed in {self.scan_info['duration']}", style="green")
        console.print(f"[+] Total findings: {len(all_findings)}", style="green")

        if all_findings:
            console.print("\n[!] Findings by severity:", style="yellow")
            severity_counts = {}
            for f in all_findings:
                sev = f.get('severity', 'Info')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1

            for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']:
                if severity in severity_counts:
                    console.print(f"    - {severity}: {severity_counts[severity]}", style="red")

        return all_findings

    def generate_report(self, output_file: str = 'report.html', format: str = 'html'):
        """Generate security report"""
        if not self.findings:
            console.print("[!] No findings to report", style="yellow")
            return

        generator = ReportGenerator()
        generator.generate_report(
            findings=self.findings,
            scan_info=self.scan_info,
            output_file=output_file,
            format=format
        )


# CLI Interface
@click.group()
def cli():
    """Web Vulnerability Scanner - Educational Security Tool"""
    pass


@cli.command()
@click.argument('target')
@click.option('--permission-file', '-p', help='Path to permission file')
@click.option('--report', '-r', default='report.html', help='Output report file')
@click.option('--format', '-f', default='html', type=click.Choice(['html', 'pdf', 'json']),
              help='Report format')
@click.option('--checks', '-c', help='Comma-separated list of checks (sqli,xss,auth,config)')
@click.option('--max-pages', '-m', default=50, help='Maximum pages to crawl')
@click.option('--no-permission-check', is_flag=True, help='Skip permission check (NOT RECOMMENDED)')
def scan(target, permission_file, report, format, checks, max_pages, no_permission_check):
    """
    Scan a target web application for vulnerabilities

    TARGET: URL of the target application (e.g., https://example.com)
    """
    # Check permission
    if not no_permission_check:
        if not PermissionChecker.verify_permission(permission_file):
            console.print("[!] Aborting scan", style="red")
            return

    # Parse checks
    if checks:
        checks_list = [c.strip().lower() for c in checks.split(',')]
        valid_checks = ['sqli', 'xss', 'auth', 'config']
        checks_list = [c for c in checks_list if c in valid_checks]
    else:
        checks_list = ['sqli', 'xss', 'auth', 'config']

    # Run scan
    scanner = WebVulnScanner(target)

    try:
        findings = asyncio.run(scanner.scan(checks=checks_list, max_pages=max_pages))

        # Generate report
        if findings:
            scanner.generate_report(output_file=report, format=format)

    except KeyboardInterrupt:
        console.print("\n[!] Scan interrupted by user", style="yellow")
    except Exception as e:
        console.print(f"[!] Error during scan: {e}", style="red")


@cli.command()
@click.argument('target')
def quick(target):
    """Quick scan with basic checks"""
    console.print("[*] Running quick scan...", style="cyan")

    if not PermissionChecker.verify_permission():
        return

    scanner = WebVulnScanner(target)

    try:
        findings = asyncio.run(scanner.scan(checks=['sqli', 'xss'], max_pages=20))

        if findings:
            scanner.generate_report(output_file='quick_report.html')

    except Exception as e:
        console.print(f"[!] Error: {e}", style="red")


@cli.command()
def disclaimer():
    """Show legal disclaimer"""
    console.print("\n" + "="*60, style="yellow")
    console.print("⚠️  LEGAL DISCLAIMER", style="bold red")
    console.print("="*60, style="yellow")
    console.print("""
Web Vulnerability Scanner - Educational and Defensive Security Tool

This tool is intended SOLELY for:

1. Testing applications YOU OWN
2. Testing applications with EXPLICIT WRITTEN PERMISSION
3. Educational purposes in isolated lab environments
4. Defensive security research

By using this tool, you agree that:

• You have legal authorization to scan the target
• You will use findings responsibly and ethically
• You will report vulnerabilities to the appropriate parties
• You understand unauthorized testing is illegal

The authors and contributors of this tool:
• Are NOT responsible for misuse
• Are NOT responsible for any damage caused
• Provide this tool for educational and defensive purposes ONLY

Always:
• Get written permission before scanning
• Follow responsible disclosure practices
• Respect laws and regulations in your jurisdiction
• Use findings to improve security, not exploit it

Remember: With great power comes great responsibility.
""")
    console.print("="*60 + "\n", style="yellow")


if __name__ == '__main__':
    cli()
