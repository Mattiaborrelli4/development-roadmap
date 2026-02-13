# 📊 Web Vulnerability Scanner - Panoramica Progetto

## 🎯 Cos'è

Un tool di sicurezza web **educativo e difensivo** che scansiona applicazioni web alla ricerca di vulnerabilità comuni (OWASP Top 10).

**⚠️ SOLO per uso educativo e con permesso esplicito!**

---

## 📁 Struttura Progetto

```
web-vuln-scanner/
│
├── 📄 README.md                 # Documentazione principale (Italiano)
├── 📄 QUICKSTART.md             # Guida rapida
├── 📄 ARCHITECTURE.md           # Architettura tecnica
├── 📄 CONTRIBUTING.md           # Come contribuire
├── 📄 LICENSE                   # Licenza MIT
│
├── 🐍 main.py                   # Entry point CLI
├── ⚙️ setup.py                  # Setup automatico
├── 📋 requirements.txt          # Dipendenze Python
│
├── 📂 config/                   # Configurazioni
│   ├── payloads.yaml           # Payload di test (SICURI)
│   └── scanner_config.yaml     # Config scanner
│
├── 📂 scanners/                 # Scanner vulnerabilità
│   ├── crawler.py             # Crawling siti web
│   ├── sql_injection.py        # SQL Injection
│   ├── xss_scanner.py          # Cross-Site Scripting
│   ├── auth_scanner.py         # Autenticazione
│   └── config_scanner.py       # Configurazioni
│
├── 📂 parsers/                  # Parser HTML/HTTP
│   ├── form_parser.py         # Analisi forms
│   └── link_parser.py         # Analisi links
│
├── 📂 reporters/                # Generatori report
│   └── report_generator.py    # HTML/PDF/JSON
│
├── 📂 tests/                    # Unit tests
│   └── test_scanners.py        # Test suite
│
└── 📂 examples/                 # Esempi
    ├── example_usage.py        # Codice esempi
    └── permission_template.txt # Template permesso
```

---

## 🔑 Componenti Chiave

### 1. 🕷️ Web Crawler
- Scopre pagine web
- Estrae forms e links
- Rispetta robots.txt
- Rate limiting integrato

### 2. 🔬 Vulnerability Scanners
| Scanner | Cosa Trova | Severità |
|---------|-----------|----------|
| **SQLi** | Injection SQL | 🔴 Critical |
| **XSS** | Cross-Site Scripting | 🔴 Critical |
| **Auth** | Autenticazione debole | 🟠 High |
| **Config** | Headers mancanti | 🟡 Medium |

### 3. 📝 Report Generator
- **HTML**: Report interattivo professionale
- **PDF**: Report stampabile
- **JSON**: Dati strutturati per integrazione

### 4. ✅ Permission System
- Verifica file di permesso
- Conferma interattiva
- Disclaimer legale
- Audit trail

---

## 🚀 Quick Start

```bash
# 1. Setup
python setup.py

# 2. Crea permesso
cp examples/permission_template.txt permission.txt
# Edit permission.txt con i tuoi dettagli

# 3. Scansiona
python main.py scan http://localhost:8080 --permission-file permission.txt

# 4. Vedi report
# Apri report.html nel browser
```

---

## 🎓 Funzionalità Educative

### Impara:
- ✅ OWASP Top 10 vulnerabilities
- ✅ Come funzionano SQL injection
- ✅ Tipi di XSS attacks
- ✅ Security headers
- ✅ Authentication issues
- ✅ Safe coding practices

### Pratica:
- ✅ Scansiona le tue app
- ✅ Vedi esempi reali
- ✅ Capisci i report
- ✅ Apprendi come fixare

---

## 🛡️ Safety Features

| Feature | Descrizione |
|---------|-------------|
| **Safe Mode** | Payload read-only, non distruttivi |
| **Rate Limiting** | 5 richieste/secondo max |
| **Permission Check** | Verifica obbligatoria |
| **Robots.txt** | Rispetto regole |
| **No Destructive** | Niente DELETE/DROP |

---

