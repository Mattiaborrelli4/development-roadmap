# =============================================================================
# GIOCO: INDOVINA IL NUMERO (Number Guessing Game)
# =============================================================================
# Autore: Studente Python
# Scopo: Esercitazione su funzioni, cicli, condizioni e input validation
# =============================================================================

# Importiamo la libreria random per generare numeri casuali
# random è un modulo della libreria standard di Python
import random


# =============================================================================
# FUNZIONE: mostra_intestazione()
# =============================================================================
# Scopo: Stampa il titolo del gioco e le istruzioni iniziali
# Input: Nessuno
# Output: None (solo stampa a video)
# =============================================================================
def mostra_intestazione():
    """
    Mostra il titolo del gioco e il benvenuto.
    Questa funzione non restituisce nulla, si limita a stampare.
    """
    print("=" * 60)  # Stampa 60 volte il carattere "=" per creare una linea
    print("   BENVENUTO AL GIOCO 'INDOVINA IL NUMERO'!")
    print("=" * 60)
    print()
    print("Il computer ha scelto un numero casuale tra 1 e 100.")
    print("Il tuo obiettivo è indovinarlo nel minor numero di tentativi.")
    print("Dopo ogni tentativo, ti verrà detto se il numero è più alto o più basso.")
    print()
    print("Livelli di difficoltà disponibili:")
    print("  [F] Facile   - 15 tentativi")
    print("  [M] Medio   - 10 tentativi")
    print("  [D] Difficile - 5 tentativi")
    print()
    print("-" * 60)  # Linea tratteggiata
    print()


# =============================================================================
# FUNZIONE: scegli_difficolta()
# =============================================================================
# Scopo: Permette all'utente di scegliere il livello di difficoltà
# Input: Nessuno (legge l'input dall'utente)
# Output: Integer - numero di tentativi consentiti
# =============================================================================
def scegli_difficolta():
    """
    Chiede all'utente di scegliere la difficoltà e restituisce il numero
    di tentativi corrispondenti al livello scelto.

    Returns:
        int: Il numero di tentativi consentiti (15, 10, o 5)
    """

    # Loop infinito che continua finché l'utente non inserisce un input valido
    while True:  # True con la T maiuscola è una parola chiave di Python

        # input() legge una stringa da tastiera
        # .strip() rimuove gli spazi all'inizio e alla fine
        # .upper() converte tutto in maiuscolo per gestire F/f/M/m/D/d
        scelta = input("Scegli la difficoltà (F/M/D): ").strip().upper()

        # Verifichiamo quale difficoltà è stata scelta
        if scelta == "F":
            # L'utente ha scelto Facile
            tentativi = 15
            print(f"\nHai scelto: FACILE - Hai {tentativi} tentativi disponibili.\n")
            return tentativi  # return termina la funzione e restituisce il valore

        elif scelta == "M":
            # L'utente ha scelto Medio
            tentativi = 10
            print(f"\nHai scelto: MEDIO - Hai {tentativi} tentativi disponibili.\n")
            return tentativi

        elif scelta == "D":
            # L'utente ha scelto Difficile
            tentativi = 5
            print(f"\nHai scelto: DIFFICILE - Hai {tentativi} tentativi disponibili.\n")
            return tentativi

        else:
            # L'utente ha inserito un valore non valido
            print("\n[!] Scelta non valida! Inserisci F, M, o D.")
            # Il loop continua, chiedendo nuovamente l'input


# =============================================================================
# FUNZIONE: genera_numero_segreto()
# =============================================================================
# Scopo: Genera un numero casuale tra 1 e 100
# Input: Nessuno
# Output: Integer - il numero casuale generato
# =============================================================================
def genera_numero_segreto():
    """
    Genera e restituisce un numero casuale compreso tra 1 e 100.

    Returns:
        int: Un numero casuale tra 1 e 100 (inclusi)
    """
    # random.randint(a, b) restituisce un intero casuale tra a e b (inclusi)
    numero_segreto = random.randint(1, 100)
    return numero_segreto


