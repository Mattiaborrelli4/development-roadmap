"""
Analyzer per il contenuto delle email
Rileva tattiche di phishing, keyword e indicatori nel contenuto
"""

import re
import email
from email import policy
from email.parser import BytesParser
from typing import Dict, List, Set
import yaml
from html import unescape

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ContentAnalyzer:
    """Analizza il contenuto delle email per rilevare indicatori di phishing"""

    def __init__(self, patterns_file: str = None):
        """
        Inizializza l'analizzatore del contenuto

        Args:
            patterns_file: Percorso al file YAML con i pattern
        """
        self.patterns = self._load_patterns(patterns_file)

        # Estensioni di file pericolose
        self.dangerous_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.com', '.pif',
            '.vbs', '.js', '.jse', '.wsf', '.wsh', '.msi',
            '.docm', '.xlsm', '.pptm', '.sldm', '.dotm',
            '.zip', '.rar', '.7z', '.tar', '.gz'
        ]

        # Estensioni sospette
        self.suspicious_extensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt',
            '.pps', '.pptx', '.jar', '.hta'
        ]

    def _load_patterns(self, patterns_file: str) -> Dict:
        """Carica i pattern dal file YAML"""
        if patterns_file is None:
            patterns_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'knowledge',
                'patterns.yaml'
            )

        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️  Impossibile caricare patterns.yaml: {e}")
            return {}

    def analyze_content(self, email_message: email.message.Message) -> Dict:
        """
        Analizza il contenuto completo della email

        Args:
            email_message: Oggetto email.message.EmailMessage

        Returns:
            Dict con risultati dell'analisi
        """
        # Estrai testo e HTML
        text_content = self._extract_text_content(email_message)
        html_content = self._extract_html_content(email_message)

        # Combina tutto per l'analisi
        full_content = text_content + ' ' + html_content

        result = {
            'subject': self._analyze_subject(email_message.get('Subject', '')),
            'urgency_detected': False,
            'pressure_tactics': False,
            'credential_requests': False,
            'financial_keywords': False,
            'urgency_keywords': [],
            'pressure_keywords': [],
            'credential_keywords': [],
            'financial_keywords_found': [],
            'suspicious_phrases': [],
            'urgency_score': 0,
            'pressure_score': 0,
            'credential_score': 0,
            'financial_score': 0
        }

        # Analizza il contenuto
        phishing_keywords = self.patterns.get('phishing_keywords', {})

        # 1. Cerca keyword di urgenza
        urgency_keywords = phishing_keywords.get('urgency', [])
        for keyword in urgency_keywords:
            if keyword.lower() in full_content.lower():
                result['urgency_keywords'].append(keyword)
                result['urgency_score'] += 3

        if result['urgency_keywords']:
            result['urgency_detected'] = True

        # 2. Cerca tattiche di pressione
        pressure_keywords = phishing_keywords.get('pressure_tactics', [])
        for keyword in pressure_keywords:
            if keyword.lower() in full_content.lower():
                result['pressure_keywords'].append(keyword)
                result['pressure_score'] += 4

        if result['pressure_keywords']:
            result['pressure_tactics'] = True

        # 3. Cerca richieste di credenziali
        credential_keywords = phishing_keywords.get('credential_harvesting', [])
        for keyword in credential_keywords:
            # Controlla anche pattern più complessi
            if keyword.lower() in full_content.lower():
                # Verifica che sia una richiesta attiva
                if self._is_credential_request(full_content, keyword):
                    result['credential_keywords'].append(keyword)
                    result['credential_score'] += 10

        if result['credential_keywords']:
            result['credential_requests'] = True

        # 4. Cerca indicatori finanziari
        financial_keywords = phishing_keywords.get('financial_indicators', [])
        for keyword in financial_keywords:
            if keyword.lower() in full_content.lower():
                result['financial_keywords_found'].append(keyword)
                result['financial_score'] += 2

        if result['financial_keywords_found']:
            result['financial_keywords'] = True

        # 5. Cerca frasi sospette
        result['suspicious_phrases'] = self._find_suspicious_phrases(full_content)

        # 6. Analizza allegati
        result['attachments'] = self._analyze_attachments(email_message)

        # Calcola punteggio complessivo del contenuto
        result['total_score'] = (
            result['urgency_score'] +
            result['pressure_score'] +
            result['credential_score'] +
            result['financial_score']
        )

        return result

    def _extract_text_content(self, email_message: email.message.Message) -> str:
        """Estrae il contenuto testuale dalla email"""
        text_content = ''

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))

                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        text_content += part.get_payload(decode=True).decode(charset, errors='ignore')
                    except:
                        try:
                            text_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except:
                            pass
        elif email_message.get_content_type() == 'text/plain':
            charset = email_message.get_content_charset() or 'utf-8'
            try:
                text_content = email_message.get_payload(decode=True).decode(charset, errors='ignore')
            except:
                try:
                    text_content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass

        return text_content

    def _extract_html_content(self, email_message: email.message.Message) -> str:
        """Estrae il contenuto HTML dalla email"""
        html_content = ''

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))

                if content_type == 'text/html' and 'attachment' not in content_disposition:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        html_content += part.get_payload(decode=True).decode(charset, errors='ignore')
                    except:
                        try:
                            html_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except:
                            pass
        elif email_message.get_content_type() == 'text/html':
            charset = email_message.get_content_charset() or 'utf-8'
            try:
                html_content = email_message.get_payload(decode=True).decode(charset, errors='ignore')
            except:
                try:
                    html_content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass

        # Rimuovi tag HTML per l'analisi
        from html.parser import HTMLParser

        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.text = []

            def handle_data(self, d):
                self.text.append(d)

            def get_data(self):
                return ''.join(self.text)

        stripper = MLStripper()
        try:
            stripper.feed(html_content)
            return stripper.get_data()
        except:
            return html_content

    def _analyze_subject(self, subject: str) -> Dict:
        """Analizza l'oggetto della email"""
        # Decodifica subject se necessario
        try:
            from email.header import decode_header
            decoded_parts = []
            for part, encoding in decode_header(subject):
                if isinstance(part, bytes):
                    if encoding:
                        decoded_parts.append(part.decode(encoding))
                    else:
                        decoded_parts.append(part.decode('utf-8', errors='ignore'))
                else:
                    decoded_parts.append(str(part))
            subject = ''.join(decoded_parts)
        except:
            pass

        result = {
            'subject': subject,
            'has_urgency': False,
            'is_all_caps': False,
            'has_exclamation': False,
            'suspicious_words': []
        }

        if not subject:
            return result

        # Controlla urgenza
        urgency_words = ['urgente', 'immediato', 'importante', 'azione richiesta', 'scadenza']
        for word in urgency_words:
            if word.lower() in subject.lower():
                result['has_urgency'] = True
                result['suspicious_words'].append(word)

        # Controlla maiuscole
        if subject.isupper() and len(subject) > 10:
            result['is_all_caps'] = True

        # Controlla esclamazioni
        if '!' in subject or subject.count('!') > 1:
            result['has_exclamation'] = True

        return result

    def _is_credential_request(self, content: str, keyword: str) -> bool:
        """
        Verifica se la keyword è parte di una richiesta di credenziali
        """
        # Pattern che indicano una richiesta attiva
        request_indicators = [
            'inserisci', 'inserisca', 'digita', 'digiti', 'clicca', 'clicchi',
            'conferma', 'confermi', 'verifica', 'verifichi', 'login', 'accedi',
            'aggiorna', 'aggiorni', 'modifica', 'modifichi'
        ]

        content_lower = content.lower()
        keyword_lower = keyword.lower()

        # Cerca indicatori vicino alla keyword
        for indicator in request_indicators:
            # Cerca pattern come "inserisci la tua password"
            pattern = f'{indicator}.*{keyword_lower}|{keyword_lower}.*{indicator}'
            if re.search(pattern, content_lower):
                return True

        return False

    def _find_suspicious_phrases(self, content: str) -> List[str]:
        """Trova frasi sospette nel contenuto"""
        suspicious_phrases = []

        # Frasi comuni di phishing
        phrases = [
            r'verifica.*identità',
            r'conferma.*password',
            r'aggiorna.*informazioni',
            r'account.*sospeso',
            r'attività.*sospetta',
            r'accesso.*non autorizzato',
            r'pagamento.*rimborso',
            r'fattura.*allegata',
            r'click.*qui',
            r'clicca.*subito',
            r'scarica.*allegato',
            r'entro.*24.*ore',
            r'entro.*48.*ore',
            r'ultimo.*avviso'
        ]

        for phrase in phrases:
            if re.search(phrase, content, re.IGNORECASE):
                suspicious_phrases.append(phrase)

        return suspicious_phrases

    def _analyze_attachments(self, email_message: email.message.Message) -> Dict:
        """Analizza gli allegati della email"""
        result = {
            'has_attachments': False,
            'attachments': [],
            'dangerous_count': 0,
            'suspicious_count': 0,
            'suspicious_extensions': False
        }

        for part in email_message.walk():
            content_disposition = str(part.get('Content-Disposition', ''))

            if 'attachment' in content_disposition:
                filename = part.get_filename()

                if filename:
                    result['has_attachments'] = True

                    # Analizza il nome del file
                    attachment_info = {
                        'filename': filename,
                        'extension': None,
                        'dangerous': False,
                        'suspicious': False
                    }

                    # Estrai estensione
                    if '.' in filename:
                        extension = '.' + filename.rsplit('.', 1)[-1].lower()
                        attachment_info['extension'] = extension

                        # Verifica se è pericolosa
                        if extension in self.dangerous_extensions:
                            attachment_info['dangerous'] = True
                            result['dangerous_count'] += 1
                            result['suspicious_extensions'] = True

                        # Verifica se è sospetta
                        elif extension in self.suspicious_extensions:
                            attachment_info['suspicious'] = True
                            result['suspicious_count'] += 1

                    # Verifica doppie estensioni (es. file.pdf.exe)
                    if filename.count('.') > 1:
                        attachment_info['dangerous'] = True
                        result['dangerous_count'] += 1
                        result['suspicious_extensions'] = True

                    result['attachments'].append(attachment_info)

        return result

    def format_content_report(self, analysis: Dict) -> str:
        """Formatta il report dell'analisi del contenuto"""
        report = []
        report.append("\n📄 ANALISI CONTENUTO")
        report.append("─" * 60)

        # Subject
        subject = analysis.get('subject', {})
        report.append(f"\nOggetto: {subject.get('subject', '(vuoto)')}")
        if subject.get('has_urgency'):
            report.append("  ⚠️  Contiene parole di urgenza")
        if subject.get('is_all_caps'):
            report.append("  ⚠️  Tutto in maiuscolo")
        if subject.get('has_exclamation'):
            report.append("  ⚠️  Contiene esclamazioni")

        # Analisi del contenuto
        if analysis.get('urgency_detected'):
            report.append(f"\n🔴 TATTICHE DI URGENZA TROVATE:")
            for keyword in analysis.get('urgency_keywords', [])[:5]:
                report.append(f"  • {keyword}")

        if analysis.get('pressure_tactics'):
            report.append(f"\n🟠 TATTICHE DI PRESSIONE TROVATE:")
            for keyword in analysis.get('pressure_keywords', [])[:5]:
                report.append(f"  • {keyword}")

        if analysis.get('credential_requests'):
            report.append(f"\n🔴 RICHIESTA DI CREDENZIALI:")
            for keyword in analysis.get('credential_keywords', [])[:5]:
                report.append(f"  • {keyword}")
            report.append("  ⚠️  LE AZIENDE NON CHIEDONO MAI PASSWORD VIA EMAIL!")

        if analysis.get('financial_keywords'):
            report.append(f"\n🟡 CONTENUTO FINANZIARIO:")
            for keyword in analysis.get('financial_keywords_found', [])[:5]:
                report.append(f"  • {keyword}")

        # Frasi sospette
        if analysis.get('suspicious_phrases'):
            report.append(f"\n🔍 FRASI SOSPETTE:")
            for phrase in analysis.get('suspicious_phrases', [])[:5]:
                report.append(f"  • {phrase}")

        # Allegati
        attachments = analysis.get('attachments', {})
        if attachments.get('has_attachments'):
            report.append(f"\n📎 ALLEGATI ({len(attachments.get('attachments', []))}):")
            for att in attachments.get('attachments', []):
                status = "✅"
                if att.get('dangerous'):
                    status = "🔴 PERICOLOSO"
                elif att.get('suspicious'):
                    status = "🟠 SOSPETTO"
                report.append(f"  {status} {att['filename']}")

            if attachments.get('suspicious_extensions'):
                report.append("\n  ⚠️  ⚠️  ⚠️  ATTENZIONE: Allegati con estensioni pericolose!")
        else:
            report.append("\n📎 Nessun allegato presente")

        # Punteggio
        report.append(f"\nPunteggio contenuto: {analysis.get('total_score', 0)}/100")

        return '\n'.join(report)
