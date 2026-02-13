# Guida Rapida - Spring Auth System

## Avvio Rapido

### 1. Compilare il Progetto
```bash
cd spring-auth-system
mvn clean install
```

### 2. Avviare l'Applicazione
```bash
mvn spring-boot:run
```

### 3. Testare l'API

#### Registrazione
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "firstName": "Test",
    "lastName": "User"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "usernameOrEmail": "testuser",
    "password": "password123"
  }'
```

Salva `accessToken` e `refreshToken` dalla risposta!

#### Accesso Endpoint Protetto
```bash
curl -X GET http://localhost:8080/api/users/me \
  -H "Authorization: Bearer <tuo-access-token>"
```

## Console H2

- **URL**: http://localhost:8080/h2-console
- **JDBC URL**: `jdbc:h2:mem:authdb`
- **Username**: `sa`
- **Password**: (vuoto)

## Struttura Database

```sql
-- Query per vedere tutti gli utenti
SELECT * FROM users;

-- Query per vedere i refresh token
SELECT * FROM refresh_tokens;

-- Query per verificare un utente specifico
SELECT * FROM users WHERE username = 'testuser';
```

## Troubleshooting

### Porta già in uso
Cambia la porta in `application.properties`:
```properties
server.port=8081
```

### Errori JWT
Verifica che `jwt.secret` sia encodato in Base64 e sia almeno 256 bit (32 byte).

### Errori di validazione
Verifica che tutti i campi obbligatori siano presenti:
- username: 3-50 caratteri
- email: formato valido
- password: 6-100 caratteri

## Prossimi Passi

1. Importa il progetto in IntelliJ IDEA o Eclipse
2. Esplora i controller in `src/main/java/com/example/auth/controller/`
3. Leggi la documentazione completa nel README.md
4. Prova gli endpoint con Postman o Insomnia
