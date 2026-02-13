"""
DNS Tools per verifiche di sicurezza email
Module per controlli SPF, DKIM e DMARC
"""

import dns.resolver
import dns.exception
from typing import Dict, Optional, List


class DNSChecker:
    """Classe per eseguire verifiche DNS relative alla sicurezza email"""

    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 3
        self.resolver.lifetime = 3

    def check_spf(self, domain: str) -> Dict[str, any]:
        """
        Verifica il record SPF (Sender Policy Framework) di un dominio

        SPF specifica quali server sono autorizzati a inviare email per un dominio

        Args:
            domain: Il dominio da verificare

        Returns:
            Dict con: status (pass/fail/none/softfail), record, details
        """
        try:
            answers = self.resolver.resolve(domain, 'TXT')
            spf_record = None

            for rdata in answers:
                for txt_string in rdata.strings:
                    txt_string = txt_string.decode('utf-8')
                    if txt_string.startswith('v=spf1'):
                        spf_record = txt_string
                        break

            if spf_record:
                if '-all' in spf_record or '~all' in spf_record:
                    if '-all' in spf_record:
                        return {
                            'status': 'pass',
                            'record': spf_record,
                            'details': 'Policy SPF rigorosa: rifiuta email non autorizzate'
                        }
                    else:
                        return {
                            'status': 'softfail',
                            'record': spf_record,
                            'details': 'Policy SPF softfail: accetta ma marca email non autorizzate'
                        }
                elif '?all' in spf_record or 'redirect=' in spf_record:
                    return {
                        'status': 'neutral',
                        'record': spf_record,
                        'details': 'Policy SPF neutra o redirect'
                    }
                else:
                    return {
                        'status': 'pass',
                        'record': spf_record,
                        'details': 'Record SPF presente'
                    }
            else:
                return {
                    'status': 'none',
                    'record': None,
                    'details': 'Nessun record SPF trovato'
                }

        except dns.exception.NXDOMAIN:
            return {
                'status': 'error',
                'record': None,
                'details': 'Dominio inesistente'
            }
        except dns.exception.Timeout:
            return {
                'status': 'error',
                'record': None,
                'details': 'Timeout DNS'
            }
        except Exception as e:
            return {
                'status': 'error',
                'record': None,
                'details': f'Errore: {str(e)}'
            }

    def check_dmarc(self, domain: str) -> Dict[str, any]:
        """
        Verifica il record DMARC (Domain-based Message Authentication)

        DMARC indica come gestire le email che falliscono SPF o DKIM

        Args:
            domain: Il dominio da verificare

        Returns:
            Dict con: status (pass/quarantine/reject/none), policy, record
        """
        dmarc_domain = f'_dmarc.{domain}'

        try:
            answers = self.resolver.resolve(dmarc_domain, 'TXT')

            for rdata in answers:
                for txt_string in rdata.strings:
                    txt_string = txt_string.decode('utf-8')
                    if txt_string.startswith('v=DMARC1'):
                        # Estrai la policy
                        policy = 'none'
                        if 'p=reject' in txt_string:
                            policy = 'reject'
                        elif 'p=quarantine' in txt_string:
                            policy = 'quarantine'
                        elif 'p=none' in txt_string:
                            policy = 'none'

                        # Estrai subpolicy se presente
                        sp = 'none'
                        if 'sp=reject' in txt_string:
                            sp = 'reject'
                        elif 'sp=quarantine' in txt_string:
                            sp = 'quarantine'
                        elif 'sp=none' in txt_string:
                            sp = 'none'

                        pct = 100
                        if 'pct=' in txt_string:
                            try:
                                pct_start = txt_string.index('pct=') + 4
                                pct_end = txt_string.find(';', pct_start)
                                if pct_end == -1:
                                    pct_end = len(txt_string)
                                pct = int(txt_string[pct_start:pct_end])
                            except:
                                pass

                        return {
                            'status': 'found',
                            'policy': policy,
                            'subpolicy': sp,
                            'pct': pct,
                            'record': txt_string,
                            'details': f'Policy DMARC: {policy} (applicata al {pct}%)'
                        }

            return {
                'status': 'none',
                'policy': None,
                'record': None,
                'details': 'Nessun record DMARC trovato'
            }

        except dns.exception.NXDOMAIN:
            return {
                'status': 'none',
                'policy': None,
                'record': None,
                'details': 'Nessun record DMARC (dominio inesistente o non configurato)'
            }
        except dns.exception.Timeout:
            return {
                'status': 'error',
                'policy': None,
                'record': None,
                'details': 'Timeout DNS'
            }
        except Exception as e:
            return {
                'status': 'error',
                'policy': None,
                'record': None,
                'details': f'Errore: {str(e)}'
            }

    def get_mx_records(self, domain: str) -> List[Dict[str, str]]:
        """
        Recupera i record MX (Mail Exchange) di un dominio

        Args:
            domain: Il dominio da interrogare

        Returns:
            Lista di dict con: preference, exchange
        """
        try:
            answers = self.resolver.resolve(domain, 'MX')
            mx_records = []

            for rdata in answers:
                mx_records.append({
                    'preference': rdata.preference,
                    'exchange': str(rdata.exchange).rstrip('.')
                })

            return mx_records

        except Exception as e:
            return []

    def get_a_records(self, domain: str) -> List[str]:
        """
        Recupera i record A (indirizzi IP) di un dominio

        Args:
            domain: Il dominio da interrogare

        Returns:
            Lista di indirizzi IP
        """
        try:
            answers = self.resolver.resolve(domain, 'A')
            return [str(rdata) for rdata in answers]
        except Exception as e:
            return []

    def check_domain_exists(self, domain: str) -> bool:
        """
        Verifica se un dominio esiste

        Args:
            domain: Il dominio da verificare

        Returns:
            True se il dominio esiste, False altrimenti
        """
        try:
            self.resolver.resolve(domain, 'A')
            return True
        except dns.exception.NXDOMAIN:
            return False
        except:
            # Il dominio potrebbe esistere ma non avere record A
            try:
                self.resolver.resolve(domain, 'MX')
                return True
            except:
                return False

    def reverse_dns(self, ip_address: str) -> Optional[str]:
        """
        Esegue un lookup DNS inverso (PTR record)

        Args:
            ip_address: L'indirizzo IP da interrogare

        Returns:
            Il nome host associato o None
        """
        try:
            reverse_name = dns.reversename.from_address(ip_address)
            answers = self.resolver.resolve(reverse_name, 'PTR')
            return str(answers[0]).rstrip('.')
        except Exception:
            return None


