"""
Analyzer per i link nelle email
Rileva URL sospetti, typosquatting e altri indicatori
"""

import re
import urllib.parse
from typing import Dict, List, Set
from urllib.parse import urlparse
import tldextract
import validators
import yaml

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LinkAnalyzer:
    """Analizza i link nelle email per rilevare minacce"""

    def __init__(self, patterns_file: str = None):
        """
        Inizializza l'analizzatore di link

        Args:
            patterns_file: Percorso al file YAML con i pattern
        """
        self.patterns = self._load_patterns(patterns_file)
        self.known_shorteners = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co',
            'ow.ly', 'is.gd', 'buff.ly', 'short.link',
            'bit.do', 'mcaf.ee', 'su.pr', 'ow.ly',
            'tr.im', 'snip.ly', 'snipurl.com'
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

    def extract_links(self, text: str) -> Set[str]:
        """
        Estrae tutti i link dal testo

        Args:
            text: Testo da analizzare

        Returns:
            Set di URL trovati
        """
        # Pattern regex per URL
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)

        # Pulisci gli URL (rimuovi caratteri di punteggiatura finali)
        cleaned_urls = set()
        for url in urls:
            # Rimuovi caratteri finali non validi
            url = re.sub(r'[.,;:!?)\]]+$', '', url)
            cleaned_urls.add(url)

        return cleaned_urls

    def analyze_link(self, url: str) -> Dict:
        """
        Analizza un singolo link per determinare se è sospetto

        Args:
            url: URL da analizzare

        Returns:
            Dict con risultati dell'analisi
        """
        result = {
            'url': url,
            'suspicious': False,
            'risk_score': 0,
            'checks': {}
        }

        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)

            # 1. Verifica HTTPS
            is_https = parsed.scheme == 'https'
            result['checks']['https'] = is_https
            if not is_https:
                result['risk_score'] += 12
                result['suspicious'] = True

            # 2. Verifica se usa indirizzo IP invece del dominio
            uses_ip = self._uses_ip_address(parsed.netloc)
            result['checks']['ip_address'] = uses_ip
            if uses_ip:
                result['risk_score'] += 20
                result['suspicious'] = True

            # 3. Verifica TLD sospetto
            suspicious_tld = self._is_suspicious_tld(extracted.suffix)
            result['checks']['suspicious_tld'] = suspicious_tld
            result['checks']['tld'] = extracted.suffix
            if suspicious_tld:
                result['risk_score'] += 15
                result['suspicious'] = True

            # 4. Verifica se è un URL accorciato
            is_shortened = self._is_shortened_url(extracted.registered_domain)
            result['checks']['shortened'] = is_shortened
            if is_shortened:
                result['risk_score'] += 10
                result['suspicious'] = True

            # 5. Verifica typosquatting (dominio con refuso)
            misspelled = self._is_misspelled_domain(extracted.registered_domain)
            result['checks']['misspelled'] = misspelled
            if misspelled:
                result['risk_score'] += 20
                result['suspicious'] = True

            # 6. Verifica lunghezza del dominio (domini molto lunghi sono sospetti)
            domain_too_long = len(extracted.registered_domain) > 50
            result['checks']['long_domain'] = domain_too_long
            if domain_too_long:
                result['risk_score'] += 8
                result['suspicious'] = True

            # 7. Verifica caratteri strani nel dominio
            has_special_chars = bool(re.search(r'[^a-zA-Z0-9.-]', extracted.registered_domain))
            result['checks']['special_chars'] = has_special_chars
            if has_special_chars:
                result['risk_score'] += 15
                result['suspicious'] = True

            # 8. Verifica numerazione eccessiva (es. paypal-12345.com)
            has_numbers = bool(re.search(r'\d{3,}', extracted.domain))
            result['checks']['excessive_numbers'] = has_numbers
            if has_numbers:
                result['risk_score'] += 10
                result['suspicious'] = True

            # 9. Verifica lookalike characters (homograph attacks)
            has_lookalike = self._has_lookalike_chars(extracted.domain)
            result['checks']['lookalike_chars'] = has_lookalike
            if has_lookalike:
                result['risk_score'] += 18
                result['suspicious'] = True

            # Informazioni estratte
            result['domain'] = extracted.registered_domain
            result['full_domain'] = parsed.netloc
            result['path'] = parsed.path

            # Calcola livello di rischio
            if result['risk_score'] >= 30:
                result['risk_level'] = 'critical'
            elif result['risk_score'] >= 20:
                result['risk_level'] = 'high'
            elif result['risk_score'] >= 10:
                result['risk_level'] = 'medium'
            else:
                result['risk_level'] = 'low'

        except Exception as e:
            result['error'] = str(e)
            result['suspicious'] = True
            result['risk_score'] = 15

        return result

    def _uses_ip_address(self, netloc: str) -> bool:
        """Verifica se l'URL usa un indirizzo IP"""
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$'
        return bool(re.match(ip_pattern, netloc.split('@')[-1]))

    def _is_suspicious_tld(self, tld: str) -> bool:
        """Verifica se il TLD è nella lista di quelli sospetti"""
        if not tld:
            return False
        suspicious_tlds = self.patterns.get('suspicious_tlds', [])
        return tld.lower() in [t.lower() for t in suspicious_tlds]

    def _is_shortened_url(self, domain: str) -> bool:
        """Verifica se è un URL accorziato"""
        return domain.lower() in [k.lower() for k in self.known_shorteners]

    def _is_misspelled_domain(self, domain: str) -> Dict:
        """
        Verifica se il dominio è un typosquatting di un marchio noto

        Returns:
            Dict con: is_suspicious, matched_brand, similarity
        """
        if not domain:
            return False

        legitimate_domains = self.patterns.get('legitimate_domains', [])
        domain_lower = domain.lower()

        for legit_domain in legitimate_domains:
            legit_lower = legit_domain.lower()

            # Verifica somiglianza con Levenshtein distance semplificata
            if self._is_similar(domain_lower, legit_lower):
                return True

        return False

    def _is_similar(self, str1: str, str2: str, threshold: float = 0.85) -> bool:
        """
        Calcola la somiglianza tra due stringhe

        Usa un algoritmo semplificato di Levenshtein
        """
        if abs(len(str1) - len(str2)) > 3:
            return False

        # Calcola distanza di Levenshtein semplificata
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

    def _has_lookalike_chars(self, domain: str) -> bool:
        """
        Verifica caratteri "lookalike" usati per attacchi homograph

        Esempio: pаypal.com (con 'а' cirillico invece di 'a' latino)
        """
        # Caratteri latini comuni
        latin_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')

        # Caratteri pericolosi che sembrano caratteri latini
        dangerous_chars = []
        for char in domain:
            if char not in latin_chars:
                # Fuori dall'ASCII range - potrebbe essere un carattere non latino
                if ord(char) > 127:
                    return True

        return False

    def analyze_email_links(self, email_body: str, html_content: str = None) -> Dict:
        """
        Analizza tutti i link in una email

        Args:
            email_body: Testo della email
            html_content: Contenuto HTML opzionale

        Returns:
            Dict con risultati dell'analisi
        """
        # Estrai link dal testo
        text_links = self.extract_links(email_body)
        if html_content:
            html_links = self.extract_links(html_content)
            text_links.update(html_links)

        analyzed_links = []
        suspicious_count = 0
        safe_count = 0

        for link in text_links:
            analysis = self.analyze_link(link)
            analyzed_links.append(analysis)
            if analysis['suspicious']:
                suspicious_count += 1
            else:
                safe_count += 1

        return {
            'total_links': len(text_links),
            'suspicious_count': suspicious_count,
            'safe_count': safe_count,
            'has_suspicious_links': suspicious_count > 0,
            'analyzed_links': analyzed_links
        }

    def format_link_report(self, analysis_result: Dict) -> str:
        """Formatta il report dell'analisi dei link"""
        report = []
        report.append(f"\n📊 ANALISI LINK ({analysis_result['total_links']} trovati)")
        report.append("─" * 60)

        for link in analysis_result['analyzed_links']:
            if link.get('suspicious'):
                risk_emoji = '🔴' if link['risk_level'] == 'critical' else '🟠'
                report.append(f"\n{risk_emoji} {link['url']}")
                report.append(f"   Dominio: {link.get('domain', 'N/A')}")

                issues = []
                checks = link.get('checks', {})

                if not checks.get('https'):
                    issues.append('❌ Non usa HTTPS')
                if checks.get('ip_address'):
                    issues.append('❌ Usa indirizzo IP')
                if checks.get('suspicious_tld'):
                    issues.append(f"⚠️  TLD sospetto: {checks.get('tld')}")
                if checks.get('shortened'):
                    issues.append('⚠️  URL accorciato')
                if checks.get('misspelled'):
                    issues.append('❌ Dominio con refuso (typosquatting)')
                if checks.get('special_chars'):
                    issues.append('❌ Contiene caratteri speciali')
                if checks.get('lookalike_chars'):
                    issues.append('❌ Caratteri lookalike (homograph)')
                if checks.get('long_domain'):
                    issues.append('⚠️  Dominio molto lungo')
                if checks.get('excessive_numbers'):
                    issues.append('⚠️  Numeri eccessivi nel dominio')

                for issue in issues:
                    report.append(f"   {issue}")

                report.append(f"   Punteggio rischio: {link['risk_score']}/100")
            else:
                report.append(f"\n✅ {link['url']}")

        return '\n'.join(report)


def check_url(url: str) -> Dict:
    """
    Funzione helper per controllare rapidamente un URL

    Args:
        url: URL da controllare

    Returns:
        Risultato dell'analisi
    """
    analyzer = LinkAnalyzer()
    return analyzer.analyze_link(url)
