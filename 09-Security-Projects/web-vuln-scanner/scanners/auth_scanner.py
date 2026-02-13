"""
Web Vulnerability Scanner - Authentication Scanner
Tests for authentication and authorization vulnerabilities
"""

import asyncio
import aiohttp
from typing import List, Dict, Any
import yaml


class AuthScanner:
    """Scanner for authentication and authorization vulnerabilities"""

    def __init__(self, payloads_file: str = 'config/payloads.yaml'):
        """
        Initialize authentication scanner

        Args:
            payloads_file: Path to payloads configuration file
        """
        self.payloads = self._load_payloads(payloads_file)
        self.results = []

    def _load_payloads(self, file_path: str) -> Dict[str, Any]:
        """Load authentication test credentials from YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('authentication', {})
        except Exception as e:
            print(f"[!] Error loading payloads: {e}")
            return {}

    async def scan(self, base_url: str, session: aiohttp.ClientSession,
                   crawl_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scan for authentication vulnerabilities

        Args:
            base_url: Base URL of target
            session: aiohttp session
            crawl_results: Results from crawler

        Returns:
            List of findings
        """
        findings = []

        print("[*] Scanning for authentication vulnerabilities...")

        # Check for default credentials
        default_creds = await self._check_default_credentials(
            base_url, session, crawl_results
        )
        findings.extend(default_creds)

        # Check for authentication bypass
        auth_bypass = await self._check_auth_bypass(base_url, session, crawl_results)
        findings.extend(auth_bypass)

        # Check for session management issues
        session_issues = await self._check_session_management(base_url, session)
        findings.extend(session_issues)

        # Check for password security
        password_issues = await self._check_password_security(base_url, session, crawl_results)
        findings.extend(password_issues)

        return findings

    async def _check_default_credentials(self, base_url: str,
                                         session: aiohttp.ClientSession,
                                         crawl_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for default/weak credentials"""
        findings = []

        # Find login forms
        login_forms = self._find_login_forms(crawl_results.get('forms', []))

        if not login_forms:
            print("[*] No login forms found")
            return findings

        print(f"[*] Found {len(login_forms)} login form(s)")

        # Test with weak credentials
        weak_creds = self.payloads.get('weak_credentials', [])

        for form in login_forms[:2]:  # Limit to 2 forms
            for cred in weak_creds[:5]:  # Limit to 5 credential pairs
                try:
                    # Prepare login data
                    login_data = self._prepare_login_data(form, cred)

                    # Attempt login
                    response = await session.post(
                        form['action'],
                        data=login_data,
                        timeout=aiohttp.ClientTimeout(total=30),
                        allow_redirects=False
                    )

                    # Check if login was successful
                    if await self._is_successful_login(response, session):
                        findings.append({
                            'vulnerability': 'Default or Weak Credentials',
                            'severity': 'Critical',
                            'url': form['action'],
                            'credentials': f"{cred['username']}:{cred['password']}",
                            'description': 'Login succeeded with weak credentials',
                            'recommendation': 'Enforce strong password policies and remove default credentials'
                        })
                        print(f"[+] Weak credentials found: {cred['username']}:{cred['password']}")
                        break

                    await asyncio.sleep(0.5)

                except Exception as e:
                    print(f"[!] Error testing credentials: {e}")
                    continue

        return findings

    def _find_login_forms(self, forms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify login forms"""
        login_forms = []

        for form in forms:
            # Check if form has password field
            has_password = any(
                f.get('type') == 'password' for f in form.get('fields', [])
            )

            # Check for login-related keywords
            action_lower = form.get('action', '').lower()
            page_lower = form.get('page_url', '').lower()

            login_keywords = ['login', 'signin', 'auth', 'logon', 'sign-in', 'sign_in']

            is_login_form = (
                has_password and
                any(keyword in action_lower or keyword in page_lower for keyword in login_keywords)
            )

            if is_login_form:
                login_forms.append(form)

        return login_forms

    def _prepare_login_data(self, form: Dict[str, Any],
                           credentials: Dict[str, str]) -> Dict[str, str]:
        """Prepare login data with credentials"""
        data = {}

        username_field = None
        password_field = None

        # Find username and password fields
        for field in form.get('fields', []):
            field_type = field.get('type', '')
            field_name = field.get('name', '')

            if field_type == 'password':
                password_field = field_name
            elif field_type in ['text', 'email'] and not username_field:
                username_field = field_name

            # Add hidden fields
            if field_type == 'hidden' and field_name:
                data[field_name] = field.get('value', '')

        # Add credentials
        if username_field:
            data[username_field] = credentials.get('username', '')
        if password_field:
            data[password_field] = credentials.get('password', '')

        return data

    async def _is_successful_login(self, response: aiohttp.ClientResponse,
                                   session: aiohttp.ClientSession) -> bool:
        """Check if login was successful"""
        # Check for redirect (usually successful login)
        if response.status in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')

            # Check if not redirecting back to login
            if 'login' not in location.lower():
                return True

        # Check response for indicators
        try:
            content = await response.text()

            # Check for error messages
            error_indicators = ['invalid', 'incorrect', 'failed', 'denied', 'error']

            if not any(indicator in content.lower() for indicator in error_indicators):
                # Check for success indicators
                success_indicators = ['welcome', 'dashboard', 'logout', 'profile']

                if any(indicator in content.lower() for indicator in success_indicators):
                    return True

        except:
            pass

        return False

    async def _check_auth_bypass(self, base_url: str,
                                 session: aiohttp.ClientSession,
                                 crawl_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for authentication bypass vulnerabilities"""
        findings = []

        # Test direct access to protected pages
        protected_paths = [
            '/admin', '/dashboard', '/profile', '/settings',
            '/account', '/user', '/console'
        ]

        for path in protected_paths:
            try:
                url = base_url.rstrip('/') + path
                response = await session.get(url, timeout=aiohttp.ClientTimeout(total=30))

                # If page accessible without auth
                if response.status == 200:
                    content = await response.text()

                    # Check if it's actually the protected page
                    if 'login' not in content.lower() and 'sign in' not in content.lower():
                        findings.append({
                            'vulnerability': 'Authentication Bypass',
                            'severity': 'High',
                            'url': url,
                            'description': f'Protected page {path} is accessible without authentication',
                            'recommendation': 'Implement proper authentication checks on all protected pages'
                        })
                        print(f"[+] Auth bypass found: {url}")

            except Exception as e:
                continue

        return findings

    async def _check_session_management(self, base_url: str,
                                       session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Check for session management issues"""
        findings = []

        try:
            # Make initial request to get session cookie
            response = await session.get(base_url, timeout=aiohttp.ClientTimeout(total=30))
            cookies = session.cookie_jar

            if not cookies:
                findings.append({
                    'vulnerability': 'Missing Session Cookie',
                    'severity': 'Info',
                    'url': base_url,
                    'description': 'No session cookie set',
                    'recommendation': 'Ensure session cookies are properly set'
                })
                return findings

            # Check cookie security
            for cookie in cookies:
                cookie_findings = []

                # Check Secure flag
                if not cookie.secure and 'https' in base_url:
                    cookie_findings.append({
                        'severity': 'Medium',
                        'issue': 'Missing Secure Flag',
                        'description': f'Cookie {cookie.name} lacks Secure flag',
                        'recommendation': 'Set Secure flag on cookies'
                    })

                # Check HttpOnly flag
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    cookie_findings.append({
                        'severity': 'Medium',
                        'issue': 'Missing HttpOnly Flag',
                        'description': f'Cookie {cookie.name} lacks HttpOnly flag',
                        'recommendation': 'Set HttpOnly flag on cookies'
                    })

                # Check SameSite attribute
                samesite = cookie.get_nonstandard_attr('SameSite', '')
                if samesite not in ['Strict', 'Lax']:
                    cookie_findings.append({
                        'severity': 'Low',
                        'issue': 'Missing SameSite Attribute',
                        'description': f'Cookie {cookie.name} lacks SameSite attribute',
                        'recommendation': 'Set SameSite attribute on cookies'
                    })

                for cf in cookie_findings:
                    findings.append({
                        'vulnerability': 'Insecure Session Cookie',
                        'url': base_url,
                        'cookie': cookie.name,
                        **cf
                    })

        except Exception as e:
            print(f"[!] Error checking session management: {e}")

        return findings

    async def _check_password_security(self, base_url: str,
                                       session: aiohttp.ClientSession,
                                       crawl_results: Dict[str, Any]) -> List[Dict[str, Any]:
        """Check for password security issues"""
        findings = []

        # Find password forms
        for form in crawl_results.get('forms', []):
            has_password = any(
                f.get('type') == 'password' for f in form.get('fields', [])
            )

            if has_password:
                # Check if form uses GET method
                if form.get('method') == 'GET':
                    findings.append({
                        'vulnerability': 'Password Over GET',
                        'severity': 'High',
                        'url': form.get('action'),
                        'description': 'Password form uses GET method (password in URL)',
                        'recommendation': 'Use POST method for password forms'
                    })

                # Check if form is over HTTP
                if form.get('action', '').startswith('http://'):
                    findings.append({
                        'vulnerability': 'Password Over HTTP',
                        'severity': 'High',
                        'url': form.get('action'),
                        'description': 'Password submitted over unencrypted connection',
                        'recommendation': 'Use HTTPS for all password forms'
                    })

                # Check for autocomplete
                password_field = next(
                    (f for f in form.get('fields', []) if f.get('type') == 'password'),
                    None
                )

                if password_field and password_field.get('autocomplete') != 'off':
                    findings.append({
                        'vulnerability': 'Password Autocomplete',
                        'severity': 'Low',
                        'url': form.get('action'),
                        'description': 'Password field may allow browser to save password',
                        'recommendation': 'Set autocomplete="off" on password fields'
                    })

        return findings


class BruteForceChecker:
    """Checks for brute force protection"""

    def __init__(self, max_attempts: int = 5):
        """
        Initialize brute force checker

        Args:
            max_attempts: Maximum number of login attempts to test
        """
        self.max_attempts = max_attempts

    async def check_protection(self, login_url: str, session: aiohttp.ClientSession,
                               login_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Check if login endpoint has brute force protection

        Args:
            login_url: Login endpoint URL
            session: aiohttp session
            login_data: Login data template

        Returns:
            Check results
        """
        results = {
            'has_protection': False,
            'protection_type': None,
            'threshold': None
        }

        for i in range(self.max_attempts):
            try:
                # Use different credentials each time
                test_data = login_data.copy()
                test_data['username'] = f'test_user_{i}'
                test_data['password'] = f'wrong_password_{i}'

                response = await session.post(
                    login_url,
                    data=test_data,
                    timeout=aiohttp.ClientTimeout(total=30),
                    allow_redirects=False
                )

                # Check for rate limiting
                if response.status == 429:
                    results['has_protection'] = True
                    results['protection_type'] = 'Rate Limiting'
                    results['threshold'] = i + 1
                    break

                # Check for account lockout message
                try:
                    content = await response.text()
                    if 'locked' in content.lower() or 'blocked' in content.lower():
                        results['has_protection'] = True
                        results['protection_type'] = 'Account Lockout'
                        results['threshold'] = i + 1
                        break
                except:
                    pass

                await asyncio.sleep(0.5)

            except Exception as e:
                break

        return results
