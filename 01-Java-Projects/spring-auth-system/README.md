# Sistema di Autenticazione Spring Boot

Sistema di autenticazione completo con JWT, H2 database e Spring Security 6.

## Caratteristiche

- ✅ Registrazione utente con email
- ✅ Login con JWT token
- ✅ Refresh token endpoint
- ✅ Protected /me endpoint
- ✅ Logout (invalidate refresh token)
- ✅ Profilo utente CRUD
- ✅ BCrypt password hashing
- ✅ Email verification mock
- ✅ H2 in-memory database
- ✅ Validazione delle richieste

## Tecnologie

- **Spring Boot** 3.2.5
- **Spring Security** 6
- **Spring Data JPA**
- **JWT** (jjwt-api 0.12.5)
- **H2 Database**
- **Maven**
- **Lombok**
- **Jakarta Validation**

## Prerequisiti

- Java 17 o superiore
- Maven 3.6+

## Configurazione

Il file `application.properties` contiene tutte le configurazioni necessarie:

```properties
# JWT Secret (cambiare in produzione)
jwt.secret=LaTuaChiaveSegretaSuperSegretaPerJWTToken123456789012345678901234567890

# JWT Expiration (ms)
jwt.expiration=86400000        # 24 ore
jwt.refresh-expiration=604800000 # 7 giorni
```

## Installazione ed Esecuzione

1. Clone o scarica il progetto

2. Compila il progetto:
```bash
mvn clean install
```

3. Esegui l'applicazione:
```bash
mvn spring-boot:run
```

L'applicazione sarà disponibile su `http://localhost:8080`

## API Endpoints

### Autenticazione

#### Registrazione
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "password": "password123",
  "firstName": "Mario",
  "lastName": "Rossi",
  "phoneNumber": "+39123456789"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "message": "Registrazione completata. Controlla la tua email per verificare l'account."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "usernameOrEmail": "mrossi",
  "password": "password123"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000",
  "username": "mrossi",
  "email": "mario.rossi@example.com",
  "message": "Login effettuato con successo"
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Logout
```http
POST /api/auth/logout
Content-Type: application/json

{
  "refreshToken": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Profilo Utente (Protetto)

Tutti gli endpoint richiedono l'header:
```
Authorization: Bearer <access_token>
```

#### Get Current User
```http
GET /api/users/me
```

**Response:**
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

#### Update Profile
```http
PUT /api/users/me
Content-Type: application/json

{
  "firstName": "Mario Giovanni",
  "lastName": "Rossi",
  "phoneNumber": "+39987654321",
  "email": "mario.rossi@newmail.com"
}
```

## H2 Console

Puoi accedere alla console H2 per vedere i dati nel database:

**URL:** `http://localhost:8080/h2-console`

**JDBC URL:** `jdbc:h2:mem:authdb`

**Username:** `sa`

**Password:** (lascia vuoto)

## Schema Database

### Tabella `users`
- `id` - Primary Key
- `username` - Unique
- `password` - BCrypt hash
- `email` - Unique
- `first_name`
- `last_name`
- `phone_number`
- `role` - USER, ADMIN
- `enabled` - Boolean
- `email_verified` - Boolean
- `verification_token`
- `created_at`
- `updated_at`

### Tabella `refresh_tokens`
- `id` - Primary Key
- `token` - Unique (UUID)
- `user_id` - Foreign Key
- `expiry_date`
- `revoked` - Boolean
- `created_at`

## Validazione

Le richieste sono validate con Jakarta Validation:

- **username**: 3-50 caratteri, obbligatorio
- **email**: formato email valido, obbligatorio
- **password**: 6-100 caratteri, obbligatorio
- **firstName**: 3-50 caratteri
- **lastName**: 3-50 caratteri
- **phoneNumber**: 9-15 caratteri

## Error Handling

L'API restituisce errori in formato JSON:

```json
{
  "timestamp": "2024-02-12T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Email già in uso"
}
```

### Codici di Errore

- `400 Bad Request` - Validazione fallita, business logic error
- `401 Unauthorized` - Credenziali non valide
- `404 Not Found` - Risorsa non trovata
- `500 Internal Server Error` - Errore server

## Email Verification (Mock)

Il sistema include un servizio email mock che logga il contenuto delle email nella console. Per vedere i token di verifica, controlla i log dell'applicazione dopo la registrazione.

Esempio di log:
```
===========================================
MOCK EMAIL - Verifica Email
===========================================
A: user@example.com
Oggetto: Verifica il tuo account
Messaggio:
Ciao,

Per verificare il tuo account, clicca sul link seguente:
http://localhost:8080/api/auth/verify?token=<uuid>

Questo link scadrà tra 24 ore.
===========================================
```

## Sicurezza

- Password hash con BCrypt
- JWT token con firma HMAC-SHA256
- Refresh token con scadenza e revoca
- CORS configurato per frontend
- Session stateless
- Protezione CSRF disabilitata (per API REST)

## Sviluppo

### Struttura del Progetto
```
src/main/java/com/example/auth/
├── config/                  # Configurazioni
│   └── SecurityConfiguration.java
├── controller/              # REST Controllers
│   ├── AuthenticationController.java
│   └── UserController.java
├── dto/                     # Data Transfer Objects
│   ├── RegisterRequest.java
│   ├── LoginRequest.java
│   ├── RefreshTokenRequest.java
│   ├── AuthenticationResponse.java
│   ├── UserResponse.java
│   └── UpdateUserRequest.java
├── exception/               # Gestione Eccezioni
│   ├── ResourceNotFoundException.java
│   └── GlobalExceptionHandler.java
├── model/                   # Entità JPA
│   ├── User.java
│   └── RefreshToken.java
├── repository/              # Repository JPA
│   ├── UserRepository.java
│   └── RefreshTokenRepository.java
├── security/                # Security & JWT
│   ├── JwtService.java
│   └── JwtAuthenticationFilter.java
├── service/                 # Business Logic
│   ├── AuthenticationService.java
│   ├── UserDetailsServiceImpl.java
│   ├── RefreshTokenService.java
│   └── EmailService.java
└── AuthApplication.java     # Main Class
```

### Test

Esegui i test:
```bash
mvn test
```

## Prossimi Passi

Possibili miglioramenti:

- [ ] Implementare verifica email reale
- [ ] Aggiungere reset password
- [ ] Implementare ruoli multipli (USER, ADMIN)
- [ ] Rate limiting
- [ ] OAuth2 (Google, Facebook)
- [ ] 2FA (Two-Factor Authentication)
- [ ] Swagger/OpenAPI documentation
- [ ] Database PostgreSQL/MySQL
- [ ] Caching con Redis
- [ ] Logging e monitoring

## Licenza

Questo progetto è creato a scopo educativo.

## Autore

Creato come esempio di sistema di autenticazione con Spring Boot 3 e JWT.
