"""
Calcolatore del rischio di phishing
Module per calcolare il punteggio di rischio complessivo
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class RiskFactor:
    """Fattore di rischio singolo"""
    name: str
    severity: str  # critical, high, medium, low, info
    score: int  # Contributo al punteggio totale
    description: str
    recommendation: str


class RiskCalculator:
    """
    Calcola il punteggio di rischio complessivo basato su tutti gli indicatori
    """

    def __init__(self):
        # Pesi per diverse categorie di controlli
        self.weights = {
            'spf': 20,
            'dkim': 15,
            'dmarc': 15,
            'sender_domain': 25,
            'links': 30,
            'content': 25,
            'urgency': 15,
            'attachments': 20,
        }

    def calculate_risk_score(self, analysis_results: Dict) -> Dict:
        """
        Calcola il punteggio di rischio complessivo

        Args:
            analysis_results: Risultati di tutti gli analyzer

        Returns:
            Dict con score, level, factors, recommendations
        """
        risk_factors = []
        total_score = 0
        max_score = 150  # Punteggio massimo possibile

        # Analisi SPF
        if 'spf' in analysis_results:
            spf_result = analysis_results['spf']
            if spf_result['status'] == 'fail':
                risk_factors.append(RiskFactor(
                    name='SPF Fallito',
                    severity='critical',
                    score=20,
                    description=spf_result.get('details', 'Server non autorizzato'),
                    recommendation='Il server che ha inviato questa email non è autorizzato dal dominio. È molto probabile che sia phishing.'
                ))
                total_score += 20
            elif spf_result['status'] == 'none':
                risk_factors.append(RiskFactor(
                    name='SPF Assente',
                    severity='medium',
                    score=10,
                    description='Il dominio non ha configurato SPF',
                    recommendation='Il dominio non ha protetto la sua reputazione con SPF. Sii cauto.'
                ))
                total_score += 10
            elif spf_result['status'] == 'softfail':
                risk_factors.append(RiskFactor(
                    name='SPF SoftFail',
                    severity='high',
                    score=15,
                    description='Server probabilmente non autorizzato',
                    recommendation='Il server potrebbe non essere autorizzato. Verifica attentamente.'
                ))
                total_score += 15

        # Analisi DKIM
        if 'dkim' in analysis_results:
            dkim_result = analysis_results['dkim']
            if dkim_result.get('valid') == False:
                risk_factors.append(RiskFactor(
                    name='DKIM Non Valido',
                    severity='critical',
                    score=15,
                    description='La firma digitale è invalida o la email è stata modificata',
                    recommendation='Questa email potrebbe essere stata modificata in transito o essere contraffatta.'
                ))
                total_score += 15
            elif dkim_result.get('valid') == None:
                risk_factors.append(RiskFactor(
                    name='DKIM Assente',
                    severity='low',
                    score=5,
                    description='La email non è firmata digitalmente',
                    recommendation='Senza firma DKIM non possiamo garantire l\'integrità del messaggio.'
                ))
                total_score += 5

        # Analisi DMARC
        if 'dmarc' in analysis_results:
            dmarc_result = analysis_results['dmarc']
            if dmarc_result['status'] == 'none':
                risk_factors.append(RiskFactor(
                    name='DMARC Assente',
                    severity='medium',
                    score=10,
                    description='Il dominio non ha configurato DMARC',
                    recommendation='Il dominio non ha una politica di autenticazione forte. Sii cauto.'
                ))
                total_score += 10
            elif dmarc_result.get('policy') == 'none':
                risk_factors.append(RiskFactor(
                    name='DMARC Debole',
                    severity='medium',
                    score=8,
                    description='Policy DMARC impostata su "none"',
                    recommendation='Il dominio non applica policy rigorose. Sii cauto.'
                ))
                total_score += 8

        # Analisi Sender
        if 'sender' in analysis_results:
            sender_result = analysis_results['sender']
            if sender_result.get('suspicious'):
                if sender_result.get('spoofed'):
                    risk_factors.append(RiskFactor(
                        name='Possibile Spoofing',
                        severity='critical',
                        score=25,
                        description='Il dominio del mittente sembra simulare un marchio noto',
                        recommendation='Attenzione! Questo dominio sembra imitare un\'azienda nota ma non è ufficiale.'
                    ))
                    total_score += 25
                elif sender_result.get('free_email'):
                    risk_factors.append(RiskFactor(
                        name='Email Gratuita',
                        severity='medium',
                        score=12,
                        description='Il mittente usa un servizio di email gratuito',
                        recommendation='Le aziende serie usano propri domini, non Gmail/Yahoo per comunicazioni ufficiali.'
                    ))
                    total_score += 12
                elif sender_result.get('display_name_mismatch'):
                    risk_factors.append(RiskFactor(
                        name='Nome Display Diverso',
                        severity='high',
                        score=15,
                        description='Il nome visualizzato non corrisponde all\'indirizzo email',
                        recommendation='Il nome mostrato può essere falsificato. Verifica l\'indirizzo email reale.'
                    ))
                    total_score += 15

        # Analisi Link
        if 'links' in analysis_results:
            links_result = analysis_results['links']
            suspicious_count = 0
            for link in links_result.get('analyzed_links', []):
                if link.get('suspicious', False):
                    suspicious_count += 1
                    if link.get('misspelled'):
                        risk_factors.append(RiskFactor(
                            name='Link con Refuso (Typosquatting)',
                            severity='critical',
                            score=20,
                            description=f'URL con refuso: {link.get("url", "")}',
                            recommendation='Questo link sembra simile a un sito noto ma ha un errore intenzionale per ingannarti.'
                        ))
                        total_score += 20
                    elif link.get('ip_address'):
                        risk_factors.append(RiskFactor(
                            name='URL con Indirizzo IP',
                            severity='critical',
                            score=20,
                            description=f'URL usa IP: {link.get("url", "")}',
                            recommendation='I siti legittimi usano nomi a dominio, non indirizzi IP.'
                        ))
                        total_score += 20
                    elif link.get('suspicious_tld'):
                        risk_factors.append(RiskFactor(
                            name='TLD Sospetto',
                            severity='high',
                            score=15,
                            description=f'URL con TLD sospetto: {link.get("url", "")}',
                            recommendation='Questo dominio usa un\'estensione sospetta spesso usata per phishing.'
                        ))
                        total_score += 15
                    elif not link.get('https', True):
                        risk_factors.append(RiskFactor(
                            name='Link Non Sicuro (HTTP)',
                            severity='high',
                            score=12,
                            description=f'URL senza HTTPS: {link.get("url", "")}',
                            recommendation='Questo link non usa una connessione sicura. I tuoi dati potrebbero essere intercettati.'
                        ))
                        total_score += 12
                    elif link.get('shortened'):
                        risk_factors.append(RiskFactor(
                            name='URL Accorciato',
                            severity='medium',
                            score=10,
                            description=f'URL accorciato: {link.get("url", "")}',
                            recommendation='Non puoi vedere la destinazione reale. Espandi l\'URL o evita di cliccare.'
                        ))
                        total_score += 10

            if links_result.get('has_suspicious_links'):
                risk_factors.append(RiskFactor(
                    name='Link Sospetti Presenti',
                    severity='high',
                    score=5,
                    description=f'Trovati {suspicious_count} link sospetti nella email',
                    recommendation='Non cliccare sui link. Verifica manualmente il sito web dell\'azienda.'
                ))
                total_score += 5

        # Analisi Contenuto
        if 'content' in analysis_results:
            content_result = analysis_results['content']

            if content_result.get('urgency_detected'):
                risk_factors.append(RiskFactor(
                    name='Tattiche di Urgenza',
                    severity='high',
                    score=15,
                    description='La email crea un falso senso di urgenza per spingerti ad agire',
                    recommendation='Questa è una tattica comune di phishing. Prenditi tempo per riflettere prima di agire.'
                ))
                total_score += 15

            if content_result.get('pressure_tactics'):
                risk_factors.append(RiskFactor(
                    name='Tattiche di Pressione',
                    severity='high',
                    score=12,
                    description='La email usa minacce o pressioni psicologiche',
                    recommendation='Le comunicazioni legittime non usano minacce o pressioni eccessive.'
                ))
                total_score += 12

            if content_result.get('credential_requests'):
                risk_factors.append(RiskFactor(
                    name='Richiesta Credenziali',
                    severity='critical',
                    score=25,
                    description='La email chiede password o credenziali di accesso',
                    recommendation='⚠ LE AZIENDE NON CHIEDONO MAI LA PASSWORD VIA EMAIL! Questa è sicuramente phishing.'
                ))
                total_score += 25

            if content_result.get('financial_keywords'):
                risk_factors.append(RiskFactor(
                    name='Contenuto Finanziario',
                    severity='medium',
                    score=10,
                    description='La email contiene riferimenti a pagamenti, bonifici o fatture',
                    recommendation='Verifica con l\'azienda tramite canali ufficiali prima di effettuare qualsiasi pagamento.'
                ))
                total_score += 10

        # Allegati
        if 'attachments' in analysis_results:
            attachments_result = analysis_results['attachments']
            if attachments_result.get('has_attachments'):
                if attachments_result.get('suspicious_extensions'):
                    risk_factors.append(RiskFactor(
                        name='Allegati Sospetti',
                        severity='critical',
                        score=20,
                        description='La email contiene allegati con estensioni pericolose',
                        recommendation='Non aprire mai allegati da fonti sospette. Potrebbero contenere malware.'
                    ))
                    total_score += 20
                else:
                    risk_factors.append(RiskFactor(
                        name='Allegati Presenti',
                        severity='low',
                        score=5,
                        description='La email contiene allegati',
                        recommendation='Verifica il contenuto degli allegati prima di aprirli. Scansiona con antivirus.'
                    ))
                    total_score += 5

        # Calcola livello di rischio
        risk_percentage = (total_score / max_score) * 100
        if risk_percentage >= 70:
            risk_level = 'CRITICO'
            risk_emoji = '🔴'
        elif risk_percentage >= 50:
            risk_level = 'ALTO'
            risk_emoji = '🟠'
        elif risk_percentage >= 30:
            risk_level = 'MEDIO'
            risk_emoji = '🟡'
        elif risk_percentage >= 15:
            risk_level = 'BASSO'
            risk_emoji = '🟢'
        else:
            risk_level = 'MOLTO BASSO'
            risk_emoji = '✅'

        return {
            'score': total_score,
            'max_score': max_score,
            'percentage': round(risk_percentage, 1),
            'level': risk_level,
            'emoji': risk_emoji,
            'factors': risk_factors,
            'recommendation': self._get_overall_recommendation(risk_level)
        }

    def _get_overall_recommendation(self, risk_level: str) -> str:
        """Restituisce una raccomandazione generale basata sul livello di rischio"""

        recommendations = {
            'CRITICO': """
