# API Reference - Spring Auth System

## Base URL
```
http://localhost:8080
```

## Authentication Flow

```
┌─────────┐                  ┌──────────────┐                  ┌─────────┐
│  Client │                  │  API Server  │                  │  H2 DB  │
└────┬────┘                  └──────┬───────┘                  └────┬────┘
     │                              │                              │
     │ 1. POST /register           │                              │
     ├─────────────────────────────►│                              │
     │    {username, email, pwd}   │                              │
     │                              │                              │
     │                              │ 2. Salva User                │
     │                              ├─────────────────────────────►│
     │                              │                              │
     │ 3. 201 Created              │ 3. User + Tokens              │
     │◄─────────────────────────────┤◄─────────────────────────────┤
     │    {accessToken,            │                              │
     │     refreshToken}           │                              │
     │                              │                              │
     │ 4. GET /api/users/me        │                              │
     │    Authorization: Bearer     │                              │
     ├─────────────────────────────►│                              │
     │    {token}                  │                              │
     │                              │ 5. Valida Token              │
     │                              │ 6. Carica User               │
     │                              │                              │
     │ 7. 200 OK                   │                              │
     │◄─────────────────────────────┤                              │
     │    {userData}               │                              │
```

## Endpoints

### 1. Register

Registra un nuovo utente nel sistema.

**Endpoint**
```http
POST /api/auth/register
```

**Request Headers**
```
Content-Type: application/json
```

**Request Body**
```json
{
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "password": "password123",
  "firstName": "Mario",
  "lastName": "Rossi",
  "phoneNumber": "+39123456789"
}
```

**Validation Rules**
- `username`: 3-50 caratteri, required
- `email`: formato valido, required
- `password`: 6-100 caratteri, required
- `firstName`: 3-50 caratteri, optional
- `lastName`: 3-50 caratteri, optional
- `phoneNumber`: 9-15 caratteri, optional

**Success Response**
```
Status: 201 Created
```
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtcm9zc2kiLCJyb2xlIjoiVVNFUiIsImlhdCI6MTYxNjIzOTAyMiwiZXhwIjoxNjE2MzI1NDIyfQ.signature",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "message": "Registrazione completata. Controlla la tua email per verificare l'account."
}
```

**Error Responses**

400 Bad Request - Validation Error
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 400,
  "error": "Validation Error",
  "errors": {
    "username": "Il nome utente deve essere tra 3 e 50 caratteri"
  }
}
```

400 Bad Request - Business Logic
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Email già in uso"
}
```

---

### 2. Login

Autentica un utente esistente.

**Endpoint**
```http
POST /api/auth/login
```

**Request Body**
```json
{
  "usernameOrEmail": "mrossi",
  "password": "password123"
}
```

**Notes**
- Puoi usare username o email
- Password inviata in chiaro (HTTPS in produzione!)

**Success Response**
```
Status: 200 OK
```
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "message": "Login effettuato con successo"
}
```

**Error Response**
```
Status: 401 Unauthorized
```
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 401,
  "error": "Unauthorized",
  "message": "Credenziali non valide"
}
```

---

### 3. Refresh Token

Ottiene un nuovo access token usando il refresh token.

**Endpoint**
```http
POST /api/auth/refresh
```

**Request Body**
```json
{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Success Response**
```
Status: 200 OK
```
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "message": "Token refreshato con successo"
}
```

**Error Response**

400 Bad Request - Token scaduto
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Refresh token scaduto. Effettua nuovamente il login."
}
```

