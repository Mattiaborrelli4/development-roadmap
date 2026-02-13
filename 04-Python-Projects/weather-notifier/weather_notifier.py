#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weather Notifier - Sistema di Monitoraggio Meteo con Notifiche Desktop
========================================================================

Questo script scarica i dati meteo da OpenWeatherMap e invia notifiche desktop
quando vengono superati determinati threshold (temperatura, pioggia, ecc.).

Autore: Tutorial educativo per studenti
Versione: 1.0.0
Licenza: MIT

Dipendenze:
    - requests: per le chiamate HTTP all'API
    - sched: per lo scheduling delle notifiche (stdlib)

Uso base:
    python weather_notifier.py --city "Rome,IT" --interval 10

Documentazione API OpenWeatherMap:
    https://openweathermap.org/api/one-call-3
"""

# ============================================================================
# SEZIONE 1: IMPORTAZIONI E CONFIGURAZIONE GLOBALE
# ============================================================================

import requests      # Per le richieste HTTP all'API meteo
import sched         # Per lo scheduling periodico delle verifiche
import time          # Per gestione tempi e sleep
import json          # Per parsing JSON e salvataggio configurazione
import logging       # Per logging e debug
import argparse      # Per parsing argomenti CLI
import csv           # Per salvataggio dati storici in CSV
import os            # Per operazioni sui file
import sys           # Per system-specific parameters
import platform      # Per identificare il sistema operativo
from datetime import datetime  # Per timestamp e formattazione date
from pathlib import Path        # Per percorsi file cross-platform

# Configurazione directory di lavoro
BASE_DIR = Path(__file__).parent.absolute()
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Creazione directory se non esistono
for dir_path in [CONFIG_DIR, DATA_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Percorsi file di configurazione e dati
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_CSV = DATA_DIR / "weather_history.csv"
NOTIFICATIONS_LOG = DATA_DIR / "notifications_log.json"
API_KEY_FILE = CONFIG_DIR / "api_key.txt"

# Configurazione logger
def setup_logging(verbose=False):
    """
    Configura il sistema di logging con livello appropriato.

    Args:
        verbose (bool): Se True, imposta livello DEBUG, altrimenti INFO

    Returns:
        logging.Logger: Logger configurato
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(LOGS_DIR / "weather_notifier.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)


# Inizializza il logger
logger = setup_logging()

# Configurazione API OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"

# API key demo (limitata per test - sostituire con propria key per uso reale)
DEMO_API_KEY = "demo"  # Placeholder: ottenere key gratuita da openweathermap.org


# ============================================================================
# SEZIONE 2: GESTIONE CONFIGURAZIONE
# ============================================================================

def load_api_key():
    """
    Carica la API key da file o restituisce la key demo.

    Priorità:
    1. File api_key.txt se esiste
    2. Variabile d'ambiente OPENWEATHER_API_KEY
    3. Key demo (limitata)

    Returns:
        str: API key da utilizzare
    """
    # Prima controlla se esiste il file con la API key
    if API_KEY_FILE.exists():
        try:
            with open(API_KEY_FILE, 'r', encoding='utf-8') as f:
                key = f.read().strip()
                if key and key != DEMO_API_KEY:
                    logger.info("[*] API key caricata da file: api_key.txt")
                    return key
        except Exception as e:
            logger.warning(f"[!] Errore lettura file API key: {e}")

    # Controlla variabile d'ambiente
    env_key = os.environ.get('OPENWEATHER_API_KEY')
    if env_key:
        logger.info("[*] API key caricata da variabile d'ambiente")
        return env_key

    # Usa demo key come fallback
    logger.warning("[!] Nessuna API key trovata, uso key demo (limitata)")
    logger.info("[*] Per ottenere una key gratuita: https://openweathermap.org/api")
    return DEMO_API_KEY


def save_api_key(api_key):
    """
    Salva la API key in file per utilizzi futuri.

    Args:
        api_key (str): La API key da salvare
    """
    try:
        with open(API_KEY_FILE, 'w', encoding='utf-8') as f:
            f.write(api_key)
        logger.info(f"[OK] API key salvata in: {API_KEY_FILE}")
    except Exception as e:
        logger.error(f"[!] Errore salvataggio API key: {e}")


def load_config():
    """
    Carica la configurazione salvata da file JSON.

    Returns:
        dict: Configurazione caricata o dict vuoto se file non esiste
    """
    default_config = {
        'city': 'Rome,IT',
        'lat': None,
        'lon': None,
        'interval_minutes': 10,
        'temp_threshold_high': 30.0,
        'temp_threshold_low': 5.0,
        'alert_rain': True,
        'alert_snow': True,
        'alert_temp_high': True,
        'alert_temp_low': True,
        'notifications_enabled': True
    }

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"[*] Configurazione caricata da: {CONFIG_FILE}")
                # Merge con default per garantire che tutte le chiavi esistano
                default_config.update(config)
                return default_config
        except json.JSONDecodeError as e:
            logger.error(f"[!] Errore parsing JSON configurazione: {e}")
        except Exception as e:
            logger.error(f"[!] Errore caricamento configurazione: {e}")

    return default_config


