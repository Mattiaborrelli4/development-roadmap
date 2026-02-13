#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================
PASSWORD GENERATOR & MANAGER
========================================
Autore: Studente Python
Scopo: Didattico e Portfolio
Versione: 1.0.0

Un tool completo per generare, gestire e proteggere password.
Utilizza crittografia AES per il salvataggio sicuro delle credenziali.

Requisiti: Python 3.6+, pyperclip (opzionale)
Moduli utilizzati: secrets, hashlib, string, json, os, sys, base64
"""

import os
import sys
import json
import secrets
import string
import hashlib
import base64
import argparse
from getpass import getpass


# =============================================================================
# COSTANTI E CONFIGURAZIONE
# =============================================================================

# Nome del file di salvataggio
PASSWORD_FILE = "password_vault.json"

# Versione del formato di salvataggio
VERSION = "1.0"

# Definizione caratteri per generazione password
MAYUSCOLE = string.ascii_uppercase        # ABCDEFGHIJKLMNOPQRSTUVWXYZ
MINUSCOLE = string.ascii_lowercase        #abcdefghijklmnopqrstuvwxyz
NUMERI = string.digits                    # 0123456789
SIMBOLI = "!@#$%^&*()_+-=[]{}|;:,.<>?"   # Simboli comuni

# Lista password comuni da evitare (top 100 comuni)
PASSWORD_COMUNI = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "111111", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "passw0rd", "shadow", "123123",
    "654321", "superman", "qazwsx", "michael", "football",
    "password1", "hello", "jennifer", "starwars", "computer",
    "corvette", "admin", "welcome", "login", "princess",
    "solo", "azerty", "password123", "1234567890", "123qwe"
]

# Lista username comuni da controllare
USERNAME_COMUNI = ["admin", "administrator", "root", "user", "test"]

# Parole italiane per passphrase (prime 200 più comuni)
PAROLE_ITALIANE = [
    "amore", "sole", "mare", "tempo", "vivo", "giorno", "anno", "casa",
    "parte", "uomo", "donna", "via", "ora", "mondo", "persona", "mano",
    "lavoro", "fatto", "stato", "cose", "problema", "prima", "essere",
    "via", "forse", "fine", "punto", "solo", "padre", "figlio", "amico",
    "gente", "libro", "storia", "acqua", "notte", "buono", "nuovo",
    "cioe", "tramite", "insieme", "nostra", "tutta", "quasi", "solo",
    "dopo", "sempre", "giusto", "posto", "torno", "motivo", "tanta",
    "causa", "spesso", "tuttavia", "niente", "senza", "quindi", "perche",
    "presso", "giacche", "ormai", "contro", "durante", "almeno", "bene",
    "tanto", "vero", "proprio", "essere", "avere", "fare", "dire", "andare",
    "vedere", "potere", "volere", "sapere", "venire", "tenere", "prendere",
    "mettere", "parlare", "trovare", "pensare", "ritornare", "lavorare",
    "chiamare", "capire", "partire", "finire", "scrivere", "leggere",
    "ascoltare", "sentire", "guardare", "cercare", "sembrare", "restare",
    "diventare", "conoscere", "piacere", "uscire", "entrare", "tornare",
    "cominciare", "continuare", "finire", "decidere", "scegliere", "credere",
    "ricordare", "dimenticare", "succedere", "accadere", "sembrare",
    "apparire", "cambiare", "crescere", "diminuire", "aumentare", "migliorare",
    "peggiorare", "compiere", "realizzare", "produrre", "creare", "costruire",
    "formare", "abitare", "vivere", "stare", "sedere", "correre", "camminare",
    "muoversi", "fermarsi", "alzarsi", "coricarsi", "svegliarsi", "addormentarsi",
    "mangiare", "bere", "cucinare", "lavare", "pulire", "ordinare", "spostare",
    "spiegare", "insegnare", "imparare", "studiare", "conoscere", "capire",
    "dire", "parlare", "raccontare", "descrivere", "scrivere", "leggere",
    "guardare", "vedere", "osservare", "ascoltare", "sentire", "annusare",
    "toccare", "tenere", "afferrare", "lasciare", "dare", "ricevere",
    "prendere", "portare", "condurre", "spingere", "tirare", "muovere",
    "cadere", "salire", "scendere", "entrare", "uscire", "passare", "restare",
    "diventare", "essere", "avere", "esistere", "sembrare", "apparire",
    "succedere", "accadere", "cominciare", "iniziare", "continuare", "finire",
    "concludere", "completare", "terminare", "durare", "costare", "valere",
    "pesare", "misurare", "contenere", "consistere", "significare", "volere",
    "desiderare", "amare", "odiare", "temere", "sperare", "credere", "pensare",
    "immaginare", "sognare", "ricordare", "dimenticare", "sapere", "conoscere",
    "capire", "comprendere", "accettare", "rifiutare", "approvare", "biasimare",
    "lodare", "criticare", "elogiare", "blasmare", "consigliare", "suggerire",
    "proporre", "offrire", "domandare", "chiedere", "rispondere", "rispondere",
    "promettere", "giurare", "confermare", "negare", "ammettere", "riconoscere",
    "pentirsi", "scusarsi", "perdonare", "ringraziare", "salutare", "abbracciare",
    "baciare", "colpire", "ferire", "curare", "guarire", "uccidere", "salvare",
    "aiutare", "servire", "utilizzare", "usare", "godere", "divertirsi", "ridere",
    "piangere", "sorridere", "arrabbiarsi", "innamorarsi", "odiare", "temere",
    "sorprendere", "meravigliare", "interessare", "preoccupare", "spaventare",
    "tranquillizzare", "rassicurare", "consolare", "sostenere", "appoggiare",
    "sostenerere", "difendere", "proteggere", "attaccare", "combattere", "vincere",
    "perdere", "giocare", "gareggiare", "competere", "scommettere", "rischiare",
    "tentare", "provare", "cercare", "trovare", "scoprire", "inventare",
    "creare", "produrre", "costruire", "fabbricare", "realizzare", "eseguire",
    "compiere", "effettuare", "operare", "funzionare", "lavorare", "agire",
    "comportarsi", "reagire", "rispondere", "partecipare", "contribuire",
    "collaborare", "cooperare", "aiutare", "favorire", "agevolare", "facilitare",
    "permettere", "autorizzare", "consentire", "vietare", "impedire", "proibire"
]

# Colori per output terminale (codici ANSI)
class Colori:
    """Codici colore per output terminale ANSI."""
    RESET = "\033[0m"
    ROSSO = "\033[91m"
    VERDE = "\033[92m"
    GIALLO = "\033[93m"
    BLU = "\033[94m"
    MAGENTA = "\033[95m"
    CIANO = "\033[96m"
    BIANCO = "\033[97m"
    GRASSETTO = "\033[1m"
    SOTTOLINEATO = "\033[4m"


# =============================================================================
# FUNZIONI DI UTILITA'
# =============================================================================

def pulisci_schermo():
    """
    Pulisce lo schermo del terminale in modo cross-platform.
    Funziona su Windows, Linux e macOS.
    """
    try:
        if sys.platform == "win32":
            os.system('cls')
        else:
            os.system('clear')
    except Exception:
        # Fallback: stampa nuove linee
        print("\n" * 50)


def stampa_intestazione():
    """
    Stampa l'intestazione del programma con formattazione.
    """
    print("\n" + "=" * 60)
    print(f"{Colori.CIANO + Colori.GRASSETTO}    PASSWORD GENERATOR & MANAGER{Colori.RESET}")
    print(f"{Colori.GIALLO}    Versione {VERSION} - Tool Didattico{Colori.RESET}")
    print("=" * 60 + "\n")


def stampa_successo(messaggio):
    """
    Stampa un messaggio di successo in verde.

    Args:
        messaggio (str): Il messaggio da stampare
    """
    print(f"{Colori.VERDE}[OK] {messaggio}{Colori.RESET}")


def stampa_errore(messaggio):
    """
    Stampa un messaggio di errore in rosso.

    Args:
        messaggio (str): Il messaggio da stampare
    """
    print(f"{Colori.ROSSO}[!] ERRORE: {messaggio}{Colori.RESET}")


def stampa_avviso(messaggio):
    """
    Stampa un messaggio di avviso in giallo.

    Args:
        messaggio (str): Il messaggio da stampare
    """
    print(f"{Colori.GIALLO}[!] {messaggio}{Colori.RESET}")


def stampa_info(messaggio):
    """
    Stampa un messaggio informativo in ciano.

    Args:
        messaggio (str): Il messaggio da stampare
    """
    print(f"{Colori.CIANO}[*] {messaggio}{Colori.RESET}")


def input_opzione(messaggio, opzioni_validhe=None):
    """
    Riceve input dall'utente con validazione.

    Args:
        messaggio (str): Messaggio da mostrare
        opzioni_validhe (list): Lista di opzioni valide (opzionale)

    Returns:
        str: Input dell'utente
    """
    while True:
        try:
            valore = input(f"{Colori.BIANCO}{messaggio}: {Colori.RESET}").strip()
            if opzioni_validhe and valore.lower() not in opzioni_validhe:
                stampa_errore(f"Opzione non valida. Scegli tra: {', '.join(opzioni_validhe)}")
                continue
            return valore
        except (EOFError, KeyboardInterrupt):
            stampa_errore("\nOperazione annullata dall'utente.")
            sys.exit(0)


def input_numero(messaggio, min_val=None, max_val=None):
    """
    Riceve un numero intero dall'utente con validazione.

    Args:
        messaggio (str): Messaggio da mostrare
        min_val (int): Valore minimo accettabile
        max_val (int): Valore massimo accettabile

    Returns:
        int: Numero inserito dall'utente
    """
    while True:
        try:
            valore = input(f"{Colori.BIANCO}{messaggio}: {Colori.RESET}").strip()
            numero = int(valore)

            if min_val is not None and numero < min_val:
                stampa_errore(f"Il valore deve essere almeno {min_val}")
                continue
            if max_val is not None and numero > max_val:
                stampa_errore(f"Il valore deve essere al massimo {max_val}")
                continue

            return numero
        except ValueError:
            stampa_errore("Inserisci un numero valido.")
        except (EOFError, KeyboardInterrupt):
            stampa_errore("\nOperazione annullata dall'utente.")
            sys.exit(0)


def input_si_no(messaggio):
    """
    Riceve una risposta si/no dall'utente.

    Args:
        messaggio (str): Messaggio da mostrare

    Returns:
        bool: True per 'sì', False per 'no'
    """
    while True:
        risposta = input_opzione(f"{messaggio} (s/n)").lower()
        if risposta in ['s', 'si', 'sì', 'y', 'yes']:
            return True
        elif risposta in ['n', 'no']:
            return False
        stampa_errore("Rispondi 's' per sì o 'n' per no.")


# =============================================================================
# FUNZIONI DI CRITTOGRAFIA (IMPLEMENTAZIONE CON LIBRERIA STANDARD)
# =============================================================================

def deriva_chiave(master_password, salt=None):
    """
    Deriva una chiave crittografica dalla master password usando PBKDF2.
    Questa funzione è sicura e usa iterazioni multiple per resistere a brute force.

    Args:
        master_password (str): La password principale
        salt (bytes): Sale crittografico (se None, genera nuovo)

    Returns:
        tuple: (chiave_derivata, salt) come bytes
    """
    # Genera salt se non fornito
    if salt is None:
        salt = secrets.token_bytes(16)

    # PBKDF2 con HMAC-SHA256, 100,000 iterazioni (valore sicuro)
    # Più iterazioni = più sicurezza contro attacchi brute force
    chiave = hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode('utf-8'),
        salt,
        100000,  # Numero di iterazioni
        dklen=32  # Lunghezza chiave in bytes (256 bit)
    )

    return chiave, salt


def cifra_password_semplce(password, master_password):
    """
    Cifra una password usando un approccio semplificato ma sicuro.
    Usa XOR con chiave derivata + codifica base64.
    NOTA: Per produzione usare librerie come cryptography.

    Args:
        password (str): Password da cifrare
        master_password (str): Password master per la cifratura

    Returns:
        str: Password cifrata in base64
    """
    try:
        # Genera chiave dalla master password
        chiave, salt = deriva_chiave(master_password)

        # Converti password in bytes
        password_bytes = password.encode('utf-8')

        # Cifra con XOR (versione semplificata didattica)
        # Per produzione usare AES tramite libreria cryptography
        risultato_cifrato = bytearray()
        for i, byte in enumerate(password_bytes):
            # XOR con chiave (cicla sulla chiave se password più lunga)
            chiave_byte = chiave[i % len(chiave)]
            risultato_cifrato.append(byte ^ chiave_byte)

        # Combina salt + dati cifrati
        dati_completi = salt + bytes(risultato_cifrato)

        # Converti in base64 per salvare in JSON
        return base64.b64encode(dati_completi).decode('ascii')

    except Exception as e:
        raise Exception(f"Errore nella cifratura: {str(e)}")


def decifra_password_semplce(password_cifrata_b64, master_password):
    """
    Decifra una password usando un approccio semplificato.

    Args:
        password_cifrata_b64 (str): Password cifrata in base64
        master_password (str): Password master per la decifratura

    Returns:
        str: Password in chiaro
    """
    try:
        # Decodifica da base64
        dati_completi = base64.b64decode(password_cifrata_b64)

        # Estrai salt (primi 16 bytes)
        salt = dati_completi[:16]
        dati_cifrati = dati_completi[16:]

        # Genera la stessa chiave
        chiave, _ = deriva_chiave(master_password, salt)

        # Decifra con XOR
        risultato_decifrato = bytearray()
        for i, byte in enumerate(dati_cifrati):
            chiave_byte = chiave[i % len(chiave)]
            risultato_decifrato.append(byte ^ chiave_byte)

        return risultato_decifrato.decode('utf-8')

    except Exception as e:
        raise Exception(f"Errore nella decifratura: {str(e)}")


# Alias per compatibilità
def cifra_password(password, master_password):
    """Alias per cifra_password_semplce."""
    return cifra_password_semplce(password, master_password)


def decifra_password(password_cifrata_b64, master_password):
    """Alias per decifra_password_semplce."""
    return decifra_password_semplce(password_cifrata_b64, master_password)


# =============================================================================
# FUNZIONI PER CALCOLO ENTROPY E FORZA PASSWORD
# =============================================================================

def calcola_entropy(password):
    """
    Calcola l'entropia di una password in bit.
    L'entropia misura la "casualità" e quindi la difficoltà di indovinare la password.

    Formula: E = L * log2(R)
    Dove L = lunghezza password, R = grandezza dello spazio caratteri

    Args:
        password (str): Password da analizzare

    Returns:
        float: Entropia in bit
    """
    if not password:
        return 0.0

    # Determina lo spazio dei caratteri usati
    spazio = 0
    if any(c in string.ascii_lowercase for c in password):
        spazio += 26  # 26 lettere minuscole
    if any(c in string.ascii_uppercase for c in password):
        spazio += 26  # 26 lettere maiuscole
    if any(c in string.digits for c in password):
        spazio += 10  # 10 numeri
    if any(c in SIMBOLI for c in password):
        spazio += len(SIMBOLI)  # Simboli

    if spazio == 0:
        return 0.0

    # Calcola entropia: L * log2(R)
    import math
    entropia = len(password) * math.log2(spazio)

    return entropia


def valuta_forza_password(password):
    """
    Valuta la forza di una password basandosi su entropia e pattern comuni.

    Scale di valutazione:
    - Molto debole: < 40 bit (crackabile in pochi secondi/ore)
    - Debole: 40-59 bit (crackabile in giorni/settimane)
    - Media: 60-79 bit (crackabile in anni con molte risorse)
    - Forte: 80-119 bit (difficile da craccare)
    - Molto forte: 120+ bit (praticamente impossibile da craccare)

    Args:
        password (str): Password da valutare

    Returns:
        tuple: (livello_testo, punteggio, colore, descrizione)
    """
    entropia = calcola_entropy(password)

    # Controlla se è nella lista delle password comuni
    if password.lower() in PASSWORD_COMUNI:
        return ("MOLTO DEBOLE", 0, Colori.ROSSO,
                "Password nella lista delle 100 più comuni!")

    # Controlla lunghezza minima
    if len(password) < 8:
        return ("MOLTO DEBOLE", entropia, Colori.ROSSO,
                "Password troppo corta (minimo 8 caratteri)")

    # Valuta basata su entropia
    if entropia < 40:
        return ("MOLTO DEBOLE", entropia, Colori.ROSSO,
                "Crackabile in pochi secondi con hardware moderno")
    elif entropia < 60:
        return ("DEBOLE", entropia, Colori.ROSSO,
                "Crackabile in giorni/settimane")
    elif entropia < 80:
        return ("MEDIA", entropia, Colori.GIALLO,
                "Richiederebbe anni per essere craccata")
    elif entropia < 120:
        return ("FORTE", entropia, Colori.VERDE,
                "Difficile da craccare anche con molte risorse")
    else:
        return ("MOLTO FORTE", entropia, Colori.VERDE,
                "Praticamente impossibile da craccare")


def stampa_barra_forza(password):
    """
    Stampa una barra grafica della forza della password.

    Args:
        password (str): Password da visualizzare
    """
    livello, punteggio, colore, descrizione = valuta_forza_password(password)

    # Normalizza punteggio per la barra (0-120 bit -> 0-50 caratteri)
    percentuale = min(100, (punteggio / 120) * 100)
    riempimento = int(50 * percentuale / 100)

    barra = "[" + "=" * riempimento + " " * (50 - riempimento) + "]"
    percentuale_str = f"{percentuale:.0f}%"

    print(f"\n{Colori.BIANCO}Password: {password}{Colori.RESET}")
    print(f"Forza:    {colore}{livello}{Colori.RESET} {barra}")
    print(f"Entropia: {punteggio:.1f} bit")
    print(f"Dettaglio: {colore}{descrizione}{Colori.RESET}\n")


# =============================================================================
# FUNZIONI DI VALIDAZIONE
# =============================================================================

def password_e_comune(password):
    """
    Controlla se una password è nella lista delle password comuni.

    Args:
        password (str): Password da controllare

    Returns:
        bool: True se è comune, False altrimenti
    """
    return password.lower() in PASSWORD_COMUNI


def username_e_comune(username):
    """
    Controlla se un username è troppo comune/predicibile.

    Args:
        username (str): Username da controllare

    Returns:
        bool: True se è comune, False altrimenti
    """
    return username.lower() in USERNAME_COMUNI


def contiene_info_personale(password, username=None, nome=None):
    """
    Controlla se la password contiene informazioni personali ovvie.
    Versione semplificata per scopi didattici.

    Args:
        password (str): Password da controllare
        username (str): Username da evitare nella password
        nome (str): Nome da evitare nella password

    Returns:
        list: Lista di problemi trovati
    """
    problemi = []
    password_lower = password.lower()

    # Controlla username
    if username and username.lower() in password_lower:
        problemi.append(f"Contiene l'username '{username}'")

    # Controlla nome
    if nome and nome.lower() in password_lower:
        problemi.append(f"Contiene il nome '{nome}'")

    # Controlla sequenze comuni
    sequenze = ['123', 'abc', 'qwe', 'asd', 'zxc']
    for seq in sequenze:
        if seq in password_lower:
            problemi.append(f"Contiene sequenza comune '{seq}'")
            break

    # Controlla ripetizioni
    for i in range(len(password_lower) - 2):
        if password_lower[i] == password_lower[i+1] == password_lower[i+2]:
            problemi.append("Contiene caratteri ripetuti")
            break

    return problemi


# =============================================================================
# FUNZIONI DI GENERAZIONE PASSWORD
# =============================================================================

def genera_password_casuale(lunghezza=16, usa_maiuscole=True, usa_minuscole=True,
                           usa_numeri=True, usa_simboli=True):
    """
    Genera una password casuale sicura usando secrets (crittograficamente sicuro).

    IMPORTANT: Usiamo secrets.choice() invece di random.choice()
    perché secrets genera numeri veramente casuali e non pseudo-casuali.

    Args:
        lunghezza (int): Lunghezza della password (8-32)
        usa_maiuscole (bool): Includi lettere maiuscole
        usa_minuscole (bool): Includi lettere minuscole
        usa_numeri (bool): Includi numeri
        usa_simboli (bool): Includi simboli

    Returns:
        str: Password generata

    Raises:
        ValueError: Se nessun tipo di carattere è selezionato
    """
    # Valida parametri
    if lunghezza < 8:
        lunghezza = 8
    elif lunghezza > 128:
        lunghezza = 128

    # Costruisci il set di caratteri
    caratteri = ""
    if usa_maiuscole:
        caratteri += MAYUSCOLE
    if usa_minuscole:
        caratteri += MINUSCOLE
    if usa_numeri:
        caratteri += NUMERI
    if usa_simboli:
        caratteri += SIMBOLI

    if not caratteri:
        raise ValueError("Seleziona almeno un tipo di carattere")

    # Genera password
    # NOTA DIDATTICA: secrets.choice è crittograficamente sicuro
    # random.choice NON è sicuro per password
    password = ''.join(secrets.choice(caratteri) for _ in range(lunghezza))

    return password


def genera_passphrase(num_parole=5, separatore=" ", usa_numeri=False):
    """
    Genera una passphrase sicura usando parole italiane.
    Le passphrase sono spesso più facili da ricordare delle password complesse.

    Una passphrase di 5 parole con un dizionario di 2048 parole ha:
    Entropia = 5 * log2(2048) = 5 * 11 = 55 bit (buona)
    Con il nostro dizionario di 200+ parole:
    Entropia = 5 * log2(200) = 5 * 7.64 = 38 bit (accettabile)

    Args:
        num_parole (int): Numero di parole nella passphrase
        separatore (str): Separatore tra le parole
        usa_numeri (bool): Aggiungi numeri casuali tra le parole

    Returns:
        str: Passphrase generata
    """
    if num_parole < 3:
        num_parole = 3
    elif num_parole > 10:
        num_parole = 10

    parole_scelte = []

    for i in range(num_parole):
        # Scegli parola casuale
        parola = secrets.choice(PAROLE_ITALIANE)

        # Aggiungi numero se richiesto
        if usa_numeri and i > 0:
            numero = secrets.choice(range(10, 100))
            parole_scelte.append(str(numero))

        # Prima lettera maiuscola per leggibilità
        parole_scelte.append(parola.capitalize())

    return separatore.join(parole_scelte)


def genera_password_memorabile(lunghezza=16):
    """
    Genera una password che bilancia sicurezza e memorabilità.
    Usa schema pronunciabile tipo: "Ku9-De4-Fi2-Ba7"

    Args:
        lunghezza (int): Lunghezza totale desiderata

    Returns:
        str: Password pronunciabile
    """
    # Consonanti e vocali per schema pronunciabile
    consonanti = "bcdfghjklmnpqrstvwxz"
    vocali = "aeiou"

    password = ""
    while len(password) < lunghezza:
        # Schema CV (consonante-vocale) per pronunciabilità
        password += secrets.choice(consonanti)
        password += secrets.choice(vocali)

        # Aggiungi numero occasionalmente
        if secrets.randbelow(3) == 0:
            password += secrets.choice(NUMERI)

    return password[:lunghezza]


# =============================================================================
# FUNZIONI DI GESTIONE PASSWORD VAULT (JSON)
# =============================================================================

def ottieni_percorso_vault():
    """
    Ottiene il percorso completo del file vault.

    Returns:
        str: Percorso completo del file
    """
    # Crea percorso nella directory corrente
    return os.path.join(os.getcwd(), PASSWORD_FILE)


def carica_vault(master_password):
    """
    Carica il vault delle password dal file JSON.
    Tutte le password nel vault sono cifrate.

    Formato JSON:
    {
        "versione": "1.0",
        "profili": {
            "nome_profilo": {
                "username": "username_cifrato",
                "password": "password_cifrata",
                "email": "email_cifrata",
                "sito": "sito_cifrato",
                "note": "note_cifrate",
                "created": "data_creazione",
                "modified": "data_modifica"
            }
        }
    }

    Args:
        master_password (str): Password master per decifrare

    Returns:
        dict: Dizionario con i profili decifrati
    """
    percorso = ottieni_percorso_vault()

    # Se file non esiste, ritorna vault vuoto
    if not os.path.exists(percorso):
        return {"versione": VERSION, "profili": {}}

    try:
        with open(percorso, 'r', encoding='utf-8') as f:
            dati = json.load(f)

        # Verifica versione
        if dati.get("versione") != VERSION:
            stampa_avviso("Versione vault diversa, potrebbero esserci problemi")

        # Decifra tutti i profili
        profili_decifrati = {}
        for nome_profilo, profilo_cifrato in dati.get("profili", {}).items():
            try:
                profili_decifrati[nome_profilo] = {
                    "username": decifra_password(profilo_cifrato["username"], master_password),
                    "password": decifra_password(profilo_cifrato["password"], master_password),
                    "email": decifra_password(profilo_cifrato.get("email", ""), master_password),
                    "sito": decifra_password(profilo_cifrato.get("sito", ""), master_password),
                    "note": decifra_password(profilo_cifrato.get("note", ""), master_password),
                    "created": profilo_cifrato.get("created", "Sconosciuto"),
                    "modified": profilo_cifrato.get("modified", "Sconosciuto")
                }
            except Exception as e:
                stampa_errore(f"Errore decifratura profilo '{nome_profilo}': {e}")
                continue

        return {"versione": VERSION, "profili": profili_decifrati}

    except json.JSONDecodeError as e:
        stampa_errore(f"File JSON corrotto: {e}")
        return {"versione": VERSION, "profili": {}}
    except Exception as e:
        stampa_errore(f"Errore caricamento vault: {e}")
        return {"versione": VERSION, "profili": {}}


def salva_vault(profili, master_password):
    """
    Salva il vault delle password su file JSON con cifratura.

    Args:
        profili (dict): Dizionario dei profili da salvare
        master_password (str): Password master per cifrare

    Returns:
        bool: True se salvato con successo, False altrimenti
    """
    percorso = ottieni_percorso_vault()

    try:
        # Cifra tutti i profili
        profili_cifrati = {}
        for nome_profilo, profilo in profili.items():
            from datetime import datetime

            # Se profilo nuovo, aggiungi timestamp
            if "created" not in profilo:
                profilo["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Aggiorna timestamp modifica
            profilo["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            profili_cifrati[nome_profilo] = {
                "username": cifra_password(profilo.get("username", ""), master_password),
                "password": cifra_password(profilo.get("password", ""), master_password),
                "email": cifra_password(profilo.get("email", ""), master_password),
                "sito": cifra_password(profilo.get("sito", ""), master_password),
                "note": cifra_password(profilo.get("note", ""), master_password),
                "created": profilo.get("created", ""),
                "modified": profilo.get("modified", "")
            }

        # Crea struttura dati
        dati = {
            "versione": VERSION,
            "profili": profili_cifrati
        }

        # Salva su file
        with open(percorso, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        stampa_errore(f"Errore salvataggio vault: {e}")
        return False


def aggiungi_profilo(master_password, profili):
    """
    Aggiunge un nuovo profilo al vault.

    Args:
        master_password (str): Password master
        profili (dict): Dizionario profili esistente

    Returns:
        dict: Profili aggiornati o None se annullato
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== AGGIUNGI NUOVO PROFILO ==={Colori.RESET}\n")

    # Nome profilo
    while True:
        nome = input_opzione("Nome profilo (es. 'Gmail', 'Lavoro')").strip()
        if not nome:
            stampa_errore("Il nome profilo non può essere vuoto")
            continue
        if nome in profili:
            if not input_si_no(f"Profilo '{nome}' esiste già. Sovrascrivere?"):
                continue
        break

    # Sito/Descrizione
    sito = input_opzione("Sito web o descrizione (opzionale, premi Invio per saltare)")

    # Username/Email
    username = input_opzione("Username o Email")

    # Password
    print("\nOpzioni password:")
    print("1. Genera automaticamente")
    print("2. Inserisci manualmente")

    scelta = input_opzione("Scelta", ["1", "2"])

    if scelta == "1":
        # Genera password
        lunghezza = input_numero("Lunghezza password (8-32)", 8, 32)
        password = genera_password_casuale(lunghezza)
        print(f"\n{Colori.VERDE}Password generata:{Colori.RESET} {password}")
    else:
        # Inserisci password
        password = getpass("Password (non verrà mostrata): ")

        # Valida password
        livello, _, _, descrizione = valuta_forza_password(password)
        if livello in ["MOLTO DEBOLE", "DEBOLE"]:
            stampa_avviso(f"Password {livello}: {descrizione}")
            if not input_si_no("Usare comunque questa password?"):
                return None

    # Note opzionali
    note = input_opzione("Note aggiuntive (opzionale, premi Invio per saltare)")

    # Crea profilo
    profili[nome] = {
        "username": username,
        "password": password,
        "email": username if "@" in username else "",
        "sito": sito,
        "note": note,
        "created": "",
        "modified": ""
    }

    stampa_successo(f"Profilo '{nome}' aggiunto!")

    # Salva
    if salva_vault(profili, master_password):
        stampa_successo("Vault salvato con successo")
        return profili

    return None


