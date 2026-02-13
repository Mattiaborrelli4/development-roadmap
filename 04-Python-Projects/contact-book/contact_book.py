"""
RUBRICA TELEFONICA - Contact Book Application
==============================================
Un'applicazione completa per gestire i contatti con funzionalita avanzate.
Scritta per studenti universitari principianti.

Autore: Project Ideas Portfolio
Linguaggio: Python 3.x
"""

# Importazione delle librerie necessarie
import json
import csv
import re
import os
import uuid
from datetime import datetime, timedelta


# ==============================================================================
# CONFIGURAZIONE E COSTANTI
# ==============================================================================

# Percorso del file JSON per salvare i contatti
PERCORSO_JSON = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\contact-book\rubrica.json"

# Pattern regex per validare l'email
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Pattern regex per validare il numero di telefono (accetta vari formati)
# Accetta: +39 123 4567890, 123-456-7890, 123.456.7890, +391234567890
TELEFONO_PATTERN = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'


# ==============================================================================
# FUNZIONI DI VALIDAZIONE
# ==============================================================================

def valida_email(email):
    """
    Valida un indirizzo email usando regex.

    Args:
        email (str): L'indirizzo email da validare

    Returns:
        bool: True se l'email e valida, False altrimenti

    Spiegazione per studenti:
    - Utilizziamo espressioni regolari (regex) per verificare il formato
    - ^ indica l'inizio della stringa
    - $ indica la fine della stringa
    - Il pattern verifica: nome@dominio.estensione
    """
    if not email or email.strip() == "":
        return False

    # Utilizza re.match() per verificare se l'email corrisponde al pattern
    if re.match(EMAIL_PATTERN, email):
        return True
    return False


def valida_telefono(telefono):
    """
    Valida un numero di telefono.

    Args:
        telefono (str): Il numero di telefono da validare

    Returns:
        bool: True se il telefono e valido, False altrimenti

    Spiegazione per studenti:
    - Accetta vari formati internazionali
    - Deve contenere solo cifre, spazi, trattini, punti o il simbolo +
    - Deve avere tra 7 e 15 cifre totali
    """
    if not telefono or telefono.strip() == "":
        return False

    # Rimuove tutti i caratteri non numerici eccetto il +
    telefono_pulito = re.sub(r'[^\d+]', '', telefono)

    # Verifica che abbia tra 7 e 15 cifre (standard internazionale)
    if len(telefono_pulito) < 7 or len(telefono_pulito) > 15:
        return False

    # Verifica che corrisponda al pattern
    if re.match(TELEFONO_PATTERN, telefono):
        return True
    return False


def genera_uuid():
    """
    Genera un identificatore univoco per ogni contatto.

    Returns:
        str: Un UUID univoco come stringa

    Spiegazione per studenti:
    - UUID = Universally Unique Identifier
    - Garantisce che ogni contatto abbia un ID univoco
    - Utile per modificare/eliminare contatti senza ambiguita
    """
    return str(uuid.uuid4())


# ==============================================================================
# FUNZIONI DI GESTIONE FILE (JSON E CSV)
# ==============================================================================

def carica_da_json():
    """
    Carica i contatti dal file JSON.

    Returns:
        list: Una lista di dizionari che rappresentano i contatti.
              Restituisce una lista vuota se il file non esiste o c'e un errore.

    Spiegazione per studenti:
    - Try/except serve per gestire gli errori senza far crashare il programma
    - json.load() legge il file e lo converte in strutture dati Python
    - OSError include: FileNotFoundError, PermissionError, ecc.
    """
    contatti = []

    try:
        # Verifica se il file esiste
        if os.path.exists(PERCORSO_JSON):
            # Apre il file in modalita lettura
            with open(PERCORSO_JSON, 'r', encoding='utf-8') as file:
                # Carica i dati dal file JSON
                contatti = json.load(file)
                print(f"\n[SUCCESSO] Caricati {len(contatti)} contatti da file.")
        else:
            print(f"\n[INFO] Il file {PERCORSO_JSON} non esiste. Verra creato al primo salvataggio.")
            contatti = []

    except json.JSONDecodeError as e:
        print(f"\n[ERRORE] Il file JSON e corrotto: {e}")
        print("[INFO] Verra creato un nuovo file vuoto.")
        contatti = []

    except OSError as e:
        print(f"\n[ERRORE] Impossibile leggere il file: {e}")
        contatti = []

    return contatti


