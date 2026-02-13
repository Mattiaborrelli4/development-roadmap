"""
==============================================================
TO-DO LIST CLI - Versione Didattica
==============================================================
Un'applicazione a riga di comando per gestire una lista di task.
Creata per scopi educativi per imparare le basi di Python.

Concetti utilizzati:
- Liste e dizionari
- Funzioni
- Cicli (for, while)
- Condizionali (if/else)
- Gestione file JSON
- Input/Output

Autore: Studente Python
Data: 2026
==============================================================
"""

import json
import os


# ==============================================================================
# GESTIONE FILE - Salvataggio e caricamento dei task
# ==============================================================================

def carica_task_da_file():
    """
    Carica i task dal file 'tasks.json' se esiste.
    Se il file non esiste o è vuoto, restituisce una lista vuota.
    Il file viene sempre cercato nella stessa cartella dello script.

    Returns:
        list: Lista dei dizionari che rappresentano i task
    """
    # Percorso assoluto hardcoded del file tasks.json
    nome_file = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\todo-list-cli\tasks.json"

    # Verifico se il file esiste
    if os.path.exists(nome_file):
        try:
            # Apro il file in modalità lettura ('r' = read)
            # encoding='utf-8' serve per gestire correttamente i caratteri italiani
            with open(nome_file, 'r', encoding='utf-8') as file:
                # json.load legge il contenuto del file e lo converte in una lista Python
                dati = json.load(file)
                # Verifico che i dati siano effettivamente una lista
                if isinstance(dati, list):
                    return dati
                else:
                    # Se il file contiene dati non validi, restituisco lista vuota
                    return []
        except json.JSONDecodeError:
            # Se il file è corrotto o non contiene JSON valido, restituisco lista vuota
            return []
    else:
        # Se il file non esiste, restituisco una lista vuota
        return []