def save_config(config):
    """
    Salva la configurazione corrente in file JSON.

    Args:
        config (dict): Dizionario con la configurazione da salvare
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info(f"[OK] Configurazione salvata in: {CONFIG_FILE}")
    except Exception as e:
        logger.error(f"[!] Errore salvataggio configurazione: {e}")


# ============================================================================
# SEZIONE 3: API OPENWEATHERMAP - GESTIONE DATI METEO
# ============================================================================

def get_coordinates(city_name, api_key):
    """
    Converte il nome della città in coordinate lat/lon tramite API Geocoding.

    Args:
        city_name (str): Nome città nel formato "City,CountryCode" (es: "Rome,IT")
        api_key (str): API key per OpenWeatherMap

    Returns:
        tuple: (lat, lon, city_name) o (None, None, None) se errore
    """
    logger.debug(f"[*] Richiesta coordinate per: {city_name}")

    # Se sono già coordinate numeriche
    try:
        if ',' in city_name:
            parts = city_name.split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            logger.info(f"[OK] Coordinate utilizzate direttamente: {lat}, {lon}")
            return lat, lon, f"{lat},{lon}"
    except ValueError:
        pass  # Non sono coordinate pure, continua con geocoding

    # Prepara parametri richiesta
    params = {
        'q': city_name,
        'limit': 1,
        'appid': api_key
    }

    try:
        # Esegue chiamata API
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()

        # Parsing risposta JSON
        data = response.json()

        if data and len(data) > 0:
            lat = data[0]['lat']
            lon = data[0]['lon']
            name = data[0].get('name', city_name)
            country = data[0].get('country', '')
            full_name = f"{name},{country}" if country else name

            logger.info(f"[OK] Coordinate trovate: {full_name} -> {lat}, {lon}")
            return lat, lon, full_name
        else:
            logger.error(f"[!] Città non trovata: {city_name}")
            return None, None, None

    except requests.exceptions.Timeout:
        logger.error("[!] Timeout nella richiesta geocoding")
        return None, None, None
    except requests.exceptions.ConnectionError:
        logger.error("[!] Errore di connessione nella richiesta geocoding")
        return None, None, None
    except requests.exceptions.HTTPError as e:
        logger.error(f"[!] Errore HTTP geocoding: {e}")
        return None, None, None
    except json.JSONDecodeError:
        logger.error("[!] Errore parsing risposta geocoding")
        return None, None, None
    except Exception as e:
        logger.error(f"[!] Errore imprevisto geocoding: {e}")
        return None, None, None


def fetch_weather_data(lat, lon, api_key):
    """
    Recupera i dati meteo correnti dall'API OpenWeatherMap.

    Args:
        lat (float): Latitudine
        lon (float): Longitudine
        api_key (str): API key per OpenWeatherMap

    Returns:
        dict: Dati meteo o None se errore
    """
    logger.debug(f"[*] Fetch dati meteo per coordinate: {lat}, {lon}")

    # Parametri richiesta API
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  # Temperatura in Celsius
        'lang': 'it'        # Descrizioni in italiano
    }

    try:
        # Esegue richiesta GET con timeout di 10 secondi
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        # Parsing JSON risposta
        data = response.json()

        # Estrazione dati principali
        current = data.get('current', {})

        weather_data = {
            'timestamp': datetime.now().isoformat(),
            'lat': lat,
            'lon': lon,
            'temperature': current.get('temp', None),
            'feels_like': current.get('feels_like', None),
            'humidity': current.get('humidity', None),
            'pressure': current.get('pressure', None),
            'wind_speed': current.get('wind_speed', None),
            'wind_direction': current.get('wind_deg', None),
            'weather_id': current.get('weather', [{}])[0].get('id', None),
            'weather_main': current.get('weather', [{}])[0].get('main', ''),
            'weather_description': current.get('weather', [{}])[0].get('description', ''),
            'clouds': current.get('clouds', None),
            'visibility': current.get('visibility', None),
            'rain_1h': current.get('rain', {}).get('1h', 0),
            'snow_1h': current.get('snow', {}).get('1h', 0),
        }

        logger.info(f"[OK] Dati meteo recuperati: {weather_data['temperature']}C, "
                   f"{weather_data['weather_description']}")

        return weather_data

    except requests.exceptions.Timeout:
        logger.error("[!] Timeout nella richiesta meteo")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("[!] Errore di connessione nella richiesta meteo")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            logger.error("[!] API key non valida. Ottenirne una gratuita da:")
            logger.error("    https://openweathermap.org/api")
        elif response.status_code == 404:
            logger.error("[!] Coordinate non valide per richiesta meteo")
        else:
            logger.error(f"[!] Errore HTTP meteo: {e}")
        return None
    except json.JSONDecodeError:
        logger.error("[!] Errore parsing risposta meteo")
        return None
    except KeyError as e:
        logger.error(f"[!] Dato mancante in risposta meteo: {e}")
        return None
    except Exception as e:
        logger.error(f"[!] Errore imprevisto fetch meteo: {e}")
        return None


# ============================================================================
# SEZIONE 4: ANALISI DATI E GESTIONE ALERT
# ============================================================================

def check_weather_alerts(weather_data, config):
    """
    Verifica se ci sono condizioni meteo che richiedono un alert.

    Controlla:
    - Temperature sopra/sotto soglia
    - Presenza di pioggia
    - Presenza di neve

    Args:
        weather_data (dict): Dati meteo correnti
        config (dict): Configurazione con threshold

    Returns:
        list: Lista di messaggi di alert (vuota se nessun alert)
    """
    alerts = []

    if not weather_data:
        logger.warning("[*] Nessun dato meteo disponibile per controllo alert")
        return alerts

    temp = weather_data.get('temperature')
    rain = weather_data.get('rain_1h', 0)
    snow = weather_data.get('snow_1h', 0)
    desc = weather_data.get('weather_description', '')

    # Alert temperatura alta
    if config.get('alert_temp_high', True) and temp is not None:
        threshold = config.get('temp_threshold_high', 30.0)
        if temp > threshold:
            msg = (f"[!] TEMPERATURA ALTA: {temp:.1f}C (soglia: {threshold}C)\n"
                   f"    Consigliato: rimanere idratati, evitare esposizione prolungata")
            alerts.append(msg)
            logger.warning(f"Alert temperatura alta: {temp}C")

    # Alert temperatura bassa
    if config.get('alert_temp_low', True) and temp is not None:
        threshold = config.get('temp_threshold_low', 5.0)
        if temp < threshold:
            msg = (f"[!] TEMPERATURA BASSA: {temp:.1f}C (soglia: {threshold}C)\n"
                   f"    Consigliato: vestirsi a strati, attenzione al ghiaccio")
            alerts.append(msg)
            logger.warning(f"Alert temperatura bassa: {temp}C")

    # Alert pioggia
    if config.get('alert_rain', True) and rain > 0:
        msg = (f"[!] PIOGGIA RILEVATA: {rain}mm/h\n"
               f"    Condizioni: {desc}\n"
               f"    Consigliato: portare ombrello, indossare impermeabile")
        alerts.append(msg)
        logger.warning(f"Alert pioggia: {rain}mm/h")

    # Alert neve
    if config.get('alert_snow', True) and snow > 0:
        msg = (f"[!] NEVE RILEVATA: {snow}mm/h\n"
               f"    Condizioni: {desc}\n"
               f"    Consigliato: precauzioni alla guida, vestiti caldi")
        alerts.append(msg)
        logger.warning(f"Alert neve: {snow}mm/h")

    # Alert condizioni avverse (base su weather ID)
    weather_id = weather_data.get('weather_id', 0)

    # Temporale (thunderstorm): 200-232
    if 200 <= weather_id <= 232:
        msg = (f"[!] TEMPORALE IN CORSO\n"
               f"    Condizioni: {desc}\n"
               f"    Consigliato: rimanere al chiuso, evitare spostamenti")
        alerts.append(msg)
        logger.warning("Alert temporale")

    # Nebbia forte (fog): 741
    if weather_id == 741:
        msg = (f"[!] NEBIA DENSE RILEVATA\n"
               f"    Visibilità ridotta\n"
               f"    Consigliato: cautela nella guida, usare luci")
        alerts.append(msg)
        logger.warning("Alert nebbia")

    return alerts


def format_weather_message(weather_data):
    """
    Formatta i dati meteo in un messaggio leggibile per notifica.

    Args:
        weather_data (dict): Dati meteo da formattare

    Returns:
        str: Messaggio formattato con tutte le informazioni
    """
    if not weather_data:
        return "Nessun dato meteo disponibile"

    temp = weather_data.get('temperature', 'N/A')
    feels = weather_data.get('feels_like', 'N/A')
    humidity = weather_data.get('humidity', 'N/A')
    desc = weather_data.get('weather_description', 'N/A').capitalize()
    wind = weather_data.get('wind_speed', 'N/A')
    pressure = weather_data.get('pressure', 'N/A')

    message = (
        f"=== METEO ATTUALE ===\n"
        f"Condizioni: {desc}\n"
        f"Temperatura: {temp}C (percepita: {feels}C)\n"
        f"Umidita: {humidity}%\n"
        f"Vento: {wind} m/s\n"
        f"Pressione: {pressure} hPa\n"
        f"====================="
    )

    return message


# ============================================================================
# SEZIONE 5: SISTEMA DI NOTIFICHE DESKTOP
# ============================================================================

def send_notification_windows(title, message):
    """
    Invia notifica desktop su Windows usando toast notifications.

    Funziona su Windows 10/11 con PowerShell.

    Args:
        title (str): Titolo della notifica
        message (str): Corpo del messaggio

    Returns:
        bool: True se inviata con successo, False altrimenti
    """
    logger.debug(f"[*] Invio notifica Windows: {title}")

    try:
        import subprocess

        # Escape per PowerShell (virgolette e caratteri speciali)
        title_escaped = title.replace('"', '`"').replace("'", "''")
        message_escaped = message.replace('"', '`"').replace("'", "''").replace('\n', '`n')

        # Script PowerShell per notifica toast
        ps_script = f'''
        Add-Type -AssemblyName Windows.UI.Notifications
        Add-Type -AssemblyName Windows.Data.Xml.Dom

        $template = @"
        <toast>
            <visual>
                <binding template="ToastGeneric">
                    <text>{title_escaped}</text>
                    <text>{message_escaped}</text>
                </binding>
            </visual>
        </toast>
        "@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("WeatherNotifier")
        $notification = New-Object Windows.UI.Notifications.ToastNotification $xml
        $toast.Show($notification)
        '''

        # Esegue script PowerShell
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            logger.info("[OK] Notifica Windows inviata")
            return True
        else:
            logger.warning(f"[!] Errore notifica Windows: {result.stderr}")
            return False

    except ImportError:
        logger.error("[!] Modulo subprocess non disponibile")
        return False
    except subprocess.TimeoutExpired:
        logger.error("[!] Timeout invio notifica Windows")
        return False
    except Exception as e:
        logger.error(f"[!] Errore invio notifica Windows: {e}")
        return False


def send_notification_linux(title, message):
    """
    Invia notifica desktop su Linux usando libnotify.

    Args:
        title (str): Titolo della notifica
        message (str): Corpo del messaggio

    Returns:
        bool: True se inviata con successo, False altrimenti
    """
    logger.debug(f"[*] Invio notifica Linux: {title}")

    try:
        import subprocess

        # Usa notify-send per notifiche Linux
        result = subprocess.run(
            ['notify-send', '-i', 'weather', title, message],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            logger.info("[OK] Notifica Linux inviata")
            return True
        else:
            logger.warning(f"[!] Errore notifica Linux: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.warning("[!] notify-send non trovato. Installa libnotify-bin")
        return False
    except subprocess.TimeoutExpired:
        logger.error("[!] Timeout invio notifica Linux")
        return False
    except Exception as e:
        logger.error(f"[!] Errore invio notifica Linux: {e}")
        return False


def send_notification_macos(title, message):
    """
    Invia notifica desktop su macOS usando osascript.

    Args:
        title (str): Titolo della notifica
        message (str): Corpo del messaggio

    Returns:
        bool: True se inviata con successo, False altrimenti
    """
    logger.debug(f"[*] Invio notifica macOS: {title}")

    try:
        import subprocess

        # Script AppleScript per notifica macOS
        script = f'''
        display notification "{message}" with title "{title}" sound name "Glass"
        '''

        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            logger.info("[OK] Notifica macOS inviata")
            return True
        else:
            logger.warning(f"[!] Errore notifica macOS: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.warning("[!] osascript non trovato su questo sistema")
        return False
    except subprocess.TimeoutExpired:
        logger.error("[!] Timeout invio notifica macOS")
        return False
    except Exception as e:
        logger.error(f"[!] Errore invio notifica macOS: {e}")
        return False


def send_notification(title, message):
    """
    Invia notifica desktop cross-platform in base al sistema operativo.

    Rileva automaticamente il sistema operativo e chiama la funzione
    appropriata per inviare la notifica.

    Args:
        title (str): Titolo della notifica
        message (str): Corpo del messaggio

    Returns:
        bool: True se inviata con successo, False altrimenti
    """
    logger.info(f"[*] Preparazione notifica: {title}")

    system = platform.system()

    if system == "Windows":
        return send_notification_windows(title, message)
    elif system == "Linux":
        return send_notification_linux(title, message)
    elif system == "Darwin":  # macOS
        return send_notification_macos(title, message)
    else:
        logger.warning(f"[!] Sistema operativo non supportato: {system}")
        return False


def log_notification(title, message, notification_type="weather"):
    """
    Salva il log di una notifica in file JSON.

    Args:
        title (str): Titolo della notifica
        message (str): Messaggio della notifica
        notification_type (str): Tipo di notifica (weather/alert)
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': notification_type,
        'title': title,
        'message': message
    }

    # Carica log esistenti
    logs = []
    if NOTIFICATIONS_LOG.exists():
        try:
            with open(NOTIFICATIONS_LOG, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logger.warning("[!] Errore parsing log notifiche esistente")

    # Aggiungi nuovo log
    logs.append(log_entry)

    # Mantieni solo ultimi 100 log per non crescere troppo
    if len(logs) > 100:
        logs = logs[-100:]

    # Salva su file
    try:
        with open(NOTIFICATIONS_LOG, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        logger.debug(f"[*] Log notifica salvato in: {NOTIFICATIONS_LOG}")
    except Exception as e:
        logger.error(f"[!] Errore salvataggio log notifica: {e}")


# ============================================================================
# SEZIONE 6: GESTIONE DATI STORICI
# ============================================================================

def save_weather_history(weather_data):
    """
    Salva i dati meteo in file CSV per analisi storica.

    Crea il file CSV con header se non esiste, altrimenti appende.

    Args:
        weather_data (dict): Dati meteo da salvare
    """
    if not weather_data:
        logger.warning("[*] Nessun dato meteo da salvare")
        return

    try:
        # Verifica se il file esiste per decidere se scrivere header
        file_exists = HISTORY_CSV.exists()

        with open(HISTORY_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=weather_data.keys())

            # Scrivi header solo se file nuovo
            if not file_exists:
                writer.writeheader()
                logger.info(f"[*] Creato nuovo file storico: {HISTORY_CSV}")

            # Scrivi riga dati
            writer.writerow(weather_data)
            logger.debug(f"[*] Dati salvati in CSV: {weather_data['timestamp']}")

    except PermissionError:
        logger.error(f"[!] Permesso negato scrittura su: {HISTORY_CSV}")
    except Exception as e:
        logger.error(f"[!] Errore salvataggio storico CSV: {e}")


def read_weather_history(limit=None):
    """
    Legge i dati storici dal file CSV.

    Args:
        limit (int, optional): Numero massimo di record da leggere

    Returns:
        list: Lista di dict con i dati storici
    """
    if not HISTORY_CSV.exists():
        logger.warning(f"[*] File storico non trovato: {HISTORY_CSV}")
        return []

    try:
        with open(HISTORY_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if limit:
                rows = rows[-limit:]

            logger.info(f"[*] Letti {len(rows)} record storici")
            return rows

    except Exception as e:
        logger.error(f"[!] Errore lettura storico CSV: {e}")
        return []


# ============================================================================
# SEZIONE 7: FUNZIONI PRINCIPALI DI MONITORAGGIO
# ============================================================================

def show_current_weather(lat, lon, api_key, config):
    """
    Mostra i dati meteo correnti e invia notifica se abilitato.

    Questa è la funzione principale chiamata periodicamente dallo scheduler.

    Args:
        lat (float): Latitudine
        lon (float): Longitudine
        api_key (str): API key
        config (dict): Configurazione

    Returns:
        bool: True se operazione completata con successo
    """
    logger.info("[*] ================================================")
    logger.info(f"[*] Controllo meteo alle {datetime.now().strftime('%H:%M:%S')}")

    # Recupera dati meteo
    weather_data = fetch_weather_data(lat, lon, api_key)

    if not weather_data:
        logger.error("[!] Impossibile recuperare dati meteo")
        return False

    # Salva nei dati storici
    save_weather_history(weather_data)

    # Formatta messaggio meteo
    weather_message = format_weather_message(weather_data)
    logger.info(f"[*] METEO:\n{weather_message}")

    # Verifica alert
    alerts = check_weather_alerts(weather_data, config)

    # Invia notifica meteo regolare se abilitato
    if config.get('notifications_enabled', True):
        title = f"Meteo: {weather_data.get('weather_description', 'N/A').capitalize()}"
        send_notification(title, weather_message)
        log_notification(title, weather_message, "weather")

    # Invia notifiche per ogni alert
    for alert in alerts:
        logger.warning(f"[*] ALERT: {alert}")
        send_notification("[!] ALERT METEO", alert)
        log_notification("[!] ALERT METEO", alert, "alert")

    logger.info("[OK] Controllo meteo completato")
    return True


def weather_monitor_job(lat, lon, api_key, config, scheduler):
    """
    Job periodico per il monitoraggio meteo.

    Questa funzione viene chiamata dallo scheduler e pianifica
    automaticamente la prossima esecuzione.

    Args:
        lat (float): Latitudine
        lon (float): Longitudine
        api_key (str): API key
        config (dict): Configurazione
        scheduler (sched.scheduler): Scheduler per prossima esecuzione
    """
    # Esegue controllo meteo
    show_current_weather(lat, lon, api_key, config)

    # Calcola intervallo in secondi
    interval_minutes = config.get('interval_minutes', 10)
    delay = interval_minutes * 60

    # Pianifica prossima esecuzione
    scheduler.enter(delay, 1, weather_monitor_job,
                   (lat, lon, api_key, config, scheduler))

    logger.info(f"[*] Prossimo controllo tra {interval_minutes} minuti")


def run_scheduler(lat, lon, api_key, config):
    """
    Avvia lo scheduler per controlli meteo periodici.

    Args:
        lat (float): Latitudine
        lon (float): Longitudine
        api_key (str): API key
        config (dict): Configurazione
    """
    logger.info("[*] Avvio scheduler Weather Notifier")
    logger.info(f"[*] Frequenza controllo: {config.get('interval_minutes', 10)} minuti")
    logger.info("[*] Premi Ctrl+C per interrompere")

    # Crea scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    # Esegui primo controllo immediato
    show_current_weather(lat, lon, api_key, config)

    # Pianifica controlli periodici
    interval_minutes = config.get('interval_minutes', 10)
    delay = interval_minutes * 60
    scheduler.enter(delay, 1, weather_monitor_job,
                   (lat, lon, api_key, config, scheduler))

    # Avvia loop scheduler (bloccante)
    try:
        scheduler.run()
    except KeyboardInterrupt:
        logger.info("\n[*] Interruzione ricevuta da utente")
        logger.info("[*] Arresto Weather Notifier...")
    except Exception as e:
        logger.error(f"[!] Errore nel scheduler: {e}")


# ============================================================================
# SEZIONE 8: INTERFACCIA CLI E MAIN
# ============================================================================

def parse_arguments():
    """
    Parsing argomenti da riga di comando con argparse.

    Returns:
        argparse.Namespace: Argomenti parsati
    """
    parser = argparse.ArgumentParser(
        description='Weather Notifier - Sistema di Monitoraggio Meteo con Notifiche',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:

  # Controllo singolo per città
  python weather_notifier.py --city "Rome,IT"

  # Monitoraggio continuo ogni 10 minuti
  python weather_notifier.py --city "Milan,IT" --interval 10

  # Con coordinate specifiche
  python weather_notifier.py --coords 41.9028,12.4964

  # Imposta threshold temperatura personalizzati
  python weather_notifier.py --city "London,GB" --temp-high 25 --temp-low 10

  # Modalità verbose per debug
  python weather_notifier.py --city "Paris,FR" --verbose

  # Specifica API key propria
  python weather_notifier.py --city "Berlin,DE" --api-key "tua_key_qui"

Per ottenere una API key gratuita:
  https://openweathermap.org/api
        """
    )

    # Argomenti posizione (mutualmente esclusivi)
    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--city',
        type=str,
        help='Nome città nel formato "City,CountryCode" (es: "Rome,IT")'
    )
    location_group.add_argument(
        '--coords',
        type=str,
        help='Coordinate nel formato "lat,lon" (es: "41.9028,12.4964")'
    )

    # Frequenza controllo
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Frequenza controllo in minuti (default: 10)'
    )

    # Threshold temperatura
    parser.add_argument(
        '--temp-high',
        type=float,
        default=30.0,
        help='Soglia temperatura alta in Celsius (default: 30.0)'
    )
    parser.add_argument(
        '--temp-low',
        type=float,
        default=5.0,
        help='Soglia temperatura bassa in Celsius (default: 5.0)'
    )

    # Toggle alert
    parser.add_argument(
        '--no-rain-alert',
        action='store_true',
        help='Disabilita alert pioggia'
    )
    parser.add_argument(
        '--no-snow-alert',
        action='store_true',
        help='Disabilita alert neve'
    )
    parser.add_argument(
        '--no-temp-alerts',
        action='store_true',
        help='Disabilita alert temperatura'
    )

    # Notifiche
    parser.add_argument(
        '--no-notifications',
        action='store_true',
        help='Disabilita notifiche desktop (solo log)'
    )

    # Modalità operativa
    parser.add_argument(
        '--once',
        action='store_true',
        help='Esegui solo un controllo e esci (nessun monitoraggio continuo)'
    )

    # API key
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key OpenWeatherMap (se non specificata, cerca file o usa demo)'
    )
    parser.add_argument(
        '--save-key',
        action='store_true',
        help='Salva la API key specificata per utilizzi futuri'
    )

    # Debug
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modalità verbose con log dettagliati'
    )

    # Storico
    parser.add_argument(
        '--show-history',
        type=int,
        metavar='N',
        help='Mostra gli ultimi N record storici e esci'
    )

    # Configurazione
    parser.add_argument(
        '--save-config',
        action='store_true',
        help='Salva la configurazione corrente per usi futuri'
    )

    return parser.parse_args()


def main():
    """
    Funzione principale di ingresso del programma.

    Gestisce il parsing degli argomenti, configurazione e avvio
    del monitoraggio meteo.
    """
    # Parse argomenti CLI
    args = parse_arguments()

    # Riconfigura logging in base a verbose
    global logger
    logger = setup_logging(args.verbose)

    logger.info("[*] ================================================")
    logger.info("[*] WEATHER NOTIFIER - Sistema di Monitoraggio Meteo")
    logger.info("[*] ================================================")

    # Gestisci visualizzazione storico
    if args.show_history:
        history = read_weather_history(args.show_history)
        if history:
            print("\n[+] ULTIMI RECORD STORICI:")
            print("-" * 80)
            for record in history:
                print(f"\nTimestamp: {record.get('timestamp', 'N/A')}")
                print(f"Temperatura: {record.get('temperature', 'N/A')}C "
                      f"(percepita: {record.get('feels_like', 'N/A')}C)")
                print(f"Condizioni: {record.get('weather_description', 'N/A')}")
                print(f"Umidita: {record.get('humidity', 'N/A')}%")
                print("-" * 80)
        else:
            print("[!] Nessun dato storico disponibile")
        return

    # Carica o usa API key
    if args.api_key:
        api_key = args.api_key
        if args.save_key:
            save_api_key(api_key)
    else:
        api_key = load_api_key()

    # Avvisa se uso demo key
    if api_key == DEMO_API_KEY:
        print("\n[!] ATTENZIONE: Stai usando la API key demo")
        print("[!] Per uso completo, ottieni una key gratuita:")
        print("[!] https://openweathermap.org/api\n")

    # Carica configurazione esistente
    saved_config = load_config()

    # Prepara configurazione corrente
    config = {
        'city': args.city if args.city else saved_config.get('city', 'Rome,IT'),
        'interval_minutes': args.interval if args.interval else saved_config.get('interval_minutes', 10),
        'temp_threshold_high': args.temp_high if args.temp_high else saved_config.get('temp_threshold_high', 30.0),
        'temp_threshold_low': args.temp_low if args.temp_low else saved_config.get('temp_threshold_low', 5.0),
        'alert_rain': not args.no_rain_alert and saved_config.get('alert_rain', True),
        'alert_snow': not args.no_snow_alert and saved_config.get('alert_snow', True),
        'alert_temp_high': not args.no_temp_alerts and saved_config.get('alert_temp_high', True),
        'alert_temp_low': not args.no_temp_alerts and saved_config.get('alert_temp_low', True),
        'notifications_enabled': not args.no_notifications and saved_config.get('notifications_enabled', True)
    }

    # Salva configurazione se richiesto
    if args.save_config:
        save_config(config)

    # Ottieni coordinate
    lat, lon, location_name = None, None, None

    if args.coords:
        # Coordinate dirette
        try:
            parts = args.coords.split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            location_name = f"{lat},{lon}"
            logger.info(f"[*] Uso coordinate dirette: {lat}, {lon}")
        except (ValueError, IndexError) as e:
            logger.error(f"[!] Formato coordinate non valido: {e}")
            print("[!] Errore: Formato coordinate deve essere 'lat,lon'")
            print("    Esempio: --coords 41.9028,12.4964")
            return 1
    else:
        # Ottieni coordinate da nome città
        city = config.get('city', 'Rome,IT')
        lat, lon, location_name = get_coordinates(city, api_key)

        if lat is None or lon is None:
            print(f"[!] Impossibile trovare coordinate per: {city}")
            print("[!] Verifica il nome della città (formato: 'City,CountryCode')")
            print("[!] Esempio: 'Rome,IT' o 'London,GB'")
            return 1

    # Mostra configurazione
    print(f"\n[+] CONFIGURAZIONE:")
    print(f"    Locazione: {location_name}")
    print(f"    Coordinate: {lat}, {lon}")
    print(f"    Intervallo: {config['interval_minutes']} minuti")
    print(f"    Soglia alta: {config['temp_threshold_high']}C")
    print(f"    Soglia bassa: {config['temp_threshold_low']}C")
    print(f"    Alert pioggia: {'SI' if config['alert_rain'] else 'NO'}")
    print(f"    Alert neve: {'SI' if config['alert_snow'] else 'NO'}")
    print(f"    Alert temperatura: {'SI' if config['alert_temp_high'] or config['alert_temp_low'] else 'NO'}")
    print(f"    Notifiche: {'SI' if config['notifications_enabled'] else 'NO'}")
    print()

    # Esegui in base alla modalità
    if args.once:
        # Controllo singolo
        success = show_current_weather(lat, lon, api_key, config)
        return 0 if success else 1
    else:
        # Monitoraggio continuo
        print("[*] Avvio monitoraggio continuo...")
        print("[*] Premi Ctrl+C per interrompere\n")

        try:
            run_scheduler(lat, lon, api_key, config)
        except KeyboardInterrupt:
            print("\n\n[*] Arrivederci!")
            return 0

    return 0


# ============================================================================
# PUNTO DI INGRESSO
# ============================================================================

if __name__ == "__main__":
    """
    Punto di ingresso principale quando lo script viene eseguito.

    Gestisce eccezioni globali e codici di uscita.
    """
    try:
        exit_code = main()
        sys.exit(exit_code if exit_code is not None else 0)
    except KeyboardInterrupt:
        print("\n\n[*] Interruzione ricevuta")
        sys.exit(130)  # 130 = standard exit code per SIGINT
    except Exception as e:
        logger.exception(f"[!] Errore fatale: {e}")
        sys.exit(1)


# ============================================================================
# FINE DEL FILE
# ============================================================================
# Questo script è stato creato a scopo educativo.
# Sentiti libero di modificarlo e migliorarlo per le tue esigenze.
#
# Risorse utili:
#   - OpenWeatherMap API: https://openweathermap.org/api
#   - Documentazione Python: https://docs.python.org/3/
#   - requests library: https://docs.python-requests.org/
# ============================================================================