def salva_su_json(contatti):
    """
    Salva i contatti nel file JSON.

    Args:
        contatti (list): Lista di dizionari che rappresentano i contatti

    Returns:
        bool: True se il salvataggio ha successo, False altrimenti

    Spiegazione per studenti:
    - json.dump() scrive le strutture dati Python su file in formato JSON
    - ensure_ascii=False permette di salvare caratteri italiani (à, è, ì, ecc.)
    - indent=4 rende il file leggibile con indentazione
    """
    try:
        # Apre il file in modalita scrittura
        with open(PERCORSO_JSON, 'w', encoding='utf-8') as file:
            # Salva i contatti su file con formattazione leggibile
            json.dump(contatti, file, ensure_ascii=False, indent=4)
        print(f"\n[SUCCESSO] Salvati {len(contatti)} contatti su file.")
        return True

    except OSError as e:
        print(f"\n[ERRORE] Impossibile salvare il file: {e}")
        return False


def importa_da_csv():
    """
    Importa contatti da un file CSV.

    Returns:
        list: Una lista di dizionari che rappresentano i contatti importati.

    Spiegazione per studenti:
    - CSV = Comma Separated Values (formato molto comune per scambiare dati)
    - csv.DictReader legge ogni riga come un dizionario
    - La prima riga del CSV deve contenere le intestazioni delle colonne
    """
    contatti_importati = []

    try:
        # Chiede all'utente il percorso del file CSV
        print("\n--- IMPORTAZIONE DA CSV ---")
        percorso_csv = input("Inserisci il percorso completo del file CSV: ").strip()

        # Rimuove le virgolette se l'utente ha incollato il percorso con virgolette
        percorso_csv = percorso_csv.strip('"').strip("'")

        # Verifica se il file esiste
        if not os.path.exists(percorso_csv):
            print(f"[ERRORE] Il file {percorso_csv} non esiste.")
            return contatti_importati

        # Apre il file CSV in modalita lettura
        with open(percorso_csv, 'r', encoding='utf-8') as file:
            # Crea il lettore CSV
            lettore_csv = csv.DictReader(file)

            # Verifica che il file abbia le colonne necessarie
            colonne_necessarie = ['nome', 'telefono']
            if not all(colonna in lettore_csv.fieldnames for colonna in colonne_necessarie):
                print(f"[ERRORE] Il CSV deve contenere almeno le colonne: {', '.join(colonne_necessarie)}")
                print(f"[INFO] Colonne trovate: {lettore_csv.fieldnames}")
                return contatti_importati

            # Legge ogni riga del CSV
            for riga in lettore_csv:
                # Crea un nuovo contatto con UUID
                nuovo_contatto = {
                    'id': genera_uuid(),
                    'nome': riga.get('nome', '').strip(),
                    'telefono': riga.get('telefono', '').strip(),
                    'email': riga.get('email', '').strip(),
                    'indirizzo': riga.get('indirizzo', '').strip(),
                    'note': riga.get('note', '').strip(),
                    'compleanno': riga.get('compleanno', '').strip()
                }

                # Aggiunge solo se ha almeno nome e telefono
                if nuovo_contatto['nome'] and nuovo_contatto['telefono']:
                    contatti_importati.append(nuovo_contatto)

        print(f"\n[SUCCESSO] Importati {len(contatti_importati)} contatti dal file CSV.")
        return contatti_importati

    except csv.Error as e:
        print(f"\n[ERRORE] Errore nella lettura del CSV: {e}")
        return contatti_importati

    except OSError as e:
        print(f"\n[ERRORE] Impossibile leggere il file: {e}")
        return contatti_importati