400 Bad Request - Token revocato
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Refresh token revocato. Effettua nuovamente il login."
}
```

---

### 4. Logout

Invalida il refresh token (logout lato server).

**Endpoint**
```http
POST /api/auth/logout
```

**Request Body**
```json
{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Success Response**
```
Status: 204 No Content
```

---

### 5. Get Current User

Ottiene il profilo dell'utente autenticato.

**Endpoint**
```http
GET /api/users/me
```

**Request Headers**
```
Authorization: Bearer <access_token>
```

**Success Response**
```
Status: 200 OK
```
```json
{
  "id": 1,
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "firstName": "Mario",
  "lastName": "Rossi",
  "phoneNumber": "+39123456789",
  "role": "USER",
  "enabled": true,
  "emailVerified": false,
  "createdAt": "2024-02-12T10:30:00",
  "updatedAt": "2024-02-12T10:30:00"
}
```

**Error Response**

401 Unauthorized - Token mancante/invalido
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 401,
  "error": "Unauthorized",
  "message": "Full authentication is required"
}
```

404 Not Found - Utente non trovato
```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 404,
  "error": "Not Found",
  "message": "Utente non trovato"
}
```

---

### 6. Update Profile

Aggiorna il profilo dell'utente autenticato.

**Endpoint**
```http
PUT /api/users/me
```

**Request Headers**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**
```json
{
  "firstName": "Mario Giovanni",
  "lastName": "Rossi",
  "phoneNumber": "+39987654321",
  "email": "mario.rossi@newmail.com"
}
```

**Notes**
- Tutti i campi sono optional
- Se cambi l'email, emailVerified diventa `false`

**Success Response**
```
Status: 200 OK
```
```json
{
  "id": 1,
  "username": "mrossi",
  "email": "mario.rossi@newmail.com",
  "firstName": "Mario Giovanni",
  "lastName": "Rossi",
  "phoneNumber": "+39987654321",
  "role": "USER",
  "enabled": true,
  "emailVerified": false,
  "createdAt": "2024-02-12T10:30:00",
  "updatedAt": "2024-02-12T11:00:00"
}
```

**Error Response**

400 Bad Request - Email già in uso
```json
{
  "timestamp": "2024-02-12T11:00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Email già in uso"
}
```

---

## Token Usage

### Access Token

Usato per autenticare le richieste agli endpoint protetti.

**Header Format**
```
Authorization: Bearer <access_token>
```

**Lifetime**
- Durata: 24 ore (configurabile)
- Scadenza: Ritorna 401 Unauthorized

**Example**
```http
GET /api/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtcm9zc2ki...
```

### Refresh Token

Usato per ottenere un nuovo access token senza reinserire le credenziali.

**Lifetime**
- Durata: 7 giorni (configurabile)
- Scadenza: Deve fare nuovo login

**Flow**
```
1. Access Token scade
   ↓
2. Client invia Refresh Token a /api/auth/refresh
   ↓
3. Server valida e genera nuovo Access Token
   ↓
4. Client usa nuovo Access Token
```

---

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 200 | OK | Richiesta completata con successo |
| 201 | Created | Risorsa creata |
| 204 | No Content | Successo senza body (logout) |
| 400 | Bad Request | Input non valido o errore business |
| 401 | Unauthorized | Non autenticato o token invalido |
| 404 | Not Found | Risorsa non trovata |
| 500 | Internal Server Error | Errore server |

---

## Rate Limiting

Attualmente non implementato. Raccomandato per produzione.

---

## CORS

Origini consentite (configurabile in SecurityConfiguration):
- `http://localhost:3000`
- `http://localhost:8080`

Metodi consentiti:
- GET, POST, PUT, DELETE, OPTIONS

---

## Esempi Completi

### Complete Flow: Register → Login → Access Protected

```bash
# 1. Registra utente
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "firstName": "Test",
    "lastName": "User"
  }'

# Response: Salva accessToken e refreshToken
export ACCESS_TOKEN="<response_accessToken>"
export REFRESH_TOKEN="<response_refreshToken>"

# 2. Accedi endpoint protetto
curl -X GET http://localhost:8080/api/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 3. Refresh token quando scade
curl -X POST http://localhost:8080/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}"

# 4. Logout
curl -X POST http://localhost:8080/api/auth/logout \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}"
```
