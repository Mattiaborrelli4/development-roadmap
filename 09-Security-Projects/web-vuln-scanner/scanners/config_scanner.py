"""
Web Vulnerability Scanner - Configuration Scanner
Tests for security misconfigurations
"""

import asyncio
import aiohttp
from typing import List, Dict, Any
import yaml


class ConfigScanner:
    """Scanner for security misconfigurations"""

    def __init__(self, payloads_file: str = 'config/payloads.yaml'):
        """
        Initialize configuration scanner

        Args:
            payloads_file: Path to payloads configuration file
        """
        self.payloads = self._load_payloads(payloads_file)
        self.results = []

    def _load_payloads(self, file_path: str) -> Dict[str, Any]:
        """Load misconfiguration tests from YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('security_misconfig', {})
        except Exception as e:
            print(f"[!] Error loading payloads: {e}")
            return {}

    async def scan(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """
        Scan for security misconfigurations

        Args:
            base_url: Base URL of target
            session: aiohttp session

        Returns:
            List of findings
        """
        findings = []

        print("[*] Scanning for security misconfigurations...")

        # Check for exposed sensitive files
        exposed_files = await self._check_exposed_files(base_url, session)
        findings.extend(exposed_files)

        # Check security headers
        header_issues = await self._check_security_headers(base_url, session)
        findings.extend(header_issues)

        # Check for default pages
        default_pages = await self._check_default_pages(base_url, session)
        findings.extend(default_pages)

        # Check for information disclosure
        info_disclosure = await self._check_information_disclosure(base_url, session)
        findings.extend(info_disclosure)

        # Check for directory listing
        dir_listing = await self._check_directory_listing(base_url, session)
        findings.extend(dir_listing)

        return findings

    async def _check_exposed_files(self, base_url: str,
                                   session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for exposed sensitive files"""
        findings = []

        sensitive_files = self.payloads.get('exposed_files', [])

        for file_path in sensitive_files:
            try:
                url = base_url.rstrip('/') + file_path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=10))

                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')

                    findings.append({
                        'vulnerability': 'Exposed Sensitive File',
                        'severity': 'Medium',
                        'url': url,
                        'file': file_path,
                        'description': f'Sensitive file {file_path} is publicly accessible',
                        'recommendation': f'Remove or restrict access to {file_path}'
                    })
                    print(f"[+] Exposed file: {url}")

            except asyncio.TimeoutError:
                pass
            except Exception:
                pass

        return findings

    async def _check_security_headers(self, base_url: str,
                                      session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for missing security headers"""
        findings = []

        required_headers = {
            'X-Frame-Options': {
                'severity': 'Medium',
                'recommendation': 'Add X-Frame-Options: DENY or SAMEORIGIN'
            },
            'X-Content-Type-Options': {
                'severity': 'Low',
                'recommendation': 'Add X-Content-Type-Options: nosniff'
            },
            'Strict-Transport-Security': {
                'severity': 'Medium',
                'recommendation': 'Add Strict-Transport-Security: max-age=31536000; includeSubDomains'
            },
            'Content-Security-Policy': {
                'severity': 'Medium',
                'recommendation': 'Implement Content-Security-Policy header'
            },
            'X-XSS-Protection': {
                'severity': 'Low',
                'recommendation': 'Add X-XSS-Protection: 1; mode=block'
            },
            'Referrer-Policy': {
                'severity': 'Low',
                'recommendation': 'Add Referrer-Policy: strict-origin-when-cross-origin'
            },
            'Permissions-Policy': {
                'severity': 'Low',
                'recommendation': 'Implement Permissions-Policy header'
            }
        }

        try:
            response = await session.get(base_url, timeout=aiohttp.ClientTimeout(total=30))
            headers = response.headers

            for header_name, config in required_headers.items():
                if header_name not in headers:
                    findings.append({
                        'vulnerability': f'Missing {header_name} Header',
                        'severity': config['severity'],
                        'url': base_url,
                        'description': f'Security header {header_name} is missing',
                        'recommendation': config['recommendation']
                    })

            # Check for information leakage in Server header
            server = headers.get('Server', '')
            if server and server not in ['nginx', 'Apache', 'cloudflare']:
                findings.append({
                    'vulnerability': 'Information Leakage',
                    'severity': 'Low',
                    'url': base_url,
                    'description': f'Server header reveals version: {server}',
                    'recommendation': 'Configure server to hide version information'
                })

            # Check for X-Powered-By header
            x_powered_by = headers.get('X-Powered-By', '')
            if x_powered_by:
                findings.append({
                    'vulnerability': 'Information Leakage',
                    'severity': 'Low',
                    'url': base_url,
                    'description': f'X-Powered-By header reveals technology: {x_powered_by}',
                    'recommendation': 'Remove X-Powered-By header'
                })

        except Exception as e:
            print(f"[!] Error checking headers: {e}")

        return findings

    async def _check_default_pages(self, base_url: str,
                                   session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for exposed administrative/ sensitive pages"""
        findings = []

        default_pages = self.payloads.get('default_pages', [])

        for page_path in default_pages:
            try:
                url = base_url.rstrip('/') + page_path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=10))

                if response.status == 200:
                    content = await response.text()

                    # Check if it's actually the admin page (not 404)
                    if 'not found' not in content.lower() and 'error' not in content.lower():
                        findings.append({
                            'vulnerability': 'Exposed Admin Page',
                            'severity': 'High',
                            'url': url,
                            'description': f'Admin or sensitive page {page_path} is accessible',
                            'recommendation': 'Restrict access to admin pages or rename them'
                        })
                        print(f"[+] Exposed page: {url}")

            except asyncio.TimeoutError:
                pass
            except Exception:
                pass

        return findings

    async def _check_information_disclosure(self, base_url: str,
                                            session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for information disclosure vulnerabilities"""
        findings = []

        # Test verbose error messages
        test_paths = [
            '/nonexistent-page-12345',
            '/?debug=true',
            '/?debug=1',
            '/?verbose=true',
            '/test'
        ]

        for path in test_paths:
            try:
                url = base_url.rstrip('/') + path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=10))

                if response.status == 500:
                    content = await response.text()

                    # Check for verbose error messages
                    error_indicators = [
                        'stack trace', 'exception', 'error in', 'line ',
                        'fatal error', 'warning:', 'notice:', 'deprecated',
                        'mysql', 'postgresql', 'oracle', 'mongodb',
                        '/var/www/', 'c:\\', 'index.php', '.php'
                    ]

                    found = [ind for ind in error_indicators if ind.lower() in content.lower()]

                    if found:
                        findings.append({
                            'vulnerability': 'Verbose Error Messages',
                            'severity': 'Medium',
                            'url': url,
                            'description': f'Error page exposes technical details: {", ".join(found[:3])}',
                            'recommendation': 'Disable verbose error messages in production'
                        })
                        print(f"[+] Verbose error at: {url}")

            except Exception:
                pass

        # Check for .git directory
        git_paths = ['/.git/config', '/.git/head', '/.git/index']

        for path in git_paths:
            try:
                url = base_url.rstrip('/') + path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=10))

                if response.status == 200:
                    findings.append({
                        'vulnerability': 'Exposed .git Directory',
                        'severity': 'Critical',
                        'url': url,
                        'description': 'Git repository is publicly accessible',
                        'recommendation': 'Remove .git directory from web root'
                    })
                    print(f"[+] .git exposed: {url}")
                    break

            except Exception:
                pass

        return findings

    async def _check_directory_listing(self, base_url: str,
                                       session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for directory listing enabled"""
        findings = []

        test_dirs = ['/assets', '/images', '/css', '/js', '/uploads']

        for dir_path in test_dirs:
            try:
                url = base_url.rstrip('/') + dir_path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=10))

                if response.status == 200:
                    content = await response.text()

                    # Check for directory listing indicators
                    listing_indicators = [
                        'index of /', 'parent directory', 'name',
                        'last modified', 'size', '<table>',
                        'directory listing for'
                    ]

                    if any(indicator in content.lower() for indicator in listing_indicators):
                        # Verify it's not a regular page
                        if '<title>' not in content.lower() or 'index of' in content.lower():
                            findings.append({
                                'vulnerability': 'Directory Listing Enabled',
                                'severity': 'Medium',
                                'url': url,
                                'description': f'Directory listing is enabled for {dir_path}',
                                'recommendation': 'Disable directory listing in web server configuration'
                            })
                            print(f"[+] Directory listing: {url}")
                            break

            except Exception:
                pass

        return findings

    async def check_ssl_tls(self, base_url: str,
                            session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check SSL/TLS configuration"""
        findings = []

        if not base_url.startswith('https://'):
            findings.append({
                'vulnerability': 'No HTTPS',
                'severity': 'High',
                'url': base_url,
                'description': 'Site does not use HTTPS',
                'recommendation': 'Implement HTTPS with valid SSL/TLS certificate'
            })
            return findings

        try:
            # Check if we can connect
            response = await session.get(base_url, timeout=aiohttp.ClientTimeout(total=30))
            cert = response.connection.transport.get_extra_info('ssl_object')

            if cert:
                # Check certificate
                findings.append({
                    'vulnerability': 'SSL/TLS Info',
                    'severity': 'Info',
                    'url': base_url,
                    'description': 'HTTPS is enabled',
                    'cert_info': 'Certificate present'
                })

        except Exception as e:
            findings.append({
                'vulnerability': 'SSL/TLS Error',
                'severity': 'High',
                'url': base_url,
                'description': f'SSL/TLS configuration issue: {str(e)}',
                'recommendation': 'Check SSL/TLS configuration'
            })

        return findings


class ScannerConfig:
    """Configuration for the scanner"""

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default scanner configuration"""
        return {
            'max_pages': 100,
            'max_depth': 3,
            'delay': 0.2,
            'timeout': 30,
            'max_retries': 3,
            'user_agent': 'WebVulnScanner/1.0 (Educational Security Tool)',
            'respect_robots_txt': True,
            'safe_mode': True,
            'checks': {
                'sqli': True,
                'xss': True,
                'auth': True,
                'config': True,
                'headers': True
            }
        }

    @staticmethod
    def load_from_file(config_file: str) -> Dict[str, Any]:
        """Load configuration from file"""
        import json

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            return ScannerConfig.get_default_config()

    @staticmethod
    def save_to_file(config: Dict[str, Any], config_file: str):
        """Save configuration to file"""
        import json

        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"[!] Error saving config: {e}")