def explain_spf():
    """
    Spiega cos'è l'SPF in modo educativo
    """
    explanation = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║              SPF - Sender Policy Framework                       ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                   ║
    ║  COS'È SPF?                                                       ║
    ║  SPF è un protocollo di autenticazione email che permette ai     ║
    ║  proprietari di dominio di specificare quali server sono         ║
    ║  autorizzati a inviare email per il loro dominio.                ║
    ║                                                                   ║
    ║  COME FUNZIONA:                                                  ║
    ║  1. Il proprietario del dominio pubblica un record SPF nel DNS   ║
    ║  2. Il server di ricezione controlla il record SPF              ║
    ║  3. Se l'IP del mittente è autorizzato → SPF passa              ║
    ║  4. Se l'IP NON è autorizzato → SPF fallisce                    ║
    ║                                                                   ║
    ║  ESEMPIO RECORD SPF:                                             ║
    ║  v=spf1 ip4:192.0.2.0/24 include:_spf.google.com -all            ║
    ║                                                                   ║
    ║  RISULTATI POSSIBILI:                                            ║
    ║  • pass: L'IP è autorizzato (✓ sicuro)                          ║
    ║  • fail: L'IP NON è autorizzato (✗ phishing probabile)          ║
    ║  • softfail: L'IP potrebbe non essere autorizzato (⚠ sospetto)   ║
    ║  • none: Nessun record SPF configurato                          ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    return explanation


def explain_dmarc():
    """
    Spiega cos'è DMARC in modo educativo
    """
    explanation = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║              DMARC - Domain-based Message Authentication          ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                   ║
    ║  COS'È DMARC?                                                    ║
    ║  DMARC è un protocollo che collega SPF e DKIM, indicando ai     ║
    ║  server di ricezione COME gestire le email che falliscono la     ║
    ║  verifica di autenticazione.                                    ║
    ║                                                                   ║
    ║  COME FUNZIONA:                                                  ║
    ║  1. Il mittente pubblica una policy DMARC nel DNS                ║
    ║  2. Il server riceve l'email e verifica SPF e DKIM              ║
    ║  3. Se entrambi passano → Email consegnata                       ║
    ║  4. Se falliscono → Applica la policy DMARC                     ║
    ║                                                                   ║
    ║  LE POLICY DMARC:                                                ║
    ║  • p=none: Monitoraggio, nessuna azione (policy debole)         ║
    ║  • p=quarantine: Metti in spam/carantina (policy media)         ║
    ║  • p=reject: Rifiuta completamente (policy forte) ✓              ║
    ║                                                                   ║
    ║  ESEMPIO RECORD DMARC:                                           ║
    ║  v=DMARC1; p=quarantine; rua=mailto:dmarc@esempio.com           ║
    ║                                                                   ║
    ║  PERCHÉ È IMPORTANTE:                                           ║
    ║  DMARC previene lo spoofing del dominio e protegge dalla        ║
    ║  contraffazione delle email. I domini senza DMARC sono più      ║
    ║  vulnerabili al phishing.                                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    return explanation


def explain_dkim():
    """
    Spiega cos'è DKIM in modo educativo
    """
    explanation = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║        DKIM - DomainKeys Identified Mail                         ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                   ║
    ║  COS'È DKIM?                                                     ║
    ║  DKIM è un metodo di autenticazione email che utilizza la        ║
    ║  crittografia a chiave pubblica per firmare digitalmente le     ║
    ║  email. Garantisce che il messaggio non sia stato modificato.    ║
    ║                                                                   ║
    ║  COME FUNZIONA:                                                  ║
    ║  1. Il server mittente firma l'email con una chiave privata     ║
    ║  2. La firma viene inserita nell'header della email             ║
    ║  3. Il server ricevente verifica la firma con la chiave pubblica║
    ║  4. Se la firma è valida → Email autentica e integra            ║
    ║                                                                   ║
    ║  VANTAGGI DI DKIM:                                               ║
    ║  ✓ Garantisce l'integrità del messaggio (non modificato)        ║
    ║  ✓ Verifica l'autenticità del mittente                          ║
    ║  ✓ Previene la manomissione delle email in transito             ║
    ║                                                                   ║
    ║  RISULTATI POSSIBILI:                                            ║
    ║  • pass: Firma valida, email autentica ✓                        ║
    ║  • fail: Firma non valida, email modificata o falsa ✗           ║
    ║  • none: Nessuna firma presente (indeterminato)                  ║
    ║                                                                   ║
    ║  ESEMPIO HEADER DKIM:                                            ║
    ║  DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;          ║
    ║    d=esempio.com; s=selector1; h=from:to:subject; bh=...; b=... ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    return explanation
