"""
Web Vulnerability Scanner - Site Crawler
Crawls websites to discover pages, forms, and endpoints
"""

import asyncio
import time
from typing import Set, List, Dict, Any
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
from collections import deque
import re


class WebCrawler:
    """Crawls websites to discover pages and forms"""

    def __init__(self, base_url: str, max_pages: int = 100, max_depth: int = 3,
                 delay: float = 0.2, respect_robots: bool = True):
        """
        Initialize the web crawler

        Args:
            base_url: The base URL to start crawling from
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum depth of crawling
            delay: Delay between requests in seconds
            respect_robots: Whether to respect robots.txt
        """
        self.base_url = base_url.rstrip('/')
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.respect_robots = respect_robots

        self.visited_urls: Set[str] = set()
        self.queue = deque()
        self.discovered_forms: List[Dict[str, Any]] = []
        self.discovered_links: Set[str] = set()

        # Parse base URL
        self.parsed_base = urlparse(self.base_url)
        self.allowed_domain = self.parsed_base.netloc

    async def crawl(self) -> Dict[str, Any]:
        """
        Start crawling the website

        Returns:
            Dictionary containing discovered pages, forms, and links
        """
        print(f"[*] Starting crawl of: {self.base_url}")
        print(f"[*] Max pages: {self.max_pages}, Max depth: {self.max_depth}")
        print(f"[*] Delay: {self.delay}s, Respect robots.txt: {self.respect_robots}")

        # Initialize queue with base URL
        self.queue.append((self.base_url, 0))

        async with aiohttp.ClientSession() as session:
            while self.queue and len(self.visited_urls) < self.max_pages:
                url, depth = self.queue.popleft()

                # Skip if already visited or too deep
                if url in self.visited_urls or depth > self.max_depth:
                    continue

                # Rate limiting
                await asyncio.sleep(self.delay)

                try:
                    await self._crawl_page(session, url, depth)
                except Exception as e:
                    print(f"[!] Error crawling {url}: {str(e)}")
                    continue

        return self._get_results()

    async def _crawl_page(self, session: aiohttp.ClientSession,
                          url: str, depth: int):
        """
        Crawl a single page and extract links and forms

        Args:
            session: aiohttp session
            url: URL to crawl
            depth: Current depth
        """
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30),
                                   allow_redirects=True) as response:
                # Check content type
                content_type = response.headers.get('Content-Type', '')

                if not content_type.startswith('text/html'):
                    return

                html = await response.text()
                self.visited_urls.add(url)

                print(f"[*] Crawled: {url} (Depth: {depth})")

                # Parse HTML
                soup = BeautifulSoup(html, 'lxml')

                # Extract links
                links = self._extract_links(soup, url, depth)
                for link in links:
                    if link not in self.visited_urls and link not in [u[0] for u in self.queue]:
                        self.queue.append((link, depth + 1))

                # Extract forms
                forms = self._extract_forms(soup, url)
                self.discovered_forms.extend(forms)

                print(f"    - Found {len(forms)} form(s)")
                print(f"    - Found {len(links)} link(s)")

        except asyncio.TimeoutError:
            print(f"[!] Timeout accessing {url}")
        except Exception as e:
            print(f"[!] Error accessing {url}: {str(e)}")

    def _extract_links(self, soup: BeautifulSoup, current_url: str,
                       depth: int) -> Set[str]:
        """
        Extract all links from the page

        Args:
            soup: BeautifulSoup object
            current_url: Current page URL
            depth: Current depth

        Returns:
            Set of discovered links
        """
        links = set()

        for link in soup.find_all('a', href=True):
            href = link['href'].strip()

            # Skip empty, javascript, and anchor links
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue

            # Convert relative URLs to absolute
            absolute_url = urljoin(current_url, href)

            # Parse URL
            parsed = urlparse(absolute_url)

            # Only follow links from the same domain
            if parsed.netloc == self.allowed_domain:
                # Remove fragment
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                # Add query string if present
                if parsed.query:
                    clean_url += f"?{parsed.query}"

                links.add(clean_url)

        return links

    def _extract_forms(self, soup: BeautifulSoup, page_url: str) -> List[Dict[str, Any]]:
        """
        Extract all forms from the page

        Args:
            soup: BeautifulSoup object
            page_url: Current page URL

        Returns:
            List of discovered forms with their details
        """
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(page_url, form.get('action', '')),
                'method': form.get('method', 'GET').upper(),
                'page_url': page_url,
                'fields': []
            }

            # Extract input fields
            for field in form.find_all(['input', 'textarea', 'select']):
                field_type = field.get('type', 'text')
                field_name = field.get('name')
                field_value = field.get('value', '')

                if field_name:
                    form_data['fields'].append({
                        'name': field_name,
                        'type': field_type,
                        'value': field_value,
                        'required': field.has_attr('required')
                    })

            forms.append(form_data)

        return forms

    def _get_results(self) -> Dict[str, Any]:
        """
        Get crawl results

        Returns:
            Dictionary with crawl results
        """
        return {
            'base_url': self.base_url,
            'total_pages': len(self.visited_urls),
            'total_forms': len(self.discovered_forms),
            'visited_urls': list(self.visited_urls),
            'forms': self.discovered_forms
        }