⚠️  AZIONE RICHIESTA ⚠️

Questa email presenta molteplici indicatori di phishing:

1. NON cliccare su alcun link
2. NON scaricare o aprire allegati
3. NON rispondere alla email
4. NON fornire nessuna informazione personale
5. Segnala la email come spam/phishing
6. Elimina immediatamente la email

Se pensavi fosse legittima, contatta l'azienda tramite il loro sito web ufficiale o telefono.
            """,
            'ALTO': """
⚠️ ALTO RISCHIO DI PHISHING ⚠️

Questa email è molto sospetta e probabilmente phishing:

1. Evita di cliccare sui link
2. Non fornire informazioni personali
3. Verifica con il mittente tramite canali ufficiali
4. Considera di segnalarla come spam

Raccomandazione: Elimina questa email e contatta l'azienda direttamente se necessario.
            """,
            'MEDIO': """
⚠️ RISCHIO MEDIO ⚠️

Questa email presenta alcuni elementi sospetti:

1. Verifica attentamente il mittente
2. Non cliccare sui link se non sei sicuro
3. Controlla l'URL reale dei link (passa il mouse sopra)
4. Se hai dubbi, contatta l'azienda tramite il sito ufficiale

Raccomandazione: Procedi con cautela e verifica l'autenticità.
            """,
            'BASSO': """
