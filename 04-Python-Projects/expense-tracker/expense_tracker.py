"""
===========================================
EXPENSE TRACKER - GESTORE DI SPES
===========================================
Un'applicazione per tracciare e gestire le spese personali.
Progetto educativo per studenti universitari.

Autore: Progetto Python per Principianti
Linguaggio: Python 3.x
===========================================
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Percorso del file JSON per salvare le spese
PERCORSO_FILE = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\expense-tracker\expenses.json"

# Categorie disponibili per le spese
CATEGORIE = ["Cibo", "Trasporti", "Intrattenimento", "Bollette", "Altro"]


def main():
    """
    Funzione principale che gestisce il menu principale dell'applicazione.
    Mostra le opzioni disponibili e gestisce il ciclo di interazione con l'utente.
    """
    # Carica le spese dal file all'avvio
    spese = carica_spese_da_file()

    # Ciclo principale del programma
    while True:
        # Mostra il menu principale
        mostra_menu_principale()

        # Ottieni la scelta dell'utente
        scelta = input("\n[+] Inserisci la tua scelta (1-9): ").strip()

        # Esegui l'azione corrispondente alla scelta
        if scelta == "1":
            spese = aggiungi_spesa(spese)
        elif scelta == "2":
            visualizza_tutte_le_spese(spese)
        elif scelta == "3":
            visualizza_per_categoria(spese)
        elif scelta == "4":
            visualizza_riepilogo_mensile(spese)
        elif scelta == "5":
            gestisci_budget(spese)
        elif scelta == "6":
            visualizza_statistiche(spese)
        elif scelta == "7":
            spese = elimina_spesa(spese)
        elif scelta == "8":
            esporta_report(spese)
        elif scelta == "9":
            # Salva le spese prima di uscire
            salva_spese_su_file(spese)
            print("\n[OK] Arrivederti! Grazie per aver usato Expense Tracker.")
            print("[*] Le spese sono state salvate automaticamente.")
            break
        else:
            print(f"\n[!] Scelta non valida. Per favore inserisci un numero tra 1 e 9.")

        # Pausa per permettere all'utente di leggere
        input("\n[*] Premi Invio per continuare...")


def mostra_menu_principale():
    """
    Mostra il menu principale dell'applicazione con tutte le opzioni disponibili.
    Utilizza caratteri ASCII per compatibilita con Windows.
    """
    # Pulisci lo schermo per una visualizzazione piu pulita
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "=" * 60)
    print("         EXPENSE TRACKER - GESTORE DI SPESE")
    print("=" * 60)
    print("\n[1] Aggiungi una nuova spesa")
    print("[2] Visualizza tutte le spese")
    print("[3] Visualizza spese per categoria")
    print("[4] Visualizza riepilogo mensile")
    print("[5] Gestisci budget per categoria")
    print("[6] Visualizza statistiche")
    print("[7] Elimina una spesa")
    print("[8] Esporta report in formato testo")
    print("[9] Esci")
    print("=" * 60)


def carica_spese_da_file() -> List[Dict[str, Any]]:
    """
    Carica le spese dal file JSON.
    Se il file non esiste o e vuoto, restituisce una lista vuota.

    Returns:
        List[Dict]: Lista di dizionari rappresentanti le spese
    """
    # Controlla se il file esiste
    if not os.path.exists(PERCORSO_FILE):
        print(f"\n[*] Il file {PERCORSO_FILE} non esiste.")
        print("[*] Verra creato un nuovo file al momento del salvataggio.")
        return []

    # Tenta di leggere il file JSON
    try:
        with open(PERCORSO_FILE, 'r', encoding='utf-8') as file:
            spese = json.load(file)
            print(f"\n[OK] Caricate {len(spese)} spese dal file.")
            return spese
    except json.JSONDecodeError:
        print("\n[!] Errore: Il file JSON e corrotto o vuoto.")
        print("[*] Verra creato un nuovo file.")
        return []
    except Exception as e:
        print(f"\n[!] Errore durante il caricamento: {e}")
        return []


def salva_spese_su_file(spese: List[Dict[str, Any]]) -> bool:
    """
    Salva le spese nel file JSON.

    Args:
        spese (List[Dict]): Lista di dizionari rappresentanti le spese

    Returns:
        bool: True se il salvataggio ha successo, False altrimenti
    """
    try:
        # Crea la directory se non esiste
        directory = os.path.dirname(PERCORSO_FILE)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Scrive le spese nel file JSON con formattazione leggibile
        with open(PERCORSO_FILE, 'w', encoding='utf-8') as file:
            json.dump(spese, file, ensure_ascii=False, indent=2)

        print(f"\n[OK] Salvate {len(spese)} spese nel file.")
        return True
    except Exception as e:
        print(f"\n[!] Errore durante il salvataggio: {e}")
        return False


def genera_nuovo_id(spese: List[Dict[str, Any]]) -> int:
    """
    Genera un ID unico per una nuova spesa.

    Args:
        spese (List[Dict]): Lista delle spese esistenti

    Returns:
        int: Nuovo ID unico
    """
    if not spese:
        return 1

    # Trova l'ID massimo esistente e aggiungi 1
    massimo_id = max(spesa.get('id', 0) for spesa in spese)
    return massimo_id + 1


def valida_importo(importo_str: str) -> float:
    """
    Valida e converte una stringa in un importo numerico valido.

    Args:
        importo_str (str): Stringa rappresentante l'importo

    Returns:
        float: Importo convertito, o None se non valido
    """
    try:
        importo = float(importo_str.replace(',', '.'))
        if importo <= 0:
            print("[!] L'importo deve essere maggiore di zero.")
            return None
        # Arrotonda a 2 decimali per i centesimi
        return round(importo, 2)
    except ValueError:
        print("[!] Importo non valido. Inserisci un numero (es. 10.50).")
        return None


def valida_data(data_str: str) -> str:
    """
    Valida il formato della data e restituisce una stringa normalizzata.

    Args:
        data_str (str): Stringa rappresentante la data

    Returns:
        str: Data nel formato DD/MM/YYYY se valida, None altrimenti
    """
    try:
        # Tenta di parsare la data nel formato DD/MM/YYYY
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.strftime("%d/%m/%Y")
    except ValueError:
        print("[!] Data non valida. Usa il formato GG/MM/AAAA (es. 25/12/2024).")
        return None


def aggiungi_spesa(spese: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Permette all'utente di aggiungere una nuova spesa con validazione degli input.

    Args:
        spese (List[Dict]): Lista delle spese esistenti

    Returns:
        List[Dict]: Lista aggiornata delle spese
    """
    print("\n" + "-" * 60)
    print("AGGIUNGI UNA NUOVA SPESA")
    print("-" * 60)

    # Validazione e input dell'importo
    while True:
        importo_str = input("\n[?] Inserisci l'importo: ").strip()
        importo = valida_importo(importo_str)
        if importo is not None:
            break

    # Selezione della categoria
    print("\n[*] Categorie disponibili:")
    for i, categoria in enumerate(CATEGORIE, 1):
        print(f"    {i}. {categoria}")

    while True:
        scelta_cat = input("\n[?] Seleziona la categoria (1-5): ").strip()
        try:
            indice = int(scelta_cat) - 1
            if 0 <= indice < len(CATEGORIE):
                categoria = CATEGORIE[indice]
                break
            else:
                print("[!] Scelta non valida. Inserisci un numero tra 1 e 5.")
        except ValueError:
            print("[!] Inserisci un numero valido.")

    # Input della descrizione
    descrizione = input("\n[?] Inserisci una descrizione (opzionale): ").strip()
    if not descrizione:
        descrizione = "Nessuna descrizione"

    # Validazione e input della data
    while True:
        data_str = input("\n[?] Inserisci la data (formato GG/MM/AAAA): ").strip()
        data = valida_data(data_str)
        if data is not None:
            break

    # Crea il dizionario della nuova spesa
    nuova_spesa = {
        'id': genera_nuovo_id(spese),
        'importo': importo,
        'categoria': categoria,
        'descrizione': descrizione,
        'data': data
    }

    # Aggiunge la spesa alla lista
    spese.append(nuova_spesa)

    # Salva automaticamente dopo l'aggiunta
    salva_spese_su_file(spese)

    print(f"\n[OK] Spesa aggiunta con successo!")
    print(f"[*] ID: {nuova_spesa['id']}")
    print(f"[*] Importo: EUR {importo:.2f}")
    print(f"[*] Categoria: {categoria}")
    print(f"[*] Data: {data}")

    return spese


