# 🚀 Guida Rapida - File Monitor

## Setup in 3 Passaggi

### 1️⃣ Installa le Dipendenze
```bash
cd file-monitor
pip install -r requirements.txt
```

### 2️⃣ Avvia il Monitoraggio
```bash
# Windows
python file_monitor.py

# Linux/macOS
python3 file_monitor.py
```

### 3️⃣ Apporta Modifiche
Crea, modifica o elimina file nella directory e guarda gli eventi in tempo reale!

## Comandi Principali

| Comando | Descrizione |
|---------|-------------|
| `python file_monitor.py` | Monitora directory corrente |
| `python file_monitor.py -v` | Output dettagliato |
| `python file_monitor.py -l log.txt` | Salva log su file |
| `python file_monitor.py --no-recursive` | Solo directory principale |
| `python test_operations.py` | Esegui test automatici |

## Quick Start Interattivo

### Windows
```bash
start_monitor.bat
```

### Linux/macOS
```bash
chmod +x start_monitor.sh
./start_monitor.sh
```

## Esempio di Utilizzo

```bash
# Terminale 1: Avvia monitor
python file_monitor.py -v

# Terminale 2: Crea modifica file
echo "test" > prova.txt
mv prova.txt nuovo.txt
rm nuovo.txt
```

Output atteso:
```
[2024-02-15 10:30:00] FILE CREATO: prova.txt
[2024-02-15 10:30:05] FILE SPOSTATO: nuovo.txt - da: prova.txt
[2024-02-15 10:30:10] FILE ELIMINATO: nuovo.txt
```

## Troubleshooting

**Problema**: `ModuleNotFoundError: No module named 'watchdog'`
**Soluzione**: `pip install watchdog`

**Problema**: Permission denied
**Soluzione**: Esegui con permessi appropriati o cambia directory

**Problema**: Nessun evento rilevato
**Soluzione**: Verifica di modificare file nella directory corretta

## Risorse

- Documentazione completa: `README.md`
- Struttura progetto: `PROJECT_STRUCTURE.md`
- Esempi avanzati: `config_example.py`

## Supporto

Per problemi o domande, consulta la documentazione nel file `README.md`.
