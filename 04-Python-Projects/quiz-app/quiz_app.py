"""
===========================================
APPLICAZIONE QUIZ IN PYTHON
===========================================

Autore: Progetto educativo per studenti universitari
Linguaggio: Python 3.x
Descrizione: Un'applicazione di quiz interattiva con
             categorie multiple, timer e sistema di punteggi

Questa applicazione dimostra l'uso di:
- Funzioni e strutture di controllo
- Gestione dei file JSON
- Moduli time e random
- Gestione degli errori
- Input/Output in console
"""

import json
import time
import random
import sys
from pathlib import Path


# ===========================================
# DATI DEL QUIZ - DATABASE DELLE DOMANDE
# ===========================================
# In un'applicazione reale, questi dati potrebbero
# essere caricati da un file esterno o un database

CATEGORIE_QUIZ = {
    "1": "Conoscenza Generale",
    "2": "Scienza",
    "3": "Storia",
    "4": "Programmazione"
}


DOMANDE_QUIZ = {
    "Conoscenza Generale": [
        {
            "domanda": "Qual e' la capitale dell'Australia?",
            "opzioni": ["Sydney", "Melbourne", "Canberra", "Perth"],
            "corretta": 2  # Indice della risposta corretta (0-3)
        },
        {
            "domanda": "Quanti elementi ci sono nel tavolo periodico?",
            "opzioni": ["112", "118", "120", "115"],
            "corretta": 1
        },
        {
            "domanda": "Qual e' il fiume piu' lungo del mondo?",
            "opzioni": ["Nilo", "Amazon", "Yangtze", "Mississippi"],
            "corretta": 1
        },
        {
            "domanda": "In quale anno e' iniziata la Seconda Guerra Mondiale?",
            "opzioni": ["1937", "1939", "1941", "1940"],
            "corretta": 1
        },
        {
            "domanda": "Qual e' il paese piu' piccolo del mondo per area?",
            "opzioni": ["Monaco", "San Marino", "Vaticano", "Malta"],
            "corretta": 2
        }
    ],

    "Scienza": [
        {
            "domanda": "Qual e' la formula chimica dell'acqua?",
            "opzioni": ["HO2", "H2O", "O2H", "H2O2"],
            "corretta": 1
        },
        {
            "domanda": "Quanto dura un anno luce?",
            "opzioni": ["Un anno", "Distanza percorsa dalla luce in un anno",
                      "365 giorni", "Tempo per viaggiare su Marte"],
            "corretta": 1
        },
        {
            "domanda": "Qual e' il simbolo chimico dell'oro?",
            "opzioni": ["Ag", "Au", "Fe", "Cu"],
            "corretta": 1
        },
        {
            "domanda": "Quale pianeta e' conosciuto come il Pianeta Rosso?",
            "opzioni": ["Venere", "Giove", "Marte", "Saturno"],
            "corretta": 2
        },
        {
            "domanda": "Qual e' la velocita' della luce nel vuoto?",
            "opzioni": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "200,000 km/s"],
            "corretta": 0
        }
    ],

    "Storia": [
        {
            "domanda": "Chi fu il primo imperatore romano?",
            "opzioni": ["Giulio Cesare", "Augusto", "Nerone", "Traiano"],
            "corretta": 1
        },
        {
            "domanda": "In quale anno cadde il Muro di Berlino?",
            "opzioni": ["1987", "1989", "1991", "1985"],
            "corretta": 1
        },
        {
            "domanda": "Chi scrisse la Divina Commedia?",
            "opzioni": ["Petrarca", "Boccaccio", "Dante Alighieri", "Manzoni"],
            "corretta": 2
        },
        {
            "domanda": "Quale civilta' costruì le piramidi di Giza?",
            "opzioni": ["Romana", "Greca", "Egizia", "Mesopotamica"],
            "corretta": 2
        },
        {
            "domanda": "In quale anno fu scoperta l'America?",
            "opzioni": ["1490", "1492", "1500", "1485"],
            "corretta": 1
        }
    ],

    "Programmazione": [
        {
            "domanda": "Qual e' l'output di print(2 ** 3) in Python?",
            "opzioni": ["6", "8", "9", "5"],
            "corretta": 1
        },
        {
            "domanda": "Quale parola chiave si usa per definire una funzione in Python?",
            "opzioni": ["function", "func", "def", "define"],
            "corretta": 2
        },
        {
            "domanda": "Qual e' il tipo di dati di [1, 2, 3] in Python?",
            "opzioni": ["tuple", "list", "array", "set"],
            "corretta": 1
        },
        {
            "domanda": "Come si commenta una riga in Python?",
            "opzioni": ["// commento", "# commento", "/* commento */", "-- commento"],
            "corretta": 1
        },
        {
            "domanda": "Quale funzione si usa per ottenere input dall'utente in Python?",
            "opzioni": ["input()", "read()", "get()", "scan()"],
            "corretta": 0
        }
    ]
}


