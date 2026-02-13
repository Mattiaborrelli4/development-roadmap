"""
Web Vulnerability Scanner - XSS Scanner
Tests for Cross-Site Scripting vulnerabilities
"""

import asyncio
import aiohttp
import re
from typing import List, Dict, Any
import yaml


class XSSScanner:
    """Scanner for Cross-Site Scripting vulnerabilities"""

    def __init__(self, payloads_file: str = 'config/payloads.yaml'):
        """
        Initialize XSS scanner

        Args:
            payloads_file: Path to payloads configuration file
        """
        self.payloads = self._load_payloads(payloads_file)
        self.results = []

    def _load_payloads(self, file_path: str) -> Dict[str, List[str]]:
        """Load XSS payloads from YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('xss', {})
        except Exception as e:
            print(f"[!] Error loading payloads: {e}")
            return {'reflected': [], 'stored': [], 'dom_based': [], 'polyglot': []}

    async def scan_form(self, form: Dict[str, Any], session: aiohttp.ClientSession,
                       page_url: str) -> List[Dict[str, Any]]:
        """
        Scan a form for XSS vulnerabilities

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

        print(f"[*] Testing form for XSS: {action_url}")

        for field in form.get('fields', []):
            if field.get('type') in ['text', 'search', 'textarea', 'url', 'email']:
                field_findings = await self._test_field(
                    session, action_url, method, form, field['name'], page_url
                )
                findings.extend(field_findings)

        return findings

    async def _test_field(self, session: aiohttp.ClientSession, url: str,
                          method: str, form: Dict[str, Any],
                          field_name: str, page_url: str) -> List[Dict[str, Any]]:
        """
        Test a form field with XSS payloads

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

        # Test with basic reflected XSS payloads
        payloads_to_test = self.payloads.get('reflected', [])[:8]

        for payload in payloads_to_test:
            try:
                # Prepare form data
                data = self._prepare_form_data(form, field_name, payload)

                # Send request
                response = await self._send_request(session, url, method, data)

                # Get response content
                content = await self._get_response_content(response)

                # Analyze response
                if self._is_vulnerable(content, payload):
                    xss_type = self._classify_xss(payload, content)
                    findings.append({
                        'vulnerability': 'Cross-Site Scripting (XSS)',
                        'severity': 'High',
                        'url': url,
                        'parameter': field_name,
                        'payload': payload,
                        'method': method,
                        'xss_type': xss_type,
                        'evidence': self._get_evidence(content, payload),
                        'description': f'{xss_type} XSS in parameter "{field_name}"',
                        'recommendation': 'Encode output and implement Content-Security-Policy'
                    })

                    print(f"[+] XSS found in {field_name} (Type: {xss_type})")
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

    async def _get_response_content(self, response: aiohttp.ClientResponse) -> str:
        """Get response content as string"""
        try:
            return await response.text()
        except:
            return ''

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

    def _is_vulnerable(self, content: str, payload: str) -> bool:
        """
        Check if response indicates XSS vulnerability

        Args:
            content: Response content
            payload: Test payload used

        Returns:
            True if vulnerable
        """
        if not content:
            return False

        # Direct reflection (most basic check)
        if payload in content:
            return True

        # Check if payload is reflected without proper encoding
        # Remove variations and check
        sanitized_payload = payload.replace(' ', '').replace('\"', "'").replace('<', '&lt;')

        # Check for script tags in response
        if '<script>' in content.lower():
            # Check if it contains our payload marker
            if 'XSS' in content or 'alert' in content.lower():
                return True

        # Check for event handlers
        event_handlers = ['onerror=', 'onload=', 'onmouseover=', 'onfocus=',
                         'onclick=', 'onmouseenter=']

        for handler in event_handlers:
            if handler in content.lower() and ('alert' in content.lower() or 'XSS' in content):
                return True

        # Check for javascript: protocol
        if 'javascript:' in content.lower():
            return True

        # Check for specific XSS patterns
        xss_patterns = [
            r'<script[^>]*>.*?alert\s*\(.*?\)',
            r'<img[^>]*onerror\s*=\s*["\'].*?alert',
            r'<svg[^>]*onload\s*=\s*["\'].*?alert',
            r'<iframe[^>]*src\s*=\s*["\']javascript:',
        ]

        for pattern in xss_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return True

        return False

    def _classify_xss(self, payload: str, content: str) -> str:
        """
        Classify the type of XSS

        Args:
            payload: Payload used
            content: Response content

        Returns:
            XSS type string
        """
        if payload in content:
            # Check if payload is reflected in HTML
            if '<script>' in payload or 'onerror=' in payload or 'onload=' in payload:
                if 'value=' in content or 'name=' in content:
                    return 'Reflected (Attribute-based)'
                return 'Reflected (Tag-based)'
            elif 'javascript:' in payload:
                return 'Reflected (Protocol-based)'
            return 'Reflected (Basic)'
        else:
            # Payload was modified/encoded - might still be executable
            if 'script' in content.lower() or 'alert' in content.lower():
                return 'Reflected (Encoded)'
            return 'Potential DOM-based'

    def _get_evidence(self, content: str, payload: str) -> str:
        """Get evidence from response"""
        # Find and return the section containing the payload
        if payload in content:
            idx = content.find(payload)
            start = max(0, idx - 50)
            end = min(len(content), idx + len(payload) + 50)
            return '...' + content[start:end] + '...'

        # Return first 500 chars if no direct match
        return content[:500] + '...' if len(content) > 500 else content

    async def scan_url(self, url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """
        Scan a URL for XSS vulnerabilities

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

            for payload in self.payloads.get('reflected', [])[:5]:
                try:
                    # Construct test URL
                    test_url = self._construct_test_url(url, param_name, payload)

                    # Send request
                    response = await session.get(test_url, timeout=aiohttp.ClientTimeout(total=30))

                    # Get response content
                    content = await response.text()

                    # Check for vulnerability
                    if self._is_vulnerable(content, payload):
                        xss_type = self._classify_xss(payload, content)
                        findings.append({
                            'vulnerability': 'Cross-Site Scripting (XSS)',
                            'severity': 'High',
                            'url': test_url,
                            'parameter': param_name,
                            'payload': payload,
                            'method': 'GET',
                            'xss_type': xss_type,
                            'evidence': self._get_evidence(content, payload),
                            'description': f'{xss_type} XSS in URL parameter "{param_name}"',
                            'recommendation': 'Encode output and implement Content-Security-Policy'
                        })

                        print(f"[+] XSS found in {param_name} (Type: {xss_type})")
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

    async def check_headers(self, session: aiohttp.ClientSession,
                            url: str) -> List[Dict[str, Any]]:
        """
        Check for security headers related to XSS prevention

        Args:
            session: aiohttp session
            url: URL to check

        Returns:
            List of findings
        """
        findings = []

        try:
            response = await session.get(url, timeout=aiohttp.ClientTimeout(total=30))
            headers = response.headers

            # Check Content-Security-Policy
            csp = headers.get('Content-Security-Policy', '')
            if not csp:
                findings.append({
                    'vulnerability': 'Missing Content-Security-Policy',
                    'severity': 'Medium',
                    'url': url,
                    'description': 'Missing Content-Security-Policy header',
                    'recommendation': 'Implement Content-Security-Policy to prevent XSS'
                })

            # Check X-XSS-Protection
            xss_protection = headers.get('X-XSS-Protection', '')
            if not xss_protection:
                findings.append({
                    'vulnerability': 'Missing X-XSS-Protection',
                    'severity': 'Low',
                    'url': url,
                    'description': 'Missing X-XSS-Protection header',
                    'recommendation': 'Add X-XSS-Protection: 1; mode=block'
                })

            # Check X-Content-Type-Options
            content_type_options = headers.get('X-Content-Type-Options', '')
            if content_type_options != 'nosniff':
                findings.append({
                    'vulnerability': 'Missing X-Content-Type-Options',
                    'severity': 'Low',
                    'url': url,
                    'description': 'Missing or incorrect X-Content-Type-Options header',
                    'recommendation': 'Add X-Content-Type-Options: nosniff'
                })

        except Exception as e:
            print(f"[!] Error checking headers: {e}")

        return findings


