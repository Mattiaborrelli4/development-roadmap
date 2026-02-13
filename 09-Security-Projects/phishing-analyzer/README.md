# 🎣 Phishing Email Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Educational](https://img.shields.io/badge/license-Educational%20Use-green.svg)](LICENSE)

> ⚠️ **IMPORTANTE:** Questo strumento è creato **esclusivamente a scopo EDUCATIVO e DIFENSIVO** per aiutare a identificare e comprendere le email di phishing.

## 📋 Indice

- [Cos'è](#cosè)
- [Disclaimer Legale](#disclaimer-legale)
- [Funzionalità](#funzionalità)
- [Come Funziona il Phishing](#come-funziona-il-phishing)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Esempi](#esemmpi)
- [Segnalare Phishing](#segnalare-phishing)
- [Best Practices](#best-practices)

## 🎯 Cos'è

**Phishing Email Analyzer** è uno strumento educativo e difensivo che analizza le email per identificare potenziali tentativi di phishing. Fornisce:

- ✅ Analisi degli header di sicurezza (SPF, DKIM, DMARC)
- ✅ Ispezione dei link per URL sospetti
- ✅ Verifica del mittente per individuare lo spoofing
- ✅ Analisi del contenuto per tattiche di manipolazione
- ✅ Calcolo del punteggio di rischio
- ✅ Spiegazioni educative per ogni indicatore

## ⚖️ Disclaimer Legale

**QUESTO STRUMENTO È DESTINATO ESCLUSIVAMENTE A SCOPO EDUCATIVO E DIFENSIVO.**

L'obiettivo è insegnare a:
- ✓ Identificare le email di phishing
- ✓ Comprendere le tecniche di attacco
- ✓ Proteggersi dalle minacce email
- ✓ Migliorare la consapevolezza della sicurezza

**NON UTILIZZARE per:**
- ✗ Inviare email di phishing
- ✗ Testare senza autorizzazione
- ✗ Qualsiasi attività illegale

**L'autore non è responsabile dell'uso improprio di questo strumento.**

## 🚀 Funzionalità

### 1. Analisi Header di Sicurezza

```
📧 SPF (Sender Policy Framework)
   Verifica se il server è autorizzato a inviare email per il dominio

🔐 DKIM (DomainKeys Identified Mail)
   Verifica la firma digitale e l'integrità del messaggio

🛡️ DMARC (Domain-based Message Authentication)
   Indica la policy del dominio per gestire le email non autenticate
```

### 2. Analisi dei Link

```
🔗 Rileva:
   • URL con refusi (typosquatting)
   • Uso di indirizzi IP
   • TLD sospette (.xyz, .top, .zip)
   • Link non sicuri (HTTP)
   • URL accorciati
   • Caratteri "lookalike"
```

### 3. Verifica del Mittente

```
👤 Controlla:
   • Spoofing di marchi noti
   • Mismatch nome/email
   • Differenza From/Reply-To
   • Domini di email gratuiti
   • Typosquatting del dominio
```

### 4. Analisi del Contenuto

```
📄 Identifica:
   • Tattiche di urgenza
   • Pressione psicologica
   • Richieste di credenziali
   • Contenuti finanziari
   • Allegati pericolosi
```

### 5. Calcolo del Rischio

```
⚠️ Punteggio complessivo:
   🔴 CRITICO (70%+)  - Phishing molto probabile
   🟠 ALTO (50-70%)   - Alta probabilità di phishing
   🟡 MEDIO (30-50%)  - Alcuni elementi sospetti
   🟢 BASSO (15-30%)  - Probabilmente sicuro
   ✅ MOLTO BASSO (<15%) - Sicuro
```

## 🎓 Come Funziona il Phishing

### Cos'è il Phishing?

Il **phishing** è un tipo di attacco di ingegneria sociale in cui i criminali si spacciano per entità affidabili (banche, aziende, servizi) per rubare informazioni sensibili.

### Il Modus Operandi

1. **Preparazione**: L'attaccante crea una email fraudolenta che imita un'azienda nota
2. **Innescazione**: Invia migliaia di email a potenziali vittime
3. **Inganno**: La email crea urgenza, preoccupazione o curiosità
4. **Azione**: Chiede di cliccare un link o aprire un allegato
5. **Compromissione**:
   - Il link porta a un sito falso che ruba le credenziali
   - L'allegato installa malware sul computer
6. **Sfruttamento**: Usa le credenziali rubate per accedere agli account

### Tecniche Comuni

| Tecnica | Descrizione | Esempio |
|---------|-------------|---------|
| **Urgenza** | Crea bisogno di agire subito | "Entro 24 ore o il conto verrà chiuso" |
| **Authority** | Si spaccia per autorità | "Amministrazione Sistema" |
| **Intimità** | Usa informazioni personali | "Gentile Mario,..." |
| **Minaccia** | Fa paventare conseguenze | "Il tuo account verrà bloccato" |
| **Premio** | Promette benefici | "Hai vinto un premio!" |

## 📦 Installazione

### Requisiti

- Python 3.10 o superiore
- pip (gestore pacchetti Python)

### Passaggi

1. **Clona o scarica il repository**
```bash
cd phishing-analyzer
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Verifica l'installazione**
```bash
python main.py --version
```

## 💻 Utilizzo

### Analizzare una Email

```bash
# Analizza un file .eml
python main.py analyze email_phishing.eml

# Leggi da stdin
cat email.eml | python main.py analyze --stdin
```

### Controllare URL

```bash
# Controlla uno o più URL
python main.py check-links https://suspicious.com https://example.xyz
```

### Verificare un Dominio

```bash
# Controlla la configurazione DNS
python main.py check-domain paypal.com
```

### Informazioni Educative

```bash
# Spiega SPF
python main.py explain-spf

# Spiega DMARC
python main.py explain-dmarc

# Spiega DKIM
python main.py explain-dkim

# Guida completa
python main.py learn
```

## 📚 Esempi

### Esempio 1: Email di Phishing PayPal

**Oggetto:** URGENTE: Il tuo account verrà chiuso!

**Mittente:** "PayPal Security" <security@paypa1.com>

**Contenuto:**
```
Gentile utente,

Il tuo account PayPal verrà chiuso entro 24 ore.
Conferma la tua password cliccando qui:

http://paypa1.com/verify

Urgente!
PayPal Security Team
```

**Risultato dell'Analisi:**
```
🔴 LIVELLO DI RISCHIO: CRITICO (85/100)

❌ SPF: Non configurato
❌ DKIM: Assente
❌ DMARC: Non configurato
🔴 Mittente: Dominio con refuso (paypa1.com)
🔴 Link: URL sospetto (typosquatting)
🔴 Contenuto: Richiesta credenziali + urgenza

⚠️  CONSIGLIO: Questa è sicuramente phishing!
```

### Esempio 2: Email Legittima

**Oggetto:** Conferma ordine #12345

**Mittente:** "Amazon" <confirm-order@amazon.com>

**Contenuto:**
```
Gentile cliente,

Il tuo ordine #12345 è stato confermato.
Puoi tracciare la spedizione dal tuo account Amazon.

Grazie per aver scelto Amazon.
```

**Risultato dell'Analisi:**
```
✅ LIVELLO DI RISCHIO: MOLTO BASSO (5/100)

✅ SPF: Pass
✅ DKIM: Valido
✅ DMARC: Policy reject
✅ Mittente: Dominio legittimo
✅ Link: Nessun link sospetto
✅ Contenuto: Nessun indicatore di phishing

✅ CONSIGLIO: Email probabilemente sicura
```

## 🚨 Segnalare Phishing

### Come Segnale

**Gmail:**
1. Apri la email
2. Clicca sui tre punti (⋮) in alto a destra
3. Seleziona "Segnala come phishing"

**Outlook:**
1. Seleziona la email
2. Vai su "Messaggio Junk" → "Phishing" → "Segnala"

**Poste Italiane:**
1. Inoltra la email a `ante@poste.it`

**Banche:**
1. Usa il servizio di segnalazione della tua banca
2. Chiama il numero verde della banca

### A chi Segnalare

| Servizio | Contatto |
|----------|----------|
| **Poste Italiane** | ante@poste.it |
| **Banca d'Italia** | phishing@bancaditalia.it |
| **CERT Italia** | info@cert.it |
| **Google** | https://support.google.com |
| **Microsoft** | https://support.microsoft.com |

## 🛡️ Best Practices per la Sicurezza Email

### Regole d'Oro

1. **✅ Verifica SEMPRE il mittente**
   - Controlla l'indirizzo email completo
   - Non fidarti solo del nome visualizzato
   - Diffida di domini strani o simili

2. **✅ Controlla i link PRIMA di cliccare**
   - Passa il mouse sopra il link
   - Verifica l'URL reale
   - Non cliccare se in dubbio

3. **✅ MAI fornire password via email**
   - Le aziende serie NON chiedono MAI la password
   - Se te la chiedono → È phishing

4. **✅ Diffida dell'urgenza**
   - "Entro 24 ore" → Sospetto
   - "Azione immediata" → Sospetto
   - Prenditi sempre tempo per verificare

5. **✅ Verifica con canali ufficiali**
   - Contatta l'azienda dal sito ufficiale
   - Usa il numero di telefono ufficiale
   - Non usare i contatti nella email sospetta

### Protezione Tecnica

- ✅ **Attiva 2FA** (autenticazione a due fattori)
- ✅ **Usa un password manager**
- ✅ **Mantieni il software aggiornato**
- ✅ **Usa un antivirus**
- ✅ **Attiva i filtri antispam**
- ✅ **Configura SPF/DKIM/DMARC** (se hai un dominio)

### Password Sicure

```
❌ sbagliata: password123
❌ sbagliata: mario1990
❌ sbagliata: 123456789

✅ giusta: Tr&7bP9x$mL2q
✅ giusta: Horse-Battery-Staple-Correct
✅ giusta: Usa un password manager!
```

## 📖 Risorse Educative

### Corsi Gratuiti

- [Google - Safety Center](https://www.google.com/safetycenter/)
- [Microsoft - Security](https://www.microsoft.com/security/)
- [Kaspersky - Courses](https://www.kaspersky.com/resources)

### Tool Utili

- [VirusTotal](https://www.virustotal.com/) - Scansione file/URL
- [URLhaus](https://urlhaus.abuse.ch/) - Database URL malevoli
- [PhishTank](https://www.phishtank.com/) - Database phishing

## 🤝 Contribuire

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti!

## 📄 Licenza

Questo strumento è rilasciato per uso **EDUCATIVO**.

---

**Ricorda:** La migliore difesa contro il phishing è la consapevolezza. 🛡️

**⚠️ Se hai dubbi su una email, non cliccare nulla! Contatta il mittente tramite canali ufficiali.**

---

*Creato a scopo educativo per insegnare la sicurezza email.*
