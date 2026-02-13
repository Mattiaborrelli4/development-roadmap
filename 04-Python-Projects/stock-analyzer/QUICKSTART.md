# Guida Rapida - Stock Price Analyzer

## Primi Passi

### 1. Installazione Dipendenze

Apri il terminale nella directory del progetto:

```bash
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\stock-analyzer"
```

Installa le librerie necessarie:

```bash
pip install -r requirements.txt
```

### 2. Verifica Installazione

```bash
python test_setup.py
```

Dovresti vedere: `[TUTTI I TEST PASSATI]`

### 3. Avvia il Programma

```bash
python stock_analyzer.py
```

## Esempio di Utilizzo Rapido

### Opzione 1: Usa Dati di Esempio (Piu Veloce)

1. Seleziona `1` dal menu
2. Inserisci simbolo: `AAPL` (o premi Invio)
3. Scegli: `2` (usa dati di esempio)
4. Scegli: `s` (visualizza grafico)
5. Scegli: `s` (salva CSV)

### Opzione 2: Usa API Alpha Vantage (Dati Reali)

1. Ottieni API key gratuita: https://www.alphavantage.co/support/#api-key
2. Seleziona `1` dal menu
3. Inserisci simbolo: `MSFT`
4. Scegli: `1` (usa API)
5. Incolla la tua API key
6. Visualizza i risultati!

## Simboli Azionari Popolari da Provare

| Simbolo | Azienda |
|---------|---------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| GOOGL | Alphabet Inc. (Google) |
| AMZN | Amazon.com Inc. |
| TSLA | Tesla Inc. |
| META | Meta Platforms (Facebook) |
| NVDA | NVIDIA Corporation |
| JPM | JPMorgan Chase & Co. |

## Cosa Imparerai

Usando questo programma, imparerai:

- **Analisi Dati**: Usare pandas per manipolare dati finanziari
- **Visualizzazione**: Creare grafici con matplotlib
- **Statistica**: Calcolare medie, deviazione standard, volatilita
- **API**: Fare richieste HTTP a servizi web
- **File I/O**: Salvare e caricare dati in CSV
- **Machine Learning Base**: Regressione lineare per previsioni

## Risoluzione Problemi

### Errore: "No module named 'pandas'"

```bash
pip install pandas matplotlib numpy requests
```

### Errore: "API call limit"

Alpha Vantage ha un limite di 5 chiamate al minuto. Aspetta un minuto e riprova.

### Il grafico non appare

Su Windows, il grafico dovrebbe aprirsi in una nuova finestra. Se non appare, controlla che matplotlib sia installato correttamente.

### Errore di permission

Assicurati di avere i permessi di scrittura nella directory del progetto.

## Prossimi Passi

Dopo aver provato il programma:

1. **Esplora il codice**: Leggi i commenti per capire come funziona
2. **Modifica i parametri**: Prova diverse medie mobili (10, 30 giorni)
3. **Aggiungi indicatori**: Implementa RSI o MACD
4. **Backend diverso**: Integra altre API (Yahoo Finance, IEX)
5. **Machine Learning**: Prova modelli piu complessi per previsioni

## Risorse Online

- **Pandas Tutorial**: https://pandas.pydata.org/docs/getting_started/intro_tutorials/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/index.html
- **Investopedia**: https://www.investopedia.com/ (per concetti finanziari)

## Supporto

Per domande o problemi:
1. Controlla la sezione "Aiuto" nel programma (opzione 5 del menu)
2. Leggi i commenti nel codice sorgente
3. Consulta la documentazione delle librerie

Buon apprendimento!
