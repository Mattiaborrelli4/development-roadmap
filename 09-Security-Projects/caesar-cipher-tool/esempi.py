"""
Esempi di utilizzo del Caesar Cipher Tool
Script dimostrativo per scopi educativi
"""

from cipher import CaesarCipher
from analysis import FrequencyAnalyzer, index_of_coincidence, entropy
from config import get_alphabet


def esempio_1_cifratura_base():
    """Esempio 1: Cifratura base"""
    print("=" * 60)
    print("ESEMPIO 1: Cifratura Base")
    print("=" * 60)

    cipher = CaesarCipher(get_alphabet("english"))

    messaggio = "HELLO WORLD"
    chiave = 3

    cifrato = cipher.encrypt(messaggio, chiave)
    decifrato = cipher.decrypt(cifrato, chiave)

    print(f"Messaggio originale: {messaggio}")
    print(f"Chiave: {chiave}")
    print(f"Messaggio cifrato: {cifrato}")
    print(f"Messaggio decifrato: {decifrato}")
    print()


def esempio_2_wraparound():
    """Esempio 2: Dimostrazione wraparound"""
    print("=" * 60)
    print("ESEMPIO 2: Wraparound (Z → A)")
    print("=" * 60)

    cipher = CaesarCipher("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # XYZ con chiave 3 diventa ABC
    originale = "XYZ"
    chiave = 3
    cifrato = cipher.encrypt(originale, chiave)

    print(f"Originale: {originale}")
    print(f"Chiave: {chiave}")
    print(f"Cifrato: {cifrato}")
    print()
    print("Spiegazione:")
    print("  X (23) + 3 = 26 → 26 mod 26 = 0 → A")
    print("  Y (24) + 3 = 27 → 27 mod 26 = 1 → B")
    print("  Z (25) + 3 = 28 → 28 mod 26 = 2 → C")
    print()


def esempio_3_brute_force():
    """Esempio 3: Brute force attack"""
    print("=" * 60)
    print("ESEMPIO 3: Brute Force Attack")
    print("=" * 60)

    cipher = CaesarCipher(get_alphabet("english"))

    # Messaggio cifrato sconosciuto
    cifrato = "KHOOR"

    print(f"Testo cifrato: {cifrato}")
    print(f"\nTentativo di tutte le chiavi possibili:")
    print("-" * 40)

    risultati = cipher.brute_force(cifrato)

    for chiave, decifrato in risultati:
        marker = " ← TESTO IN CHIARO!" if decifrato == "HELLO" else ""
        print(f"Chiave {chiave:2d}: {decifrato}{marker}")

    print()


def esempio_4_analisi_frequenze():
    """Esempio 4: Analisi delle frequenze"""
    print("=" * 60)
    print("ESEMPIO 4: Analisi delle Frequenze")
    print("=" * 60)

    analyzer = FrequencyAnalyzer(language="english")
    alphabet = get_alphabet("english")

    # Testo in inglese
    testo_inglese = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"

    print(f"Testo analizzato: {testo_inglese}\n")

    # Calcola frequenze
    freq = analyzer.count_frequency(testo_inglese, alphabet)
    percent = analyzer.calculate_percentage(freq)

    # Mostra prime 5 lettere più frequenti
    sorted_freq = sorted(percent.items(), key=lambda x: x[1], reverse=True)

    print("Lettere più frequenti:")
    print("-" * 30)
    for letter, perc in sorted_freq[:5]:
        expected = analyzer.ENGLISH_FREQUENCIES.get(letter, 0)
        print(f"{letter}: {perc:5.2f}% (atteso: {expected:5.2f}%)")

    print()


def esempio_5_indice_coincidenza():
    """Esempio 5: Indice di coincidenza"""
    print("=" * 60)
    print("ESEMPIO 5: Indice di Coincidenza")
    print("=" * 60)

    alphabet = get_alphabet("english")

    # Testo in inglese
    inglese = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"

    # Testo "casuale" (X ripetuto)
    casuale = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    ic_inglese = index_of_coincidence(inglese, alphabet)
    ic_casuale = index_of_coincidence(casuale, alphabet)

    print(f"Testo inglese:")
    print(f"  {inglese}")
    print(f"  IC = {ic_inglese:.4f}")
    print(f"  (IC atteso per inglese: ~0.0667)")
    print()

    print(f"Testo 'casuale' (tutte X):")
    print(f"  {casuale[:50]}...")
    print(f"  IC = {ic_casuale:.4f}")
    print(f"  (IC per testo uniforme: 1.0)")
    print()

    print("Conclusione: IC più alto = testo meno casuale = più strutturato")
    print()


def esempio_6_entropia():
    """Esempio 6: Entropia"""
    print("=" * 60)
    print("ESEMPIO 6: Entropia di Shannon")
    print("=" * 60)

    alphabet = get_alphabet("english")

    # Testo con bassa entropia (ripetizioni)
    bassa_entropia = "AAAAAAAAAAAAAAAA"

    # Testo con alta entropia (tutte lettere diverse)
    alta_entropia = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ent_bassa = entropy(bassa_entropia, alphabet)
    ent_alta = entropy(alta_entropia, alphabet)

    print(f"Testo a bassa entropia (tutte A):")
    print(f"  {bassa_entropia}")
    print(f"  Entropia: {ent_bassa:.4f} bit")
    print()

    print(f"Testo ad alta entropia (tutte lettere):")
    print(f"  {alta_entropia}")
    print(f"  Entropia: {ent_alta:.4f} bit")
    print()

    print("Conclusione: Maggiore entropia = più imprevedibile = più sicuro")
    print()


def esempio_7_alfabeto_italiano():
    """Esempio 7: Alfabeto italiano"""
    print("=" * 60)
    print("ESEMPIO 7: Alfabeto Italiano")
    print("=" * 60)

    cipher = CaesarCipher(get_alphabet("italian"))

    messaggio = "CIAO ITALIA"
    chiave = 3

    cifrato = cipher.encrypt(messaggio, chiave)

    print(f"Alfabeto italiano classico (21 lettere):")
    print(f"  {get_alphabet('italian')}")
    print()

    print(f"Messaggio: {messaggio}")
    print(f"Chiave: {chiave}")
    print(f"Cifrato: {cifrato}")
    print()

    print("Nota: J, K, W, X, Y non sono presenti nell'alfabeto italiano classico")
    print()


def esempio_8_crittalisi_automatica():
    """Esempio 8: Crittanalisi automatica"""
    print("=" * 60)
    print("ESEMPIO 8: Crittanalisi Automatica")
    print("=" * 60)

    # Crea un testo cifrato
    cipher = CaesarCipher(get_alphabet("english"))
    originale = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    chiave_sconosciuta = 15
    cifrato = cipher.encrypt(originale, chiave_sconosciuta)

    print(f"Testo cifrato (chiave {chiave_sconosciuta}): {cifrato}")
    print()

    # Usa analisi frequenze per trovare la chiave
    analyzer = FrequencyAnalyzer(language="english")
    best_key, score, decifrato = analyzer.find_best_key(
        cifrato, get_alphabet("english"), cipher.decrypt
    )

    print(f"Analisi automatica:")
    print(f"  Chiave trovata: {best_key}")
    print(f"  Chi-quadrato: {score:.2f}")
    print(f"  Testo decifrato: {decifrato}")
    print()

    if best_key == chiave_sconosciuta:
        print("✓ Chiave identificata correttamente!")
    else:
        print("✗ Chiave errata (raro per testi lunghi)")
    print()


def esempio_9_processo_visivo():
    """Esempio 9: Processo di cifratura visivo"""
    print("=" * 60)
    print("ESEMPIO 9: Processo di Cifratura Visivo")
    print("=" * 60)

    cipher = CaesarCipher("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    messaggio = "ABC"
    chiave = 3

    cifrato, steps = cipher.encrypt_with_visual(messaggio, chiave)

    print(f"Testo: {messaggio}")
    print(f"Chiave: {chiave}")
    print(f"\nProcesso:")
    print("-" * 60)

    for step in steps:
        print(
            f"Pos {step['position']}: "
            f"'{step['original']}' (idx {step['original_idx']}) → "
            f"{step['operation']} → "
            f"{step['modulo']} → "
            f"'{step['result']}'"
        )

    print(f"\nRisultato: {cifrato}")
    print()


def main():
    """Esegui tutti gli esempi"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "CAESAR CIPHER - ESEMPI EDUCATIVI" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    esempio_1_cifratura_base()
    input("\nPremi Enter per continuare...")

    esempio_2_wraparound()
    input("\nPremi Enter per continuare...")

    esempio_3_brute_force()
    input("\nPremi Enter per continuare...")

    esempio_4_analisi_frequenze()
    input("\nPremi Enter per continuare...")

    esempio_5_indice_coincidenza()
    input("\nPremi Enter per continuare...")

    esempio_6_entropia()
    input("\nPremi Enter per continuare...")

    esempio_7_alfabeto_italiano()
    input("\nPremi Enter per continuare...")

    esempio_8_crittalisi_automatica()
    input("\nPremi Enter per continuare...")

    esempio_9_processo_visivo()

    print("=" * 60)
    print("FINE DEGLI ESEMPI")
    print("=" * 60)
    print()
    print("⚠️  Ricorda: Questo è solo per apprendimento!")
    print("    Il cifrario di Caesar NON è sicuro per uso reale.")
    print()


if __name__ == "__main__":
    main()