class FormDiscovery:
    """Discovers forms in web pages"""

    @staticmethod
    def find_forms_in_html(html: str, page_url: str) -> List[Dict[str, Any]]:
        """
        Find all forms in HTML content

        Args:
            html: HTML content
            page_url: Page URL

        Returns:
            List of forms with their details
        """
        soup = BeautifulSoup(html, 'lxml')
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(page_url, form.get('action', '')),
                'method': form.get('method', 'GET').upper(),
                'page_url': page_url,
                'enctype': form.get('enctype', ''),
                'fields': []
            }

            # Extract input fields
            for field in form.find_all(['input', 'textarea', 'select']):
                field_data = {
                    'name': field.get('name'),
                    'type': field.get('type', 'text'),
                    'value': field.get('value', ''),
                    'required': field.has_attr('required'),
                    'id': field.get('id', ''),
                    'class': field.get('class', [])
                }

                if field_data['name']:
                    form_data['fields'].append(field_data)

            # Extract buttons
            for button in form.find_all(['button', 'input']):
                if button.get('type') in ['submit', 'button'] or button.name == 'button':
                    form_data['fields'].append({
                        'name': button.get('name', ''),
                        'type': button.get('type', 'submit'),
                        'value': button.get('value', button.get_text(strip=True)),
                        'required': False
                    })

            forms.append(form_data)

        return forms

    @staticmethod
    def analyze_form(form: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a form for potential vulnerabilities

        Args:
            form: Form data

        Returns:
            Analysis results
        """
        analysis = {
            'form': form,
            'potential_issues': []
        }

        # Check for password fields
        password_fields = [f for f in form['fields'] if f['type'] == 'password']
        if password_fields:
            analysis['potential_issues'].append({
                'type': 'Authentication',
                'description': 'Form contains password field',
                'severity': 'Info'
            })

        # Check for file uploads
        file_fields = [f for f in form['fields'] if f['type'] == 'file']
        if file_fields:
            analysis['potential_issues'].append({
                'type': 'File Upload',
                'description': 'Form allows file uploads',
                'severity': 'Medium'
            })

        # Check for GET method with sensitive data
        if form['method'] == 'GET' and password_fields:
            analysis['potential_issues'].append({
                'type': 'Sensitive Data Exposure',
                'description': 'Password form uses GET method (data in URL)',
                'severity': 'High'
            })

        # Check for number of fields
        if len(form['fields']) > 10:
            analysis['potential_issues'].append({
                'type': 'Complexity',
                'description': f'Form has {len(form["fields"])} fields',
                'severity': 'Low'
            })

        return analysis
