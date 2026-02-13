"""
UNIT CONVERTER - Convertitore di Unità Didattico
================================================

Questo programma è stato progettato per scopo educativo.
Demonstra l'uso di funzioni, condizioni, cicli e gestione input.

Autore: Studente Python
Data: 2025
"""

import math  # Importiamo il modulo math per funzioni matematiche avanzate (se necessario)


# ============================================================================
# FUNZIONI DI CONVERSIONE TEMPERATURA
# ============================================================================

def celsius_to_fahrenheit(celsius):
    """
    Converte Celsius in Fahrenheit.
    Formula: (C × 9/5) + 32

    Argomento:
        celsius (float): temperatura in gradi Celsius

    Ritorna:
        float: temperatura in gradi Fahrenheit
    """
    # Moltiplichiamo per 9/5 (che è 1.8) e aggiungiamo 32
    fahrenheit = (celsius * 9 / 5) + 32
    return fahrenheit


def fahrenheit_to_celsius(fahrenheit):
    """
    Converte Fahrenheit in Celsius.
    Formula: (F - 32) × 5/9

    Argomento:
        fahrenheit (float): temperatura in gradi Fahrenheit

    Ritorna:
        float: temperatura in gradi Celsius
    """
    # Sottraiamo 32, poi moltiplichiamo per 5/9 (che è circa 0.556)
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius


def celsius_to_kelvin(celsius):
    """
    Converte Celsius in Kelvin.
    Formula: C + 273.15

    Argomento:
        celsius (float): temperatura in gradi Celsius

    Ritorna:
        float: temperatura in Kelvin
    """
    # Aggiungiamo solo 273.15 - conversione semplice!
    kelvin = celsius + 273.15
    return kelvin


def kelvin_to_celsius(kelvin):
    """
    Converte Kelvin in Celsius.
    Formula: K - 273.15

    Argomento:
        kelvin (float): temperatura in Kelvin

    Ritorna:
        float: temperatura in gradi Celsius
    """
    # Sottraiamo solo 273.15
    celsius = kelvin - 273.15
    return celsius


def fahrenheit_to_kelvin(fahrenheit):
    """
    Converte Fahrenheit in Kelvin.
    Formula: (F - 32) × 5/9 + 273.15

    Argomento:
        fahrenheit (float): temperatura in gradi Fahrenheit

    Ritorna:
        float: temperatura in Kelvin
    """
    # Prima convertiamo in Celsius, poi aggiungiamo 273.15
    # Combiniamo le due formule in un'unica espressione
    kelvin = (fahrenheit - 32) * 5 / 9 + 273.15
    return kelvin


def kelvin_to_fahrenheit(kelvin):
    """
    Converte Kelvin in Fahrenheit.
    Formula: (K - 273.15) × 9/5 + 32

    Argomento:
        kelvin (float): temperatura in Kelvin

    Ritorna:
        float: temperatura in gradi Fahrenheit
    """
    # Prima convertiamo in Celsius, poi in Fahrenheit
    # Combiniamo le due formule
    fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
    return fahrenheit


def menu_temperature():
    """
    Mostra il menu per le conversioni di temperatura e gestisce l'input utente.
    Questa funzione NON ritorna nulla, stampa solo i risultati.
    """
    print("\n" + "=" * 60)
    print("  CONVERSIONI TEMPERATURA")
    print("=" * 60)
    print("Scegli la conversione desiderata:")
    print("  [1] Celsius -> Fahrenheit")
    print("  [2] Fahrenheit -> Celsius")
    print("  [3] Celsius -> Kelvin")
    print("  [4] Kelvin -> Celsius")
    print("  [5] Fahrenheit -> Kelvin")
    print("  [6] Kelvin -> Fahrenheit")

    # Chiediamo all'utente di scegliere un'opzione
    scelta = input("\nInserisci il numero della conversione (1-6): ").strip()

    # Verifichiamo che l'input sia valido
    if scelta not in ['1', '2', '3', '4', '5', '6']:
        print("[!] Scelta non valida. Torna al menu principale.")
        return

    # Chiediamo il valore da convertire
    try:
        # try/except ci permette di gestire errori senza far crashare il programma
        valore = float(input("Inserisci il valore da convertire: "))
    except ValueError:
        # ValueError si verifica quando l'input non è un numero valido
        print("[!] Errore: devi inserire un numero valido.")
        return

    # Eseguiamo la conversione appropriata usando if/elif/else
    if scelta == '1':
        risultato = celsius_to_fahrenheit(valore)
        print(f"\n[OK] {valore:.2f} gradi Celsius = {risultato:.2f} gradi Fahrenheit")
    elif scelta == '2':
        risultato = fahrenheit_to_celsius(valore)
        print(f"\n[OK] {valore:.2f} gradi Fahrenheit = {risultato:.2f} gradi Celsius")
    elif scelta == '3':
        risultato = celsius_to_kelvin(valore)
        print(f"\n[OK] {valore:.2f} gradi Celsius = {risultato:.2f} Kelvin")
    elif scelta == '4':
        risultato = kelvin_to_celsius(valore)
        print(f"\n[OK] {valore:.2f} Kelvin = {risultato:.2f} gradi Celsius")
    elif scelta == '5':
        risultato = fahrenheit_to_kelvin(valore)
        print(f"\n[OK] {valore:.2f} gradi Fahrenheit = {risultato:.2f} Kelvin")
    elif scelta == '6':
        risultato = kelvin_to_fahrenheit(valore)
        print(f"\n[OK] {valore:.2f} Kelvin = {risultato:.2f} gradi Fahrenheit")