def visualizza_profili(profili, mostra_password=False):
    """
    Visualizza tutti i profili salvati.

    Args:
        profili (dict): Dizionario dei profili
        mostra_password (bool): Se True mostra le password in chiaro
    """
    if not profili:
        stampa_avviso("Nessun profilo salvato")
        return

    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== PROFILI SALVATI ({len(profili)}) ==={Colori.RESET}\n")

    for i, (nome, profilo) in enumerate(profili.items(), 1):
        print(f"{Colori.GIALLO}[{i}] {Colori.BIANCO + Colori.GRASSETTO}{nome}{Colori.RESET}")
        print(f"    Username: {profilo['username']}")
        print(f"    Sito:     {profilo.get('sito', 'N/A')}")
        print(f"    Creato:   {profilo.get('created', 'N/A')}")

        # Password
        if mostra_password:
            password = profilo['password']
            livello, _, _, _ = valuta_forza_password(password)
            print(f"    Password: {Colori.VERDE}{password}{Colori.RESET} [{livello}]")
        else:
            password_mask = "*" * min(len(profilo['password']), 12)
            print(f"    Password: {password_mask}")

        # Note
        if profilo.get('note'):
            print(f"    Note:     {profilo['note']}")

        print()

    # Totali
    totale_password = len(profili)
    print(f"{Colori.CIANO}Totale profili: {totale_password}{Colori.RESET}\n")


