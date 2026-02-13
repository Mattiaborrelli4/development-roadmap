"""
Web Vulnerability Scanner - Tests
Unit tests for scanner components
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSQLiScanner:
    """Tests for SQL Injection scanner"""

    def setup_method(self):
        """Setup test fixtures"""
        from scanners.sql_injection import SQLiScanner
        self.scanner = SQLiScanner()

    def test_payload_loading(self):
        """Test that payloads are loaded correctly"""
        assert 'basic' in self.scanner.payloads
        assert isinstance(self.scanner.payloads['basic'], list)

    def test_prepare_form_data(self):
        """Test form data preparation"""
        form = {
            'fields': [
                {'name': 'username', 'type': 'text', 'value': ''},
                {'name': 'password', 'type': 'password', 'value': ''},
                {'name': 'csrf_token', 'type': 'hidden', 'value': 'abc123'}
            ]
        }

        data = self.scanner._prepare_form_data(form, 'username', "' OR '1'='1")

        assert data['username'] == "' OR '1'='1"
        assert data['csrf_token'] == 'abc123'
        assert 'password' in data

    def test_construct_test_url(self):
        """Test URL construction with payload"""
        url = "https://example.com/search?q=test&page=1"
        test_url = self.scanner._construct_test_url(url, 'q', "' OR '1'='1")

        assert "' OR '1'='1" in test_url
        assert "page=1" in test_url


class TestXSSScanner:
    """Tests for XSS scanner"""

    def setup_method(self):
        """Setup test fixtures"""
        from scanners.xss_scanner import XSSScanner
        self.scanner = XSSScanner()

    def test_payload_loading(self):
        """Test that payloads are loaded correctly"""
        assert 'reflected' in self.scanner.payloads
        assert isinstance(self.scanner.payloads['reflected'], list)

    def test_is_vulnerable_with_script_tag(self):
        """Test vulnerability detection with script tag"""
        payload = "<script>alert('XSS')</script>"
        content = f"<html><body>{payload}</body></html>"

        assert self.scanner._is_vulnerable(content, payload) == True

    def test_is_vulnerable_with_event_handler(self):
        """Test vulnerability detection with event handler"""
        payload = "<img src=x onerror=alert('XSS')>"
        content = f"<html><body>{payload}</body></html>"

        assert self.scanner._is_vulnerable(content, payload) == True

    def test_is_vulnerable_safe_content(self):
        """Test that safe content is not flagged"""
        payload = "<test>"
        content = "<html><body>Hello World</body></html>"

        assert self.scanner._is_vulnerable(content, payload) == False

    def test_classify_xss(self):
        """Test XSS classification"""
        payload = "<script>alert('XSS')</script>"
        content = f"<html>{payload}</html>"

        xss_type = self.scanner._classify_xss(payload, content)
        assert 'Reflected' in xss_type

    def test_prepare_form_data(self):
        """Test form data preparation"""
        form = {
            'fields': [
                {'name': 'comment', 'type': 'textarea', 'value': ''},
                {'name': 'submit', 'type': 'submit', 'value': 'Submit'}
            ]
        }

        data = self.scanner._prepare_form_data(form, 'comment', '<script>alert(1)</script>')

        assert data['comment'] == '<script>alert(1)</script>'


class TestCrawler:
    """Tests for web crawler"""

    def setup_method(self):
        """Setup test fixtures"""
        from scanners.crawler import WebCrawler
        self.crawler = WebCrawler(
            base_url='https://example.com',
            max_pages=10,
            max_depth=2,
            delay=0
        )

    def test_initialization(self):
        """Test crawler initialization"""
        assert self.crawler.base_url == 'https://example.com'
        assert self.crawler.max_pages == 10
        assert self.crawler.max_depth == 2
        assert len(self.crawler.visited_urls) == 0

    def test_extract_links(self):
        """Test link extraction"""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <body>
                <a href="/page1">Page 1</a>
                <a href="https://other.com/page2">External Link</a>
                <a href="#anchor">Anchor</a>
                <a href="javascript:void(0)">JS Link</a>
            </body>
        </html>
        """

        soup = BeautifulSoup(html, 'lxml')
        links = self.crawler._extract_links(soup, 'https://example.com/')

        # Should only get internal link
        assert len(links) == 1
        assert 'https://example.com/page1' in links

    def test_extract_forms(self):
        """Test form extraction"""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <body>
                <form action="/login" method="POST">
                    <input type="text" name="username">
                    <input type="password" name="password">
                    <input type="submit" value="Login">
                </form>
            </body>
        </html>
        """

        soup = BeautifulSoup(html, 'lxml')
        forms = self.crawler._extract_forms(soup, 'https://example.com/')

        assert len(forms) == 1
        assert forms[0]['action'] == 'https://example.com/login'
        assert forms[0]['method'] == 'POST'
        assert len(forms[0]['fields']) == 3


class TestFormParser:
    """Tests for form parser"""

    def setup_method(self):
        """Setup test fixtures"""
        from parsers.form_parser import FormParser
        self.parser = FormParser()

    def test_parse_form_with_csrf(self):
        """Test parsing form with CSRF token"""
        from bs4 import BeautifulSoup

        html = """
        <form action="/submit" method="POST">
            <input type="hidden" name="csrf_token" value="abc123">
            <input type="text" name="data">
            <input type="submit">
        </form>
        """

        soup = BeautifulSoup(html, 'lxml')
        form = self.parser._parse_form(
            soup.find('form'),
            'https://example.com/'
        )

        assert form['has_csrf_token'] == True
        assert form['csrf_token_name'] == 'csrf_token'
        assert len(form['fields']) == 3

    def test_get_testable_fields(self):
        """Test getting testable fields"""
        form = {
            'fields': [
                {'name': 'search', 'type': 'text', 'value': ''},
                {'name': 'submit', 'type': 'submit', 'value': 'Search'},
                {'name': 'csrf_token', 'type': 'hidden', 'value': 'xyz'}
            ]
        }

        testable = self.parser.get_testable_fields(form)

        assert len(testable) == 1
        assert testable[0]['name'] == 'search'

    def test_is_csrf_field(self):
        """Test CSRF field detection"""
        assert self.parser._is_csrf_field({'name': 'csrf_token'}) == True
        assert self.parser._is_csrf_field({'name': '_token'}) == True
        assert self.parser._is_csrf_field({'name': 'authenticity_token'}) == True
        assert self.parser._is_csrf_field({'name': 'username'}) == False


class TestLinkParser:
    """Tests for link parser"""

    def setup_method(self):
        """Setup test fixtures"""
        from parsers.link_parser import LinkParser
        self.parser = LinkParser('https://example.com')

    def test_parse_link_internal(self):
        """Test parsing internal link"""
        result = self.parser._parse_link('/page1', 'https://example.com/')

        assert result is not None
        assert result['domain'] == 'example.com'
        assert result['path'] == '/page1'

    def test_parse_link_external(self):
        """Test parsing external link"""
        result = self.parser._parse_link('https://other.com/page', 'https://example.com/')

        assert result is not None
        assert result['domain'] == 'other.com'

    def test_parse_link_javascript(self):
        """Test that javascript links are skipped"""
        result = self.parser._parse_link('javascript:void(0)', 'https://example.com/')

        assert result is None

    def test_extract_url_parameters(self):
        """Test URL parameter extraction"""
        url = 'https://example.com/search?q=test&page=1&sort=desc'
        params = self.parser.extract_url_parameters(url)

        assert params['q'] == ['test']
        assert params['page'] == ['1']
        assert params['sort'] == ['desc']


class TestConfigScanner:
    """Tests for configuration scanner"""

    def setup_method(self):
        """Setup test fixtures"""
        from scanners.config_scanner import ConfigScanner
        self.scanner = ConfigScanner()

    def test_payload_loading(self):
        """Test that payloads are loaded"""
        assert 'default_pages' in self.scanner.payloads
        assert 'exposed_files' in self.scanner.payloads


class TestAuthScanner:
    """Tests for authentication scanner"""

    def setup_method(self):
        """Setup test fixtures"""
        from scanners.auth_scanner import AuthScanner
        self.scanner = AuthScanner()

    def test_find_login_forms(self):
        """Test login form identification"""
        forms = [
            {
                'action': '/login',
                'page_url': 'https://example.com/login',
                'fields': [
                    {'name': 'username', 'type': 'text'},
                    {'name': 'password', 'type': 'password'}
                ]
            },
            {
                'action': '/search',
                'page_url': 'https://example.com/search',
                'fields': [
                    {'name': 'q', 'type': 'text'}
                ]
            }
        ]

        login_forms = self.scanner._find_login_forms(forms)

        assert len(login_forms) == 1
        assert login_forms[0]['action'] == '/login'

    def test_prepare_login_data(self):
        """Test login data preparation"""
        form = {
            'fields': [
                {'name': 'username', 'type': 'text', 'value': ''},
                {'name': 'password', 'type': 'password', 'value': ''},
                {'name': 'csrf_token', 'type': 'hidden', 'value': 'token123'}
            ]
        }

        credentials = {'username': 'admin', 'password': 'secret'}
        data = self.scanner._prepare_login_data(form, credentials)

        assert data['username'] == 'admin'
        assert data['password'] == 'secret'
        assert data['csrf_token'] == 'token123'


class TestReportGenerator:
    """Tests for report generator"""

    def setup_method(self):
        """Setup test fixtures"""
        from reporters.report_generator import ReportGenerator
        self.generator = ReportGenerator()

    def test_generate_statistics(self):
        """Test statistics generation"""
        findings = [
            {'vulnerability': 'SQL Injection', 'severity': 'High', 'url': 'https://example.com/1'},
            {'vulnerability': 'XSS', 'severity': 'High', 'url': 'https://example.com/2'},
            {'vulnerability': 'Missing Header', 'severity': 'Low', 'url': 'https://example.com/3'}
        ]

        stats = self.generator._generate_statistics(findings)

        assert stats['total'] == 3
        assert stats['by_severity']['High'] == 2
        assert stats['by_severity']['Low'] == 1
        assert stats['by_type']['SQL Injection'] == 1

    def test_sort_by_severity(self):
        """Test sorting by severity"""
        findings = [
            {'severity': 'Low'},
            {'severity': 'High'},
            {'severity': 'Medium'}
        ]

        sorted_findings = self.generator._sort_by_severity(findings)

        assert len(sorted_findings['High']) == 1
        assert len(sorted_findings['Medium']) == 1
        assert len(sorted_findings['Low']) == 1


class TestParameterAnalyzer:
    """Tests for parameter analyzer"""

    def setup_method(self):
        """Setup test fixtures"""
        from parsers.link_parser import ParameterAnalyzer
        self.analyzer = ParameterAnalyzer()

    def test_analyze_parameter_safe(self):
        """Test analysis of safe parameter"""
        result = self.analyzer.analyze_parameter('search', 'test query')

        assert len(result['risks']) == 0

    def test_analyze_parameter_sqli(self):
        """Test analysis of SQLi parameter"""
        result = self.analyzer.analyze_parameter('id', "1' OR '1'='1")

        assert len(result['risks']) > 0
        assert any(r['type'] == 'SQL Injection' for r in result['risks'])

    def test_analyze_parameter_xss(self):
        """Test analysis of XSS parameter"""
        result = self.analyzer.analyze_parameter('comment', '<script>alert(1)</script>')

        assert len(result['risks']) > 0
        assert any(r['type'] == 'XSS' for r in result['risks'])


# Integration tests
@pytest.mark.asyncio
class TestIntegration:
    """Integration tests"""

    async def test_full_scan_workflow(self):
        """Test full scan workflow"""
        # This would require a test server
        # Placeholder for now
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