# ============================================================================
# FUNZIONI DI CONVERSIONE LUNGHEZZA
# ============================================================================

def metri_to_piedi(metri):
    """
    Converte metri in piedi.
    Formula: metri × 3.28084

    Argomento:
        metri (float): lunghezza in metri

    Ritorna:
        float: lunghezza in piedi
    """
    piedi = metri * 3.28084
    return piedi


def piedi_to_metri(piedi):
    """
    Converte piedi in metri.
    Formula: piedi × 0.3048

    Argomento:
        piedi (float): lunghezza in piedi

    Ritorna:
        float: lunghezza in metri
    """
    metri = piedi * 0.3048
    return metri


def metri_to_chilometri(metri):
    """
    Converte metri in chilometri.
    Formula: metri × 0.001

    Argomento:
        metri (float): lunghezza in metri

    Ritorna:
        float: lunghezza in chilometri
    """
    # Dividiamo per 1000 (moltiplicare per 0.001 è equivalente)
    chilometri = metri * 0.001
    return chilometri


def chilometri_to_metri(chilometri):
    """
    Converte chilometri in metri.
    Formula: chilometri × 1000

    Argomento:
        chilometri (float): lunghezza in chilometri

    Ritorna:
        float: lunghezza in metri
    """
    metri = chilometri * 1000
    return metri


def metri_to_miglia(metri):
    """
    Converte metri in miglia.
    Formula: metri × 0.000621371

    Argomento:
        metri (float): lunghezza in metri

    Ritorna:
        float: lunghezza in miglia
    """
    miglia = metri * 0.000621371
    return miglia


def miglia_to_metri(miglia):
    """
    Converte miglia in metri.
    Formula: miglia × 1609.34

    Argomento:
        miglia (float): lunghezza in miglia

    Ritorna:
        float: lunghezza in metri
    """
    metri = miglia * 1609.34
    return metri


def menu_lunghezza():
    """
    Mostra il menu per le conversioni di lunghezza e gestisce l'input utente.
    Questa funzione NON ritorna nulla, stampa solo i risultati.
    """
    print("\n" + "=" * 60)
    print("  CONVERSIONI LUNGHEZZA")
    print("=" * 60)
    print("Scegli la conversione desiderata:")
    print("  [1] Metri -> Piedi")
    print("  [2] Piedi -> Metri")
    print("  [3] Metri -> Chilometri")
    print("  [4] Chilometri -> Metri")
    print("  [5] Metri -> Miglia")
    print("  [6] Miglia -> Metri")

    # Chiediamo all'utente di scegliere un'opzione
    scelta = input("\nInserisci il numero della conversione (1-6): ").strip()

    # Verifichiamo che l'input sia valido
    if scelta not in ['1', '2', '3', '4', '5', '6']:
        print("[!] Scelta non valida. Torna al menu principale.")
        return

    # Chiediamo il valore da convertire
    try:
        valore = float(input("Inserisci il valore da convertire: "))
    except ValueError:
        print("[!] Errore: devi inserire un numero valido.")
        return

    # Eseguiamo la conversione appropriata
    if scelta == '1':
        risultato = metri_to_piedi(valore)
        print(f"\n[OK] {valore:.4f} metri = {risultato:.4f} piedi")
    elif scelta == '2':
        risultato = piedi_to_metri(valore)
        print(f"\n[OK] {valore:.4f} piedi = {risultato:.4f} metri")
    elif scelta == '3':
        risultato = metri_to_chilometri(valore)
        print(f"\n[OK] {valore:.4f} metri = {risultato:.4f} chilometri")
    elif scelta == '4':
        risultato = chilometri_to_metri(valore)
        print(f"\n[OK] {valore:.4f} chilometri = {risultato:.4f} metri")
    elif scelta == '5':
        risultato = metri_to_miglia(valore)
        print(f"\n[OK] {valore:.4f} metri = {risultato:.4f} miglia")
    elif scelta == '6':
        risultato = miglia_to_metri(valore)
        print(f"\n[OK] {valore:.4f} miglia = {risultato:.4f} metri")