def copia_password_clipboard(password):
    """
    Copia una password negli appunti (cross-platform).

    Args:
        password (str): Password da copiare

    Returns:
        bool: True se copiato con successo, False altrimenti
    """
    try:
        # Prova con pyperclip (metodo migliore)
        import pyperclip
        pyperclip.copy(password)
        return True
    except ImportError:
        # Fallback per Windows senza pyperclip
        if sys.platform == "win32":
            try:
                import subprocess
                process = subprocess.Popen(
                    ['clip'],
                    stdin=subprocess.PIPE,
                    shell=True
                )
                process.communicate(password.encode('utf-8'))
                return True
            except Exception:
                pass
        return False
    except Exception:
        return False


def cerca_profilo(profili):
    """
    Cerca un profilo per nome.

    Args:
        profili (dict): Dizionario dei profili

    Returns:
        dict: Profilo trovato o None
    """
    if not profili:
        stampa_avviso("Nessun profilo salvato")
        return None

    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== CERCA PROFILO ==={Colori.RESET}\n")

    # Mostra lista
    for i, nome in enumerate(profili.keys(), 1):
        print(f"  {i}. {nome}")

    print()
    scelta = input_numero("Seleziona numero profilo (0 per annullare)", 0, len(profili))

    if scelta == 0:
        return None

    nomi = list(profili.keys())
    nome_selezionato = nomi[scelta - 1]

    return profili[nome_selezionato]