✅ RISCHIO BASSO

Questa email sembra essere legittima, ma mantieni sempre la guardia alta:

1. Il mittente sembra autentico
2. I controlli di sicurezza sono passati
3. Tuttavia, verifica sempre i contenuti sensibili

Raccomandazione: Probabilmente sicura, ma rimani vigile.
            """,
            'MOLTO BASSO': """
✅ RISCHIO MOLTO BASSO

Questa email presenta pochissimi indicatori di phishing:

1. I controlli di sicurezza sono positivi
2. Nessun elemento sospetto significativo
3. Probabile email legittima

Raccomandazione: Sembra sicura, ma mantieni sempre buone pratiche di sicurezza.
            """
        }

        return recommendations.get(risk_level, recommendations['MEDIO'])


def format_risk_report(risk_result: Dict) -> str:
    """Formatta il report del rischio per la visualizzazione CLI"""

    report = f"""
╔══════════════════════════════════════════════════════════════╗
║           REPORT DEL RISCHIO DI PHISHING                     ║
╠══════════════════════════════════════════════════════════════╣
║  Livello di Rischio: {risk_result['level']:<15} {risk_result['emoji']:>4}      ║
║  Punteggio: {risk_result['score']}/{risk_result['max_score']} ({risk_result['percentage']}%)                   ║
╚══════════════════════════════════════════════════════════════╝
"""

    if risk_result['factors']:
        report += "\n🔍 FATTORI DI RISCHIO INDIVIDUALI:\n"
        report += "─" * 60 + "\n"

        # Raggruppa per severità
        critical = [f for f in risk_result['factors'] if f.severity == 'critical']
        high = [f for f in risk_result['factors'] if f.severity == 'high']
        medium = [f for f in risk_result['factors'] if f.severity == 'medium']
        low = [f for f in risk_result['factors'] if f.severity == 'low']

        for factor in critical + high + medium + low:
            emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢',
                'info': 'ℹ️'
            }.get(factor.severity, '⚪')

            report += f"\n{emoji} {factor.name} [{factor.severity.upper()}] (+{factor.score})\n"
            report += f"   {factor.description}\n"
            report += f"   💡 {factor.recommendation}\n"

    report += f"\n{risk_result['recommendation']}\n"

    return report
