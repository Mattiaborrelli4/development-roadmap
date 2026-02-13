"""
Web Vulnerability Scanner - Example Usage
Educational and Defensive Security Tool
"""

import asyncio
from main import WebVulnScanner, PermissionChecker


async def basic_scan_example():
    """Example: Basic vulnerability scan"""
    print("\n=== Basic Scan Example ===\n")

    # Check permission
    if not PermissionChecker.verify_permission():
        print("Permission not granted. Aborting.")
        return

    # Create scanner
    scanner = WebVulnScanner('https://example.com')

    # Run scan
    findings = await scanner.scan(
        checks=['sqli', 'xss', 'config'],  # What to test
        max_pages=20                        # Max pages to crawl
    )

    # Generate report
    scanner.generate_report(
        output_file='basic_report.html',
        format='html'
    )

    print(f"\nFound {len(findings)} vulnerabilities")


async def custom_scan_example():
    """Example: Custom configuration scan"""
    print("\n=== Custom Scan Example ===\n")

    # Custom configuration
    config = {
        'max_pages': 100,
        'max_depth': 3,
        'delay': 0.5,  # Slower scan
        'timeout': 30
    }

    scanner = WebVulnScanner('https://example.com', config)

    # Run specific checks only
    findings = await scanner.scan(
        checks=['sqli'],  # Only SQL injection
        max_pages=50
    )

    # Generate PDF report
    scanner.generate_report(
        output_file='sqli_report.pdf',
        format='pdf'
    )


async def target_specific_example():
    """Example: Scan specific forms"""
    print("\n=== Targeted Scan Example ===\n")

    from scanners.sql_injection import SQLiScanner
    from scanners.xss_scanner import XSSScanner
    import aiohttp

    target_form = {
        'action': 'https://example.com/login',
        'method': 'POST',
        'fields': [
            {'name': 'username', 'type': 'text'},
            {'name': 'password', 'type': 'password'}
        ]
    }

    async with aiohttp.ClientSession() as session:
        # Test for SQLi
        sqli_scanner = SQLiScanner()
        sqli_findings = await sqli_scanner.scan_form(
            target_form,
            session,
            'https://example.com/login'
        )

        # Test for XSS
        xss_scanner = XSSScanner()
        xss_findings = await xss_scanner.scan_form(
            target_form,
            session,
            'https://example.com/login'
        )

        all_findings = sqli_findings + xss_findings

        print(f"Found {len(all_findings)} vulnerabilities in login form")


async def crawl_only_example():
    """Example: Just crawl, don't test"""
    print("\n=== Crawl Only Example ===\n")

    from scanners.crawler import WebCrawler

    crawler = WebCrawler(
        base_url='https://example.com',
        max_pages=50,
        max_depth=3,
        delay=0.2
    )

    results = await crawler.crawl()

    print(f"Crawled {results['total_pages']} pages")
    print(f"Found {results['total_forms']} forms")

    # Print URLs
    for url in results['visited_urls'][:10]:
        print(f"  - {url}")


async def report_analysis_example():
    """Example: Analyze scan results"""
    print("\n=== Report Analysis Example ===\n")

    # Assume we have findings
    findings = [
        {
            'vulnerability': 'SQL Injection',
            'severity': 'High',
            'url': 'https://example.com/login',
            'parameter': 'username'
        },
        {
            'vulnerability': 'Missing Header',
            'severity': 'Low',
            'url': 'https://example.com/',
            'header': 'X-Frame-Options'
        }
    ]

    # Analyze by severity
    from collections import defaultdict
    severity_counts = defaultdict(int)

    for f in findings:
        severity_counts[f['severity']] += 1

    print("Findings by Severity:")
    for severity, count in severity_counts.items():
        print(f"  {severity}: {count}")

    # Prioritize fixes
    critical_high = [f for f in findings if f['severity'] in ['Critical', 'High']]
    print(f"\nPriority Fixes: {len(critical_high)}")


def permission_check_example():
    """Example: Verify permission"""
    print("\n=== Permission Check Example ===\n")

    # Option 1: With permission file
    with_permission = PermissionChecker.verify_permission('permission.txt')
    print(f"With file: {with_permission}")

    # Option 2: Interactive (will prompt user)
    # interactive = PermissionChecker.verify_permission()


def safe_testing_practices():
    """Example: Safe testing configuration"""
    print("\n=== Safe Testing Practices ===\n")

    # Always use these settings
    safe_config = {
        'delay': 0.5,              # 500ms between requests
        'max_pages': 20,           # Limit pages
        'timeout': 30,             # 30 second timeout
        'respect_robots': True,    # Respect robots.txt
        'safe_mode': True,         # Enable safe mode
        'read_only': True          # Read-only operations
    }

    print("Safe Testing Checklist:")
    print("✓ Permission obtained")
    print("✓ Rate limiting enabled")
    print("✓ Backup created")
    print("✓ Test environment preferred")
    print("✓ Monitoring ready")
    print("✓ Responsible disclosure plan ready")


# MAIN - Run examples
if __name__ == '__main__':
    print("="*60)
    print("Web Vulnerability Scanner - Example Usage")
    print("="*60)

    # Uncomment the example you want to run:

    # Example 1: Basic scan
    # asyncio.run(basic_scan_example())

    # Example 2: Custom configuration
    # asyncio.run(custom_scan_example())

    # Example 3: Target specific forms
    # asyncio.run(target_specific_example())

    # Example 4: Crawl only
    # asyncio.run(crawl_only_example())

    # Example 5: Report analysis
    # asyncio.run(report_analysis_example())

    # Example 6: Permission check
    # permission_check_example()

    # Example 7: Safe testing practices
    # safe_testing_practices()

    print("\n" + "="*60)
    print("IMPORTANT: Always have permission before scanning!")
    print("="*60)