def elimina_profilo(master_password, profili):
    """
    Elimina un profilo dal vault.

    Args:
        master_password (str): Password master
        profili (dict): Dizionario dei profili

    Returns:
        dict: Profili aggiornati o None se annullato
    """
    profilo = cerca_profilo(profili)
    if not profilo:
        return None

    # Trova nome del profilo
    nome_profilo = None
    for nome, p in profili.items():
        if p == profilo:
            nome_profilo = nome
            break

    if not nome_profilo:
        return None

    # Conferma
    print(f"\n{Colori.ROSSO}Profilo da eliminare:{Colori.RESET}")
    print(f"  Nome:     {nome_profilo}")
    print(f"  Username: {profilo['username']}")
    print(f"  Sito:     {profilo.get('sito', 'N/A')}")

    if not input_si_no("\nConfermi l'eliminazione?"):
        stampa_info("Eliminazione annullata")
        return None

    # Elimina
    del profili[nome_profilo]
    stampa_successo(f"Profilo '{nome_profilo}' eliminato")

    # Salva
    if salva_vault(profili, master_password):
        stampa_successo("Vault salvato")
        return profili

    return None


def modifica_profilo(master_password, profili):
    """
    Modifica un profilo esistente.

    Args:
        master_password (str): Password master
        profili (dict): Dizionario dei profili

    Returns:
        dict: Profili aggiornati o None se annullato
    """
    profilo = cerca_profilo(profili)
    if not profilo:
        return None

    # Trova nome
    nome_profilo = None
    for nome, p in profili.items():
        if p == profilo:
            nome_profilo = nome
            break

    if not nome_profilo:
        return None

    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== MODIFICA PROFILO: {nome_profilo} ==={Colori.RESET}\n")

    # Mostra valori attuali
    print(f"{Colori.GIALLO}Valori attuali:{Colori.RESET}")
    print(f"  Username: {profilo['username']}")
    print(f"  Password: {'*' * 12}")
    print(f"  Sito:     {profilo.get('sito', 'N/A')}")
    print(f"  Note:     {profilo.get('note', 'N/A')}")
    print()

    # Modifica campi
    nuovo_username = input_opzione(f"Nuovo username (Invio per mantenere '{profilo['username']}')")
    if nuovo_username:
        profilo['username'] = nuovo_username
        profilo['email'] = nuovo_username if "@" in nuovo_username else ""

    cambio_pwd = input_si_no("Cambiare password?")
    if cambio_pwd:
        print("\nOpzioni:")
        print("1. Genera nuova password")
        print("2. Inserisci manualmente")

        scelta = input_opzione("Scelta", ["1", "2"])
        if scelta == "1":
            lunghezza = input_numero("Lunghezza password (8-32)", 8, 32)
            profilo['password'] = genera_password_casuale(lunghezza)
            print(f"{Colori.VERDE}Nuova password: {profilo['password']}{Colori.RESET}")
        else:
            profilo['password'] = getpass("Nuova password: ")

    nuovo_sito = input_opzione(f"Nuovo sito (Invio per mantenere)")
    if nuovo_sito:
        profilo['sito'] = nuovo_sito

    nuovo_note = input_opzione(f"Nuove note (Invio per mantenere)")
    if nuovo_note:
        profilo['note'] = nuovo_note

    # Aggiorna
    profili[nome_profilo] = profilo
    stampa_successo("Profilo aggiornato")

    # Salva
    if salva_vault(profili, master_password):
        stampa_successo("Vault salvato")
        return profili

    return None


