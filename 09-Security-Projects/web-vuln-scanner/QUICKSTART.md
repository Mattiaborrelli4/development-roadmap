# 🚀 Guida Rapida - Web Vulnerability Scanner

> Inizia a usare lo scanner in 5 minuti

## ⚡ Setup Rapido (3 minuti)

### 1. Installa

```bash
# Windows
cd "Project Ideas Portfolio/09-Security-Projects/web-vuln-scanner"
python setup.py

# Oppure manualmente
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Verifica

```bash
python main.py --help
```

Dovresti vedere i comandi disponibili.

### 3. Disclaimer

```bash
python main.py disclaimer
```

Leggi e comprendi il disclaimer!

---

## 🎯 Primo Scan (2 minuti)

### Passo 1: Prepara Permesso

Crea `permission.txt`:

```
I, Mario Rossi, ho explicito permesso di scansionare:
Target: http://localhost:8080
Owner: La Mia Company
Date: 2024-01-15
Signature: _________________
```

### Passo 2: Esegui Scan

```bash
python main.py scan http://localhost:8080 --permission-file permission.txt
```

### Passo 3: Vedi Report

Apri `report.html` nel browser.

---

## 📊 Comuni Comandi

### Quick Scan (Veloce)
```bash
python main.py quick http://localhost:8080
```

### Scansione Completa
```bash
python main.py scan http://localhost:8080 \
  --permission-file permission.txt \
  --report mio_report.html \
  --max-pages 100
```

### Solo SQL Injection
```bash
python main.py scan http://localhost:8080 \
  --checks sqli \
  --permission-file permission.txt
```

### Report PDF
```bash
python main.py scan http://localhost:8080 \
  --report report.pdf \
  --format pdf \
  --permission-file permission.txt
```

---

## 🐛 Ambiente di Test

### Opzione 1: Docker (Consigliato)

```bash
# DVWA (Damn Vulnerable Web App)
docker run -d -p 8080:80 vulnerables/web-dvwa

# Ora puoi scansionare:
python main.py scan http://localhost:8080 --permission-file permission.txt
```

### Opzione 2: Applicazione Propria

```bash
# La tua app su http://localhost:3000
python main.py scan http://localhost:3000 --permission-file permission.txt
```

---

## 📖 Interpretare i Risultati

### Severità

- 🔴 **Critical** - Fix immediato!
- 🟠 **High** - Fix prioritario
- 🟡 **Medium** - Fix presto
- 🔵 **Low** - Fix quando possibile
- ⚪ **Info** - Informazioni

### Esempio Finding

```
Vulnerability: SQL Injection
Severity: High
URL: http://localhost:8080/login
Parameter: username
Payload: ' OR '1'='1

Recommendation: Use parameterized queries
```

---

## 🛠️ Troubleshooting

### "Permission denied"
→ Verifica di avere il file di permesso

### "No module named X"
→ Reinstalla dipendenze: `pip install -r requirements.txt`

### "Connection timeout"
→ Verifica che il target sia accessibile

### "No forms found"
→ Il sito potrebbe essere tutto JavaScript (non ancora supportato)

---

## 🎓 Prossimi Passi

1. ✅ Leggi [README.md](README.md) completo
2. ✅ Studia [ARCHITECTURE.md](ARCHITECTURE.md)
3. ✅ Impara [OWASP Top 10](https://owasp.org/www-project-top-ten/)
4. ✅ Pratica su [WebGoat](https://owasp.org/www-project-webgoat/)
5. ✅ Correggi le vulnerabilità trovate!

---

## ⚠️ RICORDA

- ✅ **SOLO** scansiona le TUE app o con permesso
- ✅ **MAI** usare per scopi malevoli
- ✅ **SEMPRE** disclosure responsabile
- ✅ **IMPARA** dalla sicurezza!

---

**Buon apprendimento! 🎓🔒**