def visualizza_tutte_le_spese(spese: List[Dict[str, Any]]) -> None:
    """
    Visualizza tutte le spese in un formato tabellare.

    Args:
        spese (List[Dict]): Lista delle spese da visualizzare
    """
    print("\n" + "-" * 100)
    print("TUTTE LE SPESE")
    print("-" * 100)

    if not spese:
        print("\n[*] Nessuna spesa registrata.")
        return

    # Intestazione della tabella
    print(f"\n{'ID':<6} {'Data':<12} {'Categoria':<18} {'Importo':>12} {'Descrizione'}")
    print("-" * 100)

    # Ordina le spese per data (piu recenti prima)
    spese_ordinate = sorted(spese, key=lambda x: datetime.strptime(x['data'], "%d/%m/%Y"), reverse=True)

    totale = 0

    # Stampa ogni spesa
    for spesa in spese_ordinate:
        print(f"{spesa['id']:<6} {spesa['data']:<12} {spesa['categoria']:<18} EUR {spesa['importo']:>8.2f}   {spesa['descrizione']}")
        totale += spesa['importo']

    print("-" * 100)
    print(f"{'TOTALE':>36} EUR {totale:>8.2f}")
    print(f"{'Numero di spese':>36} {len(spese):>10}")


def visualizza_per_categoria(spese: List[Dict[str, Any]]) -> None:
    """
    Visualizza le spese filtrate per categoria scelta dall'utente.

    Args:
        spese (List[Dict]): Lista delle spese da filtrare
    """
    print("\n" + "-" * 60)
    print("VISUALIZZA SPESE PER CATEGORIA")
    print("-" * 60)

    if not spese:
        print("\n[*] Nessuna spesa registrata.")
        return

    # Mostra le categorie disponibili
    print("\n[*] Categorie disponibili:")
    for i, categoria in enumerate(CATEGORIE, 1):
        print(f"    {i}. {categoria}")

    # Ottieni la scelta dell'utente
    while True:
        scelta_cat = input("\n[?] Seleziona la categoria (1-5): ").strip()
        try:
            indice = int(scelta_cat) - 1
            if 0 <= indice < len(CATEGORIE):
                categoria_selezionata = CATEGORIE[indice]
                break
            else:
                print("[!] Scelta non valida. Inserisci un numero tra 1 e 5.")
        except ValueError:
            print("[!] Inserisci un numero valido.")

    # Filtra le spese per categoria
    spese_filtrate = [s for s in spese if s['categoria'] == categoria_selezionata]

    if not spese_filtrate:
        print(f"\n[*] Nessuna spesa trovata per la categoria: {categoria_selezionata}")
        return

    # Mostra le spese filtrate
    print(f"\n{'ID':<6} {'Data':<12} {'Importo':>12} {'Descrizione'}")
    print("-" * 60)

    totale_categoria = 0

    for spesa in spese_filtrate:
        print(f"{spesa['id']:<6} {spesa['data']:<12} EUR {spesa['importo']:>8.2f}   {spesa['descrizione']}")
        totale_categoria += spesa['importo']

    print("-" * 60)
    print(f"{'TOTALE ' + categoria_selezionata:>40} EUR {totale_categoria:>8.2f}")
    print(f"{'Numero di spese':>40} {len(spese_filtrate):>10}")


