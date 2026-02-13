# Web Vulnerability Scanner - Architettura

## 🏗️ Panoramica dell'Architettura

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                     (CLI - main.py)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Permission Check
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION VERIFIER                          │
│              (PermissionChecker class)                          │
│  - Verifica file di permesso                                     │
│  - Conferma interattiva                                          │
│  - Disclaimer legale                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Authorized
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WEB CRAWLER                                  │
│              (scanners/crawler.py)                              │
│  - Scopre pagine web                                             │
│  - Estrae forms                                                 │
│  - Estrae links                                                  │
│  - Rispetta robots.txt                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Pages + Forms
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PARSER LAYER                                 │
│                  (parsers/)                                      │
├─────────────────────────────────────────────────────────────────┤
│  Form Parser   │  Analizza forms HTML                            │
│  Link Parser   │  Analizza links e parametri                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Parsed Data
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VULNERABILITY SCANNERS                           │
│                 (scanners/)                                      │
├─────────────────────────────────────────────────────────────────┤
│  SQLi Scanner    │  Testa SQL Injection                         │
│  XSS Scanner     │  Testa Cross-Site Scripting                   │
│  Auth Scanner    │  Testa Autenticazione                         │
│  Config Scanner  │  Testa Configurazioni                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Findings
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ANALYZER LAYER                                 │
│              (scanner-specific)                                  │
├─────────────────────────────────────────────────────────────────┤
│  SQLi Analyzer    │  Classifica SQL Injection                    │
│  XSS Analyzer     │  Classifica XSS                              │
│  Parameter Analyzer│ Analizza parametri URL                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Analyzed Findings
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REPORT GENERATOR                                │
│              (reporters/)                                        │
├─────────────────────────────────────────────────────────────────┤
│  HTML Report  │  Report dettagliato HTML                         │
│  PDF Report   │  Report PDF professionale                       │
│  JSON Report  │  Dati strutturati JSON                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Final Report
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT                                      │
│           - report.html                                          │
│           - report.pdf                                           │
│           - findings.json                                        │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Componenti Principali

### 1. CLI Interface (main.py)

**Responsabilità:**
- Gestione comando linea
- Verifica permessi
- Configurazione scan
- Avvio processi

**Classi principali:**
- `WebVulnScanner`: Coordinatore principale
- `PermissionChecker`: Verifica autorizzazioni

### 2. Crawler (scanners/crawler.py)

**Responsabilità:**
- Scoprire pagine web
- Estrarre forms
- Estrarre links
- Gestire code di scansione

**Classi principali:**
- `WebCrawler`: Crawler asincrono
- `FormDiscovery`: Scopre forms

**Flusso:**
```
URL Iniziale
    ↓
Fetch HTML
    ↓
Parse HTML
    ↓
Estrai Links → Coda
Estrai Forms → Lista
    ↓
Prossimo URL
```

### 3. Parsers (parsers/)

#### Form Parser (form_parser.py)

**Responsabilità:**
- Analizzare forms HTML
- Identificare campi testabili
- Preparare dati per testing

**Metodi chiave:**
```python
parse_forms(html, url)        # Estrae forms
get_testable_fields(form)     # Campi da testare
prepare_form_data(form)       # Prepara dati test
analyze_form_security(form)   # Analizza sicurezza
```

#### Link Parser (link_parser.py)

**Responsabilità:**
- Analizzare links
- Estrarre parametri URL
- Trovare injection points

**Metodi chiave:**
```python
parse_links(html, url)           # Estrae links
find_injection_points(url)      # Trova punti injection
analyze_parameters(params)       # Analizza parametri
```

### 4. Vulnerability Scanners (scanners/)

#### SQL Injection Scanner (sql_injection.py)

**Flusso di Scansione:**
```
Per ogni form:
  1. Prepara payload SQLi
  2. Invia richiesta con payload
  3. Analizza risposta
  4. Cerca errori SQL
  5. Classifica vulnerability
```

**Payload Utilizzati:**
- Basic: `' OR '1'='1`, `" OR "1"="1`
- Boolean: `1' AND 1=1--`, `1' AND 1=2--`
- Time: `1' AND SLEEP(5)--`
- Union: `' UNION SELECT NULL--`

**Individuazione:**
- Error messages database
- Comportamenti anomali
- Timing responses

#### XSS Scanner (xss_scanner.py)

