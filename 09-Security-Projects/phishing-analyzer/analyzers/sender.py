"""
Analyzer per il mittente delle email
Verifica spoofing, domain similarity e altre anomalie
"""

import re
import email
from email.header import decode_header
from typing import Dict, List, Optional, Tuple
import yaml
import tldextract

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SenderAnalyzer:
    """Analizza il mittente dell'email per rilevare spoofing e anomalie"""

    def __init__(self, patterns_file: str = None):
        """
        Inizializza l'analizzatore del mittente

        Args:
            patterns_file: Percorso al file YAML con i pattern
        """
        self.patterns = self._load_patterns(patterns_file)
        self.free_email_domains = [
            'gmail.com', 'yahoo.com', 'yahoo.it', 'hotmail.com',
            'outlook.com', 'live.com', 'libero.it', 'alice.it',
            'tin.it', 'virgilio.it', 'email.it', 'ymail.com',
            'protonmail.com', 'protonmail.ch', 'icloud.com',
            'mail.com', 'gmx.com', 'gmx.net', 'aol.com'
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

    def analyze_sender(self, email_message: email.message.Message) -> Dict:
        """
        Analizza il mittente dell'email

        Args:
            email_message: Oggetto email.message.EmailMessage

        Returns:
            Dict con risultati dell'analisi
        """
        # Estrai informazioni sul mittente
        from_header = email_message.get('From', '')
        reply_to = email_message.get('Reply-To', '')
        return_path = email_message.get('Return-Path', '')
        sender_header = email_message.get('Sender', '')

        # Parse del mittente
        sender_name, sender_email = self._parse_from_header(from_header)
        reply_to_email = self._extract_email(reply_to) if reply_to else None
        return_path_email = self._extract_email(return_path) if return_path else None

        # Analisi del dominio
        if sender_email:
            domain = sender_email.split('@')[-1]
            extracted = tldextract.extract(domain)
            registered_domain = extracted.registered_domain
        else:
            domain = None
            registered_domain = None

        result = {
            'name': sender_name,
            'email': sender_email,
            'domain': domain,
            'registered_domain': registered_domain,
            'reply_to': reply_to_email,
            'return_path': return_path_email,
            'suspicious': False,
            'checks': {}
        }

        # Esegui controlli
        if sender_email:
            # 1. Verifica se è un dominio di email gratuita
            is_free_email = self._is_free_email_domain(domain)
            result['checks']['free_email'] = is_free_email

            # 2. Verifica mismatch nome display e email
            display_mismatch = self._check_display_name_mismatch(sender_name, sender_email)
            result['checks']['display_name_mismatch'] = display_mismatch

            # 3. Verifica differenza tra From e Reply-To
            reply_to_mismatch = self._check_reply_to_mismatch(sender_email, reply_to_email)
            result['checks']['reply_to_mismatch'] = reply_to_mismatch

            # 4. Verifica spoofing di marchi noti
            spoofed = self._is_spoofed_brand(sender_name, registered_domain)
            result['checks']['spoofed'] = spoofed
            if spoofed.get('is_suspicious'):
                result['checks']['spoofed_brand'] = spoofed.get('brand')
                result['checks']['spoofed_details'] = spoofed

            # 5. Verifica typosquatting
            misspelled = self._is_misspelled_domain(registered_domain)
            result['checks']['misspelled_domain'] = misspelled

            # 6. Verifica Return-Path diverso
            return_path_mismatch = self._check_return_path_mismatch(sender_email, return_path_email)
            result['checks']['return_path_mismatch'] = return_path_mismatch

            # 7. Verifica ruolo del mittente (es. support@, admin@)
            generic_role = self._is_generic_role(sender_email)
            result['checks']['generic_role'] = generic_role

            # Calcola suspicious flag
            result['suspicious'] = any([
                spoofed.get('is_suspicious', False),
                misspelled,
                reply_to_mismatch,
                return_path_mismatch
            ])

            # Calcolo punteggio base
            risk_score = 0
            if spoofed.get('is_suspensitive', False):
                risk_score += 25
            if misspelled:
                risk_score += 20
            if reply_to_mismatch:
                risk_score += 12
            if return_path_mismatch:
                risk_score += 10
            if is_free_email:
                risk_score += 8
            if display_mismatch:
                risk_score += 10

            result['risk_score'] = risk_score

        return result

    def _parse_from_header(self, from_header: str) -> Tuple[str, str]:
        """
        Estrae nome e email dall'header From

        Returns:
            Tuple (nome, email)
        """
        if not from_header:
            return None, None

        # Decodifica l'header
        decoded_parts = []
        for part, encoding in decode_header(from_header):
            if isinstance(part, bytes):
                if encoding:
                    try:
                        decoded_parts.append(part.decode(encoding))
                    except:
                        decoded_parts.append(part.decode('utf-8', errors='ignore'))
                else:
                    decoded_parts.append(part.decode('utf-8', errors='ignore'))
            else:
                decoded_parts.append(str(part))

        from_decoded = ''.join(decoded_parts)

        # Estrai nome e email
        # Pattern 1: "Nome <email@domain.com>"
        match = re.match(r'"?(.+?)"?\s*<([^>]+)>', from_decoded)
        if match:
            name = match.group(1).strip()
            email_addr = match.group(2).strip()
            return name, email_addr

        # Pattern 2: email@domain.com (senza nome)
        if '@' in from_decoded:
            return None, from_decoded.strip()

        return None, None

    def _extract_email(self, header: str) -> Optional[str]:
        """Estrae l'indirizzo email da un header"""
        if not header:
            return None

        # Cerca pattern email
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', header)
        return match.group(0) if match else None

    def _is_free_email_domain(self, domain: str) -> bool:
        """Verifica se il dominio è un servizio di email gratuito"""
        if not domain:
            return False
        return domain.lower() in [d.lower() for d in self.free_email_domains]

    def _check_display_name_mismatch(self, name: str, email_addr: str) -> bool:
        """
        Verifica se il nome display non corrisponde all'email

        Esempio: "PayPal" <notpaypal@gmail.com>
        """
        if not name or not email_addr:
            return False

        # Controlla se il nome contiene un marchio noto
        brand_keywords = self.patterns.get('brand_keywords', {})
        for brand, keywords in brand_keywords.items():
            for keyword in keywords:
                if keyword.lower() in name.lower():
                    # Il nome contiene un brand, verifica il dominio
                    if not email_addr.lower():
                        return True

                    # Il dominio dovrebbe corrispondere al brand
                    legitimate_domains = self.patterns.get('legitimate_domains', [])
                    domain = email_addr.split('@')[-1].lower()

                    # Se il nome indica un brand ma il dominio non è quello ufficiale
                    if domain not in [ld.lower() for ld in legitimate_domains]:
                        return True

        return False

    def _check_reply_to_mismatch(self, from_email: str, reply_to: str) -> bool:
        """
        Verifica se Reply-To è diverso da From

        Questo può indicare che le risposte andranno a una persona diversa
        """
        if not from_email or not reply_to:
            return False

        # Confronta i domini
        from_domain = from_email.split('@')[-1].lower() if '@' in from_email else None
        reply_domain = reply_to.split('@')[-1].lower() if '@' in reply_to else None

        return from_domain != reply_domain

    def _check_return_path_mismatch(self, from_email: str, return_path: str) -> bool:
        """
        Verifica se Return-Path è diverso da From

        Questo può indicare che la email è stata inviata attraverso un server terzo
        """
        if not from_email or not return_path:
            return False

        # Estrai dominio dal return-path (rimuovi eventuali bounce info)
        return_path_clean = return_path.split('@')[-1].split('>')[0].lower() if '@' in return_path else None
        from_domain = from_email.split('@')[-1].lower() if '@' in from_email else None

        return return_path_clean != from_domain

    def _is_spoofed_brand(self, name: str, domain: str) -> Dict:
        """
        Verifica se il mittente sta tentando di spoofare un marchio noto
        """
        if not name and not domain:
            return {'is_suspicious': False}

        brand_keywords = self.patterns.get('brand_keywords', {})
        legitimate_domains = self.patterns.get('legitimate_domains', [])

        # Cerca corrispondenze con marchi noti
        for brand, keywords in brand_keywords.items():
            # Controlla nel nome
            name_match = False
            if name:
                for keyword in keywords:
                    if keyword.lower() in name.lower():
                        name_match = True
                        break

            # Controlla nel dominio
            domain_match = False
            if domain:
                for legit_domain in legitimate_domains:
                    if legit_domain.lower() in domain.lower():
                        domain_match = True
                        break

            # Se il nome indica un brand ma il dominio non è quello legittimo
            if name_match and not domain_match:
                return {
                    'is_suspicious': True,
                    'brand': brand,
                    'name_match': name_match,
                    'domain_legitimate': False
                }

            # Se il dominio sembra simile ma non è identico
            if domain and domain_match is False:
                for legit_domain in legitimate_domains:
                    if self._is_similar_string(domain.lower(), legit_domain.lower()):
                        return {
                            'is_suspicious': True,
                            'brand': brand,
                            'legitimate_domain': legit_domain,
                            'fake_domain': domain
                        }

        return {'is_suspicious': False}

    def _is_misspelled_domain(self, domain: str) -> bool:
        """
        Verifica se il dominio è un typosquatting di un dominio legittimo
        """
        if not domain:
            return False

        legitimate_domains = self.patterns.get('legitimate_domains', [])

        for legit_domain in legitimate_domains:
            if self._is_similar_string(domain.lower(), legit_domain.lower(), threshold=0.90):
                return True

        return False

    def _is_similar_string(self, str1: str, str2: str, threshold: float = 0.90) -> bool:
        """
        Calcola la somiglianza tra due stringhe
        """
        if abs(len(str1) - len(str2)) > 3:
            return False

        # Distanza di Levenshtein semplificata
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        max_len = max(m, n)
        similarity = 1 - (dp[m][n] / max_len)

        return similarity >= threshold

    def _is_generic_role(self, email_addr: str) -> bool:
        """
        Verifica se l'email usa un ruolo generico

        Esempio: support@, admin@, info@
        """
        if not email_addr or '@' not in email_addr:
            return False

        local_part = email_addr.split('@')[0].lower()
        generic_roles = [
            'admin', 'administrator', 'support', 'info', 'contact',
            'service', 'help', 'billing', 'sales', 'noreply',
            'no-reply', 'notifications', 'alert', 'security'
        ]

        return local_part in generic_roles

    def format_sender_report(self, analysis: Dict) -> str:
        """Formatta il report dell'analisi del mittente"""
        report = []
        report.append("\n👤 ANALISI MITTENTE")
        report.append("─" * 60)

        report.append(f"Nome: {analysis.get('name', 'N/A')}")
        report.append(f"Email: {analysis.get('email', 'N/A')}")
        report.append(f"Dominio: {analysis.get('domain', 'N/A')}")

        if analysis.get('suspicious'):
            report.append("\n⚠️  INDIicatorI SOSPETTI:")

            checks = analysis.get('checks', {})

            if checks.get('spoofed'):
                spoofed = checks.get('spoofed_details', {})
                report.append(f"  🔴 Possibile spoofing del marchio: {spoofed.get('brand', 'N/A')}")

            if checks.get('misspelled_domain'):
                report.append("  🔴 Dominio con refuso (typosquatting)")

            if checks.get('reply_to_mismatch'):
                report.append(f"  🟠 Reply-To diverso: {analysis.get('reply_to')}")

            if checks.get('return_path_mismatch'):
                report.append(f"  🟠 Return-Path diverso: {analysis.get('return_path')}")

            if checks.get('display_name_mismatch'):
                report.append("  🟠 Il nome display non corrisponde al dominio")

            if checks.get('free_email'):
                report.append("  🟡 Usa servizio di email gratuito")

            report.append(f"\nPunteggio rischio: {analysis.get('risk_score', 0)}/100")
        else:
            report.append("\n✅ Nessun indicatore sospetto rilevato")

        return '\n'.join(report)