def esporta_in_csv(contatti):
    """
    Esporta i contatti in un file CSV.

    Args:
        contatti (list): Lista di dizionari che rappresentano i contatti

    Returns:
        bool: True se l'esportazione ha successo, False altrimenti

    Spiegazione per studenti:
    - csv.DictWriter scrive i dizionari su file CSV
    - La prima riga contiene le intestazioni delle colonne
    - Tutti i contatti vengono esportati con tutti i loro campi
    """
    if not contatti:
        print("\n[INFO] Non ci sono contatti da esportare.")
        return False

    try:
        # Chiede all'utente il percorso dove salvare il file CSV
        print("\n--- ESPORTAZIONE IN CSV ---")
        percorso_csv = input("Inserisci il percorso completo dove salvare il file CSV: ").strip()

        # Rimuove le virgolette se presenti
        percorso_csv = percorso_csv.strip('"').strip("'")

        # Se non finisce con .csv, lo aggiunge
        if not percorso_csv.endswith('.csv'):
            percorso_csv += '.csv'

        # Definisce le colonne da esportare
        colonne = ['id', 'nome', 'telefono', 'email', 'indirizzo', 'note', 'compleanno']

        # Apre il file CSV in modalita scrittura
        with open(percorso_csv, 'w', encoding='utf-8', newline='') as file:
            # Crea il writer CSV
            scrittore_csv = csv.DictWriter(file, fieldnames=colonne)

            # Scrive l'intestazione
            scrittore_csv.writeheader()

            # Scrive tutti i contatti
            scrittore_csv.writerows(contatti)

        print(f"\n[SUCCESSO] Esportati {len(contatti)} contatti nel file CSV.")
        print(f"[INFO] File salvato in: {percorso_csv}")
        return True

    except OSError as e:
        print(f"\n[ERRORE] Impossibile salvare il file CSV: {e}")
        return False


# ==============================================================================
# FUNZIONI DI GESTIONE CONTATTI
# ==============================================================================

def aggiungi_contatto(contatti):
    """
    Aggiunge un nuovo contatto alla rubrica.

    Args:
        contatti (list): Lista dei contatti esistenti

    Returns:
        dict: Il nuovo contatto creato, o None se l'operazione e fallita

    Spiegazione per studenti:
    - Chiede all'utente tutti i campi del contatto
    - Valida email e telefono
    - I campi obbligatori sono: nome e telefono
    - Gli altri campi sono facoltativi
    """
    print("\n" + "="*50)
    print("AGGIUNGI NUOVO CONTATTO")
    print("="*50)

    try:
        # Nome (obbligatorio)
        while True:
            nome = input("Nome: ").strip()
            if nome:
                break
            print("[ERRORE] Il nome e obbligatorio.")

        # Telefono (obbligatorio e validato)
        while True:
            telefono = input("Telefono: ").strip()
            if valida_telefono(telefono):
                break
            print("[ERRORE] Inserisci un numero di telefono valido (es: +39 123 4567890)")

        # Email (facoltativo ma validato se inserito)
        email = ""
        while True:
            email_input = input("Email (premi Invio per saltare): ").strip()
            if not email_input:
                break  # Campo facoltativo
            if valida_email(email_input):
                email = email_input
                break
            print("[ERRORE] Inserisci un'email valida (es: mario.rossi@example.com)")

        # Altri campi (tutti facoltativi)
        indirizzo = input("Indirizzo (premi Invio per saltare): ").strip()
        note = input("Note (premi Invio per saltare): ").strip()

        # Compleanno (facoltativo con validazione del formato)
        compleanno = ""
        while True:
            compleanno_input = input("Compleanno (formato GG/MM/AAAA, premi Invio per saltare): ").strip()
            if not compleanno_input:
                break  # Campo facoltativo

            # Prova a validare il formato della data
            try:
                datetime.strptime(compleanno_input, "%d/%m/%Y")
                compleanno = compleanno_input
                break
            except ValueError:
                print("[ERRORE] Formato data non valido. Usa il formato GG/MM/AAAA (es: 15/06/1990)")

        # Crea il dizionario del nuovo contatto
        nuovo_contatto = {
            'id': genera_uuid(),
            'nome': nome,
            'telefono': telefono,
            'email': email,
            'indirizzo': indirizzo,
            'note': note,
            'compleanno': compleanno
        }

        # Aggiunge il contatto alla lista
        contatti.append(nuovo_contatto)

        print(f"\n[SUCCESSO] Contatto '{nome}' aggiunto alla rubrica!")
        return nuovo_contatto

    except KeyboardInterrupt:
        print("\n[INFO] Operazione annullata dall'utente.")
        return None
    except Exception as e:
        print(f"\n[ERRORE] Si e verificato un errore: {e}")
        return None