# =============================================================================
# FUNZIONE: ottieni_tentativo(tentativi_rimasti)
# =============================================================================
# Scopo: Chiede all'utente di inserire un numero e valida l'input
# Input: tentativi_rimasti (int) - numero di tentativi ancora disponibili
# Output: Integer - il numero inserito dall'utente
# =============================================================================
def ottieni_tentativo(tentativi_rimasti):
    """
    Chiede all'utente di inserire un numero e valida l'input.
    Continua a chiedere finché l'utente non inserisce un numero valido.

    Args:
        tentativi_rimasti (int): Numero di tentativi ancora disponibili

    Returns:
        int: Il numero valido inserito dall'utente
    """

    while True:
        # Mostriamo quanti tentativi rimangono
        print(f"\nTentativi rimasti: {tentativi_rimasti}")

        # Chiediamo all'utente di inserire un numero
        input_utente = input("Inserisci un numero tra 1 e 100: ").strip()

        # Validiamo l'input con un blocco try-except
        # try-except serve a gestire gli errori (eccezioni)
        try:
            # Proviamo a convertire la stringa in intero
            numero = int(input_utente)

            # Verifichiamo che il numero sia nel range valido
            if numero < 1 or numero > 100:
                print("[!] Il numero deve essere tra 1 e 100! Riprova.")
                # Continua il loop, chiedendo nuovamente
            else:
                # Input valido! Restituiamo il numero
                return numero

        except ValueError:
            # ValueError si verifica quando int() non può convertire la stringa
            # (es. quando l'utente inserisce lettere o simboli)
            print("[!] Input non valido! Inserisci solo numeri interi.")
            # Continua il loop


# =============================================================================
# FUNZIONE: controlla_tentativo(tentativo, numero_segreto)
# =============================================================================
# Scopo: Confronta il tentativo dell'utente con il numero segreto
# Input: tentativo (int), numero_segreto (int)
# Output: Stringa - "corretto", "basso", o "alto"
# =============================================================================
def controlla_tentativo(tentativo, numero_segreto):
    """
    Confronta il tentativo dell'utente con il numero segreto e restituisce
    un indicatore di come è andato il tentativo.

    Args:
        tentativo (int): Il numero inserito dall'utente
        numero_segreto (int): Il numero da indovinare

    Returns:
        str: "corretto" se indovinato, "basso" se troppo basso, "alto" se troppo alto
    """

    if tentativo == numero_segreto:
        # L'utente ha indovinato il numero!
        return "corretto"

    elif tentativo < numero_segreto:
        # Il tentativo è più basso del numero segreto
        return "basso"

    else:
        # Il tentativo è più alto del numero segreto
        return "alto"


# =============================================================================
# FUNZIONE: mostra_feedback(risultato, tentativo)
# =============================================================================
# Scopo: Stampa un messaggio di feedback dopo ogni tentativo
# Input: risultato (str), tentativo (int)
# Output: None (solo stampa a video)
# =============================================================================
def mostra_feedback(risultato, tentativo):
    """
    Stampa un messaggio appropriato in base al risultato del tentativo.

    Args:
        risultato (str): Il risultato del controllo ("corretto", "basso", "alto")
        tentativo (int): Il numero inserito dall'utente
    """

    if risultato == "corretto":
        print(f"\n[OK] CONGRATULAZIONI! Hai indovinato il numero {tentativo}!")

    elif risultato == "basso":
        print(f"\n[^] Il numero {tentativo} e troppo BASSO.")
        print("[TIPS] Suggerimento: Prova con un numero piu alto!")

    else:  # risultato == "alto"
        print(f"\n[v] Il numero {tentativo} e troppo ALTO.")
        print("[TIPS] Suggerimento: Prova con un numero piu basso!")

    print("-" * 40)  # Linea separatrice