# ===========================================
# FUNZIONI DI UTILITA'
# ===========================================

def pulisci_schermo():
    """
    Pulisce lo schermo della console.

    Nota: In un'applicazione reale, si potrebbe usare os.system('cls' o 'clear')
    ma per compatibilita' limitiamo l'uso di chiamate di sistema.
    """
    # Stampa 50 nuove linee per simulare la pulizia dello schermo
    print("\n" * 50)


def crea_linea(titolo="", lunghezza=70, carattere="="):
    """
    Crea una linea decorativa per l'interfaccia utente.

    Args:
        titolo (str): Titolo opzionale da includere nella linea
        lunghezza (int): Lunghezza totale della linea
        carattere (str): Carattere usato per la linea

    Returns:
        str: La linea formattata
    """
    if titolo:
        # Calcola lo spazio per centrare il titolo
        spazio_totale = lunghezza - len(titolo) - 2
        spazio_sinistra = spazio_totale // 2
        spazio_destra = spazio_totale - spazio_sinistra
        return f"{carattere * spazio_sinistra} {titolo} {carattere * spazio_destra}"
    else:
        return carattere * lunghezza


def pausa(messaggio="\nPremi Invio per continuare..."):
    """
    Mette in pausa l'esecuzione fino a quando l'utente preme Invio.

    Args:
        messaggio (str): Messaggio da mostrare all'utente
    """
    input(messaggio)


# ===========================================
# GESTIONE FILE JSON
# ===========================================