**Flusso di Scansione:**
```
Per ogni form:
  1. Prepara payload XSS
  2. Invia richiesta con payload
  3. Cerca reflection in risposta
  4. Verifica esecuzione
  5. Classifica tipo XSS
```

**Tipi di XSS:**
- Reflected: Payload riflesso immediatamente
- Stored: Payload salvato e eseguito dopo
- DOM-based: Payload eseguito via JavaScript

**Payload Utilizzati:**
- Script: `<script>alert('XSS')</script>`
- Event Handler: `<img src=x onerror=alert('XSS')>`
- Polyglot: Funziona in multipli contesti

#### Auth Scanner (auth_scanner.py)

**Test Effettuati:**
- Default/weak credentials
- Authentication bypass
- Session security
- Password security

**Controlli:**
- Cookie flags (Secure, HttpOnly)
- Password over HTTP
- Autocomplete passwords
- Rate limiting

#### Config Scanner (config_scanner.py)

**Test Effettuati:**
- Exposed sensitive files
- Missing security headers
- Default pages exposed
- Information disclosure
- Directory listing

**Headers Verificati:**
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- Content-Security-Policy
- X-XSS-Protection

### 5. Report Generator (reporters/)

**Template HTML Include:**
- Executive summary
- Findings per severità
- Evidence per vulnerability
- Raccomandazioni
- Disclaimer legale

**Statistiche Generate:**
```python
{
    'total': 15,
    'by_severity': {
        'Critical': 2,
        'High': 5,
        'Medium': 6,
        'Low': 2
    },
    'by_type': {
        'SQL Injection': 5,
        'XSS': 7,
        'Missing Header': 3
    }
}
```

## 🔒 Sicurezza nell'Architettura

### 1. Safe Mode
- Payload read-only
- Nessuna modifica dati
- Rate limiting obbligatorio
- Rispetto robots.txt

### 2. Permission System
- File di permesso obbligatorio
- Conferma interattiva
- Tracciamento autorizzazione
- Disclaimer legale

### 3. Error Handling
- Timeout gestiti
- Eccezioni catturate
- Graceful degradation
- Logging degli errori

## 📊 Flusso Dati

```
Input (URL)
    ↓
Permission Check
    ↓
Crawl (Pages + Forms)
    ↓
Parse (Extract Data)
    ↓
Test (Inject Payloads)
    ↓
Analyze (Classify Findings)
    ↓
Generate (Create Report)
    ↓
Output (HTML/PDF/JSON)
```

## 🔄 Async Architecture

Il crawler utilizza `asyncio` e `aiohttp` per:

- Richieste HTTP concorrenti
- Non-blocking I/O
- Performance migliorate
- Rate limiting efficiente

```python
async with aiohttp.ClientSession() as session:
    tasks = [scan_form(form, session) for form in forms]
    results = await asyncio.gather(*tasks)
```

## 🧪 Testing Architecture

```
tests/
├── test_scanners.py       # Unit tests per scanner
├── test_parsers.py        # Unit tests per parser
├── test_reporters.py      # Unit tests per reporter
└── test_integration.py    # Test integrazione
```

Ogni componente ha test dedicati per:
- Funzionalità core
- Edge cases
- Error handling
- Performance

## 🎯 Extensibility

L'architettura permette facile aggiunta di:

1. **Nuovi Scanner:**
   - Estendi `Scanner` base class
   - Implementa `scan()` method
   - Aggiungi a `main.py`

2. **Nuovi Parser:**
   - Crea in `parsers/`
   - Segui pattern esistente
   - Aggiungi a crawler

3. **Nuovi Report:**
   - Estendi `ReportGenerator`
   - Aggiungi template
   - Supporta nuovo formato

## 📝 Best Practices Implementate

1. **Separazione delle Responsabilità**
   - Ogni modulo ha uno scopo preciso
   - Interfacce chiare tra componenti
   - Accoppiamento ridotto

2. **Configuration Management**
   - File YAML centralizzato
   - Variabili ambiente supportate
   - Default sicuri

3. **Error Handling**
   - Eccezioni specifiche
   - Messaggi chiari
   - Recovery graceful

4. **Logging**
   - Livelli configurabili
   - Formato strutturato
   - Rotation automatica

5. **Testing**
   - Unit tests completi
   - Mocking dipendenze
   - Coverage report

---

Questa architettura modulare permette manutenzione, testing e estensione agevoli mentre mantiene la sicurezza e la responsabilità come priorità.
