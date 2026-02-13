"""
Web Vulnerability Scanner - Link Parser
Parses and analyzes links for vulnerabilities
"""

import re
from typing import List, Set, Dict, Any
from urllib.parse import urlparse, urljoin, parse_qs
from bs4 import BeautifulSoup


class LinkParser:
    """Parses and analyzes links for security testing"""

    def __init__(self, base_url: str):
        """
        Initialize link parser

        Args:
            base_url: Base URL of the target
        """
        self.base_url = base_url.rstrip('/')
        self.parsed_base = urlparse(self.base_url)
        self.allowed_domain = self.parsed_base.netloc

    def parse_links(self, html: str, page_url: str) -> Dict[str, Any]:
        """
        Parse all links from HTML content

        Args:
            html: HTML content
            page_url: URL of the current page

        Returns:
            Dictionary with categorized links
        """
        soup = BeautifulSoup(html, 'lxml')

        links = {
            'internal': [],
            'external': [],
            'with_parameters': [],
            'suspicious': [],
            'all': []
        }

        # Parse <a> tags
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            parsed_url = self._parse_link(href, page_url)

            if parsed_url:
                links['all'].append(parsed_url)
                self._categorize_link(parsed_url, links)

        # Parse <link> tags (CSS, etc.)
        for link in soup.find_all('link', href=True):
            href = link['href'].strip()
            parsed_url = self._parse_link(href, page_url)

            if parsed_url:
                links['all'].append(parsed_url)

        # Parse <script> tags (JS files)
        for script in soup.find_all('script', src=True):
            src = script['src'].strip()
            parsed_url = self._parse_link(src, page_url)

            if parsed_url:
                links['all'].append(parsed_url)

        # Parse <img> tags
        for img in soup.find_all('img', src=True):
            src = img['src'].strip()
            parsed_url = self._parse_link(src, page_url)

            if parsed_url:
                links['all'].append(parsed_url)

        # Parse <iframe> tags
        for iframe in soup.find_all('iframe', src=True):
            src = iframe['src'].strip()
            parsed_url = self._parse_link(src, page_url)

            if parsed_url:
                links['suspicious'].append({
                    **parsed_url,
                    'reason': 'iframe tag detected'
                })

        return links

    def _parse_link(self, href: str, page_url: str) -> Dict[str, Any] or None:
        """
        Parse a single link

        Args:
            href: Link href attribute
            page_url: Current page URL

        Returns:
            Parsed link dictionary or None if invalid
        """
        # Skip empty or invalid links
        if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:', 'data:')):
            return None

        # Convert to absolute URL
        absolute_url = urljoin(page_url, href)

        # Parse URL
        parsed = urlparse(absolute_url)

        return {
            'url': absolute_url,
            'scheme': parsed.scheme,
            'domain': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'has_query': bool(parsed.query)
        }

    def _categorize_link(self, link: Dict[str, Any], links: Dict[str, List]):
        """
        Categorize a link

        Args:
            link: Parsed link
            links: Links dictionary to update
        """
        # Check if internal or external
        if link['domain'] == self.allowed_domain:
            links['internal'].append(link)
        else:
            links['external'].append(link)

        # Check for query parameters
        if link['has_query']:
            params = parse_qs(link['query'])
            link['parameters'] = list(params.keys())
            links['with_parameters'].append(link)

            # Check for suspicious parameters
            suspicious_params = self._check_suspicious_params(link['parameters'])
            if suspicious_params:
                links['suspicious'].append({
                    **link,
                    'reason': f'Suspicious parameters: {", ".join(suspicious_params)}'
                })

    def _check_suspicious_params(self, params: List[str]) -> List[str]:
        """
        Check for suspicious parameter names

        Args:
            params: List of parameter names

        Returns:
            List of suspicious parameter names
        """
        suspicious_indicators = [
            'password', 'passwd', 'pwd', 'secret', 'token', 'key',
            'auth', 'session', 'id', 'user', 'admin', 'debug',
            'test', 'file', 'page', 'redirect', 'url', 'next',
            'return', 'goto', 'file', 'path', 'folder', 'dir'
        ]

        found = []
        for param in params:
            param_lower = param.lower()
            if any(indicator in param_lower for indicator in suspicious_indicators):
                found.append(param)

        return found

    def extract_url_parameters(self, url: str) -> Dict[str, List[str]]:
        """
        Extract parameters from URL

        Args:
            url: URL to parse

        Returns:
            Dictionary of parameters
        """
        parsed = urlparse(url)
        return parse_qs(parsed.query)

    def find_injection_points(self, url: str) -> List[Dict[str, Any]]:
        """
        Find potential injection points in URL

        Args:
            url: URL to analyze

        Returns:
            List of injection points
        """
        injection_points = []
        params = self.extract_url_parameters(url)

        for param_name, param_values in params.items():
            injection_points.append({
                'location': 'query_parameter',
                'parameter': param_name,
                'values': param_values,
                'url': url
            })

        # Check for fragment injection
        parsed = urlparse(url)
        if parsed.fragment:
            injection_points.append({
                'location': 'fragment',
                'value': parsed.fragment,
                'url': url
            })

        # Check for path injection
        path_segments = parsed.path.split('/')
        for i, segment in enumerate(path_segments):
            if segment and '{' in segment or '%' in segment:
                injection_points.append({
                    'location': 'path_segment',
                    'segment_index': i,
                    'value': segment,
                    'url': url
                })

        return injection_points

    def analyze_links_for_vulnerabilities(self, links: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze links for potential vulnerabilities

        Args:
            links: Parsed links dictionary

        Returns:
            List of vulnerability findings
        """
        findings = []

        # Check for sensitive information in URLs
        for link in links['with_parameters']:
            params = link.get('parameters', [])

            # Check for password/token in URL
            sensitive_params = [p for p in params if any(
                indicator in p.lower() for indicator in ['password', 'token', 'secret', 'key']
            )]

            if sensitive_params:
                findings.append({
                    'severity': 'High',
                    'issue': 'Sensitive Data in URL',
                    'url': link['url'],
                    'description': f'URL contains sensitive parameters: {", ".join(sensitive_params)}',
                    'recommendation': 'Avoid passing sensitive data in URL parameters'
                })

            # Check for open redirect
            if any(p.lower() in ['redirect', 'url', 'next', 'return', 'goto', 'link']
                   for p in params):
                findings.append({
                    'severity': 'Medium',
                    'issue': 'Potential Open Redirect',
                    'url': link['url'],
                    'description': 'URL contains redirect parameter that may be vulnerable',
                    'recommendation': 'Validate and whitelist redirect URLs'
                })

        # Check for external links that could be XSS
        for link in links['external']:
            if link['domain'] not in [self.allowed_domain]:
                findings.append({
                    'severity': 'Low',
                    'issue': 'External Link',
                    'url': link['url'],
                    'description': f'External link to {link["domain"]}',
                    'recommendation': 'Ensure external links are properly validated'
                })

        return findings


class ParameterAnalyzer:
    """Analyzes URL parameters for vulnerabilities"""

    @staticmethod
    def analyze_parameter(param_name: str, param_value: str) -> Dict[str, Any]:
        """
        Analyze a URL parameter

        Args:
            param_name: Parameter name
            param_value: Parameter value

        Returns:
            Analysis results
        """
        analysis = {
            'name': param_name,
            'value': param_value,
            'risks': []
        }

        # Check for SQL injection indicators
        if any(pattern in param_value for pattern in ["'", '"', ';', 'OR', 'AND', 'UNION']):
            analysis['risks'].append({
                'type': 'SQL Injection',
                'severity': 'High'
            })

        # Check for XSS indicators
        if any(pattern in param_value for pattern in ['<script', 'javascript:', 'onerror=']):
            analysis['risks'].append({
                'type': 'XSS',
                'severity': 'High'
            })

        # Check for path traversal
        if '../' in param_value or '..\\' in param_value:
            analysis['risks'].append({
                'type': 'Path Traversal',
                'severity': 'High'
            })

        # Check for command injection
        if any(pattern in param_value for pattern in [';', '|', '&&', '`', '$(']):
            analysis['risks'].append({
                'type': 'Command Injection',
                'severity': 'High'
            })

        return analysis
