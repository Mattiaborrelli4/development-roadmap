# 🚀 Blog Platform - Guida Rapida

## Avvio Veloce

### Opzione 1: Quick Start Scripts
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Opzione 2: Manuale
```bash
# 1. Installa dipendenze
npm install

# 2. Avvia il server
npm start
```

### Opzione 3: Development Mode
```bash
# Installa nodemon globalmente
npm install -g nodemon

# Avvia con auto-reload
nodemon server.js
```

---

## 🔐 Credenziali di Accesso

**Admin di Default:**
- Username: `admin`
- Password: `admin123`

⚠️ **Cambia subito queste credenziali in produzione!**

---

## 📍 Accesso

- **URL:** http://localhost:3000
- **Porta:** 3000 (cambiabile con variabile `PORT`)

---

## 🎯 Funzionalità Principali

### Per Tutti
- ✅ Visualizzare lista post
- ✅ Leggere post singoli
- ✅ Design responsive

### Per Admin (Autenticato)
- ✅ Creare nuovi post
- ✅ Modificare post esistenti
- ✅ Eliminare post

---

## 📡 API Endpoints

### Autenticazione
```bash
# Login
POST /api/auth/login
Body: { "username": "admin", "password": "admin123" }

# Logout
POST /api/auth/logout

# Verifica stato
GET /api/auth/status
```

### Post
```bash
# Ottieni tutti i post
GET /api/posts

# Ottieni singolo post
GET /api/posts/:id

# Crea nuovo post (richiede auth)
POST /api/posts
Body: { "title": "Titolo", "content": "Contenuto" }

# Aggiorna post (richiede auth)
PUT /api/posts/:id
Body: { "title": "Nuovo titolo", "content": "Nuovo contenuto" }

# Elimina post (richiede auth)
DELETE /api/posts/:id
```

---

## 🗂️ Struttura Database

Il file `database.json` contiene:

```json
{
  "users": [
    {
      "id": 1,
      "username": "admin",
      "password": "hashed_password",
      "created_at": "2024-01-01T00:00:00.000Z"
    }
  ],
  "posts": [
    {
      "id": 1,
      "title": "Titolo del post",
      "content": "Contenuto completo...",
      "author": "admin",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

---

## 🔧 Comandi Utili

### Reset Database
```bash
# Elimina il file database
rm database.json

# Riavvia il server (verrà ricreato)
npm start
```

### Backup Database
```bash
# Crea backup
cp database.json database-backup-$(date +%Y%m%d).json
```

### Restore Database
```bash
# Ripristina backup
cp database-backup-YYYYMMDD.json database.json
```

---

## 🐛 Troubleshooting

### Porta già in uso
```bash
# Cerca processo sulla porta 3000
netstat -ano | findstr :3000

# Termina il processo (sostituisci PID)
taskkill /PID <PID> /F
```

### Reinstalla dipendenze
```bash
# Pulisci tutto
rm -rf node_modules package-lock.json

# Reinstalla
npm install
```

### Database corrotto
```bash
# Elimina e ricrea
rm database.json
npm start
```

---

## 📝 Note Importanti

### Sicurezza
⚠️ **Questo è un progetto demo. Per produzione:**
1. Cambia la session secret in `server.js`
2. Usa variabili ambiente per credenziali
3. Implementa rate limiting
4. Aggiungi HTTPS
5. Valida tutti gli input
6. Implementa CSRF protection
7. Usa un database proper (PostgreSQL, MongoDB)

### Limitazioni
- Nessun sistema di commenti
- Nessun upload immagini
- Nessuna ricerca
- Single-user (admin only)
- No pagination

---

## 🎨 Personalizzazione

### Cambiare colori
Modifica `public/styles.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Cambiare porta
```bash
PORT=8080 npm start
```

Oppure modifica `server.js`:
```javascript
const PORT = process.env.PORT || 3000;
```

### Aggiungere nuovi admin
Modifica `database.json` e aggiungi un nuovo utente con password hashed:
```javascript
const bcrypt = require('bcryptjs');
const hash = bcrypt.hashSync('password', 10);
```

---

## 📚 Risorse

- **Documentazione principale:** `README.md`
- **Struttura progetto:** `PROJECT_STRUCTURE.md`
- **Node.js:** https://nodejs.org/docs
- **Express:** https://expressjs.com/

---

## ✨ Checklist per Deployment

- [ ] Cambiare credenziali admin
- [ ] Cambiare session secret
- [ ] Configurare variabili ambiente
- [ ] Implementare rate limiting
- [ ] Aggiungere logging
- [ ] Testare tutti gli endpoint
- [ ] Backup database
- [ ] Configurare HTTPS
- [ ] Setup process manager (PM2)

---

**Divertiti con il tuo blog!** 🎉
