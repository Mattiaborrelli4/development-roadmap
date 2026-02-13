# 📝 TODO API

API REST completa per la gestione di attività TODO, costruita con Node.js, Express e database SQLite.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Avvio del Server](#avvio-del-server)
- [Endpoint API](#endpoint-api)
- [Struttura del Database](#struttura-del-database)
- [Esempi di Utilizzo](#esempi-di-utilizzo)
- [Testing con cURL](#testing-con-curl)
- [Struttura del Progetto](#struttura-del-progetto)

## ✨ Caratteristiche

- ✅ CRUD completo per i todos
- 💾 Database SQLite persistente
- 🔄 Toggle dello stato completed
- 🛡️ Validazione degli input
- 📅 Timestamp automatici (created_at, updated_at)
- 🌐 Supporto CORS
- 📖 Risposte JSON strutturate
- ⚡ Gestione errori robusta

## 🛠 Tecnologie Utilizzate

- **Node.js** - Runtime JavaScript
- **Express.js** - Framework web
- **SQLite3** - Database embedded
- **CORS** - Cross-Origin Resource Sharing
- **body-parser** - Parser del body delle richieste

## 📦 Installazione

### Prerequisiti

- Node.js (v14 o superiore)
- npm o yarn

### Passi di Installazione

1. Clona o naviga nella directory del progetto:
```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\07-Database-Projects\todo-api"
```

2. Installa le dipendenze:
```bash
npm install
```

## 🚀 Avvio del Server

### Modalità Produzione
```bash
npm start
```

### Modalità Sviluppo (con auto-reload)
```bash
npm run dev
```

Il server avvierà su `http://localhost:3000`

## 📡 Endpoint API

### Base URL
```
http://localhost:3000
```

### Liste degli Endpoint

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/` | Info API |
| GET | `/api/todos` | Ottieni tutti i todos |
| GET | `/api/todos/:id` | Ottieni un todo specifico |
| POST | `/api/todos` | Crea nuovo todo |
| PUT | `/api/todos/:id` | Aggiorna todo esistente |
| PATCH | `/api/todos/:id/toggle` | Toggle stato completed |
| DELETE | `/api/todos/:id` | Elimina todo |
| DELETE | `/api/todos` | Elimina tutti i todos |

## 💾 Struttura del Database

### Tabella: todos

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | INTEGER | Chiave primaria (auto-increment) |
| title | TEXT | Titolo del todo (obbligatorio) |
| description | TEXT | Descrizione del todo |
| completed | INTEGER | Stato completamento (0/1) |
| created_at | DATETIME | Data creazione |
| updated_at | DATETIME | Data ultimo aggiornamento |

## 📖 Esempi di Utilizzo

### 1. Ottieni Tutti i Todos
```http
GET /api/todos
```

**Risposta:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "title": "Comprare latte",
      "description": "Andare al supermercato",
      "completed": false,
      "created_at": "2024-01-15 10:30:00",
      "updated_at": "2024-01-15 10:30:00"
    },
    {
      "id": 2,
      "title": "Studiare Node.js",
      "description": "Completare tutorial Express",
      "completed": true,
      "created_at": "2024-01-15 11:00:00",
      "updated_at": "2024-01-15 12:00:00"
    }
  ]
}
```

### 2. Crea Nuovo Todo
```http
POST /api/todos
Content-Type: application/json

{
  "title": "Nuova attività",
  "description": "Descrizione dell'attività",
  "completed": false
}
```

**Risposta:**
```json
{
  "success": true,
  "message": "Todo creato con successo",
  "data": {
    "id": 3,
    "title": "Nuova attività",
    "description": "Descrizione dell'attività",
    "completed": false,
    "created_at": "2024-01-15 14:30:00",
    "updated_at": "2024-01-15 14:30:00"
  }
}
```

### 3. Aggiorna Todo
```http
PUT /api/todos/1
Content-Type: application/json

{
  "title": "Titolo aggiornato",
  "completed": true
}
```

**Risposta:**
```json
{
  "success": true,
  "message": "Todo aggiornato con successo",
  "data": {
    "id": 1,
    "title": "Titolo aggiornato",
    "description": "Descrizione dell'attività",
    "completed": true,
    "created_at": "2024-01-15 10:30:00",
    "updated_at": "2024-01-15 15:00:00"
  }
}
```

### 4. Toggle Completed
```http
PATCH /api/todos/1/toggle
```

**Risposta:**
```json
{
  "success": true,
  "message": "Todo toggle completato",
  "data": {
    "id": 1,
    "title": "Titolo aggiornato",
    "description": "Descrizione dell'attività",
    "completed": false,
    "created_at": "2024-01-15 10:30:00",
    "updated_at": "2024-01-15 15:30:00"
  }
}
```

### 5. Elimina Todo
```http
DELETE /api/todos/1
```

**Risposta:**
```json
{
  "success": true,
  "message": "Todo eliminato con successo",
  "data": {
    "id": 1,
    "deleted": true
  }
}
```

## 🧪 Testing con cURL

### Crea un Todo
```bash
curl -X POST http://localhost:3000/api/todos \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Comprare latte\",\"description\":\"Andare al supermercato\",\"completed\":false}"
```

### Ottieni Tutti i Todos
```bash
curl http://localhost:3000/api/todos
```

### Ottieni Todo Specifico
```bash
curl http://localhost:3000/api/todos/1
```

### Aggiorna Todo
```bash
curl -X PUT http://localhost:3000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Comprare latte e pane\",\"completed\":true}"
```

### Toggle Todo
```bash
curl -X PATCH http://localhost:3000/api/todos/1/toggle
```

### Elimina Todo
```bash
curl -X DELETE http://localhost:3000/api/todos/1
```

### Elimina Tutti i Todos
```bash
curl -X DELETE http://localhost:3000/api/todos
```

## 📁 Struttura del Progetto

```
todo-api/
├── server.js           # Server Express e configurazione database
├── package.json        # Dipendenze e script
├── .gitignore         # File ignorati da Git
├── README.md          # Documentazione
└── database.sqlite    # Database SQLite (creato automaticamente)
```

## 🔒 Note sulla Sicurezza

- L'API include validazione degli input
- I parametri SQL sono parametrizzati per prevenire SQL injection
- Supporto CORS abilitato per tutte le origini
- In produzione, configurare CORS con origini specifiche

## 🚀 Produzione

Per l'uso in produzione, considera:

1. Aggiungere autenticazione (JWT, OAuth)
2. Configurare CORS con origini specifiche
3. Implementare rate limiting
4. Aggiungere logging strutturato
5. Usare variabili d'ambiente per configurazioni sensibili
6. Implementare sanitization degli input
7. Aggiungere test unitari e di integrazione

## 📝 Formato Risposte

Tutte le risposte seguono questo formato:

### Successo
```json
{
  "success": true,
  "message": "Messaggio opzionale",
  "data": { ... }
}
```

### Errore
```json
{
  "success": false,
  "error": "Descrizione errore"
}
```

## 🐛 Risoluzione Problemi

### Porta già in uso
Cambia la porta modificando la variabile `PORT` in `server.js` o usando una variabile d'ambiente:
```bash
PORT=4000 npm start
```

### Database non si crea
Assicurati che la directory abbia i permessi di scrittura. Il file `database.sqlite` verrà creato automaticamente alla prima esecuzione.

### Dipendenze non installate
Esegui:
```bash
npm install
```

## 📄 Licenza

MIT

## 👤 Autore

Progetto creato per portfolio - Database Projects

---

**Happy Coding! 🚀**