class XSSAnalyzer:
    """Analyzes XSS vulnerabilities"""

    @staticmethod
    def analyze_finding(finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an XSS finding

        Args:
            finding: Vulnerability finding

        Returns:
            Enhanced analysis
        """
        xss_type = finding.get('xss_type', 'Unknown')

        analysis = {
            'finding': finding,
            'risk_level': 'High',
            'impact': [
                'Session hijacking',
                'Cookie theft',
                'Defacement of website',
                'Malware distribution',
                'Credential theft',
                'Phishing attacks'
            ],
            'remediation': {
                'immediate': 'Encode all user-supplied data before outputting to HTML',
                'long_term': [
                    'Implement Content-Security-Policy (CSP)',
                    'Use frameworks with auto-escaping (Django, React, etc.)',
                    'Validate input on server-side',
                    'Use HTTPOnly and Secure flags on cookies'
                ],
                'testing': 'Regular security testing and code review'
            },
            'references': [
                'OWASP XSS: https://owasp.org/www-community/attacks/xss/',
                'CWE-79: Cross-site Scripting',
                'OWASP XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'
            ]
        }

        # Type-specific information
        if 'Reflected' in xss_type:
            analysis['description'] = 'Reflected XSS occurs when application reflects user input without proper encoding'
            analysis['poc_example'] = finding.get('url', '')
        elif 'Stored' in xss_type:
            analysis['description'] = 'Stored XSS occurs when application stores user input and displays it later without encoding'
        elif 'DOM' in xss_type:
            analysis['description'] = 'DOM-based XSS occurs when JavaScript processes data unsafely'
            analysis['additional_rem] = 'Avoid using innerHTML, use textContent instead'

        return analysis
