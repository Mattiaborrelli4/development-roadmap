# Log Analyzer - Guida Rapida

## Primi Passi

### 1. Installazione (Opzionale)

```bash
# Installa dipendenze per colors e YAML
pip install colorama pyyaml
```

### 2. Esegui il Demo

```bash
python demo.py
```

Questo mostra tutte le funzionalità del tool.

### 3. Analizza un File di Log

```bash
# Analisi completa
python main.py analyze sample-logs/access.log

# Solo errori
python main.py analyze sample-logs/access.log --level ERROR

# Genera report HTML
python main.py analyze sample-logs/access.log --output report.html
```

### 4. Statistiche

```bash
# Per ora
python main.py stats sample-logs/access.log --by hour

# Per giorno
python main.py stats sample-logs/access.log --by day

# Per livello
python main.py stats sample-logs/access.log --by level
```

### 5. Estrai IP

```bash
# Tutti gli IP
python main.py extract-ips sample-logs/access.log

# Top 10
python main.py extract-ips sample-logs/access.log --top 10
```

### 6. Real-time Monitoring

```bash
# Segui il file in tempo reale
python main.py tail sample-logs/access.log

# Solo errori
python main.py tail sample-logs/access.log --level ERROR
```

## Log Formats Supportati

Il tool auto-rileva il formato, ma puoi specificarlo:

```bash
--format apache   # Apache CLF/Combined
--format nginx    # Nginx default
--format custom   # Custom application logs
```

## Struttura Progetto

```
log-analyzer/
├── main.py              # CLI entry point
├── parsers/             # Log parsing modules
├── analyzers/           # Analysis modules
├── reporters/           # Report generation
├── sample-logs/         # Sample log files
├── demo.py             # Demo script
└── README.md           # Documentazione completa
```

## Troubleshooting

### Errori di Encoding

Il tool usa automaticamente `errors='ignore'` per gestire caratteri non validi.

### Performance su File Grandi

Usa filtri per ridurre memoria:

```bash
python main.py analyze large.log --level ERROR
```

### Windows Console Colors

Per colors su Windows, installa colorama:

```bash
pip install colorama
```

## Concetti Appresi

Questo progetto insegna:

1. **File I/O** - Lettura efficiente di file
2. **Regex** - Pattern matching per parsing
3. **Data Structures** - Counter, defaultdict
4. **CLI Development** - argparse per CLI
5. **Real-time Monitoring** - seek/read loop
6. **Report Generation** - Text e HTML

## Risorse

- README completo: `README.md`
- Demo interattivo: `python demo.py`
- Help: `python main.py --help`

Buon apprendimento! 🎓