def visualizza_tutti_contatti(contatti):
    """
    Visualizza tutti i contatti in formato tabella.

    Args:
        contatti (list): Lista dei contatti da visualizzare

    Spiegazione per studenti:
    - Crea una tabella formattata con stringhe
    - Calcola la larghezza di ogni colonna dinamicamente
    - Formatta i dati in modo leggibile
    """
    if not contatti:
        print("\n[INFO] La rubrica e vuota. Nessun contatto da visualizzare.")
        return

    print("\n" + "="*100)
    print(f"{'TUTTI I CONTATTI':^100}")
    print("="*100)
    print(f"Totale: {len(contatti)} contatti")
    print("="*100 + "\n")

    # Definisci le colonne e le loro larghezze minime
    colonne = {
        'ID': 8,
        'NOME': 25,
        'TELEFONO': 18,
        'EMAIL': 30,
        'COMPLEANNO': 12
    }

    # Calcola la larghezza totale della tabella
    larghezza_totale = sum(colonne.values())

    # Intestazione della tabella
    header = ""
    separator = ""

    # Crea l'intestazione e il separatore
    for nome_colonna, larghezza in colonne.items():
        header += f"| {nome_colonna:<{larghezza-2}} "
        separator += "+" + "-"*(larghezza-1) + "-"

    header += "|"
    separator += "+"

    # Stampa l'intestazione
    print(separator)
    print(header)
    print(separator)

    # Stampa ogni contatto
    for contatto in contatti:
        # Tronca i campi troppo lunghi
        id_display = contatto['id'][:6] + "..." if len(contatto['id']) > 8 else contatto['id']
        nome_display = contatto['nome'][:23] + "..." if len(contatto['nome']) > 25 else contatto['nome']
        telefono_display = contatto['telefono']
        email_display = contatto['email'][:27] + "..." if len(contatto['email']) > 30 else (contatto['email'] if contatto['email'] else "-")
        compleanno_display = contatto['compleanno'] if contatto['compleanno'] else "-"

        # Stampa la riga del contatto
        riga = f"| {id_display:<{colonne['ID']-2}} "
        riga += f"| {nome_display:<{colonne['NOME']-2}} "
        riga += f"| {telefono_display:<{colonne['TELEFONO']-2}} "
        riga += f"| {email_display:<{colonne['EMAIL']-2}} "
        riga += f"| {compleanno_display:<{colonne['COMPLEANNO']-2}} |"

        print(riga)

    # Stampa il separatore finale
    print(separator)
    print()


def cerca_contatti(contatti):
    """
    Cerca contatti per nome o numero di telefono.

    Args:
        contatti (list): Lista dei contatti in cui cercare

    Returns:
        list: Lista dei contatti che corrispondono alla ricerca

    Spiegazione per studenti:
    - La ricerca e "case-insensitive" (non distingue maiuscole/minuscole)
    - Supporta la ricerca parziale (es: "mar" trova "Mario")
    - Cerca sia nel nome che nel numero di telefono
    - Utilizza l'operatore 'in' per verificare se una stringa contiene un'altra
    """
    if not contatti:
        print("\n[INFO] La rubrica e vuota. Nessun contatto da cercare.")
        return []

    print("\n" + "="*50)
    print("CERCA CONTATTO")
    print("="*50)

    # Chiede il termine di ricerca
    termine_ricerca = input("Inserisci nome o numero di telefono da cercare: ").strip().lower()

    if not termine_ricerca:
        print("[INFO] Inserisci un termine di ricerca valido.")
        return []

    # Filtra i contatti che corrispondono alla ricerca
    # List comprehension: crea una nuova lista filtrando quella esistente
    risultati = [
        contatto for contatto in contatti
        if termine_ricerca in contatto['nome'].lower() or
           termine_ricerca in contatto['telefono'].lower()
    ]

    # Mostra i risultati
    if risultati:
        print(f"\n[TROVATI] {len(risultati)} contatto/i che corrispondono alla ricerca:\n")

        # Intestazione tabella risultati
        print("-" * 80)
        for i, contatto in enumerate(risultati, 1):
            print(f"{i}. Nome: {contatto['nome']}")
            print(f"   Telefono: {contatto['telefono']}")
            if contatto['email']:
                print(f"   Email: {contatto['email']}")
            if contatto['indirizzo']:
                print(f"   Indirizzo: {contatto['indirizzo']}")
            if contatto['note']:
                print(f"   Note: {contatto['note']}")
            if contatto['compleanno']:
                print(f"   Compleanno: {contatto['compleanno']}")
            print("-" * 80)

        return risultati
    else:
        print(f"\n[INFO] Nessun contatto trovato con il termine '{termine_ricerca}'.")
        return []


