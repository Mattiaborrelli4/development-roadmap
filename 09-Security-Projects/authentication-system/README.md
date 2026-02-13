# 🔐 Sistema di Autenticazione Sicuro

Un sistema di autenticazione **production-ready** implementato con Flask e Python. Include tutte le best practices per la sicurezza: password hashing con bcrypt, JWT tokens, 2FA TOTP, rate limiting, audit logging e molto altro.

## 📋 Indice

- [Funzionalità](#-funzionalità)
- [Perché Bcrypt/Argon2](#-perché-bcryptargon2)
- [JWT Best Practices](#-jwt-best-practices)
- [Implementazione 2FA](#-implementazione-2fa)
- [Rate Limiting](#-rate-limiting)
- [Sicurezza delle Sessioni](#-sicurezza-delle-sessioni)
- [Installazione](#-installazione)
- [API Endpoints](#-api-endpoints)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Sicurezza](#-sicurezza)

## ✨ Funzionalità

### Autenticazione
- ✅ **Registrazione utenti** con validazione email
- ✅ **Login sicuro** con password hashing (bcrypt)
- ✅ **Reset password** con token sicuri via email
- ✅ **Verifica email** (opzionale)

### Sicurezza Avanzata
- 🔒 **2FA TOTP** - Autenticazione a due fattori (Google Authenticator compatibile)
- 🔑 **JWT Tokens** - Access token brevi, refresh token lunghi
- 🛡️ **Rate Limiting** - Protezione da brute force
- 📝 **Audit Logging** - Tracciamento completo delle azioni
- 🔐 **Security Headers** - CSP, HSTS, X-Frame-Options, etc.
- 🚫 **CSRF Protection** - Token CSRF per state-changing operations

### Password Policy
- Lunghezza minima 12 caratteri
- Maiuscole, minuscole, numeri, caratteri speciali
- Controllo password comuni
- Storia password (no riutilizzo)

## 🚀 Perché Bcrypt/Argon2

### ❌ NON usare MAI: MD5, SHA1, SHA256

```python
# ❌ SBAGLIATO - Hash veloci
import hashlib
hash = hashlib.sha256(password.encode()).hexdigest()
```

**Perché sono insicuri:**
- **Veloci**: Permettono milioni di tentativi al secondo con GPU
- **Non hanno salt**: Vulnerabili a rainbow table attacks
- **Non adattivi**: L'hardware migliora, ma rimangono veloci

### ✅ USA: Bcrypt o Argon2

```python
# ✅ CORRETTO - Hash lenti e sicuri
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
```

**Vantaggi Bcrypt:**
- **Lento intenzionalmente**: 12 rounds = ~300ms per hash
- **Salt automatico**: Ogni hash è unico
- **Adattivo**: Puoi aumentare i rounds con l'evoluzione dell'hardware

**Vantaggi Argon2:**
- **Resistente a GPU/ASIC**: Memory-hard algorithm
- **Winner Password Hashing Competition 2015**
- **Configurabile**: Puoi bilanciare CPU vs memoria

### Confronto Performance

| Algoritmo | Hash/secondo (GPU) | Sicurezza |
|-----------|-------------------|----------|
| MD5       | 93,000,000,000    | ❌ Insi |
| SHA256    | 13,000,000,000    | ❌ Insicuro |
| Bcrypt(12)| 3,500             | ✅ Sicuro |
| Argon2id  | 500               | ✅✅ Molto Sicuro |

## 🔑 JWT Best Practices

### 1. Short-lived Access Tokens

```python
# ✅ Access token brevi (15-60 minuti)
access_token_expires = timedelta(minutes=15)

# ❌ NO: Token che durano anni
expires = timedelta(days=365)
```

**Perché:** Se un access token viene rubato, la finestra di attacco è limitata.

### 2. Refresh Token Rotation

```python
# ✅ Genera nuovo refresh token ad ogni uso
def refresh_token(old_token):
    # 1. Verifica vecchio token
    # 2. Revoca vecchio token
    # 3. Genera nuovo refresh token
    # 4. Restituisci nuovo access + refresh token
```

**Perché:** Previene il riutilizzo di token compromessi.

### 3. Store Refresh Tokens in Database

```python
# ✅ Salva refresh token nel DB
class RefreshToken(db.Model):
    token = db.Column(db.String(255), unique=True)
    is_revoked = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime)
```

**Perché:** Permette di revocare token in caso di compromissione.

### 4. Use Strong Secrets

```bash
# ❌ SBAGLIATO
SECRET_KEY="secret"

# ✅ CORRETTO
SECRET_KEY=$(openssl rand -hex 32)
```

### 5. Verify Token Type

```python
# ✅ Verifica il tipo di token
def verify_token(token, expected_type='access'):
    payload = decode(token)
    if payload['type'] != expected_type:
        raise InvalidToken()
```

## 📱 Implementazione 2FA

### Cos'è TOTP?

**TOTP** = **Time-based One-Time Password**

- Basato su timestamp + segreto condiviso
- Genera un nuovo codice ogni 30 secondi
- Standard RFC 6238
- Compatibile con Google Authenticator, Authy, etc.

### Setup 2FA

```python
import pyotp

# 1. Genera segreto
secret = pyotp.random_base32()

# 2. Genera URI per QR code
uri = pyotp.TOTP(secret).provisioning_uri(
    name="user@example.com",
    issuer_name="SecureAuthApp"
)

# 3. Genera QR code
# (L'utente lo scansiona con l'app)

# 4. Verifica codice
totp = pyotp.TOTP(secret)
is_valid = totp.verify("123456")
```

### Backup Codes

Se l'utente perde l'accesso all'app autenticatore:

```python
# Genera 10 codici di backup
backup_codes = [secrets.token_hex(4) for _ in range(10)]
# Esempio: ['A1B2C3D4', 'E5F6G7H8', ...]

# Salvali crittografati nel DB
# Ogni codice può essere usato UNA SOLA VOLTA
```

### 2FA vs SMS

| metodo | Sicurezza | Costo | UX |
|--------|----------|-------|-----|
| TOTP   | ✅ Alta | Gratis | Buona |
| SMS    | ⚠️ Media | Costoso | Ottima |
| Email  | ❌ Bassa | Gratis | Buona |

**TOTP è più sicuro perché:**
- Non vulnerabile a SIM swapping
- Non dipende da terze parti
- Funziona offline

## 🚦 Rate Limiting

### Perché è Importante

**Senza rate limiting:**
- Attaccante può fare 1,000,000 tentativi/secondo
- Se password è "Password123", la trova in 1 secondo

**Con rate limiting:**
- 5 tentativi per 5 minuti
- 1,000,000 tentativi = 1,904 giorni 😄

### Implementazione

```python
# Configurazione rate limits
RATE_LIMITS = {
    'login': {'limit': 5, 'period': 300},       # 5 per 5 minuti
    'register': {'limit': 5, 'period': 3600},    # 5 per ora
    'password_reset': {'limit': 3, 'period': 3600},  # 3 per ora
}

# Implementazione
@rate_limit('login', limit=5, period=300)
def login():
    # Codice login
```

### Dove Fare Rate Limiting

1. **Login** - Più importante!
2. **Registrazione** - Previene spam
3. **Reset password** - Previene flooding email
4. **API generali** - Previene DOS

### Backend vs Frontend

```python
# ❌ SBAGLIATO - Solo frontend
if attempts >= 5:
    disable_button()

# ✅ CORRETTO - Backend + Frontend
if rate_limit_exceeded():
    return 429 Too Many Requests
```

**Il frontend è controllabile dall'utente, il backend NO!**

## 🔒 Sicurezza delle Sessioni

### 1. HttpOnly Cookies

```python
# ✅ Cookie HTTP-only
response.set_cookie(
    'session_id',
    value=token,
    httponly=True  # JavaScript non può leggere
)
```

**Perché:** Previene XSS cookie theft.

### 2. Secure Flag

```python
# ✅ Cookie Secure (solo HTTPS)
response.set_cookie(
    'session_id',
    value=token,
    secure=True  # Trasmetti solo su HTTPS
)
```

### 3. SameSite

```python
# ✅ SameSite Strict
response.set_cookie(
    'session_id',
    value=token,
    samesite='Strict'  # Protezione CSRF
)
```

**SameSite Levels:**
- `Strict`: Non invia cookie su navigazione esterna
- `Lax`: Invia solo su navigation sicure
- `None`: Invia sempre (richiede Secure)

### 4. Session Expiration

```python
# ✅ Access token brevi
access_token_expires = 15 minuti

# ✅ Refresh token più lunghi
refresh_token_expires = 30 giorni

# ✅ Ma verificane la validità nel DB
if token.is_revoked or token.is_expired:
    raise InvalidToken()
```

### 5. Revoke on Logout

```python
@app.route('/logout')
def logout():
    # ✅ Revoca refresh token
    token.revoke()
    return jsonify({'success': True})
```

## 📦 Installazione

### Prerequisiti

- Python 3.10+
- pip
- SQLite (development) o PostgreSQL (production)
- Redis (opzionale, per rate limiting distribuito)

### Setup

```bash
# 1. Clona il repository
cd authentication-system

# 2. Crea virtual environment
python -m venv venv

# 3. Attiva virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Installa dipendenze
pip install -r requirements.txt

# 5. Configura variabili d'ambiente
cp .env.example .env
# Modifica .env con i tuoi valori

# 6. Inizializza database
flask init-db

# 7. Crea utente admin (opzionale)
flask create-admin

# 8. Esegui l'app
flask run
```

### Variabili d'Ambiente

```bash
# Required
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///auth.db

# Email (per password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis (opzionale)
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
BCRYPT_LOG_ROUNDS=12
RATE_LIMIT_ENABLED=True
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=300
```

## 🌐 API Endpoints

### Registrazione

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "Mario",
  "last_name": "Rossi"
}

Response 201:
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_verified": false
  }
}
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response 200:
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...},
  "requires_2fa": false
}
```

### 2FA Verification (se abilitato)

```http
POST /auth/verify-2fa
Content-Type: application/json

{
  "email": "user@example.com",
  "totp_code": "123456"
}

Response 200:
{
  "success": true,
  "access_token": "...",
  "refresh_token": "..."
}
```

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Protected Route (Esempio)

```http
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response 200:
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    ...
  }
}
```

### Reset Password

```http
# 1. Richiedi reset
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}

