"""
Web Vulnerability Scanner - SQL Injection Scanner
Tests for SQL injection vulnerabilities in forms and URLs
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import yaml
import re


class SQLiScanner:
    """Scanner for SQL Injection vulnerabilities"""

    def __init__(self, payloads_file: str = 'config/payloads.yaml'):
        """
        Initialize SQLi scanner

        Args:
            payloads_file: Path to payloads configuration file
        """
        self.payloads = self._load_payloads(payloads_file)
        self.results = []

    def _load_payloads(self, file_path: str) -> Dict[str, List[str]]:
        """Load SQL injection payloads from YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('sql_injection', {})
        except Exception as e:
            print(f"[!] Error loading payloads: {e}")
            return {'basic': [], 'time_based': [], 'boolean_based': []}

    async def scan_form(self, form: Dict[str, Any], session: aiohttp.ClientSession,
                       page_url: str) -> List[Dict[str, Any]]:
        """
        Scan a form for SQL injection vulnerabilities

        Args:
            form: Form data
            session: aiohttp session
            page_url: Page URL

        Returns:
            List of findings
        """
        findings = []
        action_url = form.get('action', page_url)
        method = form.get('method', 'GET')

        print(f"[*] Testing form for SQLi: {action_url}")

        for field in form.get('fields', []):
            if field.get('type') in ['text', 'search', 'number', 'email', 'tel', 'textarea']:
                field_findings = await self._test_field(
                    session, action_url, method, form, field['name'], page_url
                )
                findings.extend(field_findings)

        return findings

    async def _test_field(self, session: aiohttp.ClientSession, url: str,
                          method: str, form: Dict[str, Any],
                          field_name: str, page_url: str) -> List[Dict[str, Any]]:
        """
        Test a form field with SQLi payloads

        Args:
            session: aiohttp session
            url: Form action URL
            method: HTTP method
            form: Form data
            field_name: Field name to test
            page_url: Original page URL

        Returns:
            List of findings
        """
        findings = []

        # Test with basic payloads
        for payload in self.payloads.get('basic', [])[:10]:  # Limit to 10 basic tests
            try:
                # Prepare form data
                data = self._prepare_form_data(form, field_name, payload)

                # Send request
                response = await self._send_request(session, url, method, data)

                # Analyze response
                if self._is_vulnerable(response, payload):
                    findings.append({
                        'vulnerability': 'SQL Injection',
                        'severity': 'High',
                        'url': url,
                        'parameter': field_name,
                        'payload': payload,
                        'method': method,
                        'evidence': self._get_evidence(response),
                        'description': f'Potential SQL injection in parameter "{field_name}"',
                        'recommendation': 'Use parameterized queries or prepared statements'
                    })

                    print(f"[+] SQLi found in {field_name} with payload: {payload[:50]}...")
                    break  # Found vulnerability, stop testing this field

                # Rate limiting
                await asyncio.sleep(0.2)

            except Exception as e:
                print(f"[!] Error testing {field_name}: {e}")
                continue

        return findings

    async def _send_request(self, session: aiohttp.ClientSession, url: str,
                            method: str, data: Dict[str, str]) -> aiohttp.ClientResponse:
        """Send HTTP request"""
        if method == 'POST':
            return await session.post(url, data=data, timeout=aiohttp.ClientTimeout(total=30))
        else:
            return await session.get(url, params=data, timeout=aiohttp.ClientTimeout(total=30))

    def _prepare_form_data(self, form: Dict[str, Any],
                           field_name: str, payload: str) -> Dict[str, str]:
        """Prepare form data with payload"""
        data = {}

        for field in form.get('fields', []):
            if field.get('name'):
                if field['name'] == field_name:
                    data[field['name']] = payload
                elif field['type'] == 'hidden' and field.get('value'):
                    data[field['name']] = field['value']

        return data

    def _is_vulnerable(self, response: aiohttp.ClientResponse,
                       payload: str) -> bool:
        """
        Check if response indicates SQL injection vulnerability

        Args:
            response: HTTP response
            payload: Test payload used

        Returns:
            True if vulnerable
        """
        try:
            content = response.text
            # For async response, need to await
            if hasattr(content, '__await__'):
                content = asyncio.get_event_loop().run_until_complete(content)
        except:
            return False

        # Check for SQL error messages
        error_patterns = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"MySQLSyntaxErrorException",
            r"valid MySQL result",
            r"check the manual that corresponds to your MySQL",
            r"PostgreSQL.*ERROR",
            r"Warning.*pg_.*",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            r"Driver.*SQL.*Server",
            r"OLE DB.*SQL Server",
            r"SQLServer JDBC Driver",
            r"SqlException",
            r"Oracle error",
            r"Oracle.*Driver",
            r"Warning.*oci_.*",
            r"Warning.*ora_.*",
            r"SQLite/JDBCDriver",
            r"SQLite.Exception",
            r"System.Data.SQLite.SQLiteException",
            r"sqlite3.OperationalError",
            r"sqlite3.DatabaseError",
        ]

        for pattern in error_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        # Check for specific payload reflection
        if "'" in payload and "error" in content.lower():
            return True

        # Check for database syntax errors
        db_errors = [
            "unclosed quotation mark",
            "quoted string not properly terminated",
            "syntax error",
            "unexpected end of command",
            "mysql_fetch",
            "ORA-",
            "PL/SQL"
        ]

        for error in db_errors:
            if error.lower() in content.lower():
                return True

        return False

    def _get_evidence(self, response: aiohttp.ClientResponse) -> str:
        """Get evidence from response"""
        try:
            content = response.text
            if hasattr(content, '__await__'):
                content = asyncio.get_event_loop().run_until_complete(content)

            # Return first 500 characters
            return content[:500] + '...' if len(content) > 500 else content
        except:
            return 'Unable to retrieve response'

    async def scan_url(self, url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """
        Scan a URL for SQL injection vulnerabilities

        Args:
            url: URL to test
            session: aiohttp session

        Returns:
            List of findings
        """
        findings = []

        # Parse URL to get query parameters
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)

        if not parsed.query:
            return findings

        params = parse_qs(parsed.query)

        for param_name in params.keys():
            print(f"[*] Testing URL parameter: {param_name}")

            for payload in self.payloads.get('basic', [])[:5]:
                try:
                    # Construct test URL
                    test_url = self._construct_test_url(url, param_name, payload)

                    # Send request
                    response = await session.get(test_url, timeout=aiohttp.ClientTimeout(total=30))

                    # Check for vulnerability
                    if self._is_vulnerable(response, payload):
                        findings.append({
                            'vulnerability': 'SQL Injection',
                            'severity': 'High',
                            'url': test_url,
                            'parameter': param_name,
                            'payload': payload,
                            'method': 'GET',
                            'evidence': self._get_evidence(response),
                            'description': f'Potential SQL injection in URL parameter "{param_name}"',
                            'recommendation': 'Use parameterized queries or prepared statements'
                        })

                        print(f"[+] SQLi found in {param_name}")
                        break

                    await asyncio.sleep(0.2)

                except Exception as e:
                    print(f"[!] Error testing {param_name}: {e}")
                    continue

        return findings

    def _construct_test_url(self, url: str, param_name: str, payload: str) -> str:
        """Construct test URL with payload"""
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        # Replace parameter value with payload
        params[param_name] = [payload]

        # Reconstruct URL
        new_query = urlencode(params, doseq=True)
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))

        return new_url