def salva_task_su_file(tasks):
    """
    Salva la lista dei task nel file 'tasks.json' in formato JSON.
    Il file viene salvato sempre nella stessa cartella dello script.
    JSON è un formato di testo che permette di salvare dati strutturati.

    Args:
        tasks (list): Lista dei dizionari che rappresentano i task
    """
    # Percorso assoluto hardcoded del file tasks.json
    nome_file = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\todo-list-cli\tasks.json"

    # Apro il file in modalità scrittura ('w' = write)
    # Se il file esiste già, viene sovrascritto
    # indent=4 rende il JSON più leggibile con indentazione
    # ensure_ascii=False permette di salvare caratteri come è, à, è, ù
    with open(nome_file, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


# ==============================================================================
# OPERAZIONI SUI TASK
# ==============================================================================

def genera_nuovo_id(tasks):
    """
    Genera un nuovo ID univoco per un task.
    L'ID sarà il massimo ID esistente + 1, oppure 1 se non ci sono task.

    Args:
        tasks (list): Lista dei task esistenti

    Returns:
        int: Il nuovo ID da assegnare al task
    """
    # Se non ci sono task, partiamo da 1
    if len(tasks) == 0:
        return 1

    # Creo una lista con tutti gli ID esistenti
    # Uso una list comprehension: [espressione for elemento in lista]
    lista_id = [task["id"] for task in tasks]

    # max() trova il valore più grande nella lista
    massimo_id = max(lista_id)

    # Restituisco il massimo ID + 1
    return massimo_id + 1


def aggiungi_task(tasks):
    """
    Aggiunge un nuovo task alla lista.
    Chiede all'utente di inserire il titolo del task.

    Args:
        tasks (list): Lista dei task esistenti

    Returns:
        list: La lista aggiornata dei task
    """
    print("\n" + "="*50)
    print("AGGIUNGI NUOVO TASK")
    print("="*50)

    # Chiedo all'utente di inserire il titolo del task
    # strip() rimuove gli spazi all'inizio e alla fine
    titolo = input("Inserisci il titolo del task: ").strip()

    # Verifico che l'utente abbia inserito qualcosa
    # Se la stringa è vuota dopo aver rimosso gli spazi, non accetto
    if titolo == "":
        print("[!] Errore: Il titolo non puo essere vuoto!")
        return tasks

    # Creo il nuovo task come dizionario
    nuovo_task = {
        "id": genera_nuovo_id(tasks),    # Genero ID univoco
        "title": titolo,                  # Titolo inserito dall'utente
        "completed": False                # Di default il task non è completato
    }

    # Aggiungo il nuovo task alla lista usando append()
    tasks.append(nuovo_task)

    # Salvo i dati su file
    salva_task_su_file(tasks)

    print(f"[OK] Task aggiunto con successo! (ID: {nuovo_task['id']})")

    return tasks


def rimuovi_task(tasks):
    """
    Rimuove un task dalla lista in base al suo ID.
    Chiede all'utente di inserire l'ID del task da rimuovere.

    Args:
        tasks (list): Lista dei task esistenti

    Returns:
        list: La lista aggiornata dei task
    """
    print("\n" + "="*50)
    print("RIMUOVI TASK")
    print("="*50)

    # Se non ci sono task, avviso l'utente
    if len(tasks) == 0:
        print("[!] Nessun task presente. Nessun task da rimuovere.")
        return tasks

    # Mostro tutti i task per aiutare l'utente a scegliere
    visualizza_tutti_task(tasks)

    try:
        # Chiedo all'utente l'ID del task da rimuovere
        id_da_rimuovere = int(input("\nInserisci l'ID del task da rimuovere: "))

        # Cerco il task con l'ID specificato
        task_trovato = False
        for task in tasks:
            if task["id"] == id_da_rimuovere:
                # Rimuovo il task usando remove()
                tasks.remove(task)
                task_trovato = True
                print(f"[OK] Task '{task['title']}' rimosso con successo!")
                break  # Esco dal ciclo perché ho trovato il task

        # Se non ho trovato nessun task con quell'ID
        if not task_trovato:
            print(f"[!] Errore: Nessun task trovato con ID {id_da_rimuovere}")
            return tasks

        # Salvo i dati su file
        salva_task_su_file(tasks)

    except ValueError:
        # Se l'utente non inserisce un numero valido
        print("[!] Errore: Devi inserire un numero valido per l'ID!")

    return tasks


def visualizza_tutti_task(tasks):
    """
    Visualizza tutti i task presenti nella lista in modo ordinato.
    I task completati vengono mostrati con un simbolo diverso.

    Args:
        tasks (list): Lista dei task da visualizzare
    """
    print("\n" + "="*50)
    print("TUTTI I TASK")
    print("="*50)

    # Se non ci sono task, avviso l'utente
    if len(tasks) == 0:
        print("Nessun task presente. La tua lista è vuota!")
        return

    # Uso enumerate() per avere sia l'indice che il task
    # start=1 fa partire la numerazione da 1 invece di 0
    for indice, task in enumerate(tasks, start=1):
        # Se il task è completato, mostro X, altrimenti uno spazio
        stato = "X" if task["completed"] else " "

        # Stampo le informazioni del task formattate
        # f-string permette di inserire variabili nelle stringhe
        print(f"{indice}. {stato} ID: {task['id']} | {task['title']}")

    # Mostro un riepilogo
    totali = len(tasks)
    completati = sum(1 for task in tasks if task["completed"])
    da_fare = totali - completati

    print(f"\nStatistiche: {totali} totali | {completati} completati | {da_fare} da fare")


def segna_completato(tasks):
    """
    Segna un task come completato o non completato.
    Se il task è già completato, lo rimette come "da fare".

    Args:
        tasks (list): Lista dei task esistenti

    Returns:
        list: La lista aggiornata dei task
    """
    print("\n" + "="*50)
    print("SEGNAGNA TASK COME COMPLETATO")
    print("="*50)

    # Se non ci sono task, avviso l'utente
    if len(tasks) == 0:
        print("[!] Nessun task presente.")
        return tasks

    # Mostro solo i task non completati
    print("\nTask non completati:")
    task_non_completati = [task for task in tasks if not task["completed"]]

    if len(task_non_completati) == 0:
        print("Ottimo lavoro! Tutti i task sono completati!")
        return tasks

    # Mostro i task non completati
    for task in task_non_completati:
        print(f"  - ID: {task['id']} | {task['title']}")

    try:
        # Chiedo all'utente l'ID del task da segnare come completato
        id_task = int(input("\nInserisci l'ID del task completato: "))

        # Cerco il task e cambio il suo stato
        task_trovato = False
        for task in tasks:
            if task["id"] == id_task:
                # Inverto lo stato: se era False diventa True, e viceversa
                task["completed"] = not task["completed"]
                task_trovato = True

                if task["completed"]:
                    print(f"[OK] Task '{task['title']}' segnato come COMPLETATO!")
                else:
                    print(f"↩️ Task '{task['title']}' rimesso come DA FARE!")

                break  # Esco dal ciclo perché ho trovato il task

        # Se non ho trovato nessun task con quell'ID
        if not task_trovato:
            print(f"[!] Errore: Nessun task trovato con ID {id_task}")
            return tasks

        # Salvo i dati su file
        salva_task_su_file(tasks)

    except ValueError:
        # Se l'utente non inserisce un numero valido
        print("[!] Errore: Devi inserire un numero valido per l'ID!")

    return tasks


# ==============================================================================
# INTERFACCIA UTENTE
# ==============================================================================

def mostra_menu():
    """
    Mostra il menu principale con tutte le opzioni disponibili.
    """
    print("\n" + "="*50)
    print("TO-DO LIST - Menu Principale")
    print("="*50)
    print("1. Aggiungi nuovo task")
    print("2. Rimuovi task")
    print("3. Visualizza tutti i task")
    print("4. Segna task come completato")
    print("5. Esci")
    print("="*50)


def ottieni_scelta_utente():
    """
    Chiede all'utente di scegliere un'opzione dal menu.
    Verifica che l'input sia valido.

    Returns:
        int: Il numero dell'opzione scelta, oppure None se l'input non è valido
    """
    try:
        # input() restituisce sempre una stringa, quindi la converto in int
        # flush=True assicura che il messaggio venga mostrato prima di aspettare l'input
        print("\nInserisci il numero dell'opzione desiderata:", flush=True)
        scelta = int(input(">> "))

        # Verifico che la scelta sia nel range valido
        if 1 <= scelta <= 5:
            return scelta
        else:
            print("[!] Errore: Inserisci un numero tra 1 e 5!")
            return None

    except ValueError:
        # Se l'utente non inserisce un numero
        print("[!] Errore: Devi inserire un numero!")
        return None


def pulisci_schermo():
    """
    Pulisce lo schermo del terminale per una visualizzazione più pulita.
    Funziona sia su Windows che su Unix (Linux/Mac).
    """
    # os.name è 'nt' su Windows, 'posix' su Unix
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')


def main():
    """
    Funzione principale che contiene il loop del programma.
    Gestisce il menu principale e chiama le funzioni appropriate.
    """
    # Messaggio di benvenuto
    print("\n" + "="*50)
    print("   BENVENUTO NELLA TO-DO LIST!")
    print("="*50)
    print("Un'applicazione semplice per gestire i tuoi compiti.")
    print("I tuoi task verranno salvati automaticamente.")
    print("="*50)

    # Carico i task dal file all'avvio del programma
    tasks = carica_task_da_file()

    # Loop principale del programma
    # while True crea un ciclo infinito che verrà interrotto solo con 'break'
    while True:
        # Mostro il menu
        mostra_menu()

        # Ottengo la scelta dell'utente
        scelta = ottieni_scelta_utente()

        # Se la scelta non è valida (None), continuo il ciclo
        if scelta is None:
            input("\nPremi Invio per continuare...")
            continue

        # Eseguo l'azione in base alla scelta dell'utente
        # Uso if/elif/else per gestire le diverse opzioni
        if scelta == 1:
            # Aggiungi task
            tasks = aggiungi_task(tasks)

        elif scelta == 2:
            # Rimuovi task
            tasks = rimuovi_task(tasks)

        elif scelta == 3:
            # Visualizza tutti i task
            visualizza_tutti_task(tasks)

        elif scelta == 4:
            # Segna task come completato
            tasks = segna_completato(tasks)

        elif scelta == 5:
            # Esci dal programma
            print("\n" + "="*50)
            print("Grazie per aver usato la To-Do List!")
            print("I tuoi task sono stati salvati.")
            print("="*50)
            # break interrompe il ciclo while e termina il programma
            break

        # Chiedo all'utente di premere Invio per continuare
        # Questo dà il tempo di leggere il risultato prima di tornare al menu
        input("\nPremi Invio per continuare...")


# ==============================================================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# ==============================================================================

# Questo blocco verifica se questo file viene eseguito direttamente
# __name__ è una variabile speciale di Python
# Se il file viene eseguito direttamente, __name__ == '__main__'
# Se il file viene importato come modulo, questo blocco non viene eseguito
if __name__ == "__main__":
    # Chiamo la funzione principale per avviare il programma
    main()
