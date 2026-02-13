#!/usr/bin/env python3
"""
Log Analyzer - Demo Script
Mostra le funzionalità principali del tool
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from parsers import ApacheLogParser, CustomLogParser
from analyzers import LogStatistics, DataExtractor, LogFilter
from reporters import TextReporter


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_apache_parser():
    """Demo Apache log parser"""
    print_header("DEMO 1: Apache Log Parser")

    # Sample Apache log lines
    sample_logs = [
        '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326',
        '192.168.1.100 - - [10/Oct/2023:13:55:40 +0000] "POST /api/login HTTP/1.1" 401 567',
        '192.168.1.101 - - [10/Oct/2023:13:55:42 +0000] "GET /admin HTTP/1.1" 403 234',
    ]

    parser = ApacheLogParser()

    print("Parsing Apache log entries:")
    for line in sample_logs:
        parsed = parser.parse_line(line)
        if parsed:
            print(f"  ✓ {parsed['ip']} - {parsed['method']} {parsed['path']} - {parsed['status']}")


def demo_custom_parser():
    """Demo custom application log parser"""
    print_header("DEMO 2: Custom Application Log Parser")

    sample_logs = [
        '2024-01-15 10:30:00,123 [INFO] [main] Application started',
        '2024-01-15 10:30:05,456 [ERROR] [database] Connection failed',
        '2024-01-15 10:30:10,567 [WARN] [memory] Memory usage at 75%',
    ]

    parser = CustomLogParser()

    print("Parsing custom application log entries:")
    for line in sample_logs:
        parsed = parser.parse_line(line)
        if parsed:
            level = parsed.get('level', '???')
            message = parsed.get('message', line[:60])
            print(f"  [{level}] {message}")


def demo_statistics():
    """Demo statistics generation"""
    print_header("DEMO 3: Statistics Generation")

    # Sample entries
    sample_entries = [
        {'level': 'INFO', 'status': 200, 'ip': '192.168.1.100', 'path': '/index.html', 'timestamp_parsed': None},
        {'level': 'INFO', 'status': 200, 'ip': '192.168.1.100', 'path': '/about', 'timestamp_parsed': None},
        {'level': 'ERROR', 'status': 500, 'ip': '192.168.1.101', 'path': '/api/data', 'timestamp_parsed': None},
        {'level': 'WARN', 'status': 404, 'ip': '192.168.1.102', 'path': '/missing', 'timestamp_parsed': None},
        {'level': 'ERROR', 'status': 401, 'ip': '192.168.1.103', 'path': '/admin', 'timestamp_parsed': None},
        {'level': 'INFO', 'status': 200, 'ip': '192.168.1.100', 'path': '/contact', 'timestamp_parsed': None},
    ]

    stats = LogStatistics(sample_entries)

    print("Statistics:")
    print(f"  Total entries: {len(sample_entries)}")
    print(f"  By level: {stats.count_by_level()}")
    print(f"  By status: {stats.http_status_codes()}")
    print(f"  Top IPs: {stats.top_ips(3)}")
    print(f"  Top paths: {stats.top_paths(3)}")


def demo_filtering():
    """Demo log filtering"""
    print_header("DEMO 4: Log Filtering")

    sample_entries = [
        {'level': 'INFO', 'status': 200, 'ip': '192.168.1.100', 'path': '/index.html'},
        {'level': 'WARN', 'status': 404, 'ip': '192.168.1.100', 'path': '/missing'},
        {'level': 'ERROR', 'status': 500, 'ip': '192.168.1.101', 'path': '/api/data'},
        {'level': 'ERROR', 'status': 401, 'ip': '192.168.1.102', 'path': '/admin'},
        {'level': 'INFO', 'status': 200, 'ip': '192.168.1.103', 'path': '/about'},
    ]

    print("Original entries:", len(sample_entries))

    # Filter by level
    errors = LogFilter().by_min_level('ERROR').apply(sample_entries)
    print(f"  Errors only (ERROR+): {len(errors)} entries")

    # Filter by IP
    ip_filtered = LogFilter().by_ip('192.168.1.100').apply(sample_entries)
    print(f"  From IP 192.168.1.100: {len(ip_filtered)} entries")

    # Filter by status range
    failed = LogFilter().by_status_range(400, 599).apply(sample_entries)
    print(f"  Failed requests (4xx-5xx): {len(failed)} entries")


def demo_extraction():
    """Demo data extraction"""
    print_header("DEMO 5: Data Extraction")

    sample_entries = [
        {'message': 'Connection failed for 192.168.1.100', 'ip': '192.168.1.100', 'level': 'ERROR'},
        {'message': 'SQL injection attempt from 10.0.0.1', 'ip': '10.0.0.1', 'level': 'ERROR'},
        {'message': 'Database timeout for 192.168.1.100', 'ip': '192.168.1.100', 'level': 'ERROR'},
        {'message': 'Request successful', 'ip': '192.168.1.101', 'level': 'INFO'},
    ]

    extractor = DataExtractor()

    print("Data extraction:")

    # Extract IPs
    ips = extractor.extract_ips(sample_entries)
    print(f"  Unique IPs: {ips}")

    # Extract error patterns
    errors = extractor.extract_error_patterns(sample_entries)
    for category, messages in errors.items():
        if messages:
            print(f"  {category}: {len(messages)} occurrences")


def demo_text_report():
    """Demo text report generation"""
    print_header("DEMO 6: Text Report Generation")

    # Create sample stats
    stats = {
        'total_entries': 150,
        'unique_ips': 12,
        'time_range': {
            'first_timestamp': None,
            'last_timestamp': None,
        },
        'by_level': {'INFO': 100, 'WARN': 30, 'ERROR': 15, 'DEBUG': 5},
        'http_status_codes': {200: 100, 404: 25, 500: 15, 403: 10},
        'top_errors': [
            ('Database connection failed', 10),
            ('File not found', 5),
        ],
        'top_ips': [
            ('192.168.1.100', 50),
            ('192.168.1.101', 30),
        ],
        'top_paths': [
            ('/index.html', 40),
            ('/api/users', 25),
        ],
        'by_hour': {
            '2024-01-15 10:00': 50,
            '2024-01-15 11:00': 60,
            '2024-01-15 12:00': 40,
        },
        'error_rate': {'total': 150, 'errors': 15, 'error_rate': 10.0},
        'avg_response_size': {'avg_size': 15432.5, 'total_size': 2314875},
    }

    reporter = TextReporter()
    report = reporter.generate_summary(stats)
    print(report)


def demo_file_analysis():
    """Demo analyzing sample log file"""
    print_header("DEMO 7: Analyze Sample Log File")

    sample_file = Path(__file__).parent / 'sample-logs' / 'access.log'

    if not sample_file.exists():
        print(f"Sample file not found: {sample_file}")
        return

    print(f"Analyzing: {sample_file}\n")

    # Parse file
    parser = ApacheLogParser()
    entries = parser.parse_file(str(sample_file))

    print(f"Parsed {len(entries)} log entries\n")

    if entries:
        # Generate statistics
        stats = LogStatistics(entries)

        print("Quick Stats:")
        print(f"  Total entries: {len(entries)}")
        print(f"  Unique IPs: {stats.unique_ips()}")
        print(f"  By level: {stats.count_by_level()}")
        print(f"  Top IPs: {stats.top_ips(5)}")

        # Show sample entries
        print("\nSample entries:")
        for entry in entries[:3]:
            print(f"  {entry['ip']} - {entry['method']} {entry['path']} - {entry['status']}")


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("  LOG ANALYZER - DEMO".center(80))
    print("  Educational Tool for System Programming".center(80))
    print("=" * 80)

    try:
        demo_apache_parser()
        demo_custom_parser()
        demo_statistics()
        demo_filtering()
        demo_extraction()
        demo_text_report()
        demo_file_analysis()

        print_header("DEMO COMPLETED")
        print("All demos ran successfully!")
        print("\nNext steps:")
        print("  1. Try: python main.py analyze sample-logs/access.log")
        print("  2. Try: python main.py tail sample-logs/access.log")
        print("  3. Try: python main.py stats sample-logs/access.log --by hour")
        print("  4. Try: python main.py analyze sample-logs/access.log --output report.html")
        print()

    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