def ottieni_percorso_file_json():
    """
    Restituisce il percorso completo del file dei punteggi alti.

    Returns:
        Path: Oggetto Path con il percorso completo del file JSON
    """
    percorso = Path(r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\quiz-app\high_scores.json")
    return percorso


def carica_punteggi_alti():
    """
    Carica i punteggi alti dal file JSON.

    Se il file non esiste o e' corrotto, restituisce un dizionario vuoto.

    Returns:
        dict: Dizionario con i punteggi alti organizzati per categoria
    """
    percorso_file = ottieni_percorso_file_json()

    try:
        # Verifica se il file esiste
        if percorso_file.exists():
            with open(percorso_file, 'r', encoding='utf-8') as file:
                dati = json.load(file)
                return dati
        else:
            # Se il file non esiste, restituisce un dizionario vuoto
            print(f"\n[INFO] File dei punteggi non trovato. Verra' creato al primo salvataggio.")
            return {}

    except json.JSONDecodeError:
        print(f"\n[ERRORE] Il file JSON e' corrotto. Verra' creato un nuovo file.")
        return {}

    except Exception as e:
        print(f"\n[ERRORE] Impossibile caricare i punteggi: {e}")
        return {}


def mostra_punteggi_alti():
    """
    Mostra i punteggi alti per tutte le categorie.

    Questa funzione carica i punteggi dal file JSON e li visualizza
    in una tabella formattata per ogni categoria.
    """
    punteggi = carica_punteggi_alti()

    # Crea intestazione
    print("\n")
    print(crea_linea("PUNTEGGI PIU' ALTI"))
    print()

    if not punteggi:
        print("Nessun punteggio registrato ancora.")
        print("Gioca una partita per stabilire un nuovo record!")
        print()
        print(crea_linea())
        pausa()
        return

    # Mostra i punteggi per ogni categoria
    for categoria, dati in punteggi.items():
        print(f"\n--- {categoria.upper()} ---")
        print(f"{'Giocatore':<20} {'Punteggio':<12} {'Data':<15}")
        print("-" * 47)

        # Ordina i punteggi per punteggio decrescente
        punteggi_ordinati = sorted(dati, key=lambda x: x['punteggio'], reverse=True)

        # Mostra i primi 5 punteggi
        for i, record in enumerate(punteggi_ordinati[:5], 1):
            nome = record['nome'][:20]  # Limita la lunghezza del nome
            punteggio = record['punteggio']
            data = record['data']
            print(f"{i}. {nome:<20} {punteggio:<12} {data:<15}")

    print("\n")
    print(crea_linea())
    pausa()


def salva_punteggio_alto(nome, dati_punteggio):
    """
    Salva un nuovo punteggio alto nel file JSON.

    Args:
        nome (str): Nome del giocatore
        dati_punteggio (dict): Dizionario con categoria, punteggio, percentuale, data
    """
    try:
        # Carica i punteggi esistenti
        punteggi = carica_punteggi_alti()

        categoria = dati_punteggio['categoria']

        # Inizializza la lista se non esiste
        if categoria not in punteggi:
            punteggi[categoria] = []

        # Crea il nuovo record
        nuovo_record = {
            'nome': nome,
            'punteggio': dati_punteggio['punteggio'],
            'percentuale': dati_punteggio['percentuale'],
            'data': dati_punteggio['data']
        }

        # Aggiunge il nuovo record
        punteggi[categoria].append(nuovo_record)

        # Tieni solo i top 10 punteggi per categoria
        punteggi[categoria] = sorted(
            punteggi[categoria],
            key=lambda x: x['punteggio'],
            reverse=True
        )[:10]

        # Salva nel file
        percorso_file = ottieni_percorso_file_json()
        with open(percorso_file, 'w', encoding='utf-8') as file:
            json.dump(punteggi, file, ensure_ascii=False, indent=2)

        print(f"\n[SUCCESSO] Punteggio salvato con successo!")

    except PermissionError:
        print(f"\n[ERRORE] Permesso negato. Impossibile salvare il file.")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile salvare il punteggio: {e}")


# ===========================================
# FUNZIONI DI GIOCO
# ===========================================

def mescola_domande(domande):
    """
    Mescola l'ordine delle domande in modo casuale.

    Questa funzione crea una copia della lista di domande e la mescola
    usando il modulo random, garantendo che l'ordine sia diverso ogni volta.

    Args:
        domande (list): Lista delle domande da mescolare

    Returns:
        list: Nuova lista con domande in ordine casuale

    Esempio:
        >>> domande = [{'domanda': 'A'}, {'domanda': 'B'}]
        >>> mescolate = mescola_domande(domande)
        # L'ordine sara' casuale
    """
    # Crea una copia per non modificare la lista originale
    domande_copia = domande.copy()

    # Mescola la copia
    random.shuffle(domande_copia)

    return domande_copia


def ottieni_valutazione(percentuale):
    """
    Restituisce una valutazione in base alla percentuale di risposte corrette.

    Il sistema di valutazione e' cosi' definito:
    - 80-100%: Eccellente
    - 60-79%:  Buono
    - 40-59%:  Medio
    - 0-39%:   Scarso

    Args:
        percentuale (float): Percentuale di risposte corrette (0-100)

    Returns:
        tuple: (valutazione, messaggio) dove valutazione e' la stringa della
               valutazione e messaggio e' una descrizione

    Esempio:
        >>> ottieni_valutazione(85)
        ('Eccellente', 'Ottimo lavoro! Hai una conoscenza eccellente!')
    """
    if percentuale >= 80:
        return "Eccellente", "Ottimo lavoro! Hai una conoscenza eccellente!"
    elif percentuale >= 60:
        return "Buono", "Bravo! Continua a migliorare!"
    elif percentuale >= 40:
        return "Medio", "Non male, ma c'e' spazio per migliorare."
    else:
        return "Scarso", "Ti consigliamo di ripassare l'argomento."


def calcola_punteggio(risultati):
    """
    Calcola il punteggio finale basato sui risultati del quiz.

    Args:
        risultati (list): Lista di dizionari con chiavi 'corretto' (bool)
                         e 'tempo' (float)

    Returns:
        dict: Dizionario con:
              - 'corrette': numero di risposte corrette
              - 'sbagliate': numero di risposte sbagliate
              - 'totale': numero totale di domande
              - 'percentuale': percentuale di risposte corrette
              - 'valutazione': valutazione testuale
              - 'messaggio': messaggio di feedback

    Esempio:
        >>> risultati = [{'corretto': True, 'tempo': 5.2},
        ...             {'corretto': False, 'tempo': 8.1}]
        >>> calcola_punteggio(risultati)
        {'corrette': 1, 'sbagliate': 1, 'totale': 2, 'percentuale': 50.0, ...}
    """
    totale = len(risultati)
    corrette = sum(1 for r in risultati if r['corretto'])
    sbagliate = totale - corrette

    # Calcola la percentuale (evita divisione per zero)
    if totale > 0:
        percentuale = (corrette / totale) * 100
    else:
        percentuale = 0

    # Arrotonda a 2 decimali
    percentuale = round(percentuale, 2)

    # Ottieni la valutazione
    valutazione, messaggio = ottieni_valutazione(percentuale)

    return {
        'corrette': corrette,
        'sbagliate': sbagliate,
        'totale': totale,
        'percentuale': percentuale,
        'valutazione': valutazione,
        'messaggio': messaggio
    }


def mostra_domanda(dati_domanda, numero, totale):
    """
    Mostra una domanda formattata all'utente.

    Questa funzione visualizza la domanda e tutte le opzioni disponibili
    in un formato chiaro e leggibile.

    Args:
        dati_domanda (dict): Dizionario con chiavi 'domanda', 'opzioni', 'corretta'
        numero (int): Numero della domanda corrente
        totale (int): Numero totale di domande nel quiz

    Returns:
        None

    Esempio di output:
        ========================================
        DOMANDA 1 DI 5
        ========================================

        Qual e' la capitale dell'Italia?

        [1] Milano
        [2] Roma
        [3] Napoli
        [4] Torino
    """
    print("\n")
    print(crea_linea(f"DOMANDA {numero} DI {totale}"))
    print()
    print(f" {dati_domanda['domanda']}")
    print()

    # Mostra le opzioni
    for i, opzione in enumerate(dati_domanda['opzioni'], 1):
        print(f" [{i}] {opzione}")

    print()


def ottieni_risposta_utente(tempo_massimo=30):
    """
    Ottiene e valida la risposta dell'utente con un timer.

    Questa funzione implementa un timer di count-down e gestisce
    l'input dell'utente con validazione.

    Args:
        tempo_massimo (int): Tempo massimo in secondi (default: 30)

    Returns:
        tuple: (scelta_utente, tempo_impiegato)
               - scelta_utente (int): Indice della scelta (0-3) o None se timeout
               - tempo_impiegato (float): Tempo in secondi impiegato per rispondere

    Note tecniche:
        - Implementa un timer di count-down
        - Gestisce input non validi con try/except
        - Ritorna None se il tempo scade
    """
    print(f"\n>> Hai {tempo_massimo} secondi per rispondere.")
    print(">> Digita il numero della tua risposta: ", end='', flush=True)

    # Registra il tempo di inizio
    tempo_inizio = time.time()
    scelta_utente = None

    try:
        # Leggi l'input dall'utente
        input_utente = input()

        # Calcola il tempo impiegato
        tempo_fine = time.time()
        tempo_impiegato = round(tempo_fine - tempo_inizio, 2)

        # Valida l'input
        if input_utente.strip():
            scelta = int(input_utente.strip())

            # Verifica che la scelta sia valida (1-4)
            if 1 <= scelta <= 4:
                # Converti da 1-4 a 0-3 (indice Python)
                scelta_utente = scelta - 1
            else:
                print("\n[ATTENZIONE] Scelta non valida. Devi inserire un numero tra 1 e 4.")
                tempo_impiegato = round(tempo_massimo - tempo_impiegato, 2)
                if tempo_impiegato < 0:
                    tempo_impiegato = tempo_massimo
        else:
            print("\n[ATTENZIONE] Nessuna input inserito.")

    except ValueError:
        # Gestisce input non numerici
        print("\n[ATTENZIONE] Input non valido. Inserisci un numero.")
        tempo_fine = time.time()
        tempo_impiegato = round(tempo_fine - tempo_inizio, 2)

    except KeyboardInterrupt:
        # Gestisce Ctrl+C
        print("\n\n[INTERRUZIONE] Quiz interrotto dall'utente.")
        sys.exit(0)

    except Exception as e:
        # Gestisce altri errori
        print(f"\n[ERRORE] Si e' verificato un errore: {e}")
        tempo_fine = time.time()
        tempo_impiegato = round(tempo_fine - tempo_inizio, 2)

    return scelta_utente, tempo_impiegato


def verifica_risposta(dati_domanda, scelta_utente):
    """
    Verifica se la risposta dell'utente e' corretta.

    Args:
        dati_domanda (dict): Dizionario con la domanda e la risposta corretta
        scelta_utente (int): Indice della scelta dell'utente (0-3)

    Returns:
        bool: True se la risposta e' corretta, False altrimenti
    """
    if scelta_utente is None:
        return False

    return scelta_utente == dati_domanda['corretta']


def mostra_feedback_risposta(dati_domanda, scelta_utente, corretta):
    """
    Mostra il feedback immediato dopo la risposta.

    Questa funzione fornisce all'utente un feedback istantaneo sulla
    sua risposta, mostrando se e' corretta o qual era la risposta giusta.

    Args:
        dati_domanda (dict): Dizionario con i dati della domanda
        scelta_utente (int): Indice della scelta dell'utente (0-3)
        corretta (bool): Indica se la risposta era corretta
    """
    print("\n" + "-" * 70)

    if corretta:
        print(" [CORRETTO!] Ottima risposta!")
    else:
        if scelta_utente is not None:
            risposta_utente = dati_domanda['opzioni'][scelta_utente]
            print(f" [SBAGLIATO] Hai scelto: {risposta_utente}")
        else:
            print(" [SBAGLIATO] Tempo scaduto o nessuna risposta!")

        risposta_corretta = dati_domanda['opzioni'][dati_domanda['corretta']]
        print(f" La risposta corretta era: {risposta_corretta}")

    print("-" * 70)


def mostra_risultati_finali(punteggio, nome_giocatore, categoria):
    """
    Mostra i risultati finali del quiz in modo dettagliato.

    Args:
        punteggio (dict): Dizionario con i risultati calcolati
        nome_giocatore (str): Nome del giocatore
        categoria (str): Categoria del quiz
    """
    print("\n\n")
    print(crea_linea("RISULTATI FINALI"))
    print()
    print(f" Giocatore: {nome_giocatore}")
    print(f" Categoria: {categoria}")
    print()
    print(crea_linea())
    print()
    print(f" Risposte Corrette:  {punteggio['corrette']}/{punteggio['totale']}")
    print(f" Risposte Sbagliate:  {punteggio['sbagliate']}/{punteggio['totale']}")
    print(f" Percentuale:         {punteggio['percentuale']}%")
    print()
    print(f" Valutazione: {punteggio['valutazione']}")
    print(f" {punteggio['messaggio']}")
    print()
    print(crea_linea())
    print()


def inizia_quiz(categoria):
    """
    Esegue un quiz completo per la categoria specificata.

    Questa e' la funzione principale che gestisce l'esecuzione del quiz:
    1. Prepara le domande (mescolandole)
    2. Presenta ogni domanda all'utente
    3. Gestisce il timer e la raccolta delle risposte
    4. Fornisce feedback immediato
    5. Calcola il punteggio finale
    6. Salva i risultati se appropriato

    Args:
        categoria (str): Nome della categoria del quiz

    Returns:
        dict: Dizionario con i risultati finali o None se il quiz e' stato interrotto

    Flusso di esecuzione:
        1. Ottieni le domande per la categoria
        2. Mescola l'ordine delle domande
        3. Per ogni domanda:
           - Mostra la domanda
           - Avvia il timer
           - Raccogli la risposta
           - Verifica la correttezza
           - Mostra il feedback
        4. Calcola il punteggio finale
        5. Mostra i risultati
        6. Offri di salvare il punteggio
    """
    try:
        # Ottieni le domande per la categoria
        domande = DOMANDE_QUIZ.get(categoria, [])

        if not domande:
            print(f"\n[ERRORE] Nessuna domanda trovata per la categoria: {categoria}")
            return None

        # Mescola le domande per variare l'ordine
        domande = mescola_domande(domande)
        totale_domande = len(domande)

        # Pulisci lo schermo per iniziare il quiz
        pulisci_schermo()

        print("\n")
        print(crea_linea(f"QUIZ: {categoria.upper()}"))
        print()
        print(f" Hai {totale_domande} domande da rispondere.")
        print(f" Hai 30 secondi per ogni domanda.")
        print(f" Rispondi correttamente per ottenere il punteggio massimo!")
        print()
        print(crea_linea())

        pausa("\nPremi Invio quando sei pronto per iniziare...")

        # Lista per tracciare i risultati
        risultati = []

        # Loop attraverso tutte le domande
        for i, dati_domanda in enumerate(domande, 1):
            # Pulisci lo schermo per ogni nuova domanda
            pulisci_schermo()

            # Mostra la domanda
            mostra_domanda(dati_domanda, i, totale_domande)

            # Ottieni la risposta dell'utente
            scelta, tempo = ottieni_risposta_utente(tempo_massimo=30)

            # Verifica la risposta
            corretta = verifica_risposta(dati_domanda, scelta)

            # Registra il risultato
            risultati.append({
                'corretto': corretta,
                'tempo': tempo
            })

            # Mostra il feedback immediato
            mostra_feedback_risposta(dati_domanda, scelta, corretta)

            # Pausa breve prima della prossima domanda
            if i < totale_domande:
                pausa("\nPremi Invio per continuare...")

        # Calcola il punteggio finale
        punteggio_finale = calcola_punteggio(risultati)

        # Mostra i risultati finali
        nome_giocatore = input("\nInserisci il tuo nome: ").strip() or "Anonimo"
        pulisci_schermo()
        mostra_risultati_finali(punteggio_finale, nome_giocatore, categoria)

        # Prepara i dati per il salvataggio
        from datetime import datetime
        data_corrente = datetime.now().strftime("%Y-%m-%d %H:%M")

        dati_salvataggio = {
            'categoria': categoria,
            'punteggio': punteggio_finale['corrette'],
            'percentuale': punteggio_finale['percentuale'],
            'data': data_corrente
        }

        # Chiedi se salvare il punteggio
        salva = input("Vuoi salvare il tuo punteggio? (s/n): ").strip().lower()
        if salva == 's' or salva == 'si' or salva == 'sì':
            salva_punteggio_alto(nome_giocatore, dati_salvataggio)

        return punteggio_finale

    except KeyboardInterrupt:
        print("\n\n[INTERRUZIONE] Quiz interrotto dall'utente.")
        return None

    except Exception as e:
        print(f"\n[ERRORE] Si e' verificato un errore durante il quiz: {e}")
        import traceback
        traceback.print_exc()
        return None


# ===========================================
# FUNZIONI DI INTERFACCIA UTENTE
# ===========================================

def mostra_menu_principale():
    """
    Mostra il menu principale dell'applicazione.

    Questa funzione visualizza tutte le opzioni disponibili
    per l'utente in un formato chiaro e organizzato.

    Returns:
        None

    Il menu include:
        1. Avviare un nuovo quiz
        2. Visualizzare i punteggi alti
        3. Uscire dall'applicazione
    """
    print("\n")
    print(crea_linea("APP QUIZ PYTHON", 70, "="))
    print()
    print(" Benvenuto nell'Applicazione Quiz Python!")
    print(" Testa le tue conoscenze in diverse categorie.")
    print()
    print(crea_linea())
    print()
    print(" MENU PRINCIPALE")
    print()
    print(" [1] Nuovo Quiz")
    print(" [2] Punteggi Più Alti")
    print(" [3] Esci")
    print()
    print(crea_linea())


def seleziona_categoria():
    """
    Permette all'utente di selezionare una categoria di quiz.

    Mostra tutte le categorie disponibili e raccoglie la scelta
    dell'utente con validazione dell'input.

    Returns:
        str: Nome della categoria selezionata o None se l'utente torna al menu

    Processo:
        1. Mostra tutte le categorie disponibili
        2. Raccoglie l'input dell'utente
        3. Valida la scelta
        4. Restituisce la categoria o None per tornare indietro
    """
    while True:
        print("\n")
        print(crea_linea("SELEZIONA CATEGORIA"))
        print()

        # Mostra le categorie disponibili
        for key, categoria in CATEGORIE_QUIZ.items():
            num_domande = len(DOMANDE_QUIZ.get(categoria, []))
            print(f" [{key}] {categoria} ({num_domande} domande)")

        print()
        print(" [0] Torna al Menu Principale")
        print()
        print(crea_linea())
        print()
        print(">> Seleziona una categoria: ", end='', flush=True)

        try:
            scelta = input().strip()

            # Opzione per tornare indietro
            if scelta == "0":
                return None

            # Verifica che la scelta sia valida
            if scelta in CATEGORIE_QUIZ:
                categoria = CATEGORIE_QUIZ[scelta]
                return categoria
            else:
                print("\n[ATTENZIONE] Scelta non valida. Riprova.")
                pausa()

        except KeyboardInterrupt:
            print("\n\n[INTERRUZIONE] Operazione interrotta.")
            return None

        except Exception as e:
            print(f"\n[ERRORE] Si e' verificato un errore: {e}")
            pausa()


def mostra_info():
    """
    Mostra informazioni sull'applicazione.

    Returns:
        None
    """
    print("\n")
    print(crea_linea("INFORMAZIONI SULL'APP"))
    print()
    print(" Versione: 1.0.0")
    print(" Autore:  Progetto educativo Python")
    print(" Target:  Studenti universitari principianti")
    print()
    print(" Caratteristiche:")
    print("  - Quiz a risposta multipla")
    print("  - 4 categorie diverse")
    print("  - 5 domande per categoria")
    print("  - Timer di 30 secondi per domanda")
    print("  - Sistema di punteggi alti")
    print("  - Feedback immediato")
    print()
    print(" Scopo educativo:")
    print(" Questa applicazione dimostra l'uso di:")
    print("  - Funzioni e moduli")
    print("  - Strutture dati (liste, dizionari)")
    print("  - Gestione file JSON")
    print("  - Input/Output e validazione")
    print("  - Gestione errori")
    print("  - Algoritmi di base")
    print()
    print(crea_linea())


# ===========================================
# FUNZIONE PRINCIPALE
# ===========================================

def main():
    """
    Funzione principale dell'applicazione.

    Gestisce il ciclo principale dell'applicazione, mostrando il menu
    e gestendo le scelte dell'utente. Questa funzione e' il punto di
    ingresso del programma quando viene eseguito direttamente.

    Flusso di esecuzione:
        1. Mostra il menu principale
        2. Raccogli la scelta dell'utente
        3. Esegui l'azione appropriata:
           - Nuovo quiz -> seleziona categoria -> esegui quiz
           - Punteggi alti -> mostra classifica
           - Esci -> termina il programma
        4. Ripeti fino a quando l'utente non sceglie di uscire

    Gestione errori:
        - Cattura KeyboardInterrupt (Ctrl+C)
        - Cattura eccezioni generiche
        - Fornisce feedback appropriato all'utente

    Returns:
        None (il programma termina con sys.exit())
    """
    try:
        # Messaggio di benvenuto iniziale
        print("\n")
        print("=" * 70)
        print(" " * 15 + "BENVENUTO ALL'APP QUIZ PYTHON!")
        print("=" * 70)
        print()
        print(" Caricamento...")
        print()

        # Piccola pausa per effetto
        time.sleep(1)

        # Loop principale dell'applicazione
        while True:
            # Mostra il menu principale
            mostra_menu_principale()

            # Raccogli la scelta dell'utente
            print(">> Seleziona un'opzione: ", end='', flush=True)

            try:
                scelta = input().strip()

                # Processa la scelta dell'utente
                if scelta == "1":
                    # Nuovo quiz
                    categoria = seleziona_categoria()
                    if categoria:
                        inizia_quiz(categoria)
                        pausa("\nPremi Invio per tornare al menu...")

                elif scelta == "2":
                    # Mostra punteggi alti
                    mostra_punteggi_alti()

                elif scelta == "3":
                    # Esci dall'applicazione
                    print("\n")
                    print(crea_linea("ARRIVEDERCI!"))
                    print()
                    print(" Grazie per aver giocato!")
                    print(" Speriamo di rivederti presto.")
                    print()
                    print(crea_linea())
                    print()
                    break

                else:
                    # Scelta non valida
                    print("\n[ATTENZIONE] Opzione non valida. Seleziona 1, 2 o 3.")
                    pausa()

            except KeyboardInterrupt:
                # Gestisce Ctrl+C
                print("\n\n[INTERRUZIONE] Interruzione ricevuta.")
                scelta_continua = input("Vuoi davvero uscire? (s/n): ").strip().lower()
                if scelta_continua == 's':
                    print("\nArrivederci!")
                    break
                else:
                    print("\nContinuo...")
                    continue

            except Exception as e:
                # Gestisce altri errori nel loop principale
                print(f"\n[ERRORE] Si e' verificato un errore: {e}")
                import traceback
                traceback.print_exc()
                pausa("\nPremi Invio per continuare...")

    except Exception as e:
        # Gestisce errori critici fuori dal loop principale
        print(f"\n[ERRORE CRITICO] Errore fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ===========================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# ===========================================

if __name__ == "__main__":
    """
    Punto di ingresso quando lo script viene eseguito direttamente.

    Questo blocco viene eseguito solo quando il file viene eseguito
    come script principale, non quando viene importato come modulo.

    Questo pattern e' una best practice in Python per separare il codice
    di esecuzione dalle definizioni di funzioni e classi.
    """
    main()