def modifica_contatto(contatti):
    """
    Modifica un contatto esistente.

    Args:
        contatti (list): Lista dei contatti

    Returns:
        bool: True se la modifica ha successo, False altrimenti

    Spiegazione per studenti:
    - Prima cerca il contatto da modificare
    - Poi permette di modificare ogni campo
    - L'utente può premere Invio per mantenere il valore esistente
    - Valida email e telefono se modificati
    """
    if not contatti:
        print("\n[INFO] La rubrica e vuota. Nessun contatto da modificare.")
        return False

    print("\n" + "="*50)
    print("MODIFICA CONTATTO")
    print("="*50)

    # Prima cerca il contatto
    termine_ricerca = input("Inserisci il nome del contatto da modificare: ").strip().lower()

    if not termine_ricerca:
        print("[INFO] Inserisci un nome valido.")
        return False

    # Trova i contatti corrispondenti
    risultati = [
        contatto for contatto in contatti
        if termine_ricerca in contatto['nome'].lower()
    ]

    if not risultati:
        print(f"[INFO] Nessun contatto trovato con il nome '{termine_ricerca}'.")
        return False

    # Se ci sono piu risultati, mostra la lista e fai scegliere
    contatto_da_modificare = None

    if len(risultati) == 1:
        contatto_da_modificare = risultati[0]
    else:
        print(f"\n[TROVATI] {len(risultati)} contatti:")
        for i, contatto in enumerate(risultati, 1):
            print(f"{i}. {contatto['nome']} - {contatto['telefono']}")

        # Fai scegliere all'utente
        while True:
            scelta = input("\nQuale contatto vuoi modificare? (inserisci il numero): ").strip()
            try:
                indice = int(scelta) - 1
                if 0 <= indice < len(risultati):
                    contatto_da_modificare = risultati[indice]
                    break
                else:
                    print(f"[ERRORE] Inserisci un numero tra 1 e {len(risultati)}.")
            except ValueError:
                print("[ERRORE] Inserisci un numero valido.")

    # Mostra il contatto da modificare
    print(f"\nContatto selezionato:")
    print(f"  Nome: {contatto_da_modificare['nome']}")
    print(f"  Telefono: {contatto_da_modificare['telefono']}")
    print(f"  Email: {contatto_da_modificare['email'] or '-'}")
    print(f"  Indirizzo: {contatto_da_modificare['indirizzo'] or '-'}")
    print(f"  Note: {contatto_da_modificare['note'] or '-'}")
    print(f"  Compleanno: {contatto_da_modificare['compleanno'] or '-'}")

    print("\n--- Inserisci i nuovi valori (premi Invio per mantenere il valore esistente) ---")

    try:
        # Modifica nome
        nuovo_nome = input(f"Nome [{contatto_da_modificare['nome']}]: ").strip()
        if nuovo_nome:
            contatto_da_modificare['nome'] = nuovo_nome

        # Modifica telefono con validazione
        while True:
            nuovo_telefono = input(f"Telefono [{contatto_da_modificare['telefono']}]: ").strip()
            if not nuovo_telefono:
                break  # Mantiene il valore esistente
            if valida_telefono(nuovo_telefono):
                contatto_da_modificare['telefono'] = nuovo_telefono
                break
            print("[ERRORE] Inserisci un numero di telefono valido.")

        # Modifica email con validazione
        while True:
            nuova_email = input(f"Email [{contatto_da_modificare['email'] or '-'}]: ").strip()
            if not nuova_email:
                contatto_da_modificare['email'] = ""  # Può essere vuoto
                break
            if valida_email(nuova_email):
                contatto_da_modificare['email'] = nuova_email
                break
            print("[ERRORE] Inserisci un'email valida.")

        # Altri campi (nessuna validazione richiesta)
        nuovo_indirizzo = input(f"Indirizzo [{contatto_da_modificare['indirizzo'] or '-'}]: ").strip()
        if nuovo_indirizzo:
            contatto_da_modificare['indirizzo'] = nuovo_indirizzo

        nuove_note = input(f"Note [{contatto_da_modificare['note'] or '-'}]: ").strip()
        if nuove_note:
            contatto_da_modificare['note'] = nuove_note

        # Modifica compleanno con validazione
        while True:
            nuovo_compleanno = input(f"Compleanno [{contatto_da_modificare['compleanno'] or '-'}]: ").strip()
            if not nuovo_compleanno:
                contatto_da_modificare['compleanno'] = ""  # Può essere vuoto
                break
            try:
                datetime.strptime(nuovo_compleanno, "%d/%m/%Y")
                contatto_da_modificare['compleanno'] = nuovo_compleanno
                break
            except ValueError:
                print("[ERRORE] Formato data non valido. Usa il formato GG/MM/AAAA.")

        print(f"\n[SUCCESSO] Contatto '{contatto_da_modificare['nome']}' modificato!")
        return True

    except KeyboardInterrupt:
        print("\n[INFO] Operazione annullata dall'utente.")
        return False
    except Exception as e:
        print(f"\n[ERRORE] Si e verificato un errore: {e}")
        return False