def visualizza_riepilogo_mensile(spese: List[Dict[str, Any]]) -> None:
    """
    Visualizza un riepilogo delle spese per mese e anno.

    Args:
        spese (List[Dict]): Lista delle spese da riepilogare
    """
    print("\n" + "-" * 80)
    print("RIEPILOGO MENSILE")
    print("-" * 80)

    if not spese:
        print("\n[*] Nessuna spesa registrata.")
        return

    # Crea un dizionario per raggruppare le spese per mese/anno
    riepilogo_mensile = {}

    for spesa in spese:
        # Estrae mese e anno dalla data
        data_obj = datetime.strptime(spesa['data'], "%d/%m/%Y")
        chiave = f"{data_obj.year}-{data_obj.month:02d}"

        if chiave not in riepilogo_mensile:
            riepilogo_mensile[chiave] = {
                'totale': 0,
                'conteggio': 0,
                'categorie': {}
            }

        riepilogo_mensile[chiave]['totale'] += spesa['importo']
        riepilogo_mensile[chiave]['conteggio'] += 1

        # Aggiunge alla categoria
        categoria = spesa['categoria']
        if categoria not in riepilogo_mensile[chiave]['categorie']:
            riepilogo_mensile[chiave]['categorie'][categoria] = 0
        riepilogo_mensile[chiave]['categorie'][categoria] += spesa['importo']

    # Ordina per mese (piu recenti prima)
    mesi_ordinati = sorted(riepilogo_mensile.keys(), reverse=True)

    # Mostra il riepilogo per ogni mese
    for mese in mesi_ordinati:
        dati = riepilogo_mensile[mese]
        anno, mese_num = mese.split('-')
        nome_mese = datetime(int(anno), int(mese_num), 1).strftime('%B %Y')

        print(f"\n{'=' * 80}")
        print(f"Mese: {nome_mese.upper()}")
        print(f"{'=' * 80}")

        # Mostra il totale per categoria
        for categoria in CATEGORIE:
            if categoria in dati['categorie']:
                importo_cat = dati['categorie'][categoria]
                percentuale = (importo_cat / dati['totale']) * 100
                print(f"  {categoria:<18}: EUR {importo_cat:>8.2f} ({percentuale:>5.1f}%)")

        print(f"  {'-' * 50}")
        print(f"  {'TOTALE':<18}: EUR {dati['totale']:>8.2f}")
        print(f"  {'Numero spese':<18}: {dati['conteggio']:>10}")


