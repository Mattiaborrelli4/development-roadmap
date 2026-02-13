# Analizzatore di Prezzi Azionari / Stock Price Analyzer

Programma educativo per l'analisi tecnica di base dei prezzi azionari, scritto in Python.

## Caratteristiche

- **Recupero Dati**: API Alpha Vantage o dati di esempio generati automaticamente
- **Medie Mobili**: Calcolo SMA a 20 e 50 giorni
- **Grafici**: Visualizzazione con matplotlib dei prezzi e indicatori
- **Statistiche**: Min, max, media, mediana, deviazione standard, volatilita
- **Previsioni**: Regressione lineare per identificare trend
- **CSV**: Salvataggio e caricamento dati per analisi offline
- **Interfaccia**: Menu testuale semplice in italiano

## Requisiti

- Python 3.7+
- Librerie: pandas, matplotlib, numpy, requests

## Installazione

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

2. Esegui il programma:
```bash
python stock_analyzer.py
```

## Come Funziona

### Modalita Dati di Esempio (Nessuna API Key Richiesta)

Il programma genera automaticamente dati realistici per testare tutte le funzionalita senza bisogno di registrarsi a servizi esterni.

### Modalita API (Opzionale)

Per usare dati reali:
1. Registrati gratis su https://www.alphavantage.co/support/#api-key
2. Copia la tua API key
3. Incollala quando il programma la richiede

**Nota**: Alpha Vantage ha un limite di 5 chiamate/minute per account gratuiti.

## Funzionalita Principali

### 1. Analizza Azione
- Inserisci simbolo (es. AAPL, MSFT, GOOGL)
- Scegli tra API o dati di esempio
- Visualizza automaticamente:
  - Grafico con prezzi e medie mobili
  - Statistiche complete
  - Analisi del trend
  - Suggerimento di investimento (educativo)

### 2. Carica da CSV
- Analizza file CSV precedentemente salvati
- Perfetto per analisi offline

### 3. Visualizza Grafico
- Crea solo il grafico da CSV esistente

### 4. File CSV Disponibili
- Mostra tutti i file nella directory

## Spiegazione Indicatori

### Medie Mobili (MA)
- **MA20**: Media degli ultimi 20 giorni (breve termine)
  - Il prezzo sopra MA20 indica forza
  - Il prezzo sotto MA20 indica debolezza
- **MA50**: Media degli ultimi 50 giorni (lungo termine)
  - Usata per confermare trend principali

### Volatilita
- Misurata dalla deviazione standard
- Alta volatilita = grandi oscillazioni
- Bassa volatilita = prezzo stabile

### Regressione Lineare
- Trova la retta che meglio approssima i dati
- Slope positivo = trend rialzista
- Slope negativo = trend ribassista

## Struttura File

```
stock-analyzer/
├── stock_analyzer.py    # Programma principale
├── requirements.txt      # Dipendenze Python
├── README.md            # Questo file
├── stock_data.csv       # Dati salvati (generato dopo primo uso)
└── charts/              # Directory per i grafici salvati
    └── *.png            # Grafici esportati
```

## Esempio di Output

```
============================================================
ANALISI COMPLETA: AAPL
============================================================

[INFO GENERALI]
  Simbolo:        AAPL
  Periodo:        2024-01-01 a 2024-03-31
  Giorni analizzati: 90

[STATISTICHE PREZZO]
  Prezzo Corrente: $172.50
  Massimo:        $178.25
  Minimo:         $145.30
  Media:          $162.40
  Variazione:     $32.95 (22.7%)

[VOLATILITA']
  Deviazione Std: $8.45
  Volatilita':    5.20%
  Livello:        Media

[TREND]
  Variazione giornaliera media: $0.3680
  Variazione prevista 30gg:     $11.04
  Trend attuale: RIALZISTA FORTE
  Suggerimento: OPPORTUNITA' DI ACQUISTO
```

## Progetti Educativi Correlati

Questo e' il progetto n.4 della serie "Project Ideas Portfolio":
1. Todo List Manager
2. Password Manager
3. Weather Dashboard
4. **Stock Price Analyzer** (questo progetto)
5. E-commerce Simulator

## Note Importanti

- Questo programma e' **solo a scopo educativo**
- Non costituisce consiglio di investimento
- I dati e le analisi sono a titolo dimostrativo
- Investire in borsa comporta rischi reali

## Concetti Python Imparati

- **Pandas**: Manipolazione dati tabellari (DataFrame)
- **Matplotlib**: Creazione grafici scientifici
- **NumPy**: Calcoli numerici e statistici
- **Requests**: Chiamate HTTP a API esterne
- **File I/O**: Lettura/scrittura CSV
- **Statistica**: Medie, deviazione standard, regressione

## Risorse per Ulteriori Studi

- Documentazione Pandas: https://pandas.pydata.org/docs/
- Documentazione Matplotlib: https://matplotlib.org/stable/contents.html
- Alpha Vantage Documentation: https://www.alphavantage.co/documentation/
- Analisi Tecnica: https://www.investopedia.com/terms/t/technicalanalysis.asp

## Licenza

Progetto educativo open source. Usa e modifica liberamente per scopi didattici.
