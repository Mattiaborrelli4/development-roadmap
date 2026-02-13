# Weather Notifier

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Utility Python per monitoraggio meteo con notifiche desktop automatizzate**

[Features](#-features)  [Installation](#-installazione)  [Usage](#-utilizzo)  [Documentation](#-documentazione)

</div>

---

## Introduction

Weather Notifier e un'applicazione Python che recupera dati meteorologici in tempo reale dall'API OpenWeatherMap e invia notifiche desktop quando si verificano condizioni meteorologiche specifiche. Ideale per monitorare multiple citta, ricevere avvisi per temperature estreme o condizioni avverse, e mantenere uno storico delle osservazioni.

### Esempio di Output

```
2026-02-11 14:30:15 - INFO - Weather data fetched for Milan: 22.5°C
2026-02-11 14:30:15 - INFO - Notification sent: Weather Alert
2026-02-11 14:30:15 - INFO - Milan: 22.5°C, Clear, Umidità: 65%
```

Notifica Desktop:
> **Weather Alert**<br>
> ⚠️ Temperatura elevata a Milan: 35°C

---

## Features

- **Monitoraggio Multi-Citta**: Traccia simultaneamente piu localita
- **Notifiche Desktop**: Alert cross-platform (Windows, Linux, macOS)
- **Alert Configurabili**: Soglie temperatura personalizzabili
- **Condizioni Avverse**: Avvisi per pioggia, neve, temporali
- **Storico Dati**: Salvataggio automatico in CSV
- **Scheduling Flessibile**: Controlli a intervalli regolari
- **CLI Completa**: Interfaccia a riga di comando versatile
- **Logging Integrato**: Tracciamento dettagliato delle attivita

---

## Why This Project?

### Valore Didattico

Questo progetto e eccellente per studenti universitari e principianti perche:

- **API Integration**: Impara a lavorare con API REST reali
- **HTTP Requests**: Gestione richieste HTTP con `requests`
- **JSON Parsing**: Elaborazione risposte JSON strutturate
- **File I/O**: Gestione file CSV e JSON
- **Scheduling**: Implementazione di task periodici
- **Error Handling**: Gestione robusta degli errori
- **Logging**: Best practices per logging professionale
- **CLI Development**: Creazione interfacce a riga di comando con `argparse`

### Valore Portfolio

Per il tuo portfolio GitHub, questo progetto dimostra:

- Capacita di integrazione con servizi di terze parti
- Conoscenza librerie Python standard e di terze parti
- Strutturazione codice modulare e manutenibile
- Documentazione e configurazione professionali
- Gestione errori e edge cases
- Cross-platform compatibility

### Casi d'Uso Reali

Applicazioni reali di questo tipo di tool:

- **Automazione Personale**: Ricevere avvisi meteo senza aprire app
- **Monitoring Server**: Alert per condizioni che potrebbero affecting infrastrutture
- **Agricultura**: Notifiche per gelate o temperature pericolose per coltivazioni
- **Event Planning**: Monitoraggio meteo per eventi outdoor
- **Smart Home**: Integrazione con sistemi domotici
- **Travel Planning**: Verifica periodica destinazioni di viaggio

---

## Installation

### Prerequisiti

- **Python 3.7 o superiore**
- **Connessione Internet** (per accedere all'API OpenWeatherMap)
- **API Key OpenWeatherMap** gratuita (ottenibile da https://openweathermap.org/api)

### Installazione Dipendenze

Clona o scarica il progetto, quindi installa le dipendenze richieste:

```bash
pip install -r requirements.txt
```

Oppure installa manualmente:

```bash
pip install requests plyer
```

| Libreria | Versione | Descrizione |
|----------|----------|-------------|
| `requests` | >= 2.31.0 | HTTP client per chiamate API |
| `plyer` | >= 2.1.0 | Notifiche desktop cross-platform |

### Ottenere una API Key

1. Registrati su [OpenWeatherMap](https://openweathermap.org/api)
2. Vai alla sezione "API Keys"
3. Copia la tua API key (puo richiedere 10-15 minuti per attivarsi)

---

## Utilizzo

### Creazione Configurazione

Crea un file `config.json` personalizzato:

```bash
python weather_notifier.py --create-config
```

Questo creera un file `config.json` di esempio:

```json
{
  "cities": ["Milan", "Rome", "Naples"],
  "check_interval": 3600,
  "alerts": {
    "temp_high": 35,
    "temp_low": 0,
    "conditions": ["Rain", "Snow", "Thunderstorm", "Extreme"]
  },
  "units": "metric"
}
```

### Esecuzione Base

Esegui un singolo controllo meteo:

```bash
python weather_notifier.py --api-key TUA_API_KEY --once
```

### Monitoraggio Continuo

Avvia il monitoraggio continuo (con default da config.json):

```bash
python weather_notifier.py --api-key TUA_API_KEY
```

Specifica una durata limitata (es. 1 ora = 3600 secondi):

```bash
python weather_notifier.py --api-key TUA_API_KEY --duration 3600
```

### Specificare Citta da CLI

Sovrascrivi le citta del file di configurazione:

```bash
python weather_notifier.py --api-key TUA_API_KEY --cities London Paris Berlin
```

### Visualizzare Storico

Mostra gli ultimi 20 record salvati:

```bash
python weather_notifier.py --api-key TUA_API_KEY --history 20
```

### Configurazione Personalizzata

Usa un file di configurazione diverso:

```bash
python weather_notifier.py --api-key TUA_API_KEY --config my_config.json
```

### Tutte le Opzioni CLI

```
usage: weather_notifier.py [-h] --api-key API_KEY [--config CONFIG]
                          [--once] [--duration DURATION]
                          [--create-config] [--history N]
                          [--cities [CITIES ...]]

opzioni:
  -h, --help            mostra help
  --api-key API_KEY     OpenWeatherMap API key (richiesto)
  --config CONFIG       Path del file di configurazione (default: config.json)
  --once                Esegue un solo controllo invece del loop continuo
  --duration DURATION   Durata totale in secondi per il loop (default: infinito)
  --create-config       Crea un file di configurazione di esempio ed esci
  --history N           Mostra gli ultimi N record dallo storico
  --cities [CITIES ...] Lista di città da monitorare (sovrascrive config)
```

---

## Documentazione del Codice

### Architettura

Il progetto segue un'architettura modulare basata su una classe principale:

```
weather_notifier.py
├── WeatherNotifier (classe principale)
│   ├── __init__()
│   ├── _load_config()
│   ├── _init_history_file()
│   ├── _save_to_history()
│   ├── fetch_weather()
│   ├── _send_notification()
│   ├── _check_alerts()
│   ├── process_city()
│   ├── run_once()
│   ├── run_scheduled()
│   └── get_history()
├── create_sample_config()
└── main()
```

### Analisi Funzione per Funzione

#### 1. `__init__(self, api_key, config_file)`

Inizializza il notifier con API key e configurazione.

```python
def __init__(self, api_key, config_file='config.json'):
    self.api_key = api_key
    self.config_file = config_file
    self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    self.config = self._load_config()
    self.history_file = Path('weather_history.csv')
```

**Concetti Python utilizzati:**
- Pathlib per gestione percorsi file
- Attributi di istanza
- Metodi privati (convenzione `_`)

---

#### 2. `_load_config(self)`

Carica la configurazione da JSON con fallback su defaults.

```python
def _load_config(self):
    default_config = {
        "cities": ["Milan", "Rome", "Naples"],
        "check_interval": 3600,
        "alerts": {"temp_high": 35, "temp_low": 0},
        "units": "metric"
    }
    try:
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            # Merge con defaults
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except FileNotFoundError:
        logger.warning(f"Config file not found, using defaults")
        return default_config
```

**Concetti Python utilizzati:**
- Gestione eccezioni (`try/except`)
- Context manager (`with`)
- JSON parsing
- Dictionary manipulation

---

#### 3. `fetch_weather(self, city)`

Recupera dati meteo dall'API OpenWeatherMap.

```python
def fetch_weather(self, city):
    try:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': self.config['units']
        }
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()  # Solleva eccezione per errori HTTP

        data = response.json()

        # Estrai informazioni rilevanti
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'condition': data['weather'][0]['main']
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather: {e}")
        return None
```

**Concetti Python utilizzati:**
- HTTP requests con parametri query
- JSON deserializzazione
- Dictionary nesting
- Error handling specifico
- Timeout configuration

---

#### 4. `_send_notification(self, title, message)`

Invia notifica desktop con fallback su console.

```python
def _send_notification(self, title, message):
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Weather Notifier",
            timeout=10
        )
        logger.info(f"Notification sent: {title}")
    except ImportError:
        logger.warning("plyer not installed, falling back to console")
        print(f"\n🔔 {title}\n   {message}\n")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
```

**Concetti Python utilizzati:**
- Import condizionali
- Graceful degradation
- Exception handling gerarchico
- Logging multilivello

---

#### 5. `_check_alerts(self, weather_data)`

Verifica condizioni meteo contro soglie configurate.

```python
def _check_alerts(self, weather_data):
    alerts = []
    temp = weather_data['temperature']
    condition = weather_data['condition']

    # Temperatura alta
    if temp >= self.config['alerts']['temp_high']:
        alerts.append({
            'type': 'temp_high',
            'message': f"⚠️ Temperatura elevata: {temp}°C"
        })

    # Temperatura bassa
    if temp <= self.config['alerts']['temp_low']:
        alerts.append({
            'type': 'temp_low',
            'message': f"❄️ Temperatura bassa: {temp}°C"
        })

    # Condizioni avverse
    if condition in self.config['alerts']['conditions']:
        alerts.append({
            'type': 'condition',
            'message': f"🌧️ {condition}: {weather_data['description']}"
        })

    return alerts
```

**Concetti Python utilizzati:**
- List comprehension pattern
- Conditional logic
- Dictionary creation
- String formatting (f-strings)

---

#### 6. `run_scheduled(self, duration=None)`

Esegue loop di monitoring con scheduling.

```python
def run_scheduled(self, duration=None):
    interval = self.config['check_interval']
    start_time = time.time()

    logger.info(f"Starting checks every {interval} seconds...")

    try:
        while True:
            # Verifica durata
            if duration and (time.time() - start_time) >= duration:
                logger.info("Scheduled run completed")
                break

            self.run_once()

            # Attendi prossimo controllo
            logger.info(f"Next check in {interval} seconds...")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Stopped by user")
```

**Concetti Python utilizzati:**
- Infinite loop pattern
- Time handling
- KeyboardInterrupt handling
- Conditional exit

---

#### 7. `main()`

Funzione entry point con argparse per CLI.

```python
def main():
    parser = argparse.ArgumentParser(
        description='Weather Notifier - Monitoraggio meteo con notifiche'
    )
    parser.add_argument('--api-key', required=True, help='API Key')
    parser.add_argument('--once', action='store_true', help='Single check')
    parser.add_argument('--duration', type=int, help='Duration in seconds')
    # ... altri argomenti

    args = parser.parse_args()

    notifier = WeatherNotifier(args.api_key, args.config)

    if args.once:
        notifier.run_once()
    else:
        notifier.run_scheduled(duration=args.duration)
```

**Concetti Python utilizzati:**
- argparse per CLI
- Argument parsing
- Action flags
- Type conversion
- Required/optional arguments

---

## Moduli e Librerie

### requests (HTTP Client)

Libreria de facto standard per HTTP in Python.

```python
import requests

# GET request semplice
response = requests.get('https://api.example.com/data')

# Con parametri
params = {'key': 'value', 'units': 'metric'}
response = requests.get('https://api.example.com/data', params=params)

# Con timeout
response = requests.get('https://api.example.com/data', timeout=10)

# Verifica errori HTTP
response.raise_for_status()

# Accesso dati JSON
data = response.json()
```

**Caratteristiche principali:**
- Keep-alive automatico
- Decodifica automatica content-type
- SSL verification
- Supporto multipart uploads
- Connection pooling

---

### plyer (Notifiche Desktop)

Libreria per notifiche cross-platform.

```python
from plyer import notification

notification.notify(
    title='Titolo',
    message='Messaggio',
    app_name='App Name',
    timeout=10  # secondi
)
```

**Piattaforme supportate:**
- Windows (via toast notifications)
- Linux (via notify-send)
- macOS (via terminal-notifier)

---

### argparse (CLI Parsing)

Modulo standard per parsing argomenti CLI.

```python
import argparse

parser = argparse.ArgumentParser(description='Description')

# Argomento richiesto
parser.add_argument('--api-key', required=True)

# Argomento opzionale con default
parser.add_argument('--config', default='config.json')

# Flag booleano
parser.add_argument('--once', action='store_true')

# Argomento con type
parser.add_argument('--duration', type=int)

# Argomenti multipli
parser.add_argument('--cities', nargs='+')

args = parser.parse_args()
```

---

### logging (Logging System)

Modulo standard per logging professionale.

```python
import logging

# Configurazione base
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Livelli di log
logger.debug('Dettagli debug')
logger.info('Informazione generale')
logger.warning('Avviso')
logger.error('Errore')
logger.critical('Errore critico')
```

**Livelli di severita:**
```
DEBUG < INFO < WARNING < ERROR < CRITICAL
```

---

### json (JSON Handling)

Modulo standard per manipolazione JSON.

```python
import json

# Leggere JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Scrivere JSON
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)

# String to dict
data = json.loads('{"key": "value"}')

# Dict to string
json_str = json.dumps(data)
```

---

### csv (CSV Handling)

Modulo standard per file CSV.

```python
import csv

# Scrivere CSV
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['col1', 'col2', 'col3'])
    writer.writerow(['val1', 'val2', 'val3'])

# Leggere CSV
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['col1'])
```

---

### time (Time Functions)

Modulo standard per operazioni temporali.

```python
import time

# Timestamp corrente
now = time.time()

# Sleep (pausa esecuzione)
time.sleep(60)  # 60 secondi

# Misurare durata
start = time.time()
# ... codice ...
elapsed = time.time() - start
```

---

### pathlib (Path Objects)

Modulo moderno per percorsi file.

```python
from pathlib import Path

# Creare percorso
file_path = Path('data/file.txt')

# Verifica esistenza
if file_path.exists():
    # Leggi file
    content = file_path.read_text()

# Scrivi file
file_path.write_text('content')

# Join percorsi
full_path = Path('folder') / 'subfolder' / 'file.txt'
```

---

## OpenWeatherMap API

### Endpoint Utilizzato

```
GET https://api.openweathermap.org/data/2.5/weather
```

### Parametri Richiesta

| Parametro | Richiesto | Descrizione |
|-----------|-----------|-------------|
| `q` | Si | Nome citta o codice paese (es. "London,UK") |
| `appid` | Si | La tua API key |
| `units` | No | `metric` (Celsius), `imperial` (Fahrenheit), `kelvin` (default) |
| `lang` | No | Codice lingua per descrizioni |
| `mode` | No | `json` (default) o `xml` |

### Esempio Richiesta

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Milan&appid=YOUR_API_KEY&units=metric"
```

### Formato Risposta JSON

```json
{
  "name": "Milan",
  "sys": {
    "country": "IT"
  },
  "main": {
    "temp": 22.5,
    "feels_like": 22.1,
    "humidity": 65,
    "pressure": 1015
  },
  "weather": [
    {
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "wind": {
    "speed": 3.5,
    "deg": 120
  },
  "dt": 1707666615,
  "id": 3173435
}
```

### Limiti API Free Tier

- **60 chiamate/minute**
- **1,000,000 chiamate/month**
- **Current weather data**
- **Forecast data disponibile con piani paid**

---

## Scheduling e Notifiche

### Scheduling con time.sleep()

Implementazione semplice ma efficace per task periodici:

```python
def run_scheduled(self, duration=None):
    interval = self.config['check_interval']
    start_time = time.time()

    try:
        while True:
            # Check durata
            if duration and (time.time() - start_time) >= duration:
                break

            # Esegui task
            self.run_once()

            # Attendi prossimo intervallo
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Stopped by user")
```

**Vantaggi:**
- Semplice e intuitivo
- Nessuna dipendenza aggiuntiva
- Funziona su tutte le piattaforme

**Svantaggi:**
- Non precisa per scheduling complessi
- Il tempo di esecuzione si somma all'intervallo

### Alternativa: sched.scheduler

Per scheduling più preciso:

```python
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def scheduled_event():
    print("Event executed")
    # Riprogramma prossimo evento
    scheduler.enter(3600, 1, scheduled_event)

# Prima esecuzione tra 60 secondi
scheduler.enter(60, 1, scheduled_event)
scheduler.run()
```

### Notifiche Cross-Platform

Il modulo `plyer` astrae le differenze tra piattaforme:

```python
from plyer import notification

notification.notify(
    title='Weather Alert',
    message='High temperature detected!',
    app_name='Weather Notifier',
    timeout=10
)
```

**Fallback per sistemi non supportati:**

```python
try:
    from plyer import notification
    notification.notify(...)
except ImportError:
    # Fallback su console
    print("Notification: ", message)
```

---

## Alert e Automazione

### Configurazione Soglie Temperature

Modifica `config.json`:

```json
{
  "alerts": {
    "temp_high": 35,      // Soglia caldo estremo (°C)
    "temp_low": -5,       // Soglia freddo estremo (°C)
    "conditions": [
      "Rain",             // Pioggia
      "Snow",             // Neve
      "Thunderstorm",     // Temporale
      "Extreme"           // Condizioni estreme
    ]
  }
}
```

### Condizioni Meteo Disponibili

OpenWeatherMap restituisce queste condizioni principali:

| Condizione | Descrizione |
|------------|-------------|
| `Clear` | Cielo sereno |
| `Clouds` | Nuvoloso |
| `Rain` | Pioggia |
| `Drizzle` | Pioggerella |
| `Thunderstorm` | Temporale |
| `Snow` | Neve |
| `Mist` | Nebbia leggera |
| `Fog` | Nebbia |
| `Haze` | Caligine |

### Log Storico Formato CSV

Il file `weather_history.csv` mantiene storico completo:

```csv
timestamp,city,temperature,feels_like,humidity,pressure,condition,wind_speed
2026-02-11T14:30:15.123456,Milan,22.5,22.1,65,1015,Clear,3.5
2026-02-11T14:30:16.234567,Rome,25.0,24.5,55,1012,Clouds,4.2
```

### Analisi Storico con Python

```python
import csv
from datetime import datetime

# Leggi storico
with open('weather_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamp = datetime.fromisoformat(row['timestamp'])
        temp = float(row['temperature'])
        print(f"{timestamp}: {temp}°C")
```

---

## Esempi di Configurazione

### Configurazione Multi-Citta

```json
{
  "cities": [
    "Milan,IT",
    "Rome,IT",
    "London,UK",
    "Paris,FR",
    "Berlin,DE",
    "New York,US"
  ],
  "check_interval": 1800,
  "units": "metric"
}
```

### Frequenze Diverse

```json
{
  "check_interval": 900,     // 15 minuti per monitoring frequente
  "alerts": {
    "temp_high": 30,
    "temp_low": 5,
    "conditions": ["Rain", "Snow", "Thunderstorm"]
  }
}
```

```json
{
  "check_interval": 7200,    // 2 ore per monitoring meno frequente
  "alerts": {
    "temp_high": 38,
    "temp_low": -10,
    "conditions": ["Extreme"]
  }
}
```

### Alert Personalizzati per Clima

```json
{
  "alerts": {
    "temp_high": 25,         // Soglia bassa per clima freddo
    "temp_low": 15,
    "conditions": ["Rain", "Drizzle", "Mist", "Fog"]
  },
  "units": "metric"
}
```

```json
{
  "alerts": {
    "temp_high": 40,         // Soglie alte per clima caldo
    "temp_low": 20,
    "conditions": ["Sand", "Dust"]
  },
  "units": "metric"
}
```

### Units Diverse

```json
{
  "units": "imperial",       // Fahrenheit per US
  "alerts": {
    "temp_high": 95,         // 95°F
    "temp_low": 32           // 32°F (freezing)
  }
}
```

---

## Troubleshooting

### Errori Comuni

#### 1. API Key Invalida

```
Error: 401 Unauthorized
```

**Soluzioni:**
- Verifica che l'API key sia corretta
- Le nuove API keys richiedono 10-15 minuti per attivarsi
- Controlla di aver copiato tutta la key senza spazi

#### 2. Citta Non Trovata

```
Error: 404 Not Found
```

**Soluzioni:**
- Verifica ortografia citta
- Aggiungi codice paese: `"London,UK"` invece di `"London"`
- Usa nomi in inglese per citta straniere

#### 3. Rate Limiting

```
Error: 429 Too Many Requests
```

**Soluzioni:**
- Aumenta `check_interval` in config.json
- Riduci numero di citta monitorate
- Verifica limiti piano API gratuito

#### 4. Notifiche Non Appaiono

**Windows:**
- Abilita notifiche in Settings > System > Notifications
- Verifica che Python sia permesso a inviare notifiche

**Linux:**
- Installa `libnotify-bin`:
  ```bash
  sudo apt-get install libnotify-bin
  ```

**macOS:**
- Installa `terminal-notifier`:
  ```bash
  brew install terminal-notifier
  ```

#### 5. plyer Import Error

```
ImportError: No module named 'plyer'
```

**Soluzione:**
```bash
pip install plyer
```

#### 6. Permission Denied

```
PermissionError: [Errno 13] Permission denied: 'weather_history.csv'
```

**Soluzioni:**
- Verifica permessi scrittura directory
- Chiudi il file CSV se aperto in Excel
- Esegui con permessi appropriati

### Debug Tips

#### Abilita Debug Logging

Modifica `weather_notifier.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Cambia da INFO a DEBUG
    ...
)
```

Oppure da CLI:

```bash
# Aggiungi questo alla sezione if __name__ == "__main__":
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

#### Test API Manualmente

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Milan&appid=YOUR_API_KEY&units=metric"
```

#### Verifica Configurazione

```python
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    print(json.dumps(config, indent=2))
```

#### Test Singola Citta

```bash
python weather_notifier.py --api-key YOUR_KEY --once --cities Milan
```

---

## Considerazioni Etiche e Legali

### Termini di Servizio API

**OpenWeatherMap ToS Key Points:**
- **Attribution**: Credita OpenWeatherMap in ogni utilizzo pubblico
- **Rate Limits**: Rispetta i limiti del tuo piano (60/minuto per free)
- **Commercial Use**: Piano free per uso personale/educational
- **Data Redistribution**: Non ridistribuire raw data API senza permesso

**Best Practices:**
- Implementa backoff esponenziale per retry
- Caching intelligente per ridurre chiamate
- Non revocare/sharing API keys
- Monitora utilizzo per evitare limiti

### Privacy e Protezione Dati

**Considerazioni:**
- Il file `weather_history.csv` contiene dati sensibili di posizione
- Non commitare API keys in version control
- Non condividere config con API keys pubbliche
- Considera encrypting dati sensibili per produzione

**.gitignore Raccomandato:**

```gitignore
# File sensibili
config.json
weather_history.csv
weather_notifier.log

# Python
__pycache__/
*.pyc
.venv/
```

### API Key Security

**Best Practices:**

1. **Environment Variables** (raccomandato):

```python
import os

api_key = os.getenv('OPENWEATHER_API_KEY')
```

```bash
export OPENWEATHER_API_KEY='your_key_here'
python weather_notifier.py --api-key $OPENWEATHER_API_KEY
```

2. **File Separato** (mai commitato):

```bash
# secrets.json (in .gitignore)
{
  "api_key": "your_actual_key"
}
```

3. **Input Interattivo**:

```python
api_key = input("Enter API key: ")
```

---

## Risorse

### Documentazione API

- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [Current Weather API](https://openweathermap.org/current)
- [API Parameters Reference](https://openweathermap.org/appid)

### Tutorial e Guide

- [Requests Library Docs](https://requests.readthedocs.io/)
- [Plyer Documentation](https://plyer.readthedocs.io/)
- [Python Logging Tutorial](https://docs.python.org/3/howto/logging.html)
- [Argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

### Siti Meteo Alternativi

| Service | Free Tier | Features |
|---------|-----------|----------|
| [WeatherAPI.com](https://www.weatherapi.com/) | 1M calls/month | Forecast, History, Alerts |
| [OpenMeteo](https://open-meteo.com/) | No API key needed | Free forever, no registration |
| [AccuWeather](https://developer.accuweather.com/) | 50 calls/day | Severe weather, Minute cast |
| [Weatherbit](https://www.weatherbit.io/) | 200 calls/day | 16-day forecast, Air quality |

### Community e Forum

- [Stack Overflow - Python tag](https://stackoverflow.com/questions/tagged/python)
- [Reddit r/Python](https://reddit.com/r/Python)
- [Python Discord Server](https://discord.gg/python)
- [OpenWeatherMap Community](https://community.openweathermap.org/)

---

## Esercizi Proposti

### Livello 1 - Base

1. **Hello World Meteo**
   - Scrivi uno script che recupera il meteo per la tua citta
   - Stampa temperatura e condizione in console
   - Niente notifiche, niente config file

2. **Personalizzazione Messaggi**
   - Modifica i messaggi di notifica con emoji personalizzate
   - Aggiungi il simbolo della temperatura appropriato (°C/°F)

3. **Logging Analysis**
   - Scrivi una funzione che legga `weather_notifier.log`
   - Stampa statistiche: quante chiamate API fatte, errori totali

4. **Unit Conversion**
   - Aggiungi supporto per unita Kelvin
   - Scrivi funzione helper per conversione tra unita

---

### Livello 2 - Intermedio

1. **Forecast Data**
   - Integra l'endpoint forecast (5 giorni/3 ore)
   - Mostra previsioni per le prossime 24 ore
   - Crea funzione `fetch_forecast(city)`

2. **Telegram Bot Integration**
   - Crea bot Telegram che invia notifiche
   - Usa python-telegram-bot wrapper
   - Comando /weather per richiesta manuale

3. **Email Alerts**
   - Invia email quando avvisi si attivano
   - Usa smtplib o servizio SendGrid/Mailgun
   - Template HTML per email formattate

4. **Dashboard Web**
   - Semplice web app con Flask/FastAPI
   - Grafico temperature storiche con Plotly
   - Pagina per configurare alert via web UI

5. **Database Integration**
   - Sostituisci CSV con SQLite
   - Query per media temperature periodi
   - Export in Excel con pandas

---

### Livello 3 - Avanzato

1. **Multi-Source Aggregation**
   - Combina dati da OpenWeatherMap + altri servizi
   - Media delle temperature da multiple fonti
   - Fallback se API primaria fallisce

2. **Machine Learning Prediction**
   - Usa dati storici per predire temperature
   - Modello regression con scikit-learn
   - Valutazione accuracy predizioni

3. **Mobile App**
   - Versione mobile con Kivy o BeeWare
   - Background service su Android/iOS
   - Push notifications reali

4. **Docker Deployment**
   - Containerizza applicazione
   - Dockerfile per immagine Python
   - docker-compose per deployment

5. **Cloud Functions**
   - Deploy come serverless function
   - AWS Lambda o Google Cloud Functions
   - Trigger via timer cloud

---

### Idee Progetti Correlati

#### Weather Dashboard
```python
# Semplice dashboard con Flask
from flask import Flask, render_template
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Genera grafici temperatura
    fig = create_temperature_chart()
    return render_template('dashboard.html', plot=fig)
```

#### 7-Day Forecaster
```python
def fetch_week_forecast(city):
    """Recupera previsioni 7 giorni."""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': API_KEY,
        'cnt': 7 * 8  # 8 forecasts per day (3-hour intervals)
    }
    response = requests.get(url, params=params)
    return response.json()['list']
```

#### Weather Comparer
```python
def compare_cities(city_list):
    """Confronta meteo tra multiple citta."""
    results = {}
    for city in city_list:
        weather = fetch_weather(city)
        results[city] = weather['temperature']

    # Ordina per temperatura
    return dict(sorted(results.items(), key=lambda x: x[1]))
```

#### Personal Weather Recommender
```python
def generate_recommendation(weather_data):
    """Genera consigli base meteo."""
    temp = weather_data['temperature']
    condition = weather_data['condition']

    if temp < 10:
        return "Porta giacca pesante e sciarpa"
    elif temp < 20:
        return "Porta giacca leggera o felpa"
    elif condition == "Rain":
        return "Porta ombrello e impermeabile"
    else:
        return "Vestiti leggeri, bel tempo!"
```

---

## Changelog

### Version 1.0.0 (2026-02-11)

**Initial Release**

#### Features
- Monitoraggio multi-citta
- Notifiche desktop cross-platform (Windows/Linux/macOS)
- Alert configurabili per temperature
- Allerta per condizioni meteorologiche avverse
- Storico dati in CSV
- Logging dettagliato su file e console
- CLI completa con argparse
- Configurazione JSON personalizzabile
- Supporto unita metric/imperial/kelvin

#### Configuration
- File `config.json` per impostazioni globali
- API key management sicuro
- Intervallo check configurabile
- Soglie alert personalizzabili

#### Documentation
- README completo con esempi
- Documentazione API OpenWeatherMap
- Troubleshooting guide
- Esercizi proposti per studenti

### Roadmap Futura

#### v1.1.0 (Prossimo)
- [ ] Supporto forecast 5 giorni
- [ ] Grafici visualizzazione storico
- [ ] Export dati in Excel
- [ ] Telegram bot integration

#### v1.2.0
- [ ] Web dashboard con Flask
- [ ] Database SQLite opzionale
- [ ] Multi-language support
- [ ] Dark mode UI

#### v2.0.0
- [ ] Machine learning predictions
- [ ] Mobile app companion
- [ ] Docker deployment
- [ ] Multi-provider aggregation

---

## Contributing

Questo progetto e aperto a contributi! Per domande, suggerimenti o miglioramenti:

1. Fai fork del progetto
2. Crea branch per feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

---

## License

Questo progetto e rilasciato sotto licenza MIT. Vedi file LICENSE per dettagli.

---

## Author

Creato come progetto educativo per studenti universitari e portfolio GitHub.

---

<div align="center">

**Built with Python and OpenWeatherMap API**

[![Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

</div>
