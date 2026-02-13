# Quick Start Guide

Guida rapida per iniziare con il Network Echo Daemon.

## 🚀 Quick Start (5 minuti)

### 1. Installa Dipendenze

```bash
pip install pyyaml
```

### 2. Avvia il Daemon

```bash
# Linux/Mac
python echo_daemon.py start

# Windows (usa config Windows)
python echo_daemon.py --config config/config_windows.yaml start
```

### 3. Verifica Stato

```bash
python echo_daemon.py status
# Output: Status: RUNNING (PID 12345)
```

### 4. Test con Client

```bash
# Nuovo terminal
python tests/client.py --protocol tcp --message "Hello!"
# Output: [TCP] Echo OK: 'Hello!'
```

### 5. Ferma il Daemon

```bash
python echo_daemon.py stop
```

## 🧪 Esegui Tutti i Test

```bash
# Linux/Mac
bash tests/test.sh

# Windows
tests\test.bat
```

## 📝 Comandi Principali

| Comando | Descrizione |
|---------|-------------|
| `python echo_daemon.py start` | Avvia daemon |
| `python echo_daemon.py stop` | Ferma daemon |
| `python echo_daemon.py status` | Mostra stato |
| `python tests/client.py --protocol tcp` | Test TCP |
| `python tests/client.py --protocol udp` | Test UDP |

## 🔧 Configurazione Rapida

Modifica `config/config.yaml`:

```yaml
port: 8888              # Cambia porta
log_level: DEBUG        # Più verbose
daemonize: false        # Foreground mode
```

## 💡 Esempi Utili

### Test Multiple Client
```bash
for i in {1..5}; do
    python tests/client.py --protocol tcp --message "Client $i" &
done
```

### Test Continuous
```bash
# Test per 30 secondi
python tests/client.py --protocol tcp --continuous 30
```

### Monitor Log
```bash
# Linux/Mac
tail -f /var/log/echo-daemon.log

# Windows
Get-Content logs\echo-daemon.log -Wait
```

## ❓ Troubleshooting Rapido

**Porta già in uso?**
```bash
# Cambia porta in config.yaml
port: 9999
```

**Permission denied su /var/log?**
```bash
# Usa path corrente o esegui come root
# Modifica config.yaml:
log_file: ./logs/echo-daemon.log
```

**Daemon non parte?**
```bash
# Controlla i log
tail -f logs/echo-daemon.log

# O esegui in foreground (config: daemonize: false)
python echo_daemon.py start
```

## 📚 Next Steps

Leggi il [README.md](README.md) completo per:
- Spiegazione dettagliata dei concetti
- Troubleshooting avanzato
- Architettura del sistema
- Best practices

Buon apprendimento! 🎓