def gestisci_budget(spese: List[Dict[str, Any]]) -> None:
    """
    Gestisce i budget per ogni categoria, permettendo di impostare e verificare i limiti.

    Args:
        spese (List[Dict]): Lista delle spese per calcolare il totale
    """
    print("\n" + "-" * 60)
    print("GESTIONE BUDGET")
    print("-" * 60)

    # Percorso del file budget
    percorso_budget = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\expense-tracker\budget.json"

    # Carica i budget esistenti
    budget = {}
    if os.path.exists(percorso_budget):
        try:
            with open(percorso_budget, 'r', encoding='utf-8') as file:
                budget = json.load(file)
        except:
            budget = {}

    # Menu gestione budget
    while True:
        print("\n[1] Imposta/Modifica budget per categoria")
        print("[2] Visualizza stato budget")
        print("[3] Torna al menu principale")

        scelta = input("\n[?] Seleziona un'opzione (1-3): ").strip()

        if scelta == "1":
            # Imposta budget
            print("\n[*] Seleziona la categoria:")
            for i, cat in enumerate(CATEGORIE, 1):
                print(f"    {i}. {cat}")

            while True:
                scelta_cat = input("\n[?] Seleziona la categoria (1-5): ").strip()
                try:
                    indice = int(scelta_cat) - 1
                    if 0 <= indice < len(CATEGORIE):
                        categoria = CATEGORIE[indice]
                        break
                except:
                    pass

            importo_str = input(f"\n[?] Inserisci il budget mensile per {categoria}: ").strip()
            importo = valida_importo(importo_str)

            if importo is not None:
                budget[categoria] = importo

                # Salva il budget
                try:
                    with open(percorso_budget, 'w', encoding='utf-8') as file:
                        json.dump(budget, file, ensure_ascii=False, indent=2)
                    print(f"\n[OK] Budget per {categoria} impostato a EUR {importo:.2f}")
                except Exception as e:
                    print(f"\n[!] Errore nel salvataggio del budget: {e}")

        elif scelta == "2":
            # Visualizza stato budget
            if not budget:
                print("\n[*] Nessun budget impostato.")
                continue

            # Calcola il totale per categoria nel mese corrente
            mese_corrente = datetime.now().strftime("%m/%Y")

            print(f"\n{'=' * 70}")
            print(f"STATO BUDGET - {mese_corrente}")
            print(f"{'=' * 70}")

            for categoria, budget_limit in budget.items():
                # Calcola il totale speso per questa categoria nel mese corrente
                totale_speso = sum(
                    s['importo'] for s in spese
                    if s['categoria'] == categoria and
                    datetime.strptime(s['data'], "%d/%m/%Y").strftime("%m/%Y") == mese_corrente
                )

                rimanente = budget_limit - totale_speso
                percentuale_usato = (totale_speso / budget_limit) * 100 if budget_limit > 0 else 0

                # Mostra un avviso se il budget e superato
                stato = "[OK]"
                if percentuale_usato >= 100:
                    stato = "[!] BUDGET SUPERATO"
                elif percentuale_usato >= 80:
                    stato = "[!] ATTENZIONE"

                print(f"\n{categoria}:")
                print(f"  Budget:        EUR {budget_limit:>8.2f}")
                print(f"  Speso:         EUR {totale_speso:>8.2f} ({percentuale_usato:>5.1f}%)")
                print(f"  Rimanente:     EUR {rimanente:>8.2f}")
                print(f"  Stato:         {stato}")

        elif scelta == "3":
            break

        else:
            print("\n[!] Scelta non valida.")