# =============================================================================
# FUNZIONE: gioca(tentativi_massimi)
# =============================================================================
# Scopo: Gestisce una singola partita del gioco
# Input: tentativi_massimi (int) - numero di tentativi consentiti
# Output: Boolean - True se vittoria, False se sconfitta
# =============================================================================
def gioca(tentativi_massimi):
    """
    Esegue una singola partita del gioco.

    Args:
        tentativi_massimi (int): Numero massimo di tentativi consentiti

    Returns:
        bool: True se il giocatore ha vinto, False se ha perso
    """

    # Generiamo il numero segreto all'inizio del gioco
    numero_segreto = genera_numero_segreto()

    # Debug: decommenta la riga sotto per vedere il numero segreto
    # print(f"[DEBUG] Numero segreto: {numero_segreto}")

    # Inizializziamo il contatore dei tentativi
    tentativo_corrente = 0

    # Loop principale del gioco - continua finché ci sono tentativi
    while tentativo_corrente < tentativi_massimi:

        # Calcoliamo quanti tentativi rimangono
        tentativi_rimasti = tentativi_massimi - tentativo_corrente

        # Otteniamo il tentativo dell'utente (con validazione)
        tentativo = ottieni_tentativo(tentativi_rimasti)

        # Controlliamo il tentativo
        risultato = controlla_tentativo(tentativo, numero_segreto)

        # Mostriamo il feedback appropriato
        mostra_feedback(risultato, tentativo)

        # Incrementiamo il contatore dei tentativi
        # È equivalente a: tentativo_corrente = tentativo_corrente + 1
        tentativo_corrente += 1

        # Se l'utente ha indovinato, terminiamo il gioco con vittoria
        if risultato == "corretto":
            return True

    # Se arriviamo qui, i tentativi sono finiti senza indovinare
    print(f"\n[:(] HAI PERSO!")
    print(f"Il numero segreto era: {numero_segreto}")
    print(f"Hai esaurito tutti i tuoi {tentativi_massimi} tentativi.")

    return False


# =============================================================================
# FUNZIONE: mostra_risultato_finale(vittoria, tentativi_massimi)
# =============================================================================
# Scopo: Mostra il risultato finale della partita
# Input: vittoria (bool), tentativi_massimi (int)
# Output: None (solo stampa a video)
# =============================================================================
def mostra_risultato_finale(vittoria, tentativi_massimi):
    """
    Mostra un messaggio finale basato sul risultato della partita.

    Args:
        vittoria (bool): True se il giocatore ha vinto
        tentativi_massimi (int): Numero di tentativi consentiti
    """

    print("=" * 60)  # Linea di separazione finale

    if vittoria:
        print("🏆 RISULTATO: VITTORIA!")
        print("Ottimo lavoro! Hai dimostrato buone capacità deduttive.")

        # Mostriamo un messaggio diverso in base alla difficoltà
        if tentativi_massimi == 15:
            print("Livello completato: Facile ⭐")
        elif tentativi_massimi == 10:
            print("Livello completato: Medio ⭐⭐")
        else:  # 5 tentativi
            print("Livello completato: Difficile ⭐⭐⭐")
            print("Sei davvero bravo!")

    else:
        print("💔 RISULTATO: SCONFITTA")
        print("Non ti arrendere! Prova ancora, migliorerai sicuramente.")

    print("=" * 60)


# =============================================================================
# FUNZIONE: vuoi_giocare_ancora()
# =============================================================================
# Scopo: Chiede all'utente se vuole fare un'altra partita
# Input: Nessuno (legge l'input dall'utente)
# Output: Boolean - True se vuole giocare ancora, False altrimenti
# =============================================================================
def vuoi_giocare_ancora():
    """
    Chiede all'utente se vuole giocare un'altra partita.

    Returns:
        bool: True se l'utente vuole giocare ancora, False altrimenti
    """

    print()

    while True:
        # Chiediamo all'utente se vuole giocare ancora
        risposta = input("Vuoi giocare ancora? (S/N): ").strip().upper()

        if risposta == "S":
            # L'utente vuole giocare ancora
            return True

        elif risposta == "N":
            # L'utente non vuole giocare
            print("\nGrazie per aver giocato! Arrivederci!")
            return False

        else:
            # Input non valido
            print("[!] Scelta non valida! Inserisci S (Sì) o N (No).")


