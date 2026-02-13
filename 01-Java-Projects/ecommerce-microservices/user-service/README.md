# User Service

Microservizio per la gestione degli utenti nel sistema e-commerce.

## Porta

8081

## Database

H2 in-memory: `jdbc:h2:mem:userdb`

## API Endpoints

### Registrazione Utente

```http
POST /api/users/register
Content-Type: application/json

{
  "username": "mario.rossi",
  "email": "mario@email.com",
  "password": "password123",
  "firstName": "Mario",
  "lastName": "Rossi",
  "phoneNumber": "+39 333 1234567",
  "address": "Via Roma 1, Milano"
}
```

### Login

```http
POST /api/users/login
Content-Type: application/json

{
  "username": "mario.rossi",
  "password": "password123"
}
```

### Ottieni Tutti gli Utenti

```http
GET /api/users
```

### Ottieni Utente per ID

```http
GET /api/users/{id}
```

### Ottieni Utente per Username

```http
GET /api/users/username/{username}
```

### Aggiorna Profilo

```http
PUT /api/users/{id}
Content-Type: application/json

{
  "firstName": "Mario Updated",
  "lastName": "Rossi",
  "phoneNumber": "+39 333 7654321",
  "address": "Via Milano 1, Roma"
}
```

### Elimina Utente

```http
DELETE /api/users/{id}
```

### Valida Utente (usato da altri servizi)

```http
GET /api/users/validate/{id}
```

Ritorna `true` se l'utente esiste, `false` altrimenti.

## Avvio

```bash
mvn spring-boot:run
```

## H2 Console

http://localhost:8081/h2-console

JDBC URL: `jdbc:h2:mem:userdb`
Username: `sa`
Password: (vuota)