# ============================================================================
# FUNZIONI DI CONVERSIONE PESO
# ============================================================================

def chilogrammi_to_libbre(chilogrammi):
    """
    Converte chilogrammi in libbre.
    Formula: kg × 2.20462

    Argomento:
        chilogrammi (float): peso in chilogrammi

    Ritorna:
        float: peso in libbre
    """
    libbre = chilogrammi * 2.20462
    return libbre


def libbre_to_chilogrammi(libbre):
    """
    Converte libbre in chilogrammi.
    Formula: libbre × 0.453592

    Argomento:
        libbre (float): peso in libbre

    Ritorna:
        float: peso in chilogrammi
    """
    chilogrammi = libbre * 0.453592
    return chilogrammi


def menu_peso():
    """
    Mostra il menu per le conversioni di peso e gestisce l'input utente.
    Questa funzione NON ritorna nulla, stampa solo i risultati.
    """
    print("\n" + "=" * 60)
    print("  CONVERSIONI PESO")
    print("=" * 60)
    print("Scegli la conversione desiderata:")
    print("  [1] Chilogrammi -> Libbre")
    print("  [2] Libbre -> Chilogrammi")

    # Chiediamo all'utente di scegliere un'opzione
    scelta = input("\nInserisci il numero della conversione (1-2): ").strip()

    # Verifichiamo che l'input sia valido
    if scelta not in ['1', '2']:
        print("[!] Scelta non valida. Torna al menu principale.")
        return

    # Chiediamo il valore da convertire
    try:
        valore = float(input("Inserisci il valore da convertire: "))
    except ValueError:
        print("[!] Errore: devi inserire un numero valido.")
        return

    # Verifichiamo che il peso sia positivo
    if valore < 0:
        print("[!] Attenzione: il peso non può essere negativo. Usa un valore positivo.")
        return

    # Eseguiamo la conversione appropriata
    if scelta == '1':
        risultato = chilogrammi_to_libbre(valore)
        print(f"\n[OK] {valore:.2f} chilogrammi = {risultato:.2f} libbre")
    elif scelta == '2':
        risultato = libbre_to_chilogrammi(valore)
        print(f"\n[OK] {valore:.2f} libbre = {risultato:.2f} chilogrammi")


# ============================================================================
# FUNZIONE PRINCIPALE - MENU'
# ============================================================================

def menu_principale():
    """
    Funzione principale che gestisce il ciclo del programma.
    Mostra il menu principale e continua a finché l'utente non sceglie di uscire.
    """
    # Messaggio di benvenuto
    print("\n" + "=" * 60)
    print("  UNIT CONVERTER - Convertitore di Unità")
    print("=" * 60)
    print("  Programma didattico per imparare Python")
    print("=" * 60)

    # Ciclo principale del programma
    # while True significa "continua per sempre"
    # Usciremo dal ciclo con l'istruzione 'break'
    while True:
        print("\n" + "-" * 60)
        print("MENU PRINCIPALE")
        print("-" * 60)
        print("Scegli il tipo di conversione:")
        print("  [1] Temperatura")
        print("  [2] Lunghezza")
        print("  [3] Peso")
        print("  [0] Esci dal programma")

        # Chiediamo all'utente cosa vuole fare
        # .strip() rimuove spazi vuoti all'inizio e alla fine
        scelta = input("\nInserisci la tua scelta (0-3): ").strip()

        # Usiamo if/elif/else per gestire le diverse scelte
        if scelta == '1':
            # L'utente vuole convertire temperature
            menu_temperature()

        elif scelta == '2':
            # L'utente vuole convertire lunghezze
            menu_lunghezza()

        elif scelta == '3':
            # L'utente vuole convertire pesi
            menu_peso()

        elif scelta == '0':
            # L'utente vuole uscire dal programma
            print("\n" + "=" * 60)
            print("Grazie per aver usato Unit Converter!")
            print("Alla prossima!")
            print("=" * 60 + "\n")
            # 'break' ci fa uscire dal ciclo while
            break

        else:
            # L'utente ha inserito un valore non valido
            print("\n[!] Scelta non valida. Per favore inserisci un numero da 0 a 3.")

        # Small pause per rendere l'output più leggibile
        # input("\nPremi INVIO per continuare...")  # Decommenta se vuoi una pausa


# ============================================================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# ============================================================================

# Questa è la parte del codice che viene eseguita per prima
# quando si avvia il programma
if __name__ == "__main__":
    """
    __name__ è una variabile speciale di Python.
    Quando eseguiamo direttamente questo file, __name__ è "__main__".
    Se importassimo questo file in un altro programma, questo codice non verrebbe eseguito.
    """
    # Chiamiamo la funzione principale per avviare il programma
    menu_principale()