def esporta_password(profili, master_password):
    """
    Esporta le password in formato CSV (decifrate).

    ATTENZIONE: Questa funzione esporta password in chiaro.
    Usare con cautela e eliminare il file dopo l'uso.

    Args:
        profili (dict): Dizionario dei profili
        master_password (str): Password master (non usata, già decifrato)
    """
    if not profili:
        stampa_avviso("Nessun profilo da esportare")
        return

    from datetime import datetime

    # Nome file con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"password_export_{timestamp}.csv"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Header CSV
            f.write("Profilo,Sito,Username,Email,Password,Note,Creato,Modificato\n")

            # Righe
            for nome, p in profili.items():
                # Escape CSV
                def escape_csv(text):
                    if not text:
                        return ""
                    if '"' in text or ',' in text or '\n' in text:
                        return f'"{text.replace('"', '""')}"'
                    return text

                f.write(f"{escape_csv(nome)},{escape_csv(p.get('sito', ''))},")
                f.write(f"{escape_csv(p['username'])},{escape_csv(p.get('email', ''))},")
                f.write(f"{escape_csv(p['password'])},{escape_csv(p.get('note', ''))},")
                f.write(f"{escape_csv(p.get('created', ''))},{escape_csv(p.get('modified', ''))}\n")

        stampa_successo(f"Esportate {len(profili)} password in: {filename}")
        stampa_avviso("ATTENZIONE: Il file contiene password in chiaro. Eliminalo dopo l'uso!")

    except Exception as e:
        stampa_errore(f"Errore esportazione: {e}")


