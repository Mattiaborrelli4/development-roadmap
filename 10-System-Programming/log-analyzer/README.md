# Log Analyzer

**Tool Educativo per System Programming - Log Parsing e Analysis**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

## Scopo Educativo

Questo progetto è stato creato come **strumento educativo** per apprendere le tecniche di **System Programming** attraverso l'analisi di file di log. È perfetto per studenti e sviluppatori che vogliono approfondire:

- **File I/O**: Lettura efficiente di grandi file di log
- **Regex Parsing**: Pattern matching per estrarre dati strutturati
- **Data Analysis**: Statistiche e aggregazione di dati
- **CLI Development**: Creazione di interfacce a riga di comando
- **Real-time Monitoring**: Implementazione di tail -f style monitoring

## Funzionalità

### 1. Log Parsing
- **Apache Common Log Format** (CLF e Combined)
- **Nginx default format**
- **Custom application logs** (Python, Java, generici)
- **Auto-detection** del formato log

### 2. Filtering
- Per livello di log (ERROR, WARN, INFO, DEBUG)
- Per intervallo temporale
- Per IP address
- Per HTTP status code
- Per path e method
- Filtri custom composti

### 3. Statistiche
- Count per livello/ora/giorno
- Error rate calculation
- Top error messages
- Top IP addresses
- HTTP status distribution
- Request path analytics

### 4. Estrazione Dati
- IP addresses (IPv4/IPv6)
- Error patterns
- URLs e User Agents
- Status codes
- Suspicious activity detection

### 5. Report
- **Text**: Report testuali per console
- **HTML**: Report interattivi con grafici CSS
- Real-time tail mode (come `tail -f`)

## Installazione

### Requisiti
- Python 3.10 o superiore
- pip (package manager)

### Setup

```bash
# Clone o naviga nella directory del progetto
cd log-analyzer

# Installa dipendenze opzionali (per colors e YAML)
pip install colorama pyyaml
```

## Struttura del Progetto

```
log-analyzer/
├── main.py                 # Entry point CLI
├── parsers/                # Log parsers
│   ├── apache.py          # Apache log parser
│   ├── nginx.py           # Nginx log parser
│   └── custom.py          # Custom format parser
├── analyzers/              # Analysis modules
│   ├── filter.py          # Log filtering
│   ├── stats.py           # Statistics generation
│   └── extractor.py       # Data extraction
├── reporters/              # Report generators
│   ├── text.py            # Text report
│   └── html.py            # HTML report
├── config/
│   └── patterns.yaml      # Log patterns config
├── sample-logs/           # Sample log files
│   ├── access.log        # Apache access log
│   └── application.log   # Custom app log
└── README.md
```

## Utilizzo

### Analisi Base

Analizza un file di log:

```bash
python main.py analyze sample-logs/access.log
```

### Filtri

Filtra per livello:

```bash
python main.py analyze sample-logs/access.log --level ERROR
```

Filtra per tempo:

```bash
python main.py analyze sample-logs/access.log \
    --start-time "2023-10-10T13:00:00" \
    --end-time "2023-10-10T14:00:00"
```

### Genera Report HTML

```bash
python main.py analyze sample-logs/access.log --output report.html
```

Apri `report.html` nel browser per vedere statistiche interattive.

### Real-time Monitoring

Segui un file in tempo reale:

```bash
python main.py tail sample-logs/access.log
```

Filtra solo errori:

```bash
python main.py tail sample-logs/access.log --level ERROR
```

### Statistiche

Mostra statistiche orarie:

```bash
python main.py stats sample-logs/access.log --by hour
```

Mostra statistiche giornaliere:

```bash
python main.py stats sample-logs/access.log --by day
```

Mostra per livello:

```bash
python main.py stats sample-logs/access.log --by level
```

### Estrazione IP

Estrai tutti gli IP addresses:

```bash
python main.py extract-ips sample-logs/access.log
```

Mostra top 10 IP per richieste:

```bash
python main.py extract-ips sample-logs/access.log --top 10
```

### Specifica Format

Se l'auto-detection non funziona:

```bash
# Apache
python main.py analyze access.log --format apache

# Nginx
python main.py analyze access.log --format nginx

# Custom
python main.py analyze application.log --format custom
```

## Format di Log Supportati

### Apache Common Log Format (CLF)

```
127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
```

### Apache Combined Log Format

```
127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326 "http://example.com" "Mozilla/5.0"
```

### Nginx Default Format

