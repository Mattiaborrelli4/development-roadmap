"""
Analyzer per gli header delle email
Verifica SPF, DKIM, DMARC e altri header di sicurezza
"""

import email
import re
from email import policy
from email.header import decode_header
from typing import Dict, List, Optional
import yaml

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.dns_tools import DNSChecker


class HeaderAnalyzer:
    """Analizza gli header delle email per verifiche di sicurezza"""

    def __init__(self, patterns_file: str = None):
        """
        Inizializza l'analizzatore di header

        Args:
            patterns_file: Percorso al file YAML con i pattern
        """
        self.dns_checker = DNSChecker()
        self.patterns = self._load_patterns(patterns_file)

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

    def analyze_headers(self, email_message: email.message.Message) -> Dict:
        """
        Analizza tutti gli header di sicurezza della email

        Args:
            email_message: Oggetto email.message.EmailMessage

        Returns:
            Dict con risultati di SPF, DKIM, DMARC
        """
        results = {
            'spf': self._analyze_spf(email_message),
            'dkim': self._analyze_dkim(email_message),
            'dmarc': self._analyze_dmarc_header(email_message),
            'authentication_results': self._analyze_authentication_results(email_message),
            'received_headers': self._analyze_received_headers(email_message)
        }

        return results

    def _analyze_spf(self, email_message: email.message.Message) -> Dict:
        """
        Analizza il risultato SPF dell'email

        SPF (Sender Policy Framework) verifica se il server è autorizzato
        """
        # Cerca header Received-SPF
        spf_header = email_message.get('Received-SPF', '')
        authentication_results = email_message.get('Authentication-Results', '')

        result = {
            'status': 'none',
            'details': 'Nessun risultato SPF trovato',
            'header': spf_header
        }

        if spf_header:
            spf_header_lower = spf_header.lower()
            if 'pass' in spf_header_lower:
                result['status'] = 'pass'
                result['details'] = 'SPF: Il server è autorizzato a inviare email per questo dominio'
            elif 'fail' in spf_header_lower:
                result['status'] = 'fail'
                result['details'] = 'SPF: Il server NON è autorizzato - possibile phishing'
            elif 'softfail' in spf_header_lower:
                result['status'] = 'softfail'
                result['details'] = 'SPF: Il server potrebbe non essere autorizzato'
            elif 'none' in spf_header_lower:
                result['status'] = 'none'
                result['details'] = 'SPF: Nessun record SPF configurato per il dominio'
            elif 'neutral' in spf_header_lower:
                result['status'] = 'neutral'
                result['details'] = 'SPF: Risultato neutro'
            elif 'permerror' in spf_header_lower:
                result['status'] = 'error'
                result['details'] = 'SPF: Errore permanente nella verifica'
            elif 'temperror' in spf_header_lower:
                result['status'] = 'error'
                result['details'] = 'SPF: Errore temporaneo nella verifica'
        elif authentication_results and 'spf=' in authentication_results.lower():
            # Estrai SPF da Authentication-Results
            auth_match = re.search(r'spf=(\w+)', authentication_results, re.IGNORECASE)
            if auth_match:
                spf_status = auth_match.group(1).lower()
                if spf_status == 'pass':
                    result['status'] = 'pass'
                    result['details'] = 'SPF: Il server è autorizzato'
                elif spf_status == 'fail':
                    result['status'] = 'fail'
                    result['details'] = 'SPF: Il server NON è autorizzato'
                elif spf_status == 'softfail':
                    result['status'] = 'softfail'
                    result['details'] = 'SPF: Il server potrebbe non essere autorizzato'
                elif spf_status == 'none':
                    result['status'] = 'none'
                    result['details'] = 'SPF: Nessun record SPF'

        return result

    def _analyze_dkim(self, email_message: email.message.Message) -> Dict:
        """
        Analizza la firma DKIM dell'email

        DKIM (DomainKeys Identified Mail) verifica l'integrità del messaggio
        """
        dkim_headers = email_message.get_all('DKIM-Signature', [])
        authentication_results = email_message.get('Authentication-Results', '')

        result = {
            'valid': None,
            'details': 'Nessuna firma DKIM trovata',
            'signatures': len(dkim_headers)
        }

        if dkim_headers:
            result['details'] = f'Trovate {len(dkim_headers)} firme DKIM'
            # Nota: La verifica completa della firma richiede la chiave pubblica DNS
            # Qui facciamo un'analisi di base

        # Controlla Authentication-Results
        if authentication_results and 'dkim=' in authentication_results.lower():
            auth_match = re.search(r'dkim=(\w+)', authentication_results, re.IGNORECASE)
            if auth_match:
                dkim_status = auth_match.group(1).lower()
                if dkim_status == 'pass':
                    result['valid'] = True
                    result['details'] = 'DKIM: Firma valida, email autentica'
                elif dkim_status == 'fail':
                    result['valid'] = False
                    result['details'] = 'DKIM: Firma non valida - email modificata o contraffatta'
                elif dkim_status == 'none':
                    result['valid'] = None
                    result['details'] = 'DKIM: Nessuna firma presente'

        return result

    def _analyze_dmarc_header(self, email_message: email.message.Message) -> Dict:
        """
        Analizza il risultato DMARC dell'email

        DMARC (Domain-based Message Authentication) indica la policy del dominio
        """
        authentication_results = email_message.get('Authentication-Results', '')

        result = {
            'status': 'none',
            'policy': None,
            'details': 'Nessun risultato DMARC trovato'
        }

        if authentication_results and 'dmarc=' in authentication_results.lower():
            # Cerca il risultato DMARC
            dmarc_match = re.search(r'dmarc=(\w+)', authentication_results, re.IGNORECASE)
            if dmarc_match:
                dmarc_status = dmarc_match.group(1).lower()
                if dmarc_status == 'pass':
                    result['status'] = 'pass'
                    result['details'] = 'DMARC: Autenticazione passata'
                elif dmarc_status == 'fail':
                    result['status'] = 'fail'
                    result['details'] = 'DMARC: Autenticazione fallita'

            # Cerca la policy DMARC
            policy_match = re.search(r'p=(\w+)', authentication_results, re.IGNORECASE)
            if policy_match:
                result['policy'] = policy_match.group(1).lower()

        return result

    def _analyze_authentication_results(self, email_message: email.message.Message) -> Dict:
        """
        Analizza l'header Authentication-Results completo
        """
        auth_results = email_message.get('Authentication-Results', '')

        return {
            'header': auth_results,
            'has_authentication': bool(auth_results),
            'methods': self._extract_auth_methods(auth_results)
        }

    def _extract_auth_methods(self, auth_results: str) -> List[str]:
        """Estrae i metodi di autenticazione trovati"""
        methods = []
        if 'spf=' in auth_results.lower():
            methods.append('SPF')
        if 'dkim=' in auth_results.lower():
            methods.append('DKIM')
        if 'dmarc=' in auth_results.lower():
            methods.append('DMARC')
        if 'iprev=' in auth_results.lower():
            methods.append('IPRev')
        return methods

    def _analyze_received_headers(self, email_message: email.message.Message) -> Dict:
        """
        Analizza gli header Received per tracciare il percorso dell'email
        """
        received_headers = email_message.get_all('Received', [])

        received_info = []
        for i, received in enumerate(received_headers[:5]):  # Massimo 5
            # Estrai informazioni di base
            from_match = re.search(r'from\s+([^\s]+)', received, re.IGNORECASE)
            by_match = re.search(r'by\s+([^\s]+)', received, re.IGNORECASE)
            ip_match = re.search(r'\[(\d+\.\d+\.\d+\.\d+)\]', received)

            info = {
                'index': i + 1,
                'from': from_match.group(1) if from_match else None,
                'by': by_match.group(1) if by_match else None,
                'ip': ip_match.group(1) if ip_match else None
            }
            received_info.append(info)

        return {
            'count': len(received_headers),
            'hops': received_info
        }

    def check_sender_domain_spf(self, domain: str) -> Dict:
        """
        Verifica il record SPF del dominio del mittente

        Args:
            domain: Dominio da verificare

        Returns:
            Risultato della verifica SPF
        """
        return self.dns_checker.check_spf(domain)

    def check_sender_domain_dmarc(self, domain: str) -> Dict:
        """
        Verifica il record DMARC del dominio del mittente

        Args:
            domain: Dominio da verificare

        Returns:
            Risultato della verifica DMARC
        """
        return self.dns_checker.check_dmarc(domain)


def decode_header_value(header_value: str) -> str:
    """
    Decodifica un header email (gestisce encoding)

    Args:
        header_value: Valore dell'header

    Returns:
        Stringa decodificata
    """
    if not header_value:
        return ""

    decoded_parts = []
    for part, encoding in decode_header(header_value):
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

    return ''.join(decoded_parts)