def elimina_contatto(contatti):
    """
    Elimina un contatto dalla rubrica.

    Args:
        contatti (list): Lista dei contatti

    Returns:
        bool: True se l'eliminazione ha successo, False altrimenti

    Spiegazione per studenti:
    - Prima cerca il contatto da eliminare
    - Chiede conferma prima di eliminare
    - Rimuove il contatto dalla lista usando remove()
    """
    if not contatti:
        print("\n[INFO] La rubrica e vuota. Nessun contatto da eliminare.")
        return False

    print("\n" + "="*50)
    print("ELIMINA CONTATTO")
    print("="*50)

    # Prima cerca il contatto
    termine_ricerca = input("Inserisci il nome del contatto da eliminare: ").strip().lower()

    if not termine_ricerca:
        print("[INFO] Inserisci un nome valido.")
        return False

    # Trova i contatti corrispondenti
    risultati = [
        contatto for contatto in contatti
        if termine_ricerca in contatto['nome'].lower()
    ]

    if not risultati:
        print(f"[INFO] Nessun contatto trovato con il nome '{termine_ricerca}'.")
        return False

    # Se ci sono piu risultati, mostra la lista e fai scegliere
    contatto_da_eliminare = None

    if len(risultati) == 1:
        contatto_da_eliminare = risultati[0]
    else:
        print(f"\n[TROVATI] {len(risultati)} contatti:")
        for i, contatto in enumerate(risultati, 1):
            print(f"{i}. {contatto['nome']} - {contatto['telefono']}")

        # Fai scegliere all'utente
        while True:
            scelta = input("\nQuale contatto vuoi eliminare? (inserisci il numero): ").strip()
            try:
                indice = int(scelta) - 1
                if 0 <= indice < len(risultati):
                    contatto_da_eliminare = risultati[indice]
                    break
                else:
                    print(f"[ERRORE] Inserisci un numero tra 1 e {len(risultati)}.")
            except ValueError:
                print("[ERRORE] Inserisci un numero valido.")

    # Mostra il contatto da eliminare
    print(f"\nContatto da eliminare:")
    print(f"  Nome: {contatto_da_eliminare['nome']}")
    print(f"  Telefono: {contatto_da_eliminare['telefono']}")
    if contatto_da_eliminare['email']:
        print(f"  Email: {contatto_da_eliminare['email']}")

    # Chiede conferma
    conferma = input("\nSei sicuro di voler eliminare questo contatto? (s/N): ").strip().lower()

    if conferma == 's' or conferma == 'si':
        try:
            # Rimuove il contatto dalla lista
            contatti.remove(contatto_da_eliminare)
            print(f"\n[SUCCESSO] Contatto '{contatto_da_eliminare['nome']}' eliminato dalla rubrica.")
            return True
        except ValueError:
            print("\n[ERRORE] Impossibile eliminare il contatto.")
            return False
    else:
        print("\n[INFO] Eliminazione annullata.")
        return False


