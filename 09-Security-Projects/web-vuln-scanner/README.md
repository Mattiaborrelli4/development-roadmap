# 🔒 Web Vulnerability Scanner

> **Strumento Educativo per la Sicurezza Web - Scansione di Vulnerabilità**

⚠️ **IMPORTANTE:** Questo strumento è stato creato **ESCLUSIVAMENTE per scopi EDUCATIVI e DIFENSIVI.

## 📋 Indice

- [⚠️ DISCLAIMER LEGALE](#-disclaimer-legale)
- [🎯 Obiettivo del Progetto](#-obiettivo-del-progetto)
- [🌟 Caratteristiche](#-caratteristiche)
- [📚 OWASP Top 10](#-owasp-top-10)
- [🚀 Installazione](#-installazione)
- [📖 Utilizzo](#-utilizzo)
- [🛡️ Pratiche di Scansione Sicura](#️-pratiche-di-scansione-sicura)
- [🐛 Come Risolvere le Vulnerabilità](#-come-risolvere-le-vulnerabilità)
- [📊 Report](#-report)
- [🧪 Testing](#-testing)
- [👨‍💻 Struttura del Progetto](#-struttura-del-progetto)

---

## ⚠️ DISCLAIMER LEGALE

**CONDIZIONI DI UTILIZSO - LEGGERE ATTENTAMENTE**

Questo strumento è fornito **SOLO per scopi educativi e difensivi**. Utilizzando questo software, accetti quanto segue:

### ✅ COSA PUOI FARE:

1. **Scansionare le TUE applicazioni** che possiedi o che gestisci
2. **Scansionare applicazioni** con which hai **ESPLICITO PERMESSO SCRITTO** dal proprietario
3. **Utilizzare in ambienti di laboratorio isolati** per scopi educativi
4. **Apprendere** la sicurezza web e migliorare le competenze defensive

### ❌ COSA NON PUOI FARE:

1. **MAI** scansionare sistemi senza autorizzazione esplicita
2. **MAI** utilizzare questo strumento per scopi malevoli
3. **MAI** condividere risultati non autorizzati pubblicamente
4. **MAI** tentare di bypassare controlli di sicurezza senza permesso

### ⚖️ CONSEGUENZE LEGALI

Il test di penetrazione non autorizzato è **ILLEGALE** in molte giurisdizioni e può comportare:
- Accuse criminali (accesso non autorizzato a computer)
- Sanzioni civili
- Espulsione dall'università (per studenti)
- Licenziamento (per professionisti)

**SEI IL SOLO RESPONSABILE dell'uso di questo strumento.** Gli autori non sono responsabili per qualsiasi uso improprio.

### ✅ PRIMA DI SCANSIONARE

Devi avere:
- [ ] Proprietà dell'applicazione target, OPPURE
- [ ] Documentazione di permesso scritto firmata dal proprietario
- [ ] Comprensione delle leggi locali
- [ ] Intenzione di utilizzare i risultati per migliorare la sicurezza

---

## 🎯 Obiettivo del Progetto

Questo Web Vulnerability Scanner è un progetto educativo che aiuta:

1. **Sviluppatori** a identificare vulnerabilità nelle proprie applicazioni
2. **Studenti** a imparare l'OWASP Top 10 e la sicurezza web
3. **Professionisti della sicurezza** a effettuare test difensivi
4. **Team IT** a migliorare il posture di sicurezza delle proprie applicazioni

### Perché Creare Questo Scanner?

- 📚 **Apprendimento Pratico:** Impara la sicurezza web facendola
- 🔍 **Identificazione Proattiva:** Trova vulnerabilità prima degli aggressori
- 🛡️ **Miglioramento Continuo:** Testa regolarmente la tua sicurezza
- 💰 **Risparmio di Tempo:** Automatizza i test di sicurezza di base

---

## 🌟 Caratteristiche

### Scansioni di Vulnerabilità

- **SQL Injection (SQLi)** - Rileva injection SQL in forms e URL
- **Cross-Site Scripting (XSS)** - Identifica XSS riflesso e DOM-based
- **Autenticazione Debole** - Testa credenziali default e weak
- **Configurazioni Errate** - Trova file esposti e header mancanti
- **Information Disclosure** - Identifica leak di informazioni

### Funzionalità Principali

- ✅ **Crawling Intelligente** - Scopre automaticamente pagine e form
- ✅ **Testing Sicuro** - Payload non distruttivi e read-only
- ✅ **Rate Limiting** - Rispetta il server con pause tra richieste
- ✅ **Report Dettagliati** - Genera report HTML e PDF professionali
- ✅ **Consigli di Fix** - Fornisce raccomandazioni per ogni vulnerabilità
- ✅ **Controllo Permessi** - Verifica autorizzazione prima di scansionare

---

## 📚 OWASP Top 10

Lo scanner si concentra sui top 10 rischi di sicurezza secondo OWASP:

| Rank | Rischio | Descrizione | Scansioni |
|------|---------|-------------|-----------|
| 1 | **Broken Access Control** | Accesso non autorizzato a risorse | ✅ |
| 2 | **Cryptographic Failures** | Dati sensibili non criptati | ✅ |
| 3 | **Injection** | SQL, NoSQL, OS injection | ✅ |
| 4 | **Insecure Design** | Flaw di architettura | ⚠️ |
| 5 | **Security Misconfiguration** | Configurazioni di default | ✅ |
| 6 | **Vulnerable Components** | Librerie obsolete | ⚠️ |
| 7 | **Auth Failures** | Autenticazione debole | ✅ |
| 8 | **Integrity Failures** | CI/CD, API integrity | ⚠️ |
| 9 | **Logging Failures** | Log insufficienti | ⚠️ |
| 10 | **SSRF** | Server-Side Request Forgery | ⚠️ |

Legenda: ✅ = Scansionato, ⚠️ = Parziale

---

## 🚀 Installazione

### Requisiti

- Python 3.10 o superiore
- Windows, macOS, o Linux
- Connessione internet

### Passo 1: Clona il Progetto

```bash
cd "Project Ideas Portfolio/09-Security-Projects"
cd web-vuln-scanner
```

### Passo 2: Crea Ambiente Virtuale

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Installa Dipendenze

```bash
pip install -r requirements.txt
```

### Passo 4: Verifica Installazione

```bash
python main.py --help
```

Dovresti vedere l'help del comando.

---

## 📖 Utilizzo

### Mostra Disclaimer

```bash
python main.py disclaimer
```

Leggi attentamente il disclaimer prima di utilizzare lo scanner.

### Scansione Base

```bash
python main.py scan https://localhost:8000
```

### Scansione con File di Permesso

Crea un file `permission.txt`:

```
I, Mario Rossi, ho esplicito permesso di scansionare:
Target: https://myapp.local
Owner: La Mia Company
Date: 2024-01-15
Signature: _________________
```

Esegui la scansione:

```bash
python main.py scan https://myapp.local --permission-file permission.txt
```

### Scansione con Report Personalizzato

```bash
# Report HTML (default)
python main.py scan https://myapp.local --report mio_report.html

# Report PDF
python main.py scan https://myapp.local --report report.pdf --format pdf

# Report JSON
python main.py scan https://myapp.local --report data.json --format json
```

### Scansione Selettiva

Scansiona solo vulnerabilità specifiche:

```bash
# Solo SQL Injection e XSS
python main.py scan https://myapp.local --checks sqli,xss

# Solo Autenticazione
python main.py scan https://myapp.local --checks auth

# Solo Configurazione
python main.py scan https://myapp.local --checks config
```

### Quick Scan

Scansione veloce (max 20 pagine, solo SQLi e XSS):

```bash
python main.py quick https://myapp.local
```

### Opzioni Complete

```bash
python main.py scan [TARGET] [OPTIONS]

Opzioni:
  -p, --permission-file PATH  File di permesso
  -r, --report PATH           File di output (default: report.html)
  -f, --format [html|pdf|json] Formato report (default: html)
  -c, --checks TEXT           Check separati da virgola (sqli,xss,auth,config)
  -m, --max-pages INT         Max pagine da crawlare (default: 50)
  --no-permission-check       Salta controllo permesso (NON RACCOMANDATO)
```

---

## 🛡️ Pratiche di Scansione Sicura

### 1. Rate Limiting

Lo scanner include **rate limiting automatico**:

- ✅ 0.2 secondi tra richieste
- ✅ Massimo 5 richieste/secondo
- ✅ Timeout 30 secondi
- ✅ Rispetto di robots.txt

### 2. Payload Sicuri

Tutti i payload sono **NON distruttivi**:

- ✅ Solo SELECT statements (no DELETE/DROP)
- ✅ Read-only operations
- ✅ Nessuna modifica dei dati
- ✅ Nessun danno al sistema

### 3. Test in Sicurezza

**Mai scansionare in produzione senza:**

1. Backup completi
2. Permessi scritti
3. Piano di rollback
4. Monitoraggio attivo

### 4. Ambiente di Test Consigliato

```bash
# Utilizza Docker per un ambiente di test isolato
docker run -d -p 8080:80 vulnerables/web-dvwa
# Scansiona: http://localhost:8080
```

---

## 🐛 Come Risolvere le Vulnerabilità

### SQL Injection

**Problema:**
```python
# VULNERABILE
query = f"SELECT * FROM users WHERE username='{user_input}'"
```

**Soluzione:**
```python
# SICURO - Parameterized Query
query = "SELECT * FROM users WHERE username=?"
cursor.execute(query, (user_input,))
```

**Framework che aiutano:**
- SQLAlchemy, Django ORM, Hibernate

### XSS (Cross-Site Scripting)

**Problema:**
```python
# VULNERABILE
return f"<div>{user_input}</div>"
```

**Soluzione:**
```python
# SICURO - Output Encoding
import html
return f"<div>{html.escape(user_input)}</div>"
```

**Header di sicurezza:**
```
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 1; mode=block
```

### Autenticazione Debole

**Soluzioni:**
- ✅ Implementa password complesse (min 12 caratteri)
- ✅ Usa bcrypt/argon2 per hashing
- ✅ Implementa rate limiting (max 5 tentativi)
- ✅ Usa 2FA/MFA dove possibile

```python
import bcrypt

# Hash password
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verifica
if bcrypt.checkpw(password.encode(), hashed):
    # Login OK
```

### Missing Security Headers

**Header essenziali:**
```nginx
# Nginx
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header Strict-Transport-Security "max-age=31536000";
add_header Content-Security-Policy "default-src 'self'";
```

```apache
# Apache
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set Strict-Transport-Security "max-age=31536000"
```

### Information Disclosure

**Soluzioni:**
- ✅ Disabilita errori verbosi in produzione
- ✅ Rimuovi versioni dai server headers
- ✅ Limita accessi a file sensibili (.git, .env)

```python
# Django
DEBUG = False  # Mai True in produzione!
ALLOWED_HOSTS = ['your-domain.com']

# Python generic
import logging
logging.disable(logging.CRITICAL)  # In produzione
```

---

## 📊 Report

Lo scanner genera report professionali con:

### Contenuti del Report

1. **Executive Summary**
   - Totale findings
   - Gravità (Critical, High, Medium, Low)
   - Statistiche per tipo

2. **Dettagli Findings**
   - Vulnerabilità identificata
   - URL specifico
   - Payload utilizzato
   - Evidence della risposta
   - Raccomandazioni specifiche

3. **Consigli di Fix**
   - Soluzioni tecniche
   - Code examples
   - Best practices
   - Riferimenti OWASP

### Esempio Report HTML

Il report include:
- 📊 Grafici e statistiche visive
- 🎨 Codifica colori per severità
- 📝 Sezioni dettagliate per ogni finding
- 📚 Link a risorse esterne
- ⚖️ Disclaimer legale

---

## 🧪 Testing

### Esegui i Test

```bash
pytest tests/ -v
```

### Test con Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Specifici

```bash
# Solo SQLi scanner
pytest tests/test_scanners.py::TestSQLiScanner -v

# Solo XSS scanner
pytest tests/test_scanners.py::TestXSSScanner -v
```

---

## 👨‍💻 Struttura del Progetto

```
web-vuln-scanner/
│
├── main.py                 # Entry point CLI
├── requirements.txt        # Dipendenze Python
├── README.md              # Questo file
│
├── config/
│   └── payloads.yaml      # Payload di test (SICURI)
│
├── scanners/              # Moduli di scansione
│   ├── crawler.py        # Crawler del sito
│   ├── sql_injection.py  # Scanner SQLi
│   ├── xss_scanner.py    # Scanner XSS
│   ├── auth_scanner.py   # Scanner Auth
│   └── config_scanner.py # Scanner Config
│
├── parsers/              # Parser per HTML
│   ├── form_parser.py    # Parser forms
│   └── link_parser.py    # Parser links
│
├── reporters/            # Generatori di report
│   └── report_generator.py  # HTML/PDF/JSON
│
└── tests/               # Unit tests
    └── test_scanners.py
```

### Componenti

**Scanners:**
- `crawler.py` - Scopre pagine e form
- `sql_injection.py` - Testa SQL injection
- `xss_scanner.py` - Testa XSS
- `auth_scanner.py` - Testa autenticazione
- `config_scanner.py` - Testa configurazioni

**Parsers:**
- `form_parser.py` - Analizza forms HTML
- `link_parser.py` - Analizza links e URL

**Reporters:**
- `report_generator.py` - Genera report multi-formato

---

## 🔧 Troubleshooting

### Errore: "Module not found"

```bash
pip install -r requirements.txt
```

### Errore: "Permission denied"

Verifica di avere il permesso di scansionare il target.

### Errore: "Connection timeout"

- Controlla che il target sia accessibile
- Aumenta il timeout con `--timeout`
- Verifica firewall/regole di rete

### Errore: "No forms found"

- Il sito potrebbe essere JavaScript-heavy
- Prova con Selenium (non ancora implementato)
- Verifica che il sito abbia forms

---

## 📚 Risorse Educative

### OWASP
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Corsi Gratuiti
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)

### Libri
- "The Web Application Hacker's Handbook"
- "Web Security for Developers"
- "Black Hat Python"

---

## 🤝 Contribuire

Questo è un progetto educativo. Contributi benvenuti:

1. Fork il progetto
2. Crea branch feature
3. Commit le modifiche
4. Push al branch
5. Apri Pull Request

**ATTENZIONE:** Non aggiungere payload distruttivi o malevoli.

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT per scopi educativi.

**IMPORTANTE:**
- L'uso è **SOLO per scopi educativi e difensivi**
- L'autore **NON è responsabile** per uso improprio
- L'utente è **unicamente responsabile** dell'utilizzo

---

## ⚠️ Avviso Finale

Questo strumento è potente e deve essere usato **responsabilmente**.

**Ricorda:**
- 🎓 **Apprendi** - Usa per imparare la sicurezza
- 🛡️ **Proteggi** - Usa per difendere le tue applicazioni
- ⚖️ **Rispetta** - Rispetta leggi e privacy altrui
- 🤝 **Disclosing** - Disclosing responsabile delle vulnerabilità

**Non essere un "script kiddie" - Sii un professionista della sicurezza.**

---

## 📧 Supporto

Per domande o problemi:
- 📖 Leggi la documentazione
- 🔍 Cerca nelle issue GitHub
- 💬 Chiedi nei forum di sicurezza (con responsabilità)

---

**Creato per scopi educativi. Usa saggiamente.** 🎓🔒