```
192.168.1.1 - - [10/Oct/2023:13:55:36] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

### Custom Application Log

```
2024-01-15 10:30:00,123 [INFO] [main] Application started
2024-01-15 10:30:05,456 [ERROR] [database] Connection failed
```

## Concetti di System Programming

Questo progetto insegna diversi concetti fondamentali:

### 1. File I/O

```python
# Lettura efficiente di grandi file
with open(filepath, 'r', encoding='utf-8') as f:
    for line in f:
        # Process line
```

### 2. Regex Parsing

```python
# Pattern compilation per performance
pattern = re.compile(r'^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+...')
match = pattern.match(line)
data = match.groupdict()
```

### 3. List Comprehension

```python
# Filtering efficiente
errors = [e for e in entries if e.get('level') == 'ERROR']
```

### 4. Data Aggregation

```python
# collections.Counter per counting
from collections import Counter
ip_counts = Counter(entry['ip'] for entry in entries)
```

### 5. Generator Expressions

```python
# Memory efficient filtering
def filter_entries(entries):
    for entry in entries:
        if entry.get('level') == 'ERROR':
            yield entry
```

### 6. Real-time Monitoring

```python
# seek per posizionarsi alla fine del file
f.seek(0, 2)  # EOF
while True:
    line = f.readline()
    if not line:
        time.sleep(0.1)
        continue
    # Process new line
```

## Esempi di Output

### Text Report

```
====================================================================================================
                              LOG ANALYZER - RIEPILOGO STATISTICHE
====================================================================================================

INFORMAZIONI GENERALI
----------------------------------------------------------------------------------------------------
  Totale Entries:        1,523
  IP Unici:              47
  Range Temporale:       2023-10-10 13:55 - 2023-10-10 13:57 (2h 23m)

DISTRIBUZIONE PER LIVELLO
----------------------------------------------------------------------------------------------------
  ERROR        85       5.58%  ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  INFO       1,200    78.79%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░
  WARN        238     15.63%  ▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

### HTML Report

Il report HTML include:
- Tables responsive
- Bar charts CSS-based
- Color-coded status codes
- Navigation menu
- Interactive sections

## Sviluppo

### Test dei Parser

```bash
# Test Apache parser
python parsers/apache.py

# Test Nginx parser
python parsers/nginx.py

# Test Custom parser
python parsers/custom.py
```

### Test dei Moduli

```bash
# Test filtro
python analyzers/filter.py

# Test statistiche
python analyzers/stats.py

# Test estrazione
python analyzers/extractor.py
```

### Aggiungere Nuovi Parser

1. Crea un nuovo file in `parsers/`
2. Estendi la funzionalità di base
3. Implementa `parse_line()` method
4. Aggiungi al `__init__.py`

Esempio:

```python
class MyLogParser:
    def __init__(self):
        self.pattern = re.compile(...)

    def parse_line(self, line):
        match = self.pattern.match(line)
        if match:
            return match.groupdict()
        return None
```

## Troubleshooting

### Encoding Errors

Se incontri errori di encoding:

```bash
python main.py analyze file.log  # Usa errors='ignore' automatico
```

### Memory Issues per File Grandi

Per file molto grandi (>1GB), usa il filtraggio prima di caricare tutto:

```bash
# Solo errori - usa meno memoria
python main.py analyze large.log --level ERROR
```

### Performance Tips

- Usa `--format` per saltare auto-detection
- Specifica filtri per ridurre il dataset
- Usa tail mode invece di caricare file interi

## Roadmap

Funzionalità future:

- [ ] Supporto per log in formato JSON
- [ ] Export in CSV/JSON
- [ ] Grafici real-time
- [ ] Alert thresholds
- [ ] Config file personalizzabile
- [ ] Multi-file analysis
- [ ] Log rotation handling
- [ ] Compression support (.gz)

## Risorse Educativi

### Tutorial e Guide

- [Python Regex Documentation](https://docs.python.org/3/library/re.html)
- [File I/O in Python](https://docs.python.org/3/tutorial/inputoutput.html)
- [CLI Apps with argparse](https://docs.python.org/3/library/argparse.html)

### System Programming Topics

- **File Descriptors**: Understanding low-level I/O
- **Buffering**: Read buffering vs line-by-line
- **Memory Mapping**: mmap per file grandi
- **Inotify**: File system monitoring (Linux)
- **Signals**: Graceful shutdown handling

## License

Questo progetto è creato a scopo **educativo**. Sei libero di usarlo, modificarlo e distribuirlo per scopi di apprendimento.

## Contributo

Contributi educativi sono benvenuti! Idee:

- Nuovi formati di log
- Miglioramenti performance
- Nuovi tipi di grafici
- Documentazione aggiuntiva
- Esempi di casi d'uso

## Autore

Creato come progetto educativo per **System Programming**.

---

**Buon apprendimento!** 🎓

Per domande o suggerimenti, sentiti libero di aprire una issue.