def controlla_compleanni(contatti):
    """
    Controlla se ci sono compleanni nei prossimi 7 giorni.

    Args:
        contatti (list): Lista dei contatti

    Spiegazione per studenti:
    - Confronta la data odierna con i compleanni dei contatti
    - Usa datetime per calcolare le date
    - Considera anche il cambio anno (31 dicembre -> 1 gennaio)
    - timedelta serve per sommare o sottrarre giorni a una data
    """
    if not contatti:
        print("\n[INFO] La rubrica e vuota.")
        return

    print("\n" + "="*50)
    print("COMPLEANNI DEI PROSSIMI 7 GIORNI")
    print("="*50)

    # Ottieni la data odierna
    oggi = datetime.now()
    anno_corrente = oggi.year

    # Filtra solo i contatti che hanno un compleanno
    contatti_con_compleanno = [
        contatto for contatto in contatti
        if contatto.get('compleanno')
    ]

    if not contatti_con_compleanno:
        print("\n[INFO] Nessun contatto ha inserito il compleanno.")
        return

    # Lista per i compleanni trovati
    compleanni_trovati = []

    # Controlla ogni contatto
    for contatto in contatti_con_compleanni:
        try:
            # Parso la data del compleanno
            data_compleanno = datetime.strptime(contatto['compleanno'], "%d/%m/%Y")

            # Crea la data del compleanno per quest'anno
            compleanno_questo_anno = data_compleanno.replace(year=anno_corrente)

            # Se il compleanno e gia passato quest'anno, considera quello dell'anno prossimo
            if compleanno_questo_anno < oggi:
                compleanno_questo_anno = data_compleanno.replace(year=anno_corrente + 1)

            # Calcola la differenza in giorni
            differenza = compleanno_questo_anno - oggi
            giorni_mancanti = differenza.days

            # Se e nei prossimi 7 giorni (incluso oggi)
            if 0 <= giorni_mancanti <= 7:
                # Calcola l'eta che compira
                eta = compleanno_questo_anno.year - data_compleanno.year

                compleanni_trovati.append({
                    'contatto': contatto,
                    'giorni': giorni_mancanti,
                    'eta': eta,
                    'data': compleanno_questo_anno.strftime("%d/%m/%Y")
                })

        except ValueError:
            # Se c'e un errore nel parsing della data, salta questo contatto
            continue

    # Mostra i risultati
    if compleanni_trovati:
        # Ordina per giorni mancanti
        compleanni_trovati.sort(key=lambda x: x['giorni'])

        print(f"\n[TROVATI] {len(compleanni_trovati)} compleanno/i nei prossimi 7 giorni:\n")

        for item in compleanni_trovati:
            contatto = item['contatto']
            giorni = item['giorni']
            eta = item['eta']
            data = item['data']

            if giorni == 0:
                print(f"*** OGGI *** {contatto['nome']} compie {eta} anni! ({data})")
                if contatto['telefono']:
                    print(f"           Telefono: {contatto['telefono']}")
            elif giorni == 1:
                print(f"*** DOMANI *** {contatto['nome']} compira {eta} anni! ({data})")
                if contatto['telefono']:
                    print(f"             Telefono: {contatto['telefono']}")
            else:
                print(f"Tra {giorni} giorni: {contatto['nome']} compira {eta} anni ({data})")
                if contatto['telefono']:
                    print(f"                 Telefono: {contatto['telefono']}")
            print()
    else:
        print("\n[INFO] Nessun compleanno nei prossimi 7 giorni.")


# ==============================================================================
# MENU PRINCIPALE
# ==============================================================================

