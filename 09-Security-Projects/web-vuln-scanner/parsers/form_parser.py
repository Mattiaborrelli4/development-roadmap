"""
Web Vulnerability Scanner - Form Parser
Parses and analyzes HTML forms for vulnerability testing
"""

from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class FormParser:
    """Parses HTML forms and prepares them for testing"""

    def __init__(self):
        self.forms = []

    def parse_forms(self, html: str, page_url: str) -> List[Dict[str, Any]]:
        """
        Parse all forms from HTML content

        Args:
            html: HTML content
            page_url: URL of the page

        Returns:
            List of parsed forms
        """
        soup = BeautifulSoup(html, 'lxml')
        forms = []

        for form_element in soup.find_all('form'):
            form = self._parse_form(form_element, page_url)
            forms.append(form)

        self.forms = forms
        return forms

    def _parse_form(self, form_element: BeautifulSoup, page_url: str) -> Dict[str, Any]:
        """
        Parse a single form element

        Args:
            form_element: BeautifulSoup form element
            page_url: URL of the page

        Returns:
            Parsed form data
        """
        form = {
            'action': urljoin(page_url, form_element.get('action', page_url)),
            'method': form_element.get('method', 'GET').upper(),
            'enctype': form_element.get('enctype', 'application/x-www-form-urlencoded'),
            'page_url': page_url,
            'fields': [],
            'submit_fields': [],
            'has_csrf_token': False,
            'csrf_token_name': None
        }

        # Parse input fields
        for input_field in form_element.find_all('input'):
            field = self._parse_input_field(input_field)
            form['fields'].append(field)

            # Check for CSRF token
            if self._is_csrf_field(field):
                form['has_csrf_token'] = True
                form['csrf_token_name'] = field['name']

            # Track submit buttons
            if field['type'] == 'submit':
                form['submit_fields'].append(field)

        # Parse textarea fields
        for textarea in form_element.find_all('textarea'):
            field = {
                'name': textarea.get('name'),
                'type': 'textarea',
                'value': textarea.get_text(strip=True),
                'required': textarea.has_attr('required'),
                'id': textarea.get('id', ''),
                'maxlength': textarea.get('maxlength', None)
            }
            form['fields'].append(field)

        # Parse select fields
        for select in form_element.find_all('select'):
            field = self._parse_select_field(select)
            form['fields'].append(field)

        # Parse buttons
        for button in form_element.find_all('button'):
            field = {
                'name': button.get('name', ''),
                'type': button.get('type', 'submit'),
                'value': button.get('value', ''),
                'text': button.get_text(strip=True)
            }
            if field['type'] == 'submit':
                form['submit_fields'].append(field)

        return form

    def _parse_input_field(self, input_field) -> Dict[str, Any]:
        """Parse an input field"""
        return {
            'name': input_field.get('name'),
            'type': input_field.get('type', 'text'),
            'value': input_field.get('value', ''),
            'required': input_field.has_attr('required'),
            'id': input_field.get('id', ''),
            'placeholder': input_field.get('placeholder', ''),
            'maxlength': input_field.get('maxlength', None),
            'pattern': input_field.get('pattern', None),
            'min': input_field.get('min', None),
            'max': input_field.get('max', None)
        }

    def _parse_select_field(self, select) -> Dict[str, Any]:
        """Parse a select field"""
        options = []
        selected_value = ''

        for option in select.find_all('option'):
            option_value = option.get('value', option.get_text(strip=True))
            options.append({
                'value': option_value,
                'text': option.get_text(strip=True)
            })
            if option.has_attr('selected'):
                selected_value = option_value

        return {
            'name': select.get('name'),
            'type': 'select',
            'value': selected_value,
            'required': select.has_attr('required'),
            'id': select.get('id', ''),
            'multiple': select.has_attr('multiple'),
            'options': options
        }

    def _is_csrf_field(self, field: Dict[str, Any]) -> bool:
        """Check if a field looks like a CSRF token"""
        if not field['name']:
            return False

        csrf_indicators = [
            'csrf', 'token', '_token', 'authenticity_token',
            'csrf_token', 'csrfmiddlewaretoken', 'auth_token'
        ]

        field_name_lower = field['name'].lower()
        return any(indicator in field_name_lower for indicator in csrf_indicators)

    def get_testable_fields(self, form: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get fields that should be tested with payloads

        Args:
            form: Form data

        Returns:
            List of testable fields
        """
        testable_fields = []

        for field in form['fields']:
            # Skip hidden fields (usually contain tokens or IDs)
            if field['type'] == 'hidden':
                continue

            # Skip submit buttons
            if field['type'] == 'submit':
                continue

            # Skip CSRF tokens
            if self._is_csrf_field(field):
                continue

            # Test text-based fields
            if field['type'] in ['text', 'textarea', 'search', 'url', 'email',
                                  'tel', 'password', 'number']:
                testable_fields.append(field)

            # Test select fields
            if field['type'] == 'select':
                testable_fields.append(field)

        return testable_fields

    def prepare_form_data(self, form: Dict[str, Any],
                          payload: str,
                          field_name: str = None) -> Dict[str, Any]:
        """
        Prepare form data for testing with a payload

        Args:
            form: Form data
            payload: Test payload to inject
            field_name: Name of field to inject payload into (if None, use first testable field)

        Returns:
            Prepared data dictionary
        """
        data = {}
        testable_fields = self.get_testable_fields(form)

        if not testable_fields:
            return data

        # Use specified field or first testable field
        target_field = field_name or testable_fields[0]['name']

        for field in form['fields']:
            field_name = field['name']

            if not field_name:
                continue

            # Use existing value for most fields
            if field['type'] == 'hidden' or field == testable_fields[0]:
                if field == testable_fields[0]:
                    data[field_name] = payload
                else:
                    data[field_name] = field.get('value', '')
            elif field['type'] == 'checkbox':
                data[field_name] = 'on' if field.get('value') else 'off'
            elif field['type'] == 'radio':
                if field.get('checked'):
                    data[field_name] = field.get('value', 'on')

        return data

    def get_form_url(self, form: Dict[str, Any]) -> str:
        """Get the full URL where the form should be submitted"""
        return form['action']

    def get_form_method(self, form: Dict[str, Any]) -> str:
        """Get the form's HTTP method"""
        return form['method']

    def analyze_form_security(self, form: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze form for basic security issues

        Args:
            form: Form data

        Returns:
            List of security findings
        """
        findings = []

        # Check for CSRF protection
        if not form['has_csrf_token'] and form['method'] == 'POST':
            findings.append({
                'severity': 'Medium',
                'issue': 'Missing CSRF Token',
                'description': 'Form does not appear to have CSRF protection',
                'recommendation': 'Add CSRF token to form'
            })

        # Check for password field over HTTP
        has_password = any(f['type'] == 'password' for f in form['fields'])
        if has_password and not form['action'].startswith('https://'):
            findings.append({
                'severity': 'High',
                'issue': 'Password Over HTTP',
                'description': 'Password form submits over unencrypted connection',
                'recommendation': 'Use HTTPS for password forms'
            })

        # Check for autocomplete on password field
        password_field = next((f for f in form['fields'] if f['type'] == 'password'), None)
        if password_field and password_field.get('autocomplete') != 'off':
            findings.append({
                'severity': 'Low',
                'issue': 'Password Autocomplete',
                'description': 'Password field may allow browser to save password',
                'recommendation': 'Set autocomplete="off" on password fields'
            })

        return findings
