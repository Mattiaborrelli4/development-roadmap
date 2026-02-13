# Quick Start Guide

Guida rapida per iniziare con Weather Notifier in 5 minuti.

## 1. Installazione

```bash
# Installa le dipendenze
pip install -r requirements.txt
```

## 2. Ottieni API Key

1. Vai su https://openweathermap.org/api
2. Registrati gratuitamente
3. Copia la tua API Key dalla dashboard

## 3. Configurazione

```bash
# Crea il file di configurazione
python weather_notifier.py --create-config
```

Modifica `config.json` per aggiungere le tue città:

```json
{
  "cities": ["Milan", "Rome", "London"],
  "check_interval": 3600,
  "alerts": {
    "temp_high": 35,
    "temp_low": 0,
    "conditions": ["Rain", "Snow"]
  },
  "units": "metric"
}
```

## 4. Esecuzione

### Test Singolo
```bash
python weather_notifier.py --api-key TUA_API_KEY --once
```

### Monitoraggio Continuo
```bash
python weather_notifier.py --api-key TUA_API_KEY
```

### Specifica Città da CLI
```bash
python weather_notifier.py --api-key TUA_API_KEY --cities Milan Paris --once
```

## 5. Verifica

Dovresti vedere:
- Output in console con i dati meteo
- Notifiche desktop se ci sono alert
- File `weather_history.csv` creato
- File `weather_notifier.log` con log dettagliati

## Troubleshooting Rapido

| Problema | Soluzione |
|----------|-----------|
| API key non funziona | Aspetta 10-15 minuti per attivazione |
| Nessuna notifica | Installa plyer: `pip install plyer` |
| Città non trovata | Prova con codice paese: "London,UK" |
| Rate limit error | Aumenta `check_interval` nel config |

## Prossimi Passi

- Leggi `README_NOTIFIER.md` per documentazione completa
- Esplora gli esercizi proposti per imparare di più
- Personalizza gli alert in base alle tue esigenze

Buon monitoring! 🌤️