def visualizza_statistiche(spese: List[Dict[str, Any]]) -> None:
    """
    Calcola e visualizza statistiche sulle spese.

    Args:
        spese (List[Dict]): Lista delle spese per calcolare le statistiche
    """
    print("\n" + "-" * 80)
    print("STATISTICHE SPESE")
    print("-" * 80)

    if not spese:
        print("\n[*] Nessuna spesa registrata.")
        return

    # Calcola le statistiche generali
    totale_spese = sum(s['importo'] for s in spese)
    media_spese = totale_spese / len(spese)
    spesa_piu_costosa = max(spese, key=lambda x: x['importo'])
    spesa_meno_costosa = min(spese, key=lambda x: x['importo'])

    print(f"\n{'=' * 80}")
    print("STATISTICHE GENERALI")
    print(f"{'=' * 80}")
    print(f"  Numero totale di spese:     {len(spese)}")
    print(f"  Totale speso:               EUR {totale_spese:>8.2f}")
    print(f"  Media spesa:                EUR {media_spese:>8.2f}")
    print(f"\n  Spesa piu costosa:          EUR {spesa_piu_costosa['importo']:>8.2f}")
    print(f"    - Categoria:              {spesa_piu_costosa['categoria']}")
    print(f"    - Descrizione:             {spesa_piu_costosa['descrizione']}")
    print(f"    - Data:                   {spesa_piu_costosa['data']}")
    print(f"\n  Spesa meno costosa:         EUR {spesa_meno_costosa['importo']:>8.2f}")
    print(f"    - Categoria:              {spesa_meno_costosa['categoria']}")
    print(f"    - Descrizione:             {spesa_meno_costosa['descrizione']}")
    print(f"    - Data:                   {spesa_meno_costosa['data']}")

    # Calcola le statistiche per categoria
    print(f"\n{'=' * 80}")
    print("SPESO PER CATEGORIA")
    print(f"{'=' * 80}")

    for categoria in CATEGORIE:
        spese_cat = [s for s in spese if s['categoria'] == categoria]
        if spese_cat:
            totale_cat = sum(s['importo'] for s in spese_cat)
            media_cat = totale_cat / len(spese_cat)
            percentuale = (totale_cat / totale_spese) * 100

            print(f"\n  {categoria}:")
            print(f"    Numero spese:    {len(spese_cat)}")
            print(f"    Totale:          EUR {totale_cat:>8.2f} ({percentuale:>5.1f}%)")
            print(f"    Media:           EUR {media_cat:>8.2f}")

    # Trova la categoria con piu spese
    conteggio_categorie = {}
    for spesa in spese:
        cat = spesa['categoria']
        conteggio_categorie[cat] = conteggio_categorie.get(cat, 0) + 1

    if conteggio_categorie:
        categoria_top = max(conteggio_categorie, key=conteggio_categorie.get)
        print(f"\n  Categoria con piu spese: {categoria_top} ({conteggio_categorie[categoria_top]} spese)")


