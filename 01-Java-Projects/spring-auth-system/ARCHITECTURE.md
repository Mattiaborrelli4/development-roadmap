# Architettura - Spring Auth System

## Architettura ad Alto Livello

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT                                 │
│                    (React/Angular/Vue)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    SPRING BOOT APP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              CONTROLLERS (REST API)                     │   │
│  │  ┌──────────────────────┐  ┌──────────────────────┐   │   │
│  │  │  AuthController      │  │  UserController       │   │   │
│  │  │  - /register         │  │  - GET /me           │   │   │
│  │  │  - /login            │  │  - PUT /me           │   │   │
│  │  │  - /refresh          │  │                      │   │   │
│  │  │  - /logout           │  │                      │   │   │
│  │  └──────────────────────┘  └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  SERVICES (Business Logic)                │   │
│  │  ┌──────────────────┐  ┌──────────────────┐            │   │
│  │  │ AuthService      │  │  RefreshToken    │            │   │
│  │  │  - register()    │  │    Service        │            │   │
│  │  │  - login()       │  │  - create()      │            │   │
│  │  │  - refreshToken()│  │  - verify()      │            │   │
│  │  │  - logout()      │  │  - delete()      │            │   │
│  │  └──────────────────┘  └──────────────────┘            │   │
│  │                                                        │   │
│  │  ┌──────────────────┐  ┌──────────────────┐            │   │
│  │  │  EmailService    │  │  UserDetailsService│           │   │
│  │  │  (Mock)          │  │                   │           │   │
│  │  └──────────────────┘  └──────────────────┘            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              REPOSITORIES (Data Access)                  │   │
│  │  ┌──────────────────┐  ┌──────────────────┐            │   │
│  │  │  UserRepository  │  │ RefreshToken     │            │   │
│  │  │  - JPA           │  │   Repository     │            │   │
│  │  └──────────────────┘  └──────────────────┘            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 DATABASE (H2)                            │   │
│  │           ┌─────────────┐  ┌─────────────────┐          │   │
│  │           │  users      │  │  refresh_tokens │          │   │
│  │           └─────────────┘  └─────────────────┘          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                    SECURITY LAYER                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  JwtAuthenticationFilter                                  │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  1. Extract JWT from Authorization header       │   │   │
│  │  │  2. Validate token signature & expiration       │   │   │
│  │  │  3. Load user details                           │   │   │
│  │  │  4. Set authentication in SecurityContext        │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SecurityConfiguration                                   │   │
│  │  - CORS configuration                                     │   │
│  │  - Public endpoints: /api/auth/**                         │   │
│  │  - Protected endpoints: /api/users/**                     │   │
│  │  - BCrypt password encoder                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  JwtService                                              │   │
│  │  - Generate access tokens (24h)                         │   │
│  │  - Generate refresh tokens (7d)                          │   │
│  │  - Validate & extract claims                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

## Flux di Autenticazione

### 1. Registrazione
```
Client                    Controller                      Service
  │                           │                            │
  ├──── POST /register ──────►│                            │
  │                           ├───── register() ──────────►│
  │                           │                            ├────── existsByUsername() ────► Repository
  │                           │                            │◄───── false ──────────────────┘
  │                           │                            ├────── existsByEmail() ───────► Repository
  │                           │                            │◄───── false ──────────────────┘
  │                           │                            ├────── encode password (BCrypt)
  │                           │                            ├────── save() ─────────────────► Repository
  │                           │                            │◄───── User ────────────────────┘
  │                           │                            ├────── createRefreshToken() ──► RefreshTokenService
  │                           │                            │◄───── RefreshToken ────────────┘
  │                           │                            ├────── generate JWT ────────► JwtService
  │                           │                            │◄───── accessToken ────────────┘
  │                           │                            ├────── sendVerificationEmail() ► EmailService (Mock)
  │                           │                            │
  │◄──── AuthResponse ────────┤                            │
  │   (accessToken,           │                            │
  │    refreshToken)          │                            │
```

### 2. Login
```
Client                    AuthManager                    Service
  │                           │                            │
  ├──── POST /login ─────────►│                            │
  │                           ├───── authenticate() ───────►│
  │                           │                            │
  │                           │                            ├───── loadUserByUsername() ──► Repository
  │                           │                            │◄───── UserDetails ────────────┘
  │                           │                            │
  │                           │                            ├───── verify password (BCrypt)
  │                           │                            │
  │                           │                            ├───── generate JWT ────────► JwtService
  │                           │                            │◄───── accessToken ────────────┘
  │                           │                            ├───── createRefreshToken() ──► RefreshTokenService
  │                           │                            │◄───── RefreshToken ────────────┘
  │                           │                            │
  │◄──── AuthResponse ────────┤                            │
```

### 3. Accesso a Endpoint Protetto
```
Client                    JwtFilter                   Service
  │                           │                            │
  ├──── GET /api/users/me ───►│                            │
  │   (Authorization: Bearer   │                            │
  │    <token>)               │                            │
  │                           ├───── extractUsername() ────► JwtService
  │                           │◄───── username ────────────┘
  │                           ├───── loadUserByUsername() ─► UserDetailsService
  │                           │◄───── UserDetails ──────────┘
  │                           ├───── isTokenValid() ───────► JwtService
  │                           │◄───── true ─────────────────┘
  │                           ├───── Set Authentication    │
  │                           │       in SecurityContext   │
  │                           │                            │
  │                           ├───── getCurrentUser() ────► Service
  │                           │                            │◄──── UserResponse ┐
  │◄──── UserResponse ────────┤                            │                 │
  │                           │                            │                 │
```

## Componenti Chiave

### DTOs (Data Transfer Objects)
```
Request DTOs:
- RegisterRequest     : Dati registrazione
- LoginRequest        : Credenziali login
- RefreshTokenRequest : Token di refresh
- UpdateUserRequest   : Aggiornamento profilo

Response DTOs:
- AuthenticationResponse: Token + info utente
- UserResponse        : Profilo utente completo
```

### Entities (JPA)
```
User:
- id, username, password (BCrypt), email
- firstName, lastName, phoneNumber
- role, enabled, emailVerified
- verificationToken
- createdAt, updatedAt

RefreshToken:
- id, token (UUID), user (FK)
- expiryDate, revoked
- createdAt
```

### Security Flow
```
1. User registers → Account creato ma email non verificata
2. Email inviata (mock) con token verifica
3. User login → Credenziali verificate
4. JWT generato → Access token (24h) + Refresh token (7d)
5. Richieste successive → Authorization: Bearer <token>
6. Token scaduto → Usa refresh token per nuovo access token
7. Logout → Refresh token revocato/cancellato
```

## Dettagli Tecnici

### JWT Structure
```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "username",
  "role": "USER",
  "iat": 1234567890,
  "exp": 1234567890
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

### Password Encoding
```
Plain Password: "password123"
        │
        ▼
BCryptPasswordEncoder (cost=10)
        │
        ▼
Hash: $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
       │                                                    │
       └─ Hash ─────────────────────────────────────┘        │
            └─ Salt ───────────────────────┘                  │
                 └─ Cost factor ──┘                          │
                                                              │
Verification: hash.equals(BCrypt.hash(plain, salt))
```

### Refresh Token Strategy
```
1. Login → Genera UUID random come refresh token
2. Salva nel DB con expiry date (7 giorni)
3. Client salva token in localStorage/cookie
4. Quando access token scade:
   - Client invia refresh token
   - Server verifica esistenza, expiry, non revocato
   - Genera nuovo access token
   - (Opzionale) Ruota refresh token
5. Logout → Cancella/Revoca refresh token dal DB
```

## Security Best Practices Implementate

✅ **Password Security**
- BCrypt hashing con cost factor 10
- Nessuna password in chiaro nel DB
- Validazione lunghezza password (6-100 caratteri)

✅ **JWT Security**
- Signature con HMAC-SHA256
- Expiration check
- Secret key sufficientemente lunga (256+ bit)

✅ **API Security**
- CORS configurato
- CSRF disabilitato (stateless REST API)
- Session stateless
- Public/Private endpoints chiaramente separati

✅ **Data Security**
- Validazione input con Jakarta Validation
- Unique constraints su username e email
- Transaction management con @Transactional

⚠️ **Da migliorare per Produzione**
- Usare database persistente (PostgreSQL/MySQL)
- Implementare rate limiting
- Aggiungere 2FA
- Usare variabili d'ambiente per segreti
- Implementare email verification reale
- HTTPS obbligatorio
- Password history e complexity requirements