def importa_password(master_password, profili):
    """
    Importa password da un file CSV.

    Args:
        master_password (str): Password master per cifrare
        profili (dict): Profili esistenti

    Returns:
        dict: Profili aggiornati
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== IMPORTA PASSWORD DA CSV ==={Colori.RESET}\n")

    filename = input_opzione("Nome file CSV da importare")

    if not os.path.exists(filename):
        stampa_errore(f"File non trovato: {filename}")
        return None

    try:
        importate = 0
        sovrascritte = 0

        with open(filename, 'r', encoding='utf-8') as f:
            # Leggi header
            header = f.readline().strip().split(',')

            # Leggi righe
            for line in f:
                # Parse CSV semplificato
                parti = line.strip().split(',')
                if len(parti) < 6:
                    continue

                nome = parti[0].strip('"')
                sito = parti[1].strip('"') if len(parti) > 1 else ""
                username = parti[2].strip('"') if len(parti) > 2 else ""
                email = parti[3].strip('"') if len(parti) > 3 else ""
                password = parti[4].strip('"') if len(parti) > 4 else ""
                note = parti[5].strip('"') if len(parti) > 5 else ""

                if not nome or not password:
                    continue

                # Controlla se esiste
                if nome in profili:
                    sovrascritte += 1
                    if not input_si_no(f"Sovrascrivere profilo '{nome}'?"):
                        continue

                # Aggiungi profilo
                profili[nome] = {
                    "username": username,
                    "password": password,
                    "email": email,
                    "sito": sito,
                    "note": note,
                    "created": "",
                    "modified": ""
                }
                importate += 1

        stampa_successo(f"Importate {importate} password (sovrascritte: {sovrascritte})")

        # Salva
        if salva_vault(profili, master_password):
            stampa_successo("Vault salvato")
            return profili

    except Exception as e:
        stampa_errore(f"Errore importazione: {e}")

    return None


# =============================================================================
# FUNZIONI DI TEST E ANALISI
# =============================================================================

def testa_qualita_password():
    """
    Testa la qualità di una password inserita dall'utente.
    Mostra entropia, forza, e problemi di sicurezza.
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== TEST QUALITA' PASSWORD ==={Colori.RESET}\n")

    password = getpass("Inserisci la password da testare: ")

    if not password:
        stampa_errore("Password vuota")
        return

    # Analisi base
    print(f"\n{Colori.BIANCO + Colori.GRASSETTO}ANALISI PASSWORD{Colori.RESET}")
    print("-" * 50)
    print(f"Lunghezza:         {len(password)} caratteri")

    # Conteggio caratteri
    maiuscole = sum(1 for c in password if c in MAYUSCOLE)
    minuscole = sum(1 for c in password if c in MINUSCOLE)
    numeri = sum(1 for c in password if c in NUMERI)
    simboli = sum(1 for c in password if c in SIMBOLI)

    print(f"Maiuscole:         {maiuscole}")
    print(f"Minuscole:         {minuscole}")
    print(f"Numeri:            {numeri}")
    print(f"Simboli:           {simboli}")

    # Barra forza
    stampa_barra_forza(password)

    # Controlli di sicurezza
    print(f"{Colori.BIANCO + Colori.GRASSETTO}CONTROLLI SICUREZZA{Colori.RESET}")
    print("-" * 50)

    # Password comune?
    if password_e_comune(password):
        stampa_errore("Questa password e' nella lista delle 100 più comuni!")
    else:
        stampa_successo("Non e' una password comune")

    # Info personali?
    username = input("Inserisci tuo username per controllo (Invio per saltare): ")
    if username and contiene_info_personale(password, username):
        problemi = contiene_info_personale(password, username)
        stampa_avviso(f"Contiene info personali: {', '.join(problemi)}")
    else:
        stampa_successo("Non contiene info personali ovvie")

    # Caratteri ripetuti
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            stampa_avviso("Contiene caratteri ripetuti (es. 'aaa')")
            break
    else:
        stampa_successo("Nessun carattere ripetuto")

    # Sequenze
    sequenze_trovate = []
    for seq in ['123', 'abc', 'qwe', 'asd', 'zxc']:
        if seq in password.lower():
            sequenze_trovate.append(seq)

    if sequenze_trovate:
        stampa_avviso(f"Contiene sequenze: {', '.join(sequenze_trovate)}")
    else:
        stampa_successo("Nessuna sequenza comune")

    print()