def elimina_spesa(spese: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Permette all'utente di eliminare una spesa in base al suo ID.

    Args:
        spese (List[Dict]): Lista delle spese

    Returns:
        List[Dict]: Lista aggiornata delle spese
    """
    print("\n" + "-" * 60)
    print("ELIMINA SPESE")
    print("-" * 60)

    if not spese:
        print("\n[*] Nessuna spesa registrata.")
        return spese

    # Mostra tutte le spese per facilitare la scelta
    visualizza_tutte_le_spese(spese)

    while True:
        id_str = input("\n[?] Inserisci l'ID della spesa da eliminare (0 per annullare): ").strip()

        if id_str == "0":
            print("\n[*] Operazione annullata.")
            return spese

        try:
            id_da_eliminare = int(id_str)

            # Cerca la spesa con l'ID specificato
            spesa_trovata = None
            for spesa in spese:
                if spesa['id'] == id_da_eliminare:
                    spesa_trovata = spesa
                    break

            if spesa_trovata:
                # Conferma l'eliminazione
                print(f"\n[*] Sei sicuro di voler eliminare questa spesa?")
                print(f"    Importo:    EUR {spesa_trovata['importo']:.2f}")
                print(f"    Categoria:  {spesa_trovata['categoria']}")
                print(f"    Data:       {spesa_trovata['data']}")
                print(f"    Descrizione: {spesa_trovata['descrizione']}")

                conferma = input("\n[?] Confermi l'eliminazione? (s/n): ").strip().lower()

                if conferma == 's':
                    # Rimuovi la spesa
                    spese.remove(spesa_trovata)

                    # Salva le modifiche
                    salva_spese_su_file(spese)

                    print(f"\n[OK] Spesa eliminata con successo.")
                    return spese
                else:
                    print("\n[*] Operazione annullata.")
                    return spese
            else:
                print(f"\n[!] Nessuna spesa trovata con ID {id_da_eliminare}.")
                return spese

        except ValueError:
            print("\n[!] Inserisci un ID valido (numero intero).")


def esporta_report(spese: List[Dict[str, Any]]) -> None:
    """
    Esporta un report dettagliato delle spese in un file di testo.

    Args:
        spese (List[Dict]): Lista delle spese da esportare
    """
    print("\n" + "-" * 60)
    print("ESPORTA REPORT")
    print("-" * 60)

    if not spese:
        print("\n[*] Nessuna spesa da esportare.")
        return

    # Nome del file di report
    nome_file = f"report_spese_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    percorso_report = os.path.join(
        r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\expense-tracker",
        nome_file
    )

    try:
        with open(percorso_report, 'w', encoding='utf-8') as file:
            # Intestazione del report
            file.write("=" * 80 + "\n")
            file.write("REPORT SPESE\n")
            file.write(f"Generato il: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            file.write("=" * 80 + "\n\n")

            # Statistiche generali
            totale_spese = sum(s['importo'] for s in spese)
            media_spese = totale_spese / len(spese)

            file.write("STATISTICHE GENERALI\n")
            file.write("-" * 80 + "\n")
            file.write(f"Numero totale di spese: {len(spese)}\n")
            file.write(f"Totale speso: EUR {totale_spese:.2f}\n")
            file.write(f"Media spesa: EUR {media_spese:.2f}\n\n")

            # Spese per categoria
            file.write("SPESE PER CATEGORIA\n")
            file.write("-" * 80 + "\n")

            for categoria in CATEGORIE:
                spese_cat = [s for s in spese if s['categoria'] == categoria]
                if spese_cat:
                    totale_cat = sum(s['importo'] for s in spese_cat)
                    percentuale = (totale_cat / totale_spese) * 100
                    file.write(f"{categoria}: EUR {totale_cat:>8.2f} ({percentuale:>5.1f}%)\n")

            file.write("\n")

            # Dettaglio di tutte le spese
            file.write("DETTAGLIO SPESE\n")
            file.write("-" * 100 + "\n")
            file.write(f"{'ID':<6} {'Data':<12} {'Categoria':<18} {'Importo':>12} {'Descrizione'}\n")
            file.write("-" * 100 + "\n")

            # Ordina per data
            spese_ordinate = sorted(spese, key=lambda x: datetime.strptime(x['data'], "%d/%m/%Y"), reverse=True)

            for spesa in spese_ordinate:
                file.write(f"{spesa['id']:<6} {spesa['data']:<12} {spesa['categoria']:<18} EUR {spesa['importo']:>8.2f}   {spesa['descrizione']}\n")

            file.write("\n" + "=" * 80 + "\n")
            file.write(f"FINE REPORT\n")

        print(f"\n[OK] Report esportato con successo!")
        print(f"[*] File salvato in: {percorso_report}")

    except Exception as e:
        print(f"\n[!] Errore durante l'esportazione: {e}")


# Punto di ingresso del programma
if __name__ == "__main__":
    """
    Questo blocco viene eseguito solo quando il file viene eseguito direttamente,
    non quando viene importato come modulo.
    """
    try:
        main()
    except KeyboardInterrupt:
        # Gestisce l'interruzione da tastiera (Ctrl+C)
        print("\n\n[!] Programma interrotto dall'utente.")
    except Exception as e:
        # Cattura altri errori imprevisti
        print(f"\n[!] Si e verificato un errore imprevisto: {e}")
        print("[*] Contatta il supporto tecnico se il problema persiste.")
    finally:
        # Messaggio di chiusura
        print("\n[*] Grazie per aver usato Expense Tracker!")
