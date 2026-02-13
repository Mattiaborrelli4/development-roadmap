# 🔐 Password Generator & Manager

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-AES--256--GCM-red.svg)](https://cryptography.io/)
[![Type](https://img.shields.io/badge/Type-Utility-purple.svg)]()

> Un potente strumento Python per generare password sicure e gestirle con crittografia AES-256-GCM.

---

## 📋 Indice

- [Introduzione](#introduzione)
- [Caratteristiche Principali](#caratteristiche-principali)
- [Installazione](#installazione)
- [Avvio Rapido](#avvio-rapido)
- [Spiegazione del Codice](#spiegazione-del-codice)
- [Funzionalità e Comandi](#funzionalità-e-comandi)
- [Sicurezza e Best Practices](#sicurezza-e-best-practices)
- [Esempi di Utilizzo](#esmpi-di-utilizzo)
- [Troubleshooting](#troubleshooting)
- [Architettura](#architettura)
- [API Reference](#api-reference)
- [License](#license)

---

## 🎯 Introduzione

Il **Password Generator & Manager** è un'applicazione CLI (Command Line Interface) progettata per studenti e sviluppatori che vogliono comprendere come funzionano i sistemi di gestione password sicuri.

### Cos'è un Password Manager?

Un password manager è un'applicazione che:
- **Genera password complesse e uniche** per ogni servizio
- **Memorizza in modo sicuro** le credenziali
- **Crittografa i dati** con algoritmi di grado militare
- **Semplifica la gestione** della sicurezza digitale

### Perché questo progetto?

Questo progetto è perfetto per:
- 📚 **Studenti**: Imparare concetti di crittografia pratica
- 🔧 **Sviluppatori**: Esempio di Python utilities ben strutturato
- 💼 **Portfolio**: Dimostrare competenze in sicurezza e programmazione
- 🔒 **Utilizzo reale**: Gestire le proprie password in modo sicuro

---

## ✨ Caratteristiche Principali

### 🔑 Generazione Password Sicura
- **Algoritmo crittograficamente sicuro**: Usa `secrets` (non `random`)
- **Personalizzazione completa**: Lunghezza, caratteri, esclusioni
- **Profili predefiniti**: Work, Personal, PIN
- **Passphrase support**: Genera frasi password facili da memorizzare

### 📊 Misurazione Qualità (Entropy)
- **Calcolo entropia in bit**: Misura matematica della sicurezza
- **Strength meter**: Valutazione immediata della robustezza
- **Analisi composizione**: Verifica maiuscole, numeri, simboli
- **Controllo password comuni**: Database delle password più usate

### 🔒 Crittografia AES-256-GCM
- **Algoritmo AES-256**: Standard di crittografia militare
- **Modalità GCM**: Autenticazione integrata
- **Salt random**: Ogni crittografia è unica
- **PBKDF2-HMAC-SHA256**: Derivazione chiave con 100.000 iterazioni

### 👥 Gestione Profili
- **Multi-servizio**: Salva password per siti diversi
- **Metadati**: Username, note, timestamp
- **Ricerca avanzata**: Filtra per servizio o username
- **Import/Export**: JSON per portabilità

### 📋 Clipboard Integration
- **Copia automatica**: Password pronta per essere incollata
- **Modalità show**: Visualizza password se necessario
- **Masking predefinito**: Protezione da shoulder surfing

### 🛡️ Sicurezza Avanzata
- **Database cifrato**: Tutte le password protette
- **Password master**: Una sola password da ricordare
- **Backup integrati**: Salvataggio automatico dello stato
- **Nessuna classe**: Codice procedurale semplice e comprensibile

---

## 🚀 Installazione

### Prerequisiti

- **Python 3.10 o superiore**
- **Pip** (gestore pacchetti Python)
- **Sistema operativo**: Windows, macOS, Linux

### Dipendenze

```bash
pip install cryptography pyperclip
```

| Libreria | Versione | Scopo |
|----------|----------|-------|
| `cryptography` | 41.0+ | Crittografia AES-256-GCM |
| `pyperclip` | 1.8+ | Copia negli appunti |

### Installazione del Progetto

```bash
# Clona o scarica il progetto
cd path/to/04-Python-Projects/password-manager

# Verifica Python
python --version  # Python 3.10+

# Installa dipendenze
pip install cryptography pyperclip
```

### Test di Installazione

```bash
python password_generator.py --help
```

---

## 🎮 Avvio Rapido

### 1. Genera la tua prima password

```bash
python password_generator.py --length 20
```

**Output:**
```
Password generata: K9#mP2$vL5@xR8&nW3
Livello: MOLTO FORTE
Entropia: 131.2 bit
[Copiata negli appunti]
```

### 2. Genera una passphrase memorizzabile

```bash
python password_generator.py --passphrase --words 6
```

**Output:**
```
Passphrase generata: albero-mare-libro-tempo-castello-fiore
Entropia: 78.4 bit
```

### 3. Salva una password con crittografia

```bash
python password_generator.py --add github --user "me@email.com" --encrypt
```

### 4. Recupera una password

```bash
python password_generator.py --get github --copy --show
```

---

## 📚 Spiegazione del Codice

Il progetto è strutturato in sezioni funzionali chiare, senza l'uso di classi, per rendere il codice accessibile ai principianti.

### Struttura del File

```python
#!/usr/bin/env python3
"""
Password Generator & Manager
Utility per la generazione e gestione sicura di password.
"""

# 1. Import e Configurazione
import os, sys, json, base64, secrets, string, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 2. Costanti Globali
DEFAULT_LENGTH = 16
DB_FILE = "passwords.json"

# 3. Utility Functions
# 4. Password Generation
# 5. Cryptography (AES-256-GCM)
# 6. Database Management
# 7. Password CRUD Operations
# 8. CLI Interface
```

---

### Funzioni Principali

#### 1. `calculate_entropy(password: str) -> float`

**Concetto:** L'entropia misura l'imprevedibilità di una password.

```python
def calculate_entropy(password: str) -> float:
    """
    Entropia = lunghezza × log₂(pool_size)
    """
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26  # a-z
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26  # A-Z
    if any(c in string.digits for c in password):
        pool_size += 10  # 0-9
    if any(c in string.punctuation for c in password):
        pool_size += 32  # Simboli

    import math
    return len(password) * math.log2(pool_size)
```

**Tabella Entropia:**

| Bit | Sicurezza | Cracking Time (a 100B/s) |
|-----|-----------|--------------------------|
| < 28 | Molto Debole | Istantaneo |
| 28-35 | Debole | Secondi |
| 36-59 | Discreta | Giorni |
| 60-79 | Forte | Anni |
| 80+ | Molto Forte | Secoli |

#### 2. `generate_password()` - Generazione Sicura

**Differenza critica:** `secrets` vs `random`

```python
# ❌ SBAGLIATO - Non crittograficamente sicuro
import random
password = "".join(random.choice(chars) for _ in range(length))

# ✅ GIUSTO - Crittograficamente sicuro
import secrets
password = "".join(secrets.choice(chars) for _ in range(length))
```

**Perché `secrets`?**
- Usa l'OS CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
- Non prevedibile anche conoscendo lo stato interno
- Progettato specificamente per sicurezza

#### 3. Crittografia AES-256-GCM

**Workflow di Crittografia:**

```
Password Master
      ↓
  PBKDF2-HMAC-SHA256 (100,000 iterazioni)
      ↓
  Chiave derivata (256 bit)
      ↓
  AES-256-GCM Encryption
      ↓
  Salt + Nonce + Ciphertext
      ↓
  Base64 Encoding
      ↓
  JSON Salvato
```

**Implementazione:**

```python
def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    PBKDF2: Password-Based Key Derivation Function 2
    - 100,000 iterazioni di rallentamento
    - SHA256 come hash function
    - Output: 32 bytes (256 bit)
    """
    return hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        100000,  # Iterazioni
        dklen=32  # 256 bit
    )

def encrypt_data(data: str, password: str) -> dict:
    """
    AES-256-GCM:
    - AES: Advanced Encryption Standard
    - 256: Chiave di 256 bit
    - GCM: Galois/Counter Mode (con autenticazione)
    """
    salt = secrets.token_bytes(16)     # Salt casuale
    nonce = secrets.token_bytes(12)    # Nonce unico
    key = derive_key(password, salt)   # Deriva chiave

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data.encode(), None)

    return {
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }
```

**Perché AES-256-GCM?**

| Caratteristica | Descrizione |
|----------------|-------------|
| **AES-256** | Standard FIPS-approved per dati TOP SECRET |
| **GCM** | Fornisce sia crittografia che autenticazione |
| **Nonce** | Numero usato una sola volta per prevenire replay attacks |
| **Salt** | Rende unico ogni ciphertext anche con stessa password |

#### 4. Gestione Database JSON

**Struttura Database (non cifrato):**

```json
{
  "encrypted": false,
  "passwords": {
    "github": {
      "username": "user@email.com",
      "password": "K9#mP2$vL5@xR8&nW3",
      "notes": "Account principale",
      "created_at": "a1b2c3d4"
    },
    "netflix": {
      "username": "user@email.com",
      "password": "N3tf!ix@Pass#9K",
      "notes": "Condiviso con famiglia",
      "created_at": "e5f6g7h8"
    }
  }
}
```

**Struttura Database (cifrato):**

```json
{
  "encrypted": true,
  "version": "1.0",
  "encrypted_data": {
    "salt": "YWJjZGVmZ2hpams=",
    "nonce": "bW5vcHFyc3R1dnd4",
    "ciphertext": "3q7+9K2j/mN8pL4hR5t..."
  }
}
```

---

## 🎛️ Funzionalità e Comandi

### Generazione Password

#### Opzioni Base

```bash
# Lunghezza personalizzata
python password_generator.py --length 24

# Escludi simboli
python password_generator.py --exclude_symbols

# Escludi caratteri specifici
python password_generator.py --exclude "<>{}[]|\\/"

# Solo lettere e numeri (no simboli, no maiuscole)
python password_generator.py --exclude_symbols --exclude_upper
```

#### Profili Predefiniti

| Profilo | Lunghezza | Caratteristiche | Use Case |
|---------|-----------|-----------------|----------|
| `work` | 20 | Tutto, esclude simboli problematici | Enterprise, sistemi legacy |
| `personal` | 16 | Tutto incluso | Web moderno, app |
| `pin` | 6 | Solo numeri | Codici PIN, OTP |

```bash
# Usa profilo work
python password_generator.py --profile work

# Usa profilo personal
python password_generator.py --profile personal

# Usa profilo pin
python password_generator.py --profile pin
```

#### Passphrase (Password Frase)

```bash
# Genera passphrase di 5 parole
python password_generator.py --passphrase

# Genera passphrase di 8 parole
python password_generator.py --passphrase --words 8

# Passphrase con separatore custom (tramite codice)
python password_generator.py --passphrase --words 6
```

**Vantaggi Passphrase:**
- 📖 Più facili da memorizzare
- 🗣️ Facili da dettare (no "O maiuscola o zero")
- 🔒 Spesso più sicure di password corte
- ♾️ Entropia teorica illimitata

---

### Gestione Password

#### Salvare una Password

```bash
# Genera e salva
python password_generator.py --add github --user "me@email.com" --encrypt

# Salva password specifica
python password_generator.py --add netflix --user "me@email.com" \
  --password "MiaPassword123!" --notes "Condiviso" --encrypt
```

#### Recuperare una Password

```bash
# Mostra (mascherata per default)
python password_generator.py --get github

# Mostra in chiaro e copia
python password_generator.py --get github --show --copy

# Con password master
python password_generator.py --get github --master "MasterPass123!"
```

#### Listare Password

```bash
# Lista tutte
python password_generator.py --list

# Con password master
python password_generator.py --list --master "MasterPass123!"

# Cerca specifica
python password_generator.py --list --search github
```

#### Eliminare Password

```bash
# Elimina (richiede conferma)
python password_generator.py --delete github --master "MasterPass123!"
```

---

### Analisi e Controllo

#### Analizzare Qualità Password

```bash
# Analisi completa
python password_generator.py --check "MiaPassword123!"
```

**Output:**
```
Analisi Password: **************
Lunghezza: 13 caratteri
Entropia: 68.4 bit
Livello: FORTE
Descrizione: Password sicura
Password comune: NO

Composizione:
  Maiuscole: ✓
  Minuscole: ✓
  Cifre: ✓
  Simboli: ✓
```

#### Check Specifici

```bash
# Solo entropia (per script)
python password_generator.py --check "Password123!" --entropy
# Output: 57.0

# Solo strength rating
python password_generator.py --check "Password123!" --strength
# Output: DISCRETA

# Verifica se comune
python password_generator.py --check "password" --check_common
# Output: Comune: True
```

---

### Import/Export

```bash
# Esporta in JSON non cifrato (ATTENZIONE: file non protetto!)
python password_generator.py --export backup.json --master "MasterPass!"

# Importa da file
python password_generator.py --import backup.json \
  --master "MasterPass!" --encrypt
```

⚠️ **ATTENZIONE:** I file esportati sono in chiaro! Gestiscili con cautela.

---

### Backup

```bash
# Crea backup del database
python password_generator.py --backup --master "MasterPass!"
```

I backup sono salvati nella directory `backups/` con nome `backup_<hex>.json`.

---

## 🔐 Sicurezza e Best Practices

### Crittografia AES-256-GCM

L'implementazione segue questi principi:

#### 1. **Chiave Derivazione**
```
Password Master (umana) → Salt Random → PBKDF2 × 100,000 → Chiave 256-bit
```

**Perché 100,000 iterazioni?**
- Rallenta attacchi brute-force
- Ogni tentativo richiede ~0.1 secondi
- 1 miliardo di tentativi ≈ 3.17 anni

#### 2. **Salt Random**
```python
salt = secrets.token_bytes(16)  # 128 bit casuali
```

**Perché?**
- Stessa password + salt diverso = chiave diversa
- Previene attacchi rainbow table
- Ogni crittografia è unica

#### 3. **Nonce Unico**
```python
nonce = secrets.token_bytes(12)  # 96 bit unici
```

**Perché?**
- AES-GCM richiede nonce unico per ogni encrypt
- Mai riutilizzare nonce con stessa chiave
- 96 bit = collisioni statisticamente impossibili

---

### Password Strength Meter

#### Entropia e Tempo di Cracking

Assumendo:
- 100 miliardi di tentativi/secondo (hardware specializzato)
- Nessuna conoscenza preliminare della password

| Entropia | Combinazioni | Tempo di Cracking | Sicurezza |
|----------|--------------|-------------------|-----------|
| 28 bit | 268 milioni | < 1 secondo | ❌ Inaccettabile |
| 36 bit | 68 miliardi | < 1 secondo | ❌ Molto debole |
| 40 bit | 1.1 trilioni | 11 secondi | ⚠️ Debole |
| 52 bit | 4.5 quadrilioni | 12.5 ore | ⚠️ Discreta |
| 60 bit | 1.15 quintilioni | 115 giorni | ✅ Forte |
| 64 bit | 18.4 quintilioni | 5 anni | ✅ Forte |
| 80 bit | 1.2 septilioni | 391 anni | ✅✅ Molto forte |
| 128 bit | 3.4 × 10³⁸ | 108 bilioni di anni | ✅✅✅ Inattaccabile |

#### Password Comuni da Evitare

Le 20 password più comuni (NON usarle mai):

```
1. password
2. 123456
3. 12345678
4. qwerty
5. abc123
6. monkey
7. 1234567890
8. letmein
9. trustno1
10. dragon
11. baseball
12. 111111
13. iloveyou
14. master
15. sunshine
16. ashley
17. bailey
18. passw0rd
19. shadow
20. 123123
```

---

### Gestione Sicura del File JSON

#### Best Practices

1. **File Permissions**
   ```bash
   # Linux/macOS: Limita accesso al solo proprietario
   chmod 600 passwords.json
   ```

2. **Location Strategy**
   ```bash
   # Non salvare nella home directory
   # Usa invece:
   ~/.config/password-manager/    # Linux
   ~/Library/Application Support/  # macOS
   %APPDATA%/password-manager/     # Windows
   ```

3. **Non Loggare Password**
   ```python
   # ❌ SBAGLIATO
   print(f"Password: {password}")

   # ✅ GIUSTO
   print(f"Password: {'*' * len(password)}")
   ```

4. **Memory Security**
   ```python
   # Python non ha secure memory, ma possiamo minimizzare:
   password = get_password()
   # Usa password immediatamente
   encrypted = encrypt(data, password)
   # Pulisci riferimento (non garantisce eliminazione memoria)
   del password
   ```

---

## 💡 Esempi di Utilizzo

### Esempio 1: Setup Iniziale

```bash
# 1. Crea password master molto forte
python password_generator.py --length 32 --exclude "<>\"'"

# Output: rT8#kL2@mP9&xV4$nW6!qY3+zA7*cH5

# 2. Salva prima password
python password_generator.py --add github --user "dev@email.com" \
  --password "rT8#kL2@mP9&xV4$nW6!qY3+zA7*cH5" --encrypt

# Ti chiederà la password master per criptare il DB
```

### Esempio 2: Workflow Completo

```bash
# Genera password per servizio web
python password_generator.py --profile work --add netflix \
  --user "me@email.com" --encrypt

# Recupera password quando serve
python password_generator.py --get netflix --copy --show

# Lista tutti i servizi
python password_generator.py --list --master "MasterPassword123!"
```

### Esempio 3: Migrazione da Altro Password Manager

```bash
# 1. Esporta dal vecchio gestore in JSON
# 2. Formatta il JSON così:
{
  "github": {
    "username": "user@email.com",
    "password": "G1tHub@Pass#9K",
    "notes": ""
  }
}

# 3. Importa
python password_generator.py --import export.json --encrypt

# 4. Crea backup
python password_generator.py --backup
```

### Esempio 4: Controllo Periodico Sicurezza

```bash
# Crea script per verificare password deboli
python password_generator.py --check "OldWeak123" --entropy
# Se ritorna < 60, rigenera quella password

# Controlla se password è stata compromessa
python password_generator.py --check "password123" --check_common
# Output: Comune: True → DA CAMBIARE IMMEDIATAMENTE
```

---

## 🔧 Troubleshooting

### Errori Comuni

#### 1. `ModuleNotFoundError: No module named 'cryptography'`

**Soluzione:**
```bash
pip install cryptography pyperclip
```

**Verifica:**
```bash
pip list | grep cryptography
```

---

#### 2. `Error: Decrittografia fallita`

**Causa:** Password master errata o database corrotto.

**Soluzioni:**

1. Verifica password:
```bash
# Ricorda: è case-sensitive
Password123! != password123!
```

2. Ripristina da backup:
```bash
cp backups/backup_<hex>.json passwords.json
```

3. Se il database è corrotto e non hai backup:
```bash
# Purifica il database
rm passwords.json
# Ricomincia da capo
```

---

#### 3. Clipboard non funziona

**Errore:** `Errore copia appunti`

**Causa:** `pyperclip` non trova il sistema clipboard.

**Soluzioni:**

**Linux:**
```bash
# Installa xclip o xsel
sudo apt-get install xclip  # Debian/Ubuntu
sudo dnf install xclip      # Fedora
```

**macOS:** Dovrebbe funzionare nativamente.

**Windows:** Dovrebbe funzionare nativamente.

**Workaround:**
Copia manualmente usando l'opzione `--show`:
```bash
python password_generator.py --get github --show
```

---

#### 4. "Nessun carattere disponibile"

**Errore:** Generazione password fallisce.

**Causa:** Hai escluso tutti i tipi di caratteri.

**Esempio errato:**
```bash
python password_generator.py --exclude_symbols --exclude_digits --exclude_upper
# Rimangono solo minuscole → a-z
```

**Soluzione:**
```bash
# Specifica cosa VUOI usare
python password_generator.py --length 16  # Default: tutto incluso
```

---

#### 5. Permission Denied (Linux/macOS)

**Errore:** `PermissionError: [Errno 13] Permission denied`

**Soluzione:**
```bash
# Cambia permessi file
chmod 644 passwords.json

# O sposta in directory utente
mv passwords.json ~/.config/password-manager/
```

---

## 🏗️ Architettura e Modularità

### Struttura File Progetto

```
password-manager/
├── password_generator.py      # Main script (tutto incluso)
├── passwords.json             # Database password (creato a runtime)
├── backups/                   # Directory backup (creata a runtime)
│   └── backup_<hex>.json
├── README_PASSWORD.md         # Documentazione
└── LICENSE                    # License MIT
```

### Struttura Database JSON

#### Schema Database

```json
{
  "encrypted": boolean,
  "version": string,
  "encrypted_data": {
    "salt": string (base64),
    "nonce": string (base64),
    "ciphertext": string (base64)
  },
  "passwords": {
    "<service>": {
      "username": string,
      "password": string,
      "notes": string,
      "created_at": string (hex timestamp)
    }
  }
}
```

#### Esempio Completo

```json
{
  "encrypted": false,
  "passwords": {
    "github": {
      "username": "dev@email.com",
      "password": "G1tHub@Pass#9K",
      "notes": "Repository principali",
      "created_at": "a1b2c3d4e5f6"
    },
    "netflix": {
      "username": "family@email.com",
      "password": "N3tfl!x@M0vie#7",
      "notes": "Condiviso con 4 profili",
      "created_at": "f6e5d4c3b2a1"
    }
  }
}
```

---

### Gestione Profili

I profili sono dizionari Python che definiscono preimpostazioni:

```python
PROFILES = {
    "work": {
        "length": 20,           # 20 caratteri
        "use_upper": True,      # Include maiuscole
        "use_lower": True,      # Include minuscole
        "use_digits": True,     # Include numeri
        "use_symbols": True,    # Include simboli
        "exclude": "<?>{}[]|\\/:;\"'`~"  # Esclusi problematici
    }
}
```

**Perché escludere certi simboli?**
- `<` e `>` possono interferire con HTML/XML
- `\` e `/` possono causare problemi in path
- `"`, `'` e `` ` `` rompono stringhe
- `|` può interferire con pipe shell

---

## 📖 API Reference

### Moduli Python Utilizzati

#### 1. `secrets` - Generazione Sicura

```python
import secrets

# Genera byte casuali
salt = secrets.token_bytes(16)        # 16 bytes casuali
nonce = secrets.token_bytes(12)        # 12 bytes casuali

# Genera intero casuale
number = secrets.randbelow(100)        # 0-99

# Genera token esadecimale
token = secrets.token_hex(16)          # 32 hex chars

# Scelta casuale da sequenza (per password)
char = secrets.choice("abcdef12345")   # Un carattere casuale
```

**Documentazione:** [secrets — Python 3.12+](https://docs.python.org/3/library/secrets.html)

---

#### 2. `hashlib` - Hashing e Derivazione Chiave

```python
import hashlib

# PBKDF2 per derivazione chiave
key = hashlib.pbkdf2_hmac(
    "sha256",           # Hash function
    b"password",        # Password bytes
    b"salt",           # Salt
    100000,             # Iterazioni
    dklen=32           # Lunghezza output (256 bit)
)

# Altri hash comuni
md5_hash = hashlib.md5(b"data").hexdigest()
sha1_hash = hashlib.sha1(b"data").hexdigest()
sha256_hash = hashlib.sha256(b"data").hexdigest()
sha512_hash = hashlib.sha512(b"data").hexdigest()
```

**Documentazione:** [hashlib — Python 3.12+](https://docs.python.org/3/library/hashlib.html)

---

#### 3. `cryptography.hazmat.primitives.ciphers.aead.AESGCM`

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Chiave deve essere 128, 192, o 256 bit (16, 24, 32 bytes)
key = b"32_bytes_key_for_aes_256_enc_"

# Inizializza AES-GCM
aesgcm = AESGCM(key)

# Nonce deve essere unico per ogni operazione
nonce = b"12_byte_nonc"  # 12 bytes raccomandato per GCM

# Encrypt
plaintext = b"Secret message"
ciphertext = aesgcm.encrypt(nonce, plaintext, None)

# Decrypt
decrypted = aesgcm.decrypt(nonce, ciphertext, None)
```

**Documentazione:** [cryptography — AESGCM](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM)

---

#### 4. `base64` - Encoding Binario

```python
import base64

# Encode bytes to string
data = b"binary_data"
encoded = base64.b64encode(data).decode()  # "YmluYXJ5X2RhdGE="

# Decode string to bytes
decoded = base64.b64decode(encoded)        # b"binary_data"

# URL-safe encoding (per filenames)
url_encoded = base64.urlsafe_b64encode(data).decode()
```

**Perché Base64?**
- Converte dati binari in testo ASCII sicuro
- JSON non supporta byte direttamente
- Format standard, portabile

---

#### 5. `json` - Serializzazione Dati

```python
import json

# Python dict to JSON string
data = {"key": "value"}
json_str = json.dumps(data, indent=2, ensure_ascii=False)

# JSON string to Python dict
parsed = json.loads(json_str)

# Write to file
with open("file.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Read from file
with open("file.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

#### 6. `pyperclip` - Clipboard Operations

```python
import pyperclip

# Copy text to clipboard
pyperclip.copy("Hello, World!")

# Paste text from clipboard
text = pyperclip.paste()
```

**Documentazione:** [pyperclip on GitHub](https://github.com/asweigart/pyperclip)

---

### File I/O Sicuro

#### Pattern Sicuro per File Crittografati

```python
import json
import os

def save_securely(data: dict, filename: str):
    """Salva in modo atomico per prevenire corruzione."""

    # 1. Scrivi in file temporaneo
    temp_file = f"{filename}.tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 2. Sincronizza su disco
    f.flush()
    os.fsync(f.fileno())

    # 3. Sostituisci file originale (atomico su Unix)
    if os.path.exists(filename):
        os.replace(temp_file, filename)
    else:
        os.rename(temp_file, filename)
```

---

## 📄 License

Questo progetto è rilasciato sotto la **MIT License**.

```
MIT License

Copyright (c) 2025 Password Generator & Manager

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Autore

**Password Generator & Manager**

Progetto educativo e pratico per la gestione sicura delle password.

---

## 🤝 Contribuire

Questo progetto è pensato per l'apprendimento. Sentiti libero di:
- 🐛 Segnalare bug
- 💡 Suggerire miglioramenti
- 📖 Migliorare la documentazione
- 🔧 Inviare pull request

---

## ⚠️ Disclaimer

Questo software è fornito a scopo educativo. Sebbene utilizzi crittografia di grado militare (AES-256-GCM), nessun sistema è perfetto. Best practices:

1. 🔒 Usa una password master molto forte (20+ caratteri)
2. 💾 Fai backup regolarmente
3. 🚫 Non condividere il file `passwords.json`
4. ✅ Considera password manager affermati per produzione (Bitwarden, 1Password)
5. 🧪 Testa il backup/restore periodicamente

---

## 📚 Risorse per Approfondire

### Crittografia
- [Cryptography.io Documentation](https://cryptography.io/)
- [AES-GCM Explained](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
- [PBKDF2 - Wikipedia](https://en.wikipedia.org/wiki/PBKDF2)

### Python Security
- [Python secrets Module](https://docs.python.org/3/library/secrets.html)
- [Python hashlib Module](https://docs.python.org/3/library/hashlib.html)
- [OWASP Python Security](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)

### Password Security
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Entropy Calculation](https://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength)
- [Diceware Method](https://en.wikipedia.org/wiki/Diceware)

---

## 🎓 Concepts Learned

Questo progetto insegna:

- ✅ Generazione di numeri casuali sicuri (`secrets` vs `random`)
- ✅ Crittografia simmetrica (AES-256-GCM)
- ✅ Derivazione chiave (PBKDF2, salt, iterazioni)
- ✅ Calcolo entropia e misurazione sicurezza
- ✅ File I/O e serializzazione JSON
- ✅ CLI argument parsing (`argparse`)
- ✅ Gestione errori e validazione
- ✅ Integration con OS clipboard
- ✅ Best practices security
- ✅ Modularità e organizzazione codice

---

**Made with ❤️ for students and developers**

*Buona programmazione e buone password sicure!*
