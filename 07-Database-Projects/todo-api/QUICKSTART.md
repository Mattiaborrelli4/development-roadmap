# 🚀 Guida Rapida - TODO API

## Avvio Veloce

### 1. Installa le Dipendenze
```bash
npm install
```

### 2. Avvia il Server
```bash
npm start
```

Il server partirà su `http://localhost:3000`

### 3. Testa l'API

#### Opzione A: Con cURL
```bash
# Crea un todo
curl -X POST http://localhost:3000/api/todos \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Il mio primo todo\"}"

# Ottieni tutti i todos
curl http://localhost:3000/api/todos
```

#### Opzione B: Con lo script di test
```bash
# In un altro terminale
node test-manual.js
```

#### Opzione C: Con Postman/Thunder Client
Importa gli endpoint da `test-api.http` o configura manualmente:
- URL: `http://localhost:3000/api/todos`
- Method: `POST`
- Body: `{"title":"Test todo"}`

## Endpoint Principali

| Metodo | Endpoint | Scopo |
|--------|----------|-------|
| POST | `/api/todos` | Crea todo |
| GET | `/api/todos` | Lista todos |
| PUT | `/api/todos/:id` | Aggiorna todo |
| DELETE | `/api/todos/:id` | Elimina todo |

## Esempio di Utilizzo

### 1. Crea un Todo
```bash
curl -X POST http://localhost:3000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Imparare Node.js",
    "description": "Studiare Express e SQLite",
    "completed": false
  }'
```

### 2. Ottieni Tutti i Todos
```bash
curl http://localhost:3000/api/todos
```

### 3. Aggiorna un Todo
```bash
curl -X PUT http://localhost:3000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 4. Elimina un Todo
```bash
curl -X DELETE http://localhost:3000/api/todos/1
```

## Troubleshooting

### Porta 3000 già in uso?
Cambia porta:
```bash
PORT=4000 npm start
```

### Database error?
Il database SQLite viene creato automaticamente alla prima esecuzione.

### Dipendenze mancanti?
```bash
npm install
```

## File Importanti

- `server.js` - Server Express e API
- `README.md` - Documentazione completa
- `test-api.http` - Collection per REST Client
- `test-manual.js` - Script di test automatico

---

**Per maggiori dettagli, vedi [README.md](README.md)**