Response 200:
{
  "success": true,
  "message": "Se l'email esiste, riceverai un link"
}

# 2. Resetta con token
POST /auth/reset-password
Content-Type: application/json

{
  "token": "xyz123...",
  "new_password": "NewSecurePass123!"
}

Response 200:
{
  "success": true,
  "message": "Password resettata con successo"
}
```

## 📁 Struttura del Progetto

```
authentication-system/
├── app.py                      # Flask application
├── requirements.txt            # Dipendenze
├── .env.example               # Template variabili ambiente
│
├── auth/                      # Modulo autenticazione
│   ├── __init__.py
│   ├── models.py              # User, AuditLog, etc.
│   ├── routes.py              # API endpoints
│   ├── services.py            # Business logic
│   └── utils.py               # Utility (JWT, hashing, 2FA)
│
├── security/                  # Moduli sicurezza
│   ├── rate_limit.py          # Rate limiting
│   ├── password_policy.py     # Password requirements
│   └── csrf.py                # CSRF protection
│
├── middleware/                # Middleware
│   └── security_headers.py    # HTTP security headers
│
├── templates/                 # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── 2fa.html
│
└── tests/                     # Test
    └── test_auth.py
```

## 🔒 Checklist Sicurezza

### Password
- ✅ Bcrypt/Argon2 hashing (minimo 12 rounds)
- ✅ Password minimo 12 caratteri
- ✅ Complessità richiesta (maiuscole, numeri, speciali)
- ✅ Controllo password comuni
- ❌ NO: MD5, SHA1, SHA256 puri

### Tokens
- ✅ JWT con signature HS256/RS256
- ✅ Access token brevi (15-60 min)
- ✅ Refresh token con rotation
- ✅ Refresh token salvati in DB
- ❌ NO: Token lunghi senza refresh

### 2FA
- ✅ TOTP (non SMS)
- ✅ Backup codes
- ✅ Setup con QR code
- ❌ NO: SMS (quando possibile)

### Rate Limiting
- ✅ Login: 5/5 minuti
- ✅ Registrazione: 5/ora
- ✅ Reset password: 3/ora
- ✅ Implementato su backend

### Sessioni
- ✅ HttpOnly cookies
- ✅ Secure flag (HTTPS only)
- ✅ SameSite=Strict
- ✅ Rotazione refresh token
- ✅ Revoca su logout

### Logging
- ✅ Audit log di ogni azione sensibile
- ✅ IP address e user agent
- ✅ Timestamp precisi
- ✅ Log non modificabili

### Headers
- ✅ Content-Security-Policy
- ✅ Strict-Transport-Security
- ✅ X-Frame-Options
- ✅ X-Content-Type-Options
- ✅ X-XSS-Protection

### Database
- ✅ Password mai in chiaro
- ✅ Crittografia campi sensibili
- ✅ Connection SSL/TLS
- ✅ Query parametrizzate (no SQL injection)

## 🧪 Testing

```bash
# Esegui tutti i test
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Test specifici
pytest tests/test_auth.py::TestPasswordHashing

# Verbose
pytest -v
```

## 🚀 Deployment

### Production Checklist

1. **Variabili ambiente**
   - [ ] SECRET_KEY e JWT_SECRET_KEY forti
   - [ ] DATABASE_URL PostgreSQL
   - [ ] MAIL configurato

2. **HTTPS**
   - [ ] Certificato SSL/TLS
   - [ ] HSTS abilitato
   - [ ] HTTP to HTTPS redirect

3. **Database**
   - [ ] PostgreSQL (non SQLite)
   - [ ] Connection SSL
   - [ ] Backup automatici

4. **Monitoring**
   - [ ] Error logging (Sentry)
   - [ ] Performance monitoring
   - [ ] Uptime monitoring

5. **Redis** (consigliato)
   - [ ] Per rate limiting distribuito
   - [ ] Per session storage

## 📚 Risorse

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [RFC 6238 - TOTP](https://tools.ietf.org/html/rfc6238)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## 📄 Licenza

MIT License - Usa liberamente per i tuoi progetti!

---

**Creato per scopi educativi e di dimostrazione delle best practices di sicurezza.** 🛡️
