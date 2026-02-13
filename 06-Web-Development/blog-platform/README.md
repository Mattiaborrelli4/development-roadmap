# 📝 Blog Platform

Piattaforma Blog Full-Stack completa con Node.js, Express e JSON file storage.

## 🌟 Caratteristiche

### Funzionalità Principali
- ✅ **CRUD Completo** per i post blog
- ✅ **Autenticazione** sicura con bcrypt e sessioni
- ✅ **Database JSON** per persistenza dati (facile backup)
- ✅ **SPA Frontend** con Vanilla JavaScript
- ✅ **Design Responsive** e moderno
- ✅ **Interfaccia Admin** intuitiva

### Operazioni Supportate
- ➕ Crea nuovi post
- 📖 Visualizza lista post
- 👁️ Leggi post singoli
- ✏️ Modifica post esistenti
- 🗑️ Elimina post
- 🔐 Login/Logout sicuro

## 🚀 Installazione e Avvio

### Prerequisiti
- Node.js (v14 o superiore)
- npm o yarn

### Passaggi

1. **Installa le dipendenze**
```bash
npm install
```

2. **Avvia il server**
```bash
npm start
```

Per sviluppo con auto-reload:
```bash
npm run dev
```

3. **Apri il browser**
```
http://localhost:3000
```

## 🔐 Credenziali Admin

**Admin di Default:**
- Username: `admin`
- Password: `admin123`

⚠️ **Importante:** Cambia queste credenziali in produzione!

## 📁 Struttura del Progetto

```
blog-platform/
├── server.js           # Server Express + API Routes
├── package.json        # Dipendenze e script
├── database.json       # Database JSON (generato automaticamente)
├── README.md          # Documentazione
├── start.bat          # Quick Start Script (Windows)
├── start.sh           # Quick Start Script (Linux/Mac)
└── public/            # Frontend
    ├── index.html     # Struttura HTML
    ├── styles.css     # Stili CSS
    └── app.js         # Logica JavaScript SPA
```

## 🛠️ Tecnologie Utilizzate

### Backend
- **Node.js** - Runtime JavaScript
- **Express** - Web framework
- **File System** - Database JSON (nessuna dipendenza esterna)
- **bcryptjs** - Hashing password
- **express-session** - Gestione sessioni
- **cookie-parser** - Parser cookies

### Frontend
- **HTML5** - Struttura
- **CSS3** - Styling con Gradienti e Flexbox
- **JavaScript ES6+** - Logica SPA (Single Page Application)

## 📡 API Endpoints

### Autenticazione
```
POST   /api/auth/login    - Login utente
POST   /api/auth/logout   - Logout utente
GET    /api/auth/status   - Verifica stato autenticazione
```

### Post
```
GET    /api/posts         - Ottieni tutti i post
GET    /api/posts/:id     - Ottieni singolo post
POST   /api/posts         - Crea nuovo post (richiede auth)
PUT    /api/posts/:id     - Aggiorna post (richiede auth)
DELETE /api/posts/:id     - Elimina post (richiede auth)
```

## 💾 Database Schema

Il database è salvato in `database.json` con la seguente struttura:

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
      "content": "Contenuto del post",
      "author": "admin",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

## 🎨 Features del Frontend

### Single Page Application
- Navigazione senza refresh
- Routing lato client
- Stato centralizzato

### UI/UX
- Design moderno con gradienti
- Card-based layout
- Responsive design
- Loading states
- Error handling
- Conferme per azioni destructive

### Sicurezza
- XSS protection (escape HTML)
- Session-based authentication
- Password hashing con bcrypt
- CSRF protection (session-based)

## 🔧 Personalizzazione

### Cambiare Porta
Modifica in `server.js`:
```javascript
const PORT = process.env.PORT || 3000;
```

Oppure:
```bash
PORT=8080 npm start
```

### Modificare Colori
Modifica in `public/styles.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Aggiungere Nuovi Admin
Modifica il file `database.json`:

```javascript
const bcrypt = require('bcryptjs');
const user = {
  id: 2,
  username: 'nuovo_admin',
  password: bcrypt.hashSync('tua_password', 10),
  created_at: new Date().toISOString()
};
// Aggiungi all'array "users"
```

## 📝 Note di Sviluppo

### Sicurezza in Produzione
1. Cambia la session secret in `server.js`
2. Usa variabili ambiente per le credenziali
3. Implementa rate limiting
4. Aggiungi HTTPS
5. Implementa refresh tokens

### Possibili Miglioramenti
- [ ] Commenti ai post
- [ ] Upload immagini
- [ ] Categorie/Tags
- [ ] Ricerca post
- [ ] Pagination
- [ ] Markdown editor
- [ ] Email notifications
- [ ] Multi-user con ruoli
- [ ] Draft posts

## 🐛 Troubleshooting

### Database Error
Se hai problemi col database, elimina `database.json` e riavvia il server. Verrà ricreato automaticamente.

### Port Already in Use
```bash
# Su Windows (PowerShell)
netstat -ano | findstr :3000
# Termina il processo con il PID mostrato
```

### Module Not Found
```bash
# Reinstalla dependencies
rm -rf node_modules package-lock.json
npm install
```

## 📄 Licenza

MIT License - Sentiti libero di usare questo progetto per learning e progetti personali.

## 👨‍💻 Autore

Creato come progetto demo per portfolio Full-Stack.

---

**Divertiti con il tuo blog!** 🎉
