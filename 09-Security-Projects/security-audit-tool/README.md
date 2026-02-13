# 🔒 Security Audit Tool

<div align="center">

**Strumento Educativo/Difensivo per l'Analisi di Sicurezza del Codice**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Purpose](https://img.shields.io/badge/Purpose-Educational%2FDefensive-orange.svg)](#)

</div>

---

## ⚠️ DISCLAIMER IMPORTANTE

**QUESTO STRUMENTO È CREATO ESCLUSIVAMENTE PER SCOPI EDUCATIVI E DIFENSIVI**

- ✅ **Utilizzare SOLO su codice di tua proprietà**
- ✅ **Utilizzare SOLO con esplicito permesso scritto del proprietario**
- ❌ **NON utilizzare per scopi offensivi o illegali**
- ❌ **NON utilizzare su sistemi di terze parti senza autorizzazione**

L'autore non è responsabile per usi impropri o illegali di questo software.

---

## 📋 Indice

- [Descrizione](#descrizione)
- [Funzionalità](#funzionalità)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Vulnerabilità Rilevate](#vulnerabilità-rilevate)
- [Esempi](#esempi)
- [Supporto](#supporto)

---

## 🎯 Descrizione

**Security Audit Tool** è uno strumento di analisi statica del codice che aiuta gli sviluppatori a identificare vulnerabilità di sicurezza comuni nel proprio codice sorgente. È progettato per essere:

- 📚 **Educativo**: Impara le vulnerabilità comuni e come correggerle
- 🛡️ **Difensivo**: Trova e correggi vulnerabilità nel tuo codice
- 🔍 **Automatizzato**: Scansiona interi progetti rapidamente
- 📊 **Report Dettagliati**: Ottieni report HTML e testuali completi

---

## ✨ Funzionalità

### Vulnerabilità Supportate

| Vulnerabilità | Severità | CWE |
|--------------|----------|-----|
| **SQL Injection** | CRITICAL | CWE-89 |
| **XSS (Cross-Site Scripting)** | HIGH | CWE-79 |
| **Credenziali Hardcoded** | CRITICAL | CWE-798 |
| **Dipendenze Insecure** | MEDIUM | CWE-1104 |
| **Crittografia Debole** | MEDIUM | CWE-327 |
| **Mancanza Validazione Input** | MEDIUM | CWE-20 |
| **Random Insicuro** | LOW | CWE-330 |
| **Path Traversal** | HIGH | CWE-22 |
| **Command Injection** | CRITICAL | CWE-77 |
| **SSRF** | HIGH | CWE-918 |

### Linguaggi Supportati

- 🐍 **Python** (.py, .pyw)
- 📜 **JavaScript** (.js, .jsx)
- 💎 **TypeScript** (.ts, .tsx)
- 🐘 **PHP** (.php, .phtml)
- ☕ **Java** (.java)
- ♦️ **C#** (.cs)
- 🔵 **Go** (.go)

---

## 🚀 Installazione

### Requisiti

- Python 3.10 o superiore
- pip (gestore pacchetti Python)

### Passi di Installazione

1. **Clona o scarica il repository:**

```bash
cd security-audit-tool
```

2. **Installa le dipendenze:**

```bash
pip install -r requirements.txt
```

3. **Verifica l'installazione:**

```bash
python main.py --help
```

---

## 💻 Utilizzo

### Comandi Base

#### Visualizza Aiuto

```bash
python main.py --help
```

#### Esegui Audit di Sicurezza

```bash
# Analizza una directory
python main.py audit /percorso/del/tuo/progetto

# Analizza con report HTML
python main.py audit /percorso/del/progetto --report report.html

# Filtra per severità
python main.py audit /percorso/del/progetto --severity critical,high

# Output dettagliato
python main.py audit /percorso/del/progetto --verbose
```

#### Altri Comandi

```bash
# Mostra informazioni sul progetto
python main.py info /percorso/del/progetto

# Mostra pattern supportati
python main.py patterns

# Mostra disclaimer legale
python main.py disclaimer
```

### Esempi di Utilizzo

#### Esempio 1: Audit Completo con Report HTML

```bash
python main.py audit ./my-web-app --report security-audit.html
```

Questo comando:
- ✅ Analizza tutti i file nel progetto
- ✅ Genera report HTML interattivo
- ✅ Salva il report come `security-audit.html`

#### Esempio 2: Solo Vulnerabilità Critiche

```bash
python main.py audit ./my-web-app --severity critical
```

#### Esempio 3: Report Dettagliato

```bash
python main.py audit ./my-web-app --verbose --output both --report full-report.html
```

---

## 🔍 Vulnerabilità Rilevate

### SQL Injection

**Vulnerabile:**
```python
# ❌ Male - Input utente concatenato
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
cursor.execute("SELECT * FROM users WHERE name='" + name + "'")
```

**Sicuro:**
```python
# ✅ Bene - Query parametrizzata
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
```

---

### XSS (Cross-Site Scripting)

**Vulnerabile:**
```javascript
// ❌ Male - Input non sanitizzato
element.innerHTML = user_input;
document.write(user_input);
```

**Sicuro:**
```javascript
// ✅ Bene - TextContent non esegue codice
element.textContent = user_input;
```

---

### Credenziali Hardcoded

**Vulnerabile:**
```python
# ❌ Male - Password hardcoded
DB_PASSWORD = "mypassword123"
api_key = "sk_live_1234567890abcdef"
```

**Sicuro:**
```python
# ✅ Bene - Variabili ambiente
import os
DB_PASSWORD = os.environ.get('DB_PASSWORD')
api_key = os.environ.get('API_KEY')
```

---

### Crittografia Debole

**Vulnerabile:**
```python
# ❌ Male - Algoritmi obsoleti
import hashlib
hash = hashlib.md5(data)
hash = hashlib.sha1(data)
```

**Sicuro:**
```python
# ✅ Bene - Algoritmi sicuri
hash = hashlib.sha256(data)
hash = hashlib.sha512(data)
```

---

### Mancanza Validazione Input

**Vulnerabile:**
```python
# ❌ Male - Input non validato
user_id = request.GET['id']
user_name = request.POST['name']
```

**Sicuro:**
```python
# ✅ Bene - Input validato
user_id = int(request.GET.get('id', 0))
user_name = request.POST.get('name', '').strip()
```

---

## 📊 Formato Report

### Report Console

```
═══ CRITICAL (3) ═══
┏━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━━━━┓
┃ # ┃ Tipo           ┃ File      ┃ Riga┃ Codice       ┃
┡━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━━━━┩
│ 1 │ SQL Injection  │ app.py    │  42 │ cursor.ex... │
│ 2 │ Credentials    │ config.py │  15 │ password =..│
└───┴────────────────┴───────────┴─────┴──────────────┘
```

### Report HTML

Il report HTML include:
- 📊 **Dashboard** con statistiche visive
- 🎨 **Grafici** per tipo e severità
- 📝 **Dettagli completi** per ogni vulnerabilità
- 💡 **Raccomandazioni** su come fixare
- 🔗 **Riferimenti** a risorse esterne

---

## 🛠️ Sviluppo

### Eseguire i Test

```bash
python tests/test_analyzers.py
```

### Struttura Progetto

```
security-audit-tool/
├── main.py                 # Entry point CLI
├── analyzers/              # Moduli analizzatori
│   ├── sql_injection.py
│   ├── xss_detector.py
│   ├── credentials.py
│   ├── dependencies.py
│   ├── crypto.py
│   └── validation.py
├── parsers/                # Parser codice
│   ├── code_reader.py
│   └── ast_parser.py
├── reporters/              # Generatori report
│   ├── html_reporter.py
│   └── text_reporter.py
├── config/
│   └── patterns.yaml       # Pattern vulnerabilità
├── tests/
│   └── test_analyzers.py
├── requirements.txt
└── README.md
```

---

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di:

1. 🐛 Segnalare bug
2. 💡 Suggerire nuove funzionalità
3. 📚 Migliorare la documentazione
4. 🔧 Inviare pull request

---

## 📚 Risorse per Apprendere

### OWASP (Open Web Application Security Project)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [XSS](https://owasp.org/www-community/attacks/xss/)

### Cheat Sheet
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### Standard di Sicurezza
- [NIST Cryptographic Standards](https://csrc.nist.gov/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)

---

## 📄 Licenza

Questo progetto è rilasciato sotto la Licenza MIT. Vedi il file `LICENSE` per dettagli.

---

## ⚖️ Note Legali ed Etiche

### ✅ Cosa PUOI Fare

- Analizzare il tuo codice
- Analizzare codice con permesso esplicito
- Usare per scopi educativi
- Imparare sulla sicurezza
- Migliorare le tue competenze

### ❌ Cosa NON PUOI Fare

- Analizzare codice senza permesso
- Utilizzare per scopi offensivi
- Violare leggi o regolamenti
- Accedere a sistemi non autorizzati
- Distribuire malware o exploit

### 🎓 Finalità Educativa

Questo strumento è progettato per:

1. **Insegnare** agli sviluppatori le vulnerabilità comuni
2. **Prevenire** vulnerabilità nel codice prima del deployment
3. **Migliorare** la consapevolezza sulla sicurezza
4. **Fornire** un punto di partenza per analisi più approfondite

### ⚠️ Limitazioni

- ⚠️ I risultati sono **indicativi**, non definitivi
- ⚠️ Non sostituisce un penetration test professionale
- ⚠️ Richiede verifica umana dei risultati
- ⚠️ Non rileve tutte le possibili vulnerabilità
- ⚠️ Può generare falsi positivi

---

## 👨‍💻 Autore

Creato per scopi educativi e difensivi.

**Versione:** 1.0.0
**Data:** Febbraio 2025

---

## 🙏 Riconoscimenti

- OWASP per le risorse educative sulla sicurezza
- La comunità open-source per gli strumenti di analisi statica
- Tutti i ricercatori di sicurezza che condividono le loro conoscenze

---

<div align="center">

**🔒 Scrivi Codice Più Sicuro | 🛡️ Proteggi i Tuoi Progetti | 📚 Impara la Sicurezza**

Made with ❤️ for Educational Purposes

</div>
