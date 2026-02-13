"""
Analizzatore di Prezzi Azionari - Stock Price Analyzer
====================================================

Un programma educativo per l'analisi dei prezzi azionari con:
- Recupero dati da API o dati di esempio
- Calcolo medie mobili
- Visualizzazione grafici
- Analisi statistiche
- Previsioni con regressione lineare
- Salvataggio/caricamento da CSV

Autore: Progetto educativo per studenti universitari
Linguaggio: Python 3.x
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings

# Ignoriamo warning non critici per output piu' pulito
warnings.filterwarnings('ignore')

# Configurazioni paths
BASE_DIR = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\stock-analyzer"
CSV_PATH = os.path.join(BASE_DIR, "stock_data.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

# Assicuriamo che le directory esistano
os.makedirs(CHARTS_DIR, exist_ok=True)


def generate_sample_data(symbol: str = "SAMPLE") -> pd.DataFrame:
    """
    Genera dati di esempio per test senza API key.

    Args:
        symbol: Simbolo dell'azione (default: "SAMPLE")

    Returns:
        DataFrame con colonne: date, close, volume
    """
    print(f"\n[*] Generazione dati di esempio per {symbol}...")

    # Generiamo 90 giorni di dati (circa 3 mesi)
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')

    # Prezzo base iniziale (es. $150)
    base_price = 150.0

    # Generiamo prezzi con trend e volatilita' simulata
    np.random.seed(42)  # Per riproducibilita'
    random_changes = np.random.randn(90) * 2  # Variazioni casuali
    trend = np.linspace(0, 20, 90)  # Trend leggermente rialzista

    prices = base_price + trend + random_changes
    prices = np.maximum(prices, 50)  # Prezzo minimo $50

    # Volume casuale tra 1M e 10M
    volumes = np.random.randint(1000000, 10000000, 90)

    # Creiamo DataFrame
    df = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'close': prices.round(2),
        'volume': volumes
    })

    print(f"[*] Generati {len(df)} giorni di dati di esempio")
    return df


def fetch_stock_data(symbol: str, use_sample: bool = False, api_key: str = None) -> Optional[pd.DataFrame]:
    """
    Recupera i dati azionari da Alpha Vantage API o usa dati di esempio.

    Args:
        symbol: Simbolo dell'azione (es. "AAPL", "MSFT")
        use_sample: Se True, usa dati di esempio invece dell'API
        api_key: Chiave API di Alpha Vantage (opzionale)

    Returns:
        DataFrame con dati azionari o None se errore
    """
    print(f"\n[*] Recupero dati per: {symbol}")

    # Se richiesto, usiamo dati di esempio
    if use_sample:
        return generate_sample_data(symbol)

    # Se non c'e' API key, usiamo dati di esempio
    if not api_key:
        print("[!] Nessuna API key fornita - uso dati di esempio")
        return generate_sample_data(symbol)

    # Tentativo di recupero da Alpha Vantage API
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact'  # 100 giorni recenti
    }

    try:
        print("[*] Connessione a Alpha Vantage API...")
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"[!] Errore API: Status code {response.status_code}")
            return generate_sample_data(symbol)

        data = response.json()

        # Verifichiamo se abbiamo dati validi
        if 'Time Series (Daily)' not in data:
            print(f"[!] Errore: {data.get('Note', 'Nessun dato trovato')}")
            print("[!] Verifica simbolo o limite chiamate API (5/minuto)")
            return generate_sample_data(symbol)

        # Parse dei dati
        time_series = data['Time Series (Daily)']
        dates = []
        closes = []
        volumes = []

        for date, values in sorted(time_series.items()):
            dates.append(date)
            closes.append(float(values['4. close']))
            volumes.append(int(values['5. volume']))

        df = pd.DataFrame({
            'date': dates,
            'close': closes,
            'volume': volumes
        })

        # Ordiniamo per data (piu' recente prima)
        df = df.iloc[::-1].reset_index(drop=True)

        print(f"[*] Recuperati {len(df)} giorni di dati")
        return df

    except requests.exceptions.Timeout:
        print("[!] Timeout - uso dati di esempio")
        return generate_sample_data(symbol)
    except requests.exceptions.RequestException as e:
        print(f"[!] Errore di connessione: {e}")
        return generate_sample_data(symbol)
    except Exception as e:
        print(f"[!] Errore imprevisto: {e}")
        return generate_sample_data(symbol)


def calculate_moving_averages(prices: pd.Series, days: int) -> pd.Series:
    """
    Calcola la media mobile semplice (SMA - Simple Moving Average).

    La media mobile semplice e' la media dei prezzi degli ultimi N giorni.
    Utile per identificare trend e supporti/resistenze.

    Formula: SMA = (P1 + P2 + ... + Pn) / n
    Dove P sono i prezzi e n il numero di giorni

    Args:
        prices: Serie pandas con i prezzi di chiusura
        days: Numero di giorni per la media (es. 20, 50)

    Returns:
        Serie pandas con le medie mobili calcolate
    """
    print(f"[*] Calcolo media mobile a {days} giorni...")

    # Usiamo pandas rolling() per calcolare la media mobile
    # rolling() crea una finestra mobile di N giorni
    sma = prices.rolling(window=days).mean()

    return sma


def plot_chart(dates: List[str], prices: List[float], ma20: List[float],
               ma50: List[float], symbol: str, save: bool = True) -> str:
    """
    Crea e salva un grafico dei prezzi con medie mobili.

    Il grafico mostra:
    - Linea blu: Prezzo di chiusura
    - Linea arancione: Media mobile 20 giorni (breve termine)
    - Linea verde: Media mobile 50 giorni (lungo termine)

    Args:
        dates: Lista delle date
        prices: Lista dei prezzi di chiusura
        ma20: Lista media mobile 20 giorni
        ma50: Lista media mobile 50 giorni
        symbol: Simbolo dell'azione
        save: Se True, salva il grafico su file

    Returns:
        Path del file salvato
    """
    print(f"\n[*] Creazione grafico per {symbol}...")

    # Impostiamo lo stile (opzionale - rende i grafici piu' belli)
    plt.style.use('default')

    # Creiamo figura e assi
    fig, ax = plt.subplots(figsize=(12, 6))

    # Creiamo indice numerico per asse X
    x = range(len(dates))

    # Plot prezzi
    ax.plot(x, prices, label='Prezzo Chiusura', color='blue', linewidth=2)

    # Plot medie mobili
    ax.plot(x, ma20, label='MA 20 Giorni', color='orange', linewidth=1.5, alpha=0.7)
    ax.plot(x, ma50, label='MA 50 Giorni', color='green', linewidth=1.5, alpha=0.7)

    # Etichette e titolo
    ax.set_xlabel('Giorni', fontsize=10)
    ax.set_ylabel('Prezzo ($)', fontsize=10)
    ax.set_title(f'Andamento Prezzo: {symbol}\nCon Medie Mobili', fontsize=14, fontweight='bold')

    # Griglia e legenda
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='best', fontsize=9)

    # Ruotiamo le etichette X se necessario
    plt.xticks(rotation=45)

    # Ottimizziamo layout
    plt.tight_layout()

    # Salviamo il grafico
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{symbol}_chart_{timestamp}.png"
    filepath = os.path.join(CHARTS_DIR, filename)

    if save:
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        print(f"[*] Grafico salvato: {filepath}")

    # Mostriamo il grafico
    plt.show()
    plt.close()

    return filepath


def calculate_statistics(prices: pd.Series) -> Dict[str, float]:
    """
    Calcola statistiche base sui prezzi.

    Statistiche calcolate:
    - Minimo: Prezzo piu' basso
    - Massimo: Prezzo piu' alto
    - Media: Prezzo medio
    - Mediana: Prezzo centrale
    - Deviazione Standard: Measure di volatilita'
    - Variazione: Differenza max-min

    Args:
        prices: Serie pandas con i prezzi

    Returns:
        Dizionario con statistiche calcolate
    """
    print("\n[*] Calcolo statistiche...")

    stats = {
        'minimo': float(prices.min()),
        'massimo': float(prices.max()),
        'media': float(prices.mean()),
        'mediana': float(prices.median()),
        'deviazione_std': float(prices.std()),
        'variazione': float(prices.max() - prices.min()),
        'prezzo_corrente': float(prices.iloc[-1])  # Ultimo prezzo
    }

    return stats


def predict_trend(dates: List[str], prices: List[float]) -> Tuple[float, float, List[float]]:
    """
    Previsione semplice con regressione lineare.

    La regressione lineare trova la retta che meglio adatta i dati:
    y = mx + q
    Dove:
    - m = slope (pendenza) - indica il trend
    - q = intercept - punto di intersezione

    Se m > 0: trend rialzista
    Se m < 0: trend ribassista
    Maggiore e' |m| piu' forte e' il trend

    Args:
        dates: Lista delle date
        prices: Lista dei prezzi

    Returns:
        Tuple di (slope, intercept, predicted_prices)
    """
    print("\n[*] Calcolo previsione trend con regressione lineare...")

    # Convertiamo le date in numeri (giorni dal primo giorno)
    x = np.arange(len(prices))
    y = np.array(prices)

    # Calcoliamo regressione lineare con formula minimi quadrati
    # slope (m) e intercept (q)
    n = len(x)

    # Formule per regressione lineare:
    # m = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - (sum(x))^2)
    # q = (sum(y) - m*sum(x)) / n

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n

    # Calcoliamo prezzi previsti dalla retta
    predicted_prices = slope * x + intercept

    # Interpretazione del trend
    if slope > 0.1:
        trend_desc = "RAALZISTA FORTE"
    elif slope > 0.01:
        trend_desc = "Rialzista debole"
    elif slope < -0.1:
        trend_desc = "RIBASSISTA FORTE"
    elif slope < -0.01:
        trend_desc = "Ribassista debole"
    else:
        trend_desc = "Laterale (neutro)"

    print(f"[*] Trend identificato: {trend_desc}")
    print(f"[*] Slope (pendenza): {slope:.4f} $/giorno")

    return slope, intercept, list(predicted_prices)


def save_to_csv(data: pd.DataFrame, filename: str = None) -> str:
    """
    Salva i dati in un file CSV per uso offline.

    CSV (Comma Separated Values) e' un formato semplice
    per salvare dati tabellari in file di testo.

    Args:
        data: DataFrame con i dati da salvare
        filename: Nome del file (opzionale, default: stock_data.csv)

    Returns:
        Path del file salvato
    """
    print(f"\n[*] Salvataggio dati in CSV...")

    if filename is None:
        filename = CSV_PATH

    try:
        data.to_csv(filename, index=False, encoding='utf-8')
        print(f"[*] Dati salvati in: {filename}")
        print(f"[*] Totale record salvati: {len(data)}")
        return filename
    except Exception as e:
        print(f"[!] Errore salvataggio: {e}")
        return None


def load_from_csv(filename: str = None) -> Optional[pd.DataFrame]:
    """
    Carica dati da un file CSV esistente.

    Utile per analisi offline senza bisogno di chiamare l'API.

    Args:
        filename: Nome del file da caricare (opzionale)

    Returns:
        DataFrame con i dati caricati o None se errore
    """
    print(f"\n[*] Caricamento dati da CSV...")

    if filename is None:
        filename = CSV_PATH

    # Verifichiamo se il file esiste
    if not os.path.exists(filename):
        print(f"[!] File non trovato: {filename}")
        return None

    try:
        data = pd.read_csv(filename, encoding='utf-8')
        print(f"[*] Dati caricati da: {filename}")
        print(f"[*] Totale record caricati: {len(data)}")
        return data
    except Exception as e:
        print(f"[!] Errore caricamento: {e}")
        return None


def display_analysis(data: pd.DataFrame, stats: Dict[str, float],
                    slope: float, symbol: str):
    """
    Mostra l'analisi completa in formato leggibile.

    Include statistiche, trend e interpretazione.

    Args:
        data: DataFrame con dati azionari
        stats: Dizionario con statistiche calcolate
        slope: Pendenza della regressione lineare
        symbol: Simbolo dell'azione
    """
    print("\n" + "="*60)
    print(f"ANALISI COMPLETA: {symbol}")
    print("="*60)

    # Informazioni generali
    print(f"\n[INFO GENERALI]")
    print(f"  Simbolo:        {symbol}")
    print(f"  Periodo:        {data['date'].iloc[0]} a {data['date'].iloc[-1]}")
    print(f"  Giorni analizzati: {len(data)}")

    # Statistiche prezzi
    print(f"\n[STATISTICHE PREZZO]")
    print(f"  Prezzo Corrente: ${stats['prezzo_corrente']:.2f}")
    print(f"  Massimo:        ${stats['massimo']:.2f}")
    print(f"  Minimo:         ${stats['minimo']:.2f}")
    print(f"  Media:          ${stats['media']:.2f}")
    print(f"  Mediana:        ${stats['mediana']:.2f}")
    print(f"  Variazione:     ${stats['variazione']:.2f}")
    print(f"                    ({(stats['variazione']/stats['minimo']*100):.1f}%)")

    # Volatilita'
    print(f"\n[VOLATILITA']")
    print(f"  Deviazione Std: ${stats['deviazione_std']:.2f}")
    # Volatilita' percentuale (std / media * 100)
    volatility_pct = (stats['deviazione_std'] / stats['media']) * 100
    print(f"  Volatilita':    {volatility_pct:.2f}%")

    if volatility_pct > 10:
        vol_level = "ALTA"
    elif volatility_pct > 5:
        vol_level = "Media"
    else:
        vol_level = "Bassa"
    print(f"  Livello:        {vol_level}")

    # Trend
    print(f"\n[TREND]")
    print(f"  Variazione giornaliera media: ${slope:.4f}")
    print(f"  Variazione prevista 30gg:    ${slope*30:.2f}")

    if slope > 0.1:
        trend_text = "FORTEMENTE RIALZISTA"
        recommendation = "OPPORTUNITA' DI ACQUISTO"
    elif slope > 0.01:
        trend_text = "Rialzista debole"
        recommendation = "Monitorare"
    elif slope < -0.1:
        trend_text = "FORTEMENTE RIBASSISTA"
        recommendation = "CAUTELA - Vendere"
    elif slope < -0.01:
        trend_text = "Ribassista debole"
        recommendation = "Monitorare"
    else:
        trend_text = "LATERALE (Neutro)"
        recommendation = "Attendere segnali"

    print(f"  Trend attuale: {trend_text}")
    print(f"  Suggerimento: {recommendation}")

    # Volume medio
    if 'volume' in data.columns:
        avg_volume = data['volume'].mean()
        print(f"\n[VOLUME]")
        print(f"  Volume medio: {avg_volume:,.0f} azioni")

    print("\n" + "="*60)
    print("NOTA: Questa analisi e' solo a scopo educativo.")
    print("Non costituisce consiglio di investimento.")
    print("="*60 + "\n")


def main_menu() -> int:
    """
    Mostra il menu principale dell'applicazione.

    Returns:
        Scelta dell'utente (intero 1-7)
    """
    print("\n" + "="*60)
    print("  ANALIZZATORE PREZZI AZIONARI")
    print("  Stock Price Analyzer")
    print("="*60)
    print("\n[MENU PRINCIPALE]")
    print("  1. Analizza azione (con API o dati esempio)")
    print("  2. Carica e analizza da CSV")
    print("  3. Visualizza solo grafico da CSV")
    print("  4. Mostra file CSV disponibili")
    print("  5. Aiuto - come funziona")
    print("  0. Esci")
    print("="*60)

    choice = input("\n  >> Scelta (0-5): ").strip()
    return choice


def show_help():
    """
    Mostra informazioni su come usare il programma.
    """
    print("\n" + "="*60)
    print("  AIUTO - Come funziona l'Analizzatore")
    print("="*60)

    print("\n[INTRODUZIONE]")
    print("  Questo programma analizza i prezzi azionari calcolando:")
    print("  - Medie mobili (indicatori di trend)")
    print("  - Statistiche (min, max, media, volatilita')")
    print("  - Previsioni con regressione lineare")
    print("  - Grafici visuali")

    print("\n[COME OTTENERE API KEY (Opzionale)]")
    print("  1. Vai a: https://www.alphavantage.co/support/#api-key")
    print("  2. Registrati gratuitamente")
    print("  3. Copia la tua API key")
    print("  4. Incolla quando richiesto")
    print("\n  NOTA: Senza API key, userai dati di esempio generati")
    print("        automaticamente. Funziona tutto ugualmente!")

    print("\n[SPIEGAZIONE MEDIE MOBILI]")
    print("  MA20: Media ultimi 20 giorni (breve termine)")
    print("        - Sopra il prezzo = segnale di forza")
    print("        - Sotto il prezzo = segnale di debolezza")
    print("  MA50: Media ultimi 50 giorni (lungo termine)")
    print("        - Usata per confermare trend maggiori")

    print("\n[SPIEGAZIONE VOLATILITA']")
    print("  Alta volatilita' = grandi oscillazioni di prezzo")
    print("  Bassa volatilita' = prezzo stabile")
    print("  Misurata dalla deviazione standard")

    print("\n[REGRESSIONE LINEARE]")
    print("  Trova la retta che meglio approssima i dati")
    print("  Se la retta sale -> trend rialzista")
    print("  Se la retta scende -> trend ribassista")

    print("\n[AVVERTENZA]")
    print("  Questo programma e' a scopo EDUCATIVO.")
    print("  Le analisi NON sono consigli di investimento.")
    print("  Investire in borsa comporta rischi.")

    print("\n" + "="*60)


def analyze_stock():
    """
    Funzione principale per analizzare un'azione.
    Gestisce l'intero flusso di analisi.
    """
    print("\n" + "-"*60)
    print("MODULO: Analisi Azione")
    print("-"*60)

    # Input simbolo
    symbol = input("\n  >> Inserisci simbolo azione (es. AAPL, MSFT): ").strip().upper()
    if not symbol:
        symbol = "AAPL"
        print(f"[*] Usato simbolo default: {symbol}")

    # Chiediamo se usare API o dati esempio
    print("\n  Vuoi usare l'API Alpha Vantage?")
    print("  1. Si, ho una API key")
    print("  2. No, usa dati di esempio")
    api_choice = input("  >> Scelta (1-2): ").strip()

    api_key = None
    use_sample = False

    if api_choice == "1":
        api_key = input("\n  >> Inserisci API key (o premi Invio per esempio): ").strip()
        if not api_key:
            use_sample = True
            print("[!] Nessuna API key - uso dati di esempio")
    else:
        use_sample = True
        print("[!] Uso dati di esempio")

    # Recupero dati
    data = fetch_stock_data(symbol, use_sample=use_sample, api_key=api_key)

    if data is None or len(data) == 0:
        print("[!] Errore: Nessun dato disponibile")
        return

    # Calcolo medie mobili
    ma20 = calculate_moving_averages(data['close'], 20)
    ma50 = calculate_moving_averages(data['close'], 50)

    # Calcolo statistiche
    stats = calculate_statistics(data['close'])

    # Previsione trend
    slope, intercept, predicted = predict_trend(data['date'].tolist(),
                                                  data['close'].tolist())

    # Visualizzazione grafico
    print("\n  Vuoi visualizzare il grafico?")
    show_chart = input("  >> (s/n) [default: s]: ").strip().lower()
    if show_chart != 'n':
        plot_chart(data['date'].tolist(), data['close'].tolist(),
                   ma20.tolist(), ma50.tolist(), symbol)

    # Display analisi
    display_analysis(data, stats, slope, symbol)

    # Salvataggio CSV
    print("\n  Vuoi salvare i dati in CSV?")
    save_choice = input("  >> (s/n) [default: s]: ").strip().lower()
    if save_choice != 'n':
        filename = input(f"  >> Filename [default: stock_data.csv]: ").strip()
        if not filename:
            filename = CSV_PATH
        else:
            if not filename.endswith('.csv'):
                filename += '.csv'
            filename = os.path.join(BASE_DIR, filename)

        save_to_csv(data, filename)


def analyze_from_csv():
    """
    Carica e analizza dati da un file CSV esistente.
    """
    print("\n" + "-"*60)
    print("MODULO: Analisi da CSV")
    print("-"*60)

    filename = input(f"\n  >> Filename [default: stock_data.csv]: ").strip()
    if not filename:
        filename = CSV_PATH
    else:
        if not filename.endswith('.csv'):
            filename += '.csv'
        if not os.path.isabs(filename):
            filename = os.path.join(BASE_DIR, filename)

    data = load_from_csv(filename)

    if data is None or len(data) == 0:
        print("[!] Errore: Nessun dato caricato")
        return

    print(f"[*] Dati caricati con successo: {len(data)} record")

    # Calcolo medie mobili
    ma20 = calculate_moving_averages(data['close'], 20)
    ma50 = calculate_moving_averages(data['close'], 50)

    # Calcolo statistiche
    stats = calculate_statistics(data['close'])

    # Previsione trend
    slope, intercept, predicted = predict_trend(data['date'].tolist(),
                                                  data['close'].tolist())

    # Visualizzazione grafico
    print("\n  Vuoi visualizzare il grafico?")
    show_chart = input("  >> (s/n) [default: s]: ").strip().lower()
    if show_chart != 'n':
        symbol = filename.replace('.csv', '').split('\\')[-1].upper()[:5]
        plot_chart(data['date'].tolist(), data['close'].tolist(),
                   ma20.tolist(), ma50.tolist(), symbol)

    # Display analisi
    display_analysis(data, stats, slope, symbol)


def show_chart_only():
    """
    Visualizza solo il grafico da CSV senza analisi.
    """
    print("\n" + "-"*60)
    print("MODULO: Visualizzazione Grafico")
    print("-"*60)

    filename = input(f"\n  >> Filename [default: stock_data.csv]: ").strip()
    if not filename:
        filename = CSV_PATH
    else:
        if not filename.endswith('.csv'):
            filename += '.csv'
        if not os.path.isabs(filename):
            filename = os.path.join(BASE_DIR, filename)

    data = load_from_csv(filename)

    if data is None or len(data) == 0:
        print("[!] Errore: Nessun dato caricato")
        return

    # Calcolo medie mobili
    ma20 = calculate_moving_averages(data['close'], 20)
    ma50 = calculate_moving_averages(data['close'], 50)

    # Symbol dal filename
    symbol = filename.replace('.csv', '').split('\\')[-1].upper()[:5]

    plot_chart(data['date'].tolist(), data['close'].tolist(),
               ma20.tolist(), ma50.tolist(), symbol)


def list_csv_files():
    """
    Mostra tutti i file CSV disponibili nella directory.
    """
    print("\n" + "-"*60)
    print("MODULO: File CSV Disponibili")
    print("-"*60)

    print(f"\n[*] Directory: {BASE_DIR}")

    csv_files = []
    for file in os.listdir(BASE_DIR):
        if file.endswith('.csv'):
            filepath = os.path.join(BASE_DIR, file)
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            csv_files.append((file, size, mtime))

    if not csv_files:
        print("\n[!] Nessun file CSV trovato")
    else:
        print(f"\n[*] Trovati {len(csv_files)} file CSV:\n")
        for file, size, mtime in sorted(csv_files):
            size_kb = size / 1024
            print(f"  - {file}")
            print(f"    Dimensione: {size_kb:.1f} KB")
            print(f"    Modificato:  {mtime.strftime('%Y-%m-%d %H:%M')}")
            print()

    print("-"*60)


def main():
    """
    Funzione principale - entry point del programma.

    Gestisce il loop del menu e le scelte dell'utente.
    """
    print("\n" + "="*60)
    print("  BENVENUTO nell'Analizzatore di Prezzi Azionari")
    print("  Stock Price Analyzer v1.0")
    print("="*60)
    print("\n[INFO]")
    print("  Questo programma ti aiuta ad analizzare i prezzi azionari.")
    print("  Puoi usare dati reali (con API) o dati di esempio.")
    print("  Perfetto per imparare l'analisi tecnica di base!")

    while True:
        choice = main_menu()

        if choice == "1":
            analyze_stock()
        elif choice == "2":
            analyze_from_csv()
        elif choice == "3":
            show_chart_only()
        elif choice == "4":
            list_csv_files()
        elif choice == "5":
            show_help()
        elif choice == "0":
            print("\n[*] Arrivederci! Grazie per aver usato il programma.\n")
            break
        else:
            print("\n[!] Scelta non valida. Riprova.\n")

        # Pausa prima di tornare al menu
        if choice != "0":
            input("\n  >> Premi Invio per continuare...")


if __name__ == "__main__":
    """
    Entry point quando eseguito come script.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Programma interrotto dall'utente.")
        print("[!] Arrivederci!\n")
    except Exception as e:
        print(f"\n[!] Errore imprevisto: {e}")
        print("[!] Controlla i dati e riprova.\n")
