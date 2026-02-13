"""
Script di test per verificare l'installazione delle dipendenze.
Runna questo script per controllare se tutto e' installato correttamente.
"""

def test_imports():
    """Testa se tutte le librerie sono importate correttamente."""
    print("Test importazione librerie...\n")

    tests = [
        ("Pandas", "import pandas as pd"),
        ("NumPy", "import numpy as np"),
        ("Matplotlib", "import matplotlib.pyplot as plt"),
        ("Requests", "import requests"),
        ("OS", "import os"),
        ("Datetime", "from datetime import datetime, timedelta"),
        ("Typing", "from typing import Dict, List, Tuple, Optional"),
    ]

    success = 0
    failed = 0

    for name, import_cmd in tests:
        try:
            exec(import_cmd)
            print(f"[OK] {name}")
            success += 1
        except ImportError as e:
            print(f"[ERRORE] {name}: {e}")
            failed += 1

    print(f"\nRisultato: {success} OK, {failed} Falliti")

    if failed == 0:
        print("\nTutto pronto! Puoi eseguire python stock_analyzer.py")
        return True
    else:
        print("\nInstalla le dipendenze mancanti:")
        print("pip install -r requirements.txt")
        return False


def test_directories():
    """Verifica che le directory necessarie esistano."""
    print("\n\nTest directory...\n")

    import os

    base_dir = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\stock-analyzer"
    charts_dir = os.path.join(base_dir, "charts")

    checks = [
        ("Base Directory", base_dir),
        ("Charts Directory", charts_dir),
    ]

    for name, path in checks:
        if os.path.exists(path):
            print(f"[OK] {name}: {path}")
        else:
            print(f"[CREATA] {name}: {path}")
            os.makedirs(path, exist_ok=True)


def test_sample_functionality():
    """Testa una funzione di esempio dal modulo principale."""
    print("\n\nTest funzionalita' base...\n")

    try:
        import pandas as pd
        import numpy as np

        # Test creazione DataFrame
        data = {
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'close': [100.0, 102.5, 101.0],
            'volume': [1000000, 1200000, 1100000]
        }
        df = pd.DataFrame(data)
        print("[OK] Creazione DataFrame")

        # Test calcolo media mobile
        ma = df['close'].rolling(window=2).mean()
        print("[OK] Calcolo media mobile")

        # Test statistiche
        stats = {
            'min': df['close'].min(),
            'max': df['close'].max(),
            'mean': df['close'].mean()
        }
        print("[OK] Calcolo statistiche")

        # Test regressione lineare
        x = np.array([0, 1, 2])
        y = np.array([100.0, 102.5, 101.0])
        z = np.polyfit(x, y, 1)
        print("[OK] Regressione lineare")

        print("\n[TUTTI I TEST PASSATI]")
        return True

    except Exception as e:
        print(f"\n[ERRORE] {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("  TEST INSTALLAZIONE - Stock Price Analyzer")
    print("="*60)

    test_imports()
    test_directories()
    test_sample_functionality()

    print("\n" + "="*60)
    print("Per avviare il programma principale:")
    print("  python stock_analyzer.py")
    print("="*60)