def mostra_menu():
    """
    Mostra il menu principale dell'applicazione.

    Returns:
        None

    Spiegazione per studenti:
    - Usa print() per mostrare le opzioni disponibili
    - Il simbolo > indica l'opzione selezionabile
    """
    print("\n" + "="*50)
    print("RUBRICA TELEFONICA - MENU PRINCIPALE")
    print("="*50)
    print("1. Visualizza tutti i contatti")
    print("2. Aggiungi nuovo contatto")
    print("3. Cerca contatto")
    print("4. Modifica contatto")
    print("5. Elimina contatto")
    print("6. Controlla compleanni (prossimi 7 giorni)")
    print("7. Importa contatti da CSV")
    print("8. Esporta contatti in CSV")
    print("0. Esci")
    print("="*50)


def main():
    """
    Funzione principale dell'applicazione.

    Gestisce il ciclo principale del programma e il menu.

    Spiegazione per studenti:
    - Il ciclo while continua finche l'utente non sceglie di uscire
    - Ogni opzione del menu chiama una funzione specifica
    - I contatti vengono caricati all'avvio e salvati prima di uscire
    """
    # Carica i contatti dal file JSON all'avvio
    contatti = carica_da_json()

    # Messaggio di benvenuto
    print("\n" + "="*50)
    print("BENVENUTO NELLA RUBRICA TELEFONICA!")
    print("="*50)
    print("Un'applicazione per gestire i tuoi contatti")
    print("Versione 1.0 - Project Ideas Portfolio")

    # Loop principale del programma
    while True:
        try:
            # Mostra il menu
            mostra_menu()

            # Chiede all'utente di scegliere un'opzione
            scelta = input("\nSeleziona un'opzione (0-8): ").strip()

            # Elabora la scelta
            if scelta == '1':
                # Visualizza tutti i contatti
                visualizza_tutti_contatti(contatti)

            elif scelta == '2':
                # Aggiungi nuovo contatto
                aggiungi_contatto(contatti)
                # Salva automaticamente dopo l'aggiunta
                salva_su_json(contatti)

            elif scelta == '3':
                # Cerca contatto
                cerca_contatti(contatti)

            elif scelta == '4':
                # Modifica contatto
                modifica_contatto(contatti)
                # Salva automaticamente dopo la modifica
                salva_su_json(contatti)

            elif scelta == '5':
                # Elimina contatto
                elimina_contatto(contatti)
                # Salva automaticamente dopo l'eliminazione
                salva_su_json(contatti)

            elif scelta == '6':
                # Controlla compleanni
                controlla_compleanni(contatti)

            elif scelta == '7':
                # Importa da CSV
                contatti_importati = importa_da_csv()
                if contatti_importati:
                    contatti.extend(contatti_importati)
                    salva_su_json(contatti)

            elif scelta == '8':
                # Esporta in CSV
                esporta_in_csv(contatti)

            elif scelta == '0':
                # Esci dal programma
                print("\nSalvataggio in corso...")
                salva_su_json(contatti)
                print("\nGrazie per aver usato la Rubrica Telefonica!")
                print("Arrivederci!")
                break  # Esce dal loop while

            else:
                # Scelta non valida
                print("\n[ERRORE] Opzione non valida. Inserisci un numero tra 0 e 8.")

            # Pausa prima di mostrare di nuovo il menu
            input("\nPremi Invio per continuare...")

        except KeyboardInterrupt:
            # Gestisce Ctrl+C (interruzione da tastiera)
            print("\n\n[INFO] Interruzione rilevata.")
            conferma = input("Vuoi salvare prima di uscire? (s/N): ").strip().lower()
            if conferma == 's' or conferma == 'si':
                salva_su_json(contatti)
            print("\nArrivederci!")
            break

        except Exception as e:
            # Gestisce altri errori imprevisti
            print(f"\n[ERRORE] Si e verificato un errore imprevisto: {e}")
            print("[INFO] I contatti verranno salvati per evitare perdite di dati.")
            salva_su_json(contatti)
            break


# ==============================================================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# ==============================================================================

if __name__ == "__main__":
    """
    Punto di ingresso del programma.

    Spiegazione per studenti:
    - Questo blocco viene eseguito solo quando il file viene eseguito direttamente
    - Se il file viene importato come modulo, questo blocco non viene eseguito
    - main() avvia l'applicazione
    """
    main()
