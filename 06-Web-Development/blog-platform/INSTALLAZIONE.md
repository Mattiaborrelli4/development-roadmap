# 🇮🇹 Guida Installazione - Blog Platform

## 📋 Requisiti

Prima di iniziare, assicurati di avere installato:

- **Node.js** (v14 o superiore) - [Download qui](https://nodejs.org/)
- **npm** (incluso con Node.js)
- Un editor di codice (VS Code, Notepad++, etc.)

### Verifica Installazione
Apri il terminale e digita:
```bash
node --version
npm --version
```

Dovresti vedere le versioni installate.

---

## 🚀 Installazione Passo-Passo

### 1. Apri il Terminale

#### Windows
- Premi `Win + R`
- Digita `cmd` e premi Enter
- Oppure usa PowerShell o Git Bash

#### Mac/Linux
- Apri Terminal
- Premi `Cmd + Space` e cerca "Terminal"

### 2. Naviga nella Cartella del Progetto

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\06-Web-Development\blog-platform"
```

> **Nota:** Puoi anche trascinare la cartella nel terminale

### 3. Installa le Dipendenze

```bash
npm install
```

Attendi che npm scarichi tutti i pacchetti necessari. Vedrai qualcosa come:

```
added 105 packages, and audited 106 packages in 2s
found 0 vulnerabilities
```

### 4. Avvia il Server

```bash
npm start
```

Dovresti vedere:

```
🚀 Server avviato su http://localhost:3000
📝 Blog Platform Ready!
🔑 Admin Login: admin / admin123
```

### 5. Apri nel Browser

Apri il browser e vai a:
```
http://localhost:3000
```

---

## 🔐 Prima Connessione

1. Clicca su **"🔐 Login"** nel menu in alto
2. Inserisci le credenziali:
   - Username: `admin`
   - Password: `admin123`
3. Clicca su **"Accedi"**

Ora puoi creare e gestire i tuoi post!

---

## 🛑 Come Fermare il Server

Nel terminale dove gira il server:

**Windows/Linux/Mac:** Premi `CTRL + C`

---

## 🔄 Riavvio Server

Dopo aver modificato i file, riavvia con:

1. Fermare il server (`CTRL + C`)
2. Riavviare (`npm start`)

### Modalità Sviluppo (Auto-Riavvio)

Per riavvio automatico quando modifichi i file:

```bash
# Installa nodemon globalmente
npm install -g nodemon

# Avvia con nodemon
nodemon server.js
```

---

## 📁 Files Importanti

| File | Descrizione |
|------|-------------|
| `server.js` | Codice del server Express |
| `public/app.js` | Codice JavaScript frontend |
| `public/styles.css` | Stili CSS |
| `database.json` | Database con post e utenti |
| `package.json` | Configurazione progetto |

---

## 🐛 Risoluzione Problemi

### Errore: "command not found: npm"

**Soluzione:** Node.js non è installato. [Scaricalo da nodejs.org](https://nodejs.org/)

### Errore: "EADDRINUSE: address already in use"

La porta 3000 è già usata.

**Soluzione 1:** Cambia porta
```bash
PORT=8080 npm start
```

**Soluzione 2:** Termina processo esistente
```bash
# Trova il processo
netstat -ano | findstr :3000

# Termina (sostituisci PID)
taskkill /PID <numero_PID> /F
```

### Errore: "Cannot find module"

**Soluzione:** Reinstalla le dipendenze
```bash
rm -rf node_modules package-lock.json
npm install
```

### Database corrotto

**Soluzione:** Elimina e ricrea
```bash
rm database.json
npm start
```

---

## 🎯 Quick Start Scripts

### Windows
Doppio clic su `start.bat`

### Mac/Linux
```bash
chmod +x start.sh
./start.sh
```

---

## 📝 Primi Passi

1. **Crea il tuo primo post**
   - Clicca su "➕ Nuovo Post"
   - Inserisci titolo e contenuto
   - Clicca "➕ Pubblica Post"

2. **Modifica un post**
   - Dalla lista, clicca "✏️ Modifica"
   - Modifica titolo o contenuto
   - Clicca "💾 Salva Modifiche"

3. **Elimina un post**
   - Dalla lista o dal post, clicca "🗑️ Elimina"
   - Conferma l'eliminazione

4. **Logout**
   - Clicca "🚪 Logout" nel menu

---

## 🔒 Sicurezza

⚠️ **IMPORTANTE:** Questo è un progetto demo. Per uso in produzione:

1. Cambia password admin
2. Modifica la session secret in `server.js`
3. Implementa rate limiting
4. Usa un database proper (PostgreSQL, MongoDB)
5. Aggiungi HTTPS

---

## 📚 Aiuto e Risorse

- **Documentazione completa:** `README.md`
- **Guida rapida:** `QUICK_REFERENCE.md`
- **Struttura progetto:** `PROJECT_STRUCTURE.md`
- **Riepilogo:** `PROJECT_SUMMARY.md`

---

## 💡 Consigli

- Usa un editor di codice come VS Code
- Leggi i commenti nel codice per capire meglio
- Sperimenta creando e modificando post
- Guarda il file `database.json` per vedere come sono salvati i dati

---

## ✅ Checklist Installazione

- [ ] Node.js installato
- [ ] npm installato
- [ ] Dipendenze installate (`npm install`)
- [ ] Server avviato (`npm start`)
- [ ] Browser aperto su http://localhost:3000
- [ ] Login effettuato con admin/admin123
- [ ] Primo post creato

---

## 🎉 Divertiti!

Congratulazioni! Hai installato con successo la Blog Platform.

Per qualsiasi problema, consulta i file di documentazione nella cartella del progetto.

**Buon blogging!** 📝
