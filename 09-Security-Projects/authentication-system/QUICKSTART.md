# 🚀 Quick Start Guide

Guida rapida per iniziare con il Sistema di Autenticazione Sicuro.

## Setup in 3 Minuti

### 1. Installazione

```bash
# Virtual environment
python -m venv venv

# Attiva (Windows)
venv\Scripts\activate

# Attiva (Linux/Mac)
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Configurazione

```bash
# Copia il file environment
copy .env.example .env

# Modifica .env con i tuoi valori
# Minimo richiesto:
SECRET_KEY=chiave-segreta-molto-lunga-casuale
JWT_SECRET_KEY=altra-chiave-segreta-molto-lunga
```

### 3. Database

```bash
# Inizializza il database
flask init-db

# Crea utente admin (opzionale)
flask create-admin
```

### 4. Avvia l'App

```bash
# Sviluppo
flask run

# Produzione
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Visita: `http://localhost:5000`

## 📡 Test API

### Registra Utente

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "first_name": "Mario",
    "last_name": "Rossi"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

### Accesso Protetto

```bash
# Salva il token dalla risposta di login
TOKEN="your-access-token-here"

# Accedi a route protetta
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 Test

```bash
# Esegui tutti i test
pytest

# Con coverage
pytest --cov=. --cov-report=html
```

## 📝 Note Importanti

### ⚠️ Per Produzione

1. **HTTPS obbligatorio**
   ```bash
   # Usa gunicorn con certificato SSL
   gunicorn --keyfile key.pem --certfile cert.pem app:app
   ```

2. **Database PostgreSQL**
   ```bash
   # Modifica .env
   DATABASE_URL=postgresql://user:pass@localhost/authdb
   ```

3. **Strong Secrets**
   ```bash
   # Genera secrets sicuri
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **Redis per Rate Limiting**
   ```bash
   # Installa Redis
   # Modifica .env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

### 🔐 Password Policy Default

- Minimo 12 caratteri
- Almeno 1 maiuscola
- Almeno 1 minuscola
- Almeno 1 numero
- Almeno 1 carattere speciale

### 📱 2FA Setup

L'utente può abilitare 2FA dalla dashboard:

1. Richiedi abilitazione 2FA: `POST /auth/enable-2fa`
2. Scansiona QR code con Google Authenticator
3. Inserisci codice di verifica: `POST /auth/confirm-2fa`
4. Salva backup codes in luogo sicuro!

## 🛠️ Troubleshooting

### Errore: "No module named 'flask'"

```bash
# Assicurati di aver attivato il virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstalla dipendenze
pip install -r requirements.txt
```

### Errore: "Database is locked"

```bash
# Chiudi tutte le connessioni al database
# Se su Windows, verifica nessun programma abbia aperto auth.db
```

### Rate Limiting attivo nei test

```bash
# Disabilita rate limiting per test
# In .env:
RATE_LIMIT_ENABLED=False
```

## 📚 Prossimi Passi

1. **Personalizza i template** in `templates/`
2. **Modifica la password policy** in `security/password_policy.py`
3. **Aggiungi nuove rotte** in `auth/routes.py`
4. **Configura email** per password reset
5. **Deploy su produzione** con HTTPS + PostgreSQL

## 🔗 Risorse Utili

- [Documentazione Flask](https://flask.palletsprojects.com/)
- [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)

---

Buon coding! 🎉