# =============================================================================
# FUNZIONE: main()
# =============================================================================
# Scopo: Funzione principale che gestisce il flusso del gioco
# Input: Nessuno
# Output: None (ma avvia il gioco)
# =============================================================================
def main():
    """
    Funzione principale del programma.
    Gestisce il loop principale del gioco: mostra intestazione, sceglie
    difficoltà, gioca, e chiede se rigiocare.
    """

    # Mostriamo l'intestazione del gioco
    mostra_intestazione()

    # Loop principale per permettere più partite
    while True:

        # Fase 1: Scegliamo la difficoltà
        tentativi_massimi = scegli_difficolta()

        # Fase 2: Giociamo la partita
        # La funzione gioca() restituisce True (vittoria) o False (sconfitta)
        vittoria = gioca(tentativi_massimi)

        # Fase 3: Mostriamo il risultato finale
        mostra_risultato_finale(vittoria, tentativi_massimi)

        # Fase 4: Chiediamo se vuole giocare ancora
        if not vuoi_giocare_ancora():
            # Se l'utente non vuole giocare, usciamo dal loop
            break

    # Messaggio di uscita finale
    print("\n" + "=" * 60)
    print("   Fine del gioco - Speriamo ti sia piaciuto!")
    print("=" * 60)


# =============================================================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# =============================================================================
# Il blocco if __name__ == "__main__": è una convenzione Python
# Permette al file di essere eseguito direttamente come script
# ma anche di essere importato come modulo senza eseguire automaticamente il codice
# =============================================================================

if __name__ == "__main__":
    # Quando il file viene eseguito direttamente, chiamiamo la funzione main()
    main()


# =============================================================================
# NOTE DIDATTICHE PER LO STUDENTE
# =============================================================================
"""
CONCETTI CHIEVE APPRESI IN QUESTO PROGRAMMA:

1. FUNZIONI:
   - Organizzano il codice in blocchi riutilizzabili
   - Ogni funzione ha uno scopo specifico
   - Usano 'def' per essere definite
   - Possono accettare parametri (input) e restituire valori (output)

2. VARIABILI:
   - Servono a memorizzare dati
   - Hanno nomi descrittivi (es. numero_segreto, tentativi_rimasti)
   - Python è tipizzato dinamicamente (non serve dichiarare il tipo)

3. INPUT/OUTPUT:
   - input() legge da tastiera (restituisce sempre una stringa)
   - print() scrive a schermo
   - .strip() pulisce gli spazi
   - .upper()/.lower() convertono la maiuscola/minuscola

4. CONDIZIONI (if/elif/else):
   - Permettono di prendere decisioni
   - Il codice viene eseguito in base a condizioni
   - L'indentazione è OBBLIGATORIA in Python (4 spazi)

5. CICLI (while):
   - Ripetono un blocco di codice finché una condizione è vera
   - while True crea un loop infinito (si esce con break o return)

6. GESTIONE ERRORI (try/except):
   - try esegue codice che potrebbe causare errori
   - except cattura e gestisce gli errori
   - Utile per validare l'input dell'utente

7. OPERATORI DI CONFRONTO:
   - == uguale
   - != diverso
   - < minore, > maggiore
   - <= minore o uguale, >= maggiore o uguale

8. OPERATORI LOGICI:
   - and: vero se entrambe le condizioni sono vere
   - or: vero se almeno una condizione è vera
   - not: inverte il valore di verità

9. MODULO random:
   - random.randint(a, b) genera interi casuali
   - È molto utile nei giochi

10. BOOLEANI (True/False):
    - Rappresentano vero/falso
    - Usati nelle condizioni e nei valori di ritorno


SUGGERIMENTI PER APPROFONDIRE:
- Prova ad aggiungere un timer per misurare il tempo
- Aggiungi un sistema di punteggio cumulativo
- Crea un livello "Impossibile" con solo 3 tentativi
- Salva i migliori punteggi in un file
- Aggiungi la possibilità di giocare in multiplayer


COME ESEGUIRE IL PROGRAMMA:
1. Apri il terminale o prompt dei comandi
2. Naviga nella cartella dove hai salvato questo file
3. Digita: python number_guess.py
4. Oppure: python3 number_guess.py (su some sistemi)


BUON DIVERTIMENTO E BUONO STUDIO! 🚀
"""
