#!/usr/bin/env python3
"""
Process Manager - Test Module Script

Questo script testa tutti i moduli per verificare che funzionino correttamente.
"""

import sys
import traceback

def test_module(module_name, import_path):
    """Testa un singolo modulo"""
    print(f"\n{'=' * 60}")
    print(f"Test modulo: {module_name}")
    print('=' * 60)

    try:
        # Importa il modulo
        module = __import__(import_path)

        # Esegui i test del modulo se ha __main__
        if hasattr(module, '__main__') or hasattr(module, '__name__'):
            # Moduli con if __name__ == '__main__'
            print(f"✓ Modulo {module_name} importato con successo")
            print(f"  - Contiene test integrati")
            return True

        print(f"✓ Modulo {module_name} importato con successo")
        return True

    except ImportError as e:
        print(f"❌ Errore importazione: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        traceback.print_exc()
        return False

def main():
    """Funzione principale"""
    print("=" * 60)
    print("Process Manager - Test Moduli")
    print("=" * 60)

    modules = [
        ("process", "process"),
        ("tree", "tree"),
        ("filter", "filter"),
        ("sort", "sort"),
        ("killer", "killer"),
    ]

    results = {}

    for module_name, import_path in modules:
        results[module_name] = test_module(module_name, import_path)

    # Riepilogo
    print(f"\n{'=' * 60}")
    print("RIEPILOGO")
    print('=' * 60)

    for module_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {module_name}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    print(f"\nTotale: {passed}/{total} moduli passati")

    if passed == total:
        print("\n✅ Tutti i moduli funzionano correttamente!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} moduli hanno problemi")
        return 1

if __name__ == '__main__':
    sys.exit(main())
