# 🚀 Guida Rapida - Security Audit Tool

## Setup in 2 Minuti

### 1. Installa le dipendenze
```bash
cd security-audit-tool
pip install -r requirements.txt
```

### 2. Testa con il codice di esempio
```bash
python main.py audit example_vulnerable_code.py --report test-report.html
```

### 3. Apri il report
Apri `test-report.html` nel browser per vedere i risultati!

---

## Comandi Utili

### Audit Base
```bash
python main.py audit /percorso/del/progetto
```

### Con Report HTML
```bash
python main.py audit /percorso/del/progetto --report mio-report.html
```

### Solo Vulnerabilità Critiche
```bash
python main.py audit /percorso/del/progetto --severity critical
```

### Output Dettagliato
```bash
python main.py audit /percorso/del/progetto --verbose
```

### Entrambi i Report
```bash
python main.py audit /percorso/del/progetto --output both --report report.html
```

---

## Capire i Risultati

### Severità
- 🔴 **CRITICAL**: Correggi immediatamente
- 🟠 **HIGH**: Correggi presto
- 🟡 **MEDIUM**: Valuta la priorità
- 🔵 **LOW**: Miglioramento consigliato

### Tipi di Vulnerabilità

| Tipo | Descrizione | Esempio |
|------|------------|---------|
| SQL Injection | Query SQL manipolabili | `execute(f"SELECT... {user}")` |
| XSS | Output non sanitizzato | `innerHTML = user_input` |
| Credentials | Password/API key nel codice | `password = "abc123"` |
| Crypto | Algoritmi deboli | `md5(data)` |
| Validation | Input non validato | `id = request.GET['id']` |

---

## Esempio di Fix

### ❌ SQL Injection Vulnerabile
```python
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
```

### ✅ SQL Injection Sicuro
```python
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
```

---

## Risorse

- 📖 [README Completo](README.md)
- 🧪 [Esegui Test](python tests/test_analyzers.py)
- 📚 [Pattern Supportati](python main.py patterns)
- ⚖️ [Disclaimer Legale](python main.py disclaimer)

---

## Troubleshooting

### Errore: ModuleNotFoundError
```bash
# Reinstalla le dipendenze
pip install -r requirements.txt
```

### Nessun file trovato
```bash
# Verifica che il percorso contenga file supportati
python main.py info /percorso/del/progetto
```

### Troppi risultati
```bash
# Filtra per severità
python main.py audit /percorso --severity high,critical
```

---

## Prossimi Passi

1. ✅ Analizza il tuo progetto
2. 📋 Leggi il report
3. 🔧 Correggi le vulnerabilità
4. 🔄 Ri-analizza dopo le correzioni
5. 📚 Impara dalle risorse OWASP

---

**⚠️ Ricorda:** Questo è uno strumento educativo/defensivo. Usa solo su codice tuo!