## 📊 Output Esempio

```bash
$ python main.py scan http://localhost:8080 --permission-file perm.txt

[*] Starting scan of: http://localhost:8080
[*] Checks enabled: sqli, xss, auth, config

[*] Phase 1: Crawling website...
[+] Crawled 25 page(s)
[+] Found 8 form(s)

[*] Phase 2: Testing for vulnerabilities...
[*] Testing for SQL Injection...
[+] SQLi found in username with payload: ' OR '1'='1
[*] Testing for XSS...
[+] XSS found in search (Type: Reflected)
[*] Testing Authentication...
[+] Weak credentials found: admin:admin
[*] Testing Security Configuration...
[+] Missing header: X-Frame-Options

[+] Scan completed in 15.23 seconds
[+] Total findings: 12

[!] Findings by severity:
    - Critical: 2
    - High: 5
    - Medium: 4
    - Low: 1

[+] Report saved to: report.html
```

---

## 📚 Risorse di Apprendimento

### OWASP
- [Top 10](https://owasp.org/www-project-top-ten/)
- [Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Laboratori Pratici
- [PortSwigger Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)

### Libri Consigliati
- "The Web Application Hacker's Handbook"
- "Web Security for Developers"
- "Black Hat Python"

---

## 🎯 Use Cases

### 1. Sviluppatori
```bash
# Testa la tua app durante sviluppo
python main.py scan http://localhost:3000
```

### 2. Studenti
```bash
# Impara su DVWA
docker run -d -p 8080:80 vulnerables/web-dvwa
python main.py scan http://localhost:8080
```

### 3. Professionisti Security
```bash
# Test approfondito con report PDF
python main.py scan https://app.internal \
  --report security_audit.pdf \
  --format pdf \
  --checks sqli,xss,auth,config
```

### 4. Docenti
```bash
# Dimostrazioni in classe
python main.py quick http://localhost:8080
```

---

## ⚖️ Responsabilità

### ✅ Fai
- Scansiona le TUE app
- Usa per apprendere
- Disclosure responsabile
- Migliora la sicurezza

### ❌ NON Fare
- Scansionare senza permesso
- Usare per male
- Divulgare pubblicamente
- Causare danni

---

## 🔄 Roadmap

### Versione Corrente (1.0)
- ✅ Crawler base
- ✅ SQLi scanner
- ✅ XSS scanner
- ✅ Auth scanner
- ✅ Config scanner
- ✅ HTML/PDF reports

### Futuro (2.0+)
- ⏳ Selenium per JS-heavy sites
- ⏳ SSRF scanner
- ⏳ XXE scanner
- ⏳ API discovery
- ⏳ CI/CD integration
- ⏳ Docker image

---

## 📞 Supporto

- 📖 [Documentazione](README.md)
- 🚀 [Guida Rapida](QUICKSTART.md)
- 🏗️ [Architettura](ARCHITECTURE.md)
- 🤝 [Contribuire](CONTRIBUTING.md)
- 🧪 [Testing](tests/)

---

## 📊 Statistiche Progetto

- **Linguaggio**: Python 3.10+
- **Linee di codice**: ~3500+
- **Moduli**: 11
- **Test**: 50+ unit tests
- **Documentazione**: Italiano + Inglese
- **Licenza**: MIT

---

## ⭐ Riconoscimenti

Questo tool è stato creato per scopi **educativi** per aiutare:

- 🎓 Studenti a imparare la sicurezza web
- 👨‍💻 Sviluppatori a scrivere codice più sicuro
- 🔒 Professionisti security a effettuare test difensivi
- 🏫 Docenti a insegnare l'OWASP Top 10

---

## 🎓 Citazione

Se usi questo tool per ricerca o educazione:

```bibtex
@software{web_vuln_scanner,
  title={Web Vulnerability Scanner},
  author={Your Name},
  year={2024},
  note={Educational Security Tool}
}
```

---

**Creato con ❤️ per la comunità di sicurezza italiana**

🔒 **Ricorda: Conoscenza è potere. Usalo responsabilmente!**