class SQLiAnalyzer:
    """Analyzes potential SQL injection vulnerabilities"""

    @staticmethod
    def analyze_finding(finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a SQL injection finding

        Args:
            finding: Vulnerability finding

        Returns:
            Enhanced analysis
        """
        analysis = {
            'finding': finding,
            'risk_level': 'High',
            'impact': [
                'Unauthorized data access',
                'Data modification or deletion',
                'Authentication bypass',
                'Complete database compromise'
            ],
            'remediation': {
                'immediate': 'Use parameterized queries or prepared statements',
                'long_term': 'Implement input validation and ORM frameworks',
                'testing': 'Regular security testing and code review'
            },
            'references': [
                'OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection',
                'CWE-89: SQL Injection',
                'OWASP Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'
            ]
        }

        # Adjust based on payload type
        payload = finding.get('payload', '')

        if 'SLEEP' in payload.upper() or 'WAITFOR' in payload.upper():
            analysis['technique'] = 'Time-based Blind SQL Injection'
        elif 'UNION' in payload.upper():
            analysis['technique'] = 'Union-based SQL Injection'
        elif 'OR' in payload.upper() or 'AND' in payload.upper():
            analysis['technique'] = 'Boolean-based Blind SQL Injection'
        else:
            analysis['technique'] = 'Error-based SQL Injection'

        return analysis
