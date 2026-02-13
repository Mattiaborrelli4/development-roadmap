# 🚀 Guida Rapida - Phishing Email Analyzer

Guida veloce per iniziare ad usare lo strumento.

## ⚡ Installazione Rapida

```bash
# 1. Vai nella directory del progetto
cd phishing-analyzer

# 2. Crea un ambiente virtuale (consigliato)
python -m venv venv

# 3. Attiva l'ambiente virtuale
# Su Windows:
venv\Scripts\activate
# Su Linux/Mac:
source venv/bin/activate

# 4. Installa le dipendenze
pip install -r requirements.txt
```

## 🎯 Primi Passi

### 1. Verifica l'Installazione

```bash
python main.py --version
```

Dovresti vedere: `1.0.0`

### 2. Guarda la Guida Educativa

```bash
python main.py learn
```

### 3. Analizza la Email di Esempio

```bash
python main.py analyze sample_phishing.eml
```

Questo analizzerà una email di phishing simulata inclusa nel progetto.

## 📖 Comandi Principali

### Analizzare una Email

```bash
# Da file
python main.py analyze email.eml

# Da stdin
cat email.eml | python main.py analyze --stdin
```

### Controllare URL

```bash
# Uno o più URL
python main.py check-links https://suspicious.com https://example.xyz
```

### Verificare un Dominio

```bash
# Controlla SPF, DMARC, MX
python main.py check-domain paypal.com
```

### Informazioni Educativhe

```bash
# Spiega SPF
python main.py explain-spf

# Spiega DMARC
python main.py explain-dmarc

# Spiega DKIM
python main.py explain-dkim
```

## 🎓 Esempi Pratici

### Esempio 1: Email Sospetta

Hai ricevuto una email da "PayPal" che ti chiede di confermare la password:

```bash
# 1. Salva la email come .eml
# 2. Analizzala
python main.py analyze sospetta.eml
```

Guarda il punteggio di rischio:
- 🔴 CRITICO → È phishing, cancella!
- 🟠 ALTO → Molto probabile phishing, verifica con l'azienda
- 🟡 MEDIO → Alcuni sospetti, controlla attentamente
- 🟢 BASSO → Probabilmente sicura
- ✅ MOLTO BASSO → Sembra legittima

### Esempio 2: Link Sospetti

Vuoi controllare un link prima di cliccare:

```bash
python main.py check-links http://paypa1.com/login
```

### Esempio 3: Verifica Dominio

Vuoi sapere se una banca ha configurato correttamente la sicurezza:

```bash
python main.py check-domain bancoposta.it
```

## 📊 Capire il Risultato

### Punteggio di Rischio

```
╔══════════════════════════════════════════════════════════════╗
║           REPORT DEL RISCHIO DI PHISHING                     ║
╠══════════════════════════════════════════════════════════════╣
║  Livello di Rischio: CRITICO                         🔴      ║
║  Punteggio: 85/150 (56.7%)                                   ║
╚══════════════════════════════════════════════════════════════╝
```

### Fattori di Rischio

```
🔴 SPF Fallito [CRITICAL] (+20)
   Il server NON è autorizzato a inviare email per questo dominio
   💡 È molto probabile che sia phishing

🔴 Richiesta Credenziali [CRITICAL] (+25)
   La email chiede password o credenziali di accesso
   💡 LE AZIENDE NON CHIEDONO MAI LA PASSWORD VIA EMAIL!

🟠 Link Non Sicuro [HIGH] (+12)
   URL senza HTTPS: http://paypa1.com/login
   💡 Questo link non usa una connessione sicura
```

## ⚠️ Cosa Fare Se Trovi Phishing

### 1. NON Cliccare Nulla!

### 2. NON Rispondere!

### 3. Segnala la Email:

- **Gmail**: Menu (⋮) → Segnala come Phishing
- **Outlook**: Junk → Phishing → Segnala
- **Poste**: Inoltra a `ante@poste.it`

### 4. Elimina la Email

### 5. Se Hai Cliccato:

- Cambia la password immediatamente
- Contatta la banca/servizio
- Attiva l'autenticazione a due fattori
- Controlla le transazioni recenti

## 🔧 Risoluzione Problemi

### Errore: "No module named 'rich'"

```bash
pip install -r requirements.txt
```

### Errore: "File non trovato"

Assicurati di usare il percorso completo:

```bash
# Corretto
python main.py analyze C:\Users\matti\Desktop\email.eml

# Errato
python main.py analyze email.eml  (se non sei nella stessa cartella)
```

### Errore DNS

Alcune verifiche DNS richiedono connessione internet. Assicurati di essere connesso.

## 📚 Risorse Aggiuntive

- README completo: `README.md`
- Esempi: `sample_phishing.eml`
- Test: `tests/test_analyzers.py`
- Pattern di phishing: `knowledge/patterns.yaml`

## 🆘 Hai Bisogno di Aiuto?

Per maggiori informazioni:

```bash
python main.py --help
```

---

**Ricorda:** La difesa migliore contro il phishing è la consapevolezza! 🛡️