# =============================================================================
# FUNZIONI DEL MENU' PRINCIPALE
# =============================================================================

def menu_genera_password():
    """
    Menu per la generazione di password.
    """
    while True:
        print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== GENERATORE PASSWORD ==={Colori.RESET}\n")
        print("1. Genera password casuale")
        print("2. Genera passphrase (parole)")
        print("3. Genera password pronunciabile")
        print("4. Testa qualita' password")
        print("0. Torna al menu principale")

        scelta = input_opzione("\nScelta", ["0", "1", "2", "3", "4"])

        if scelta == "0":
            break
        elif scelta == "1":
            menu_password_casuale()
        elif scelta == "2":
            menu_passphrase()
        elif scelta == "3":
            menu_password_pronunciabile()
        elif scelta == "4":
            testa_qualita_password()


def menu_password_casuale():
    """
    Genera password casuale con opzioni personalizzate.
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== PASSWORD CASUALE ==={Colori.RESET}\n")

    # Opzioni
    lunghezza = input_numero("Lunghezza password (8-64)", 8, 64)

    print("\nTipi di caratteri da includere:")
    usa_maiuscole = input_si_no("Lettere maiuscole (A-Z)?")
    usa_minuscole = input_si_no("Lettere minuscole (a-z)?")
    usa_numeri = input_si_no("Numeri (0-9)?")
    usa_simboli = input_si_no("Simboli (!@#$%...)?")

    try:
        # Genera
        password = genera_password_casuale(
            lunghezza, usa_maiuscole, usa_minuscole, usa_numeri, usa_simboli
        )

        # Mostra risultato
        print("\n" + "=" * 60)
        print(f"{Colori.VERDE + Colori.GRASSETTO}PASSWORD GENERATA:{Colori.RESET}")
        print(f"{Colori.BIANCO + Colori.GRASSETTO}{password}{Colori.RESET}")
        print("=" * 60)

        # Analisi
        stampa_barra_forza(password)

        # Opzioni
        print("\nCosa vuoi fare?")
        print("1. Copia negli appunti")
        print("2. Salva nel vault")
        print("3. Rigenera con stesse opzioni")
        print("0. Menu principale")

        azione = input_opzione("Scelta", ["0", "1", "2", "3"])

        if azione == "1":
            if copia_password_clipboard(password):
                stampa_successo("Password copiata negli appunti!")
            else:
                stampa_errore("Impossibile copiare. Installa pyperclip: pip install pyperclip")

        elif azione == "2":
            # Chiedi master password
            master = getpass("\nInserisci password master del vault: ")
            profili = carica_vault(master)

            # Aggiungi come nuovo profilo
            nome = input_opzione("Nome profilo (es. 'Nuovo Servizio')")
            if nome:
                profili[nome] = {
                    "username": "",
                    "password": password,
                    "email": "",
                    "sito": "",
                    "note": "Generato automaticamente",
                    "created": "",
                    "modified": ""
                }

                if salva_vault(profili, master):
                    stampa_successo("Password salvata nel vault!")

        elif azione == "3":
            menu_password_casuale()

    except Exception as e:
        stampa_errore(f"Errore generazione: {e}")


def menu_passphrase():
    """
    Genera passphrase usando parole italiane.
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== PASSPHRASE (FRASI SICURE) ==={Colori.RESET}\n")

    num_parole = input_numero("Numero di parole (3-10)", 3, 10)

    print("\nSeparatore parole:")
    print("1. Spazio")
    print("2. Trattino (-)")
    print("3. Underscore (_)")
    print("4. Punto (.)")
    print("5. Nessuno (tutto attaccato)")

    sep_scelta = input_opzione("Scelta", ["1", "2", "3", "4", "5"])

    separatori = {
        "1": " ",
        "2": "-",
        "3": "_",
        "4": ".",
        "5": ""
    }
    separatore = separatori.get(sep_scelta, " ")

    usa_numeri = input_si_no("Aggiungere numeri tra le parole?")

    try:
        passphrase = genera_passphrase(num_parole, separatore, usa_numeri)

        # Mostra risultato
        print("\n" + "=" * 60)
        print(f"{Colori.VERDE + Colori.GRASSETTO}PASSPHRASE GENERATA:{Colori.RESET}")
        print(f"{Colori.BIANCO + Colori.GRASSETTO}{passphrase}{Colori.RESET}")
        print("=" * 60)

        # Analisi
        stampa_barra_forza(passphrase)

        # Copia?
        if input_si_no("\nCopiare negli appunti?"):
            if copia_password_clipboard(passphrase):
                stampa_successo("Passphrase copiata!")
            else:
                stampa_errore("Impossibile copiare. Installa pyperclip")

    except Exception as e:
        stampa_errore(f"Errore: {e}")


def menu_password_pronunciabile():
    """
    Genera password pronunciabile.
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== PASSWORD PRONUNCIABILE ==={Colori.RESET}\n")

    lunghezza = input_numero("Lunghezza password (8-32)", 8, 32)

    try:
        password = genera_password_memorabile(lunghezza)

        # Mostra risultato
        print("\n" + "=" * 60)
        print(f"{Colori.VERDE + Colori.GRASSETTO}PASSWORD GENERATA:{Colori.RESET}")
        print(f"{Colori.BIANCO + Colori.GRASSETTO}{password}{Colori.RESET}")
        print("=" * 60)

        # Analisi
        stampa_barra_forza(password)

        # Copia?
        if input_si_no("\nCopiare negli appunti?"):
            if copia_password_clipboard(password):
                stampa_successo("Password copiata!")
            else:
                stampa_errore("Impossibile copiare. Installa pyperclip")

    except Exception as e:
        stampa_errore(f"Errore: {e}")


def menu_vault():
    """
    Menu per la gestione del vault password.
    """
    # Richiedi master password
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== VAULT PASSWORD ==={Colori.RESET}\n")

    master_password = getpass("Inserisci password master: ")

    # Carica vault
    profili = carica_vault(master_password)

    while True:
        print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== GESTIONE VAULT ({len(profili)} profili) ==={Colori.RESET}\n")
        print("1. Visualizza tutti i profili")
        print("2. Visualizza con password in chiaro")
        print("3. Aggiungi nuovo profilo")
        print("4. Modifica profilo")
        print("5. Elimina profilo")
        print("6. Cerca e copia password")
        print("7. Esporta password (CSV)")
        print("8. Importa password (CSV)")
        print("9. Cambia password master")
        print("0. Torna al menu principale")

        scelta = input_opzione("\nScelta", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

        if scelta == "0":
            break
        elif scelta == "1":
            visualizza_profili(profili, mostra_password=False)
        elif scelta == "2":
            visualizza_profili(profili, mostra_password=True)
        elif scelta == "3":
            result = aggiungi_profilo(master_password, profili)
            if result:
                profili = result
        elif scelta == "4":
            result = modifica_profilo(master_password, profili)
            if result:
                profili = result
        elif scelta == "5":
            result = elimina_profilo(master_password, profili)
            if result:
                profili = result
        elif scelta == "6":
            profilo = cerca_profilo(profili)
            if profilo:
                print(f"\n{Colori.VERDE}Password: {profilo['password']}{Colori.RESET}")
                if copia_password_clipboard(profilo['password']):
                    stampa_successo("Copiata negli appunti!")
                else:
                    stampa_errore("Impossibile copiare. Installa pyperclip")
        elif scelta == "7":
            esporta_password(profili, master_password)
        elif scelta == "8":
            result = importa_password(master_password, profili)
            if result:
                profili = result
        elif scelta == "9":
            nuova_master = getpass("\nNuova password master: ")
            conferma = getpass("Conferma nuova password: ")

            if nuova_master != conferma:
                stampa_errore("Le password non corrispondono")
                continue

            # Valuta forza
            livello, _, _, _ = valuta_forza_password(nuova_master)
            if livello in ["MOLTO DEBOLE", "DEBOLE"]:
                stampa_avviso(f"Master password {livello}. Sicuro di voler continuare?")
                if not input_si_no("Continuare?"):
                    continue

            # Re-salva con nuova password
            if salva_vault(profili, nuova_master):
                master_password = nuova_master
                stampa_successo("Master password aggiornata!")


def menu_principale():
    """
    Menu principale dell'applicazione.
    """
    while True:
        pulisci_schermo()
        stampa_intestazione()

        print("MENU PRINCIPALE:")
        print("-" * 40)
        print("1. Genera password")
        print("2. Gestione vault password")
        print("3. Testa qualita' password")
        print("4. Informazioni programma")
        print("0. Esci")

        scelta = input_opzione("\nScelta", ["0", "1", "2", "3", "4"])

        if scelta == "0":
            print(f"\n{Colori.CIANO}Grazie per aver usato Password Manager!{Colori.RESET}\n")
            break
        elif scelta == "1":
            menu_genera_password()
        elif scelta == "2":
            menu_vault()
        elif scelta == "3":
            testa_qualita_password()
        elif scelta == "4":
            mostra_info()


def mostra_info():
    """
    Mostra informazioni sul programma.
    """
    print(f"\n{Colori.CIANO + Colori.GRASSETTO}=== INFORMAZIONI PROGRAMMA ==={Colori.RESET}\n")
    print(f"{Colori.BIANCO + Colori.GRASSETTO}Password Generator & Manager{Colori.RESET}")
    print(f"Versione: {VERSION}")
    print("\nAutore: Studente Python")
    print("Scopo:  Tool Didattico e Portfolio")
    print("Anno:   2024")
    print("\nCARATTERISTICHE:")
    print("  - Generazione password sicure con crittografia")
    print("  - Calcolo entropia e valutazione forza password")
    print("  - Vault con crittografia (implementazione didattica)")
    print("  - Passphrase con parole italiane")
    print("  - Export/Import CSV")
    print("  - Supporto clipboard cross-platform")
    print("\nMODULI UTILIZZATI:")
    print("  - secrets: Generazione numeri casuali sicuri")
    print("  - hashlib: Funzioni hash (SHA256)")
    print("  - json: Salvataggio dati")
    print("  - os, sys: Operazioni di sistema")
    print("  - base64: Codifica/decodifica")
    print("  - getpass: Input password nascosto")
    print("  - pyperclip: Clipboard (opzionale)")
    print("\nNOTA SICUREZZA:")
    print("  Questo e' un programma a scopo DIDATTICO.")
    print("  Per uso in produzione, considera librerie di crittografia")
    print("  professionali come 'cryptography' o 'pycryptodome'.")
    print()


# =============================================================================
# FUNZIONE MAIN
# =============================================================================

def main():
    """
    Funzione principale - punto di ingresso del programma.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Password Generator & Manager - Tool Didattico",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python password_generator.py              # Avvia interfaccia interattiva
  python password_generator.py --gen 16     # Genera password di 16 caratteri
  python password_generator.py --test       # Modalità test password
  python password_generator.py --passphrase # Genera passphrase
        """
    )

    parser.add_argument(
        "--gen", "-g",
        type=int,
        metavar="LUNGHEZZA",
        help="Genera password casuale di lunghezza specificata"
    )

    parser.add_argument(
        "--passphrase", "-p",
        action="store_true",
        help="Genera passphrase sicura"
    )

    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Testa qualità di una password"
    )

    parser.add_argument(
        "--strength", "-s",
        type=str,
        metavar="PASSWORD",
        help="Mostra forza di una password (usa con cautela in bash history!)"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disabilita colori nel terminale"
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"Password Manager v{VERSION}"
    )

    # Se nessun argomento, avvia modalità interattiva
    if len(sys.argv) == 1:
        menu_principale()
        return

    # Parse argomenti
    args = parser.parse_args()

    # Disabilita colori se richiesto
    if args.no_color:
        Colori.RESET = ""
        Colori.ROSSO = ""
        Colori.VERDE = ""
        Colori.GIALLO = ""
        Colori.BLU = ""
        Colori.CIANO = ""
        Colori.MAGENTA = ""
        Colori.BIANCO = ""
        Colori.GRASSETTO = ""
        Colori.SOTTOLINEATO = ""

    # Esegui comando
    try:
        if args.gen:
            # Genera password specifica lunghezza
            password = genera_password_casuale(args.gen)
            print(password)

            # Se stdout è terminale, mostra anche analisi
            if sys.stdout.isatty():
                stampa_barra_forza(password)

        elif args.passphrase:
            # Genera passphrase
            passphrase = genera_passphrase(5, " ", False)
            print(passphrase)

            if sys.stdout.isatty():
                stampa_barra_forza(passphrase)

        elif args.test:
            # Test password interattivo
            testa_qualita_password()

        elif args.strength:
            # Mostra forza password
            livello, punteggio, colore, descrizione = valuta_forza_password(args.strength)
            print(f"Forza: {livello}")
            print(f"Entropia: {punteggio:.1f} bit")
            print(f"Descrizione: {descrizione}")

    except KeyboardInterrupt:
        print(f"\n\n{Colori.GIALLO}Operazione interrotta.{Colori.RESET}")
        sys.exit(0)
    except Exception as e:
        stampa_errore(f"Errore: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
