# Contact Book - Rubrica Telefonica

Un'applicazione CLI per gestire i contatti, progettata per studenti universitari che imparano Python.

## Descrizione

Contact Book e un programma a riga di comando che permette di:
- Gestire una rubrica completa
- Aggiungere, modificare, eliminare contatti
- Cercare contatti rapidamente
- Importare/esportare contatti CSV
- Ricevere promemoria compleanni

## Caratteristiche

- **Gestione Completa**: Nome, telefono, email, indirizzo, note, compleanno
- **Ricerca Avanzata**: Ricerca parziale su nome e telefono
- **Validazione**: Email con regex, telefono internazionale
- **CSV Support**: Importa/esporta in formato CSV
- **Promemoria Compleanni**: Avvisi per compleanni nei prossimi 7 giorni
- **Storage JSON**: Database persistente e leggibile
- **UUID Unico**: Identificatore univoco per ogni contatto

## Requisiti

- Python 3.7 o superiore
- Nessuna dipendenza esterna (solo libreria standard)

## Installazione

1. Clona o scarica questo repository
2. Naviga nella cartella del progetto:
   ```bash
   cd contact-book
   ```
3. Esegui il programma:
   ```bash
   python contact_book.py
   ```

## Utilizzo

### Menu Principale

```
==================================================
RUBRICA TELEFONICA - MENU PRINCIPALE
==================================================
1. Visualizza tutti i contatti
2. Aggiungi nuovo contatto
3. Cerca contatto
4. Modifica contatto
5. Elimina contatto
6. Controlla compleanni (prossimi 7 giorni)
7. Importa contatti da CSV
8. Esporta contatti in CSV
0. Esci
==================================================
```

### Esempi di Utilizzo

#### Aggiungere un Contatto

1. Seleziona "Aggiungi nuovo contatto"
2. Compila i campi richiesti:
   - Nome: Mario Rossi
   - Telefono: +39 123 456 7890
   - Email: mario@example.com
   - Indirizzo: Via Roma 1, Milano
   - Note: Amico del college
   - Compleanno: 15/05/1990 (DD/MM/YYYY)

#### Cercare un Contatto

1. Seleziona "Cerca contatto"
2. Inserisci nome o telefono (anche parziale)
3. Visualizza risultati corrispondenti

#### Controllare Compleanni

1. Seleziona "Controlla compleanni"
2. Vedi contatti con compleanno nei prossimi 7 giorni
3. Il programma mostra anche quanti anni compiranno

## Struttura del File

```
contact-book/
├── contact_book.py    # File principale dell'applicazione
├── rubrica.json       # Database contatti (auto-creato)
└── README.md         # Questa documentazione
```

## Concetti Python Imparati

### Fondamentali
- **Funzioni**: Organizzazione del codice
- **Dizionari**: Strutture dati per contatti
- **Liste**: Collezioni di contatti
- **Cicli**: Iterazione attraverso dati
- **Condizioni**: Decisioni logiche

### Intermedi
- **Modulo re**: Regex per validazione email
- **Modulo csv**: Import/export CSV
- **Modulo uuid**: Generazione ID univoci
- **Modulo datetime**: Calcolo compleanni

### Avanzati
- **Validazione input**: Robustezza dell'input utente
- **Gestione file JSON**: Persistenza dati
- **Ricerca parziale**: String matching case-insensitive
- **Calcolo date**: Differenza tra date

## Funzioni principali

```python
carica_da_json()                  # Carica contatti da file
salva_su_json(contatti)           # Salva contatti su file
aggiungi_contatto(contatti)        # Aggiunge nuovo contatto
visualizza_tutti_contatti(contatti) # Mostra tutti contatti
cerca_contatti(contatti)          # Ricerca contatti
modifica_contatto(contatti)       # Modifica esistente
elimina_contatto(contatti)        # Elimina contatto
importa_da_csv()                 # Importa da CSV
esporta_in_csv(contatti)          # Esporta in CSV
controlla_compleanni(contatti)    # Controlla compleanni
valida_email(email)               # Validazione email
valida_telefono(telefono)         # Validazione telefono
genera_uuid()                    # Genera ID univoco
```

## Struttura Dati

### Formato Contatto (JSON)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nome": "Mario Rossi",
  "telefono": "+39 123 456 7890",
  "email": "mario@example.com",
  "indirizzo": "Via Roma 1, Milano",
  "note": "Amico del college",
  "compleanno": "1990-05-15"
}
```

### Formato CSV Export

```csv
ID,Nome,Telefono,Email,Indirizzo,Note,Compleanno
uuid1,Mario Rossi,+39 1234567890,mario@example.com,Via Roma 1,,1990-05-15
uuid2,Lisa Bianchi,+39 0987654321,lisa@example.com,Via Milano 2,,1992-08-20
```

## Validazione

### Email (Regex)

Pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

Esempi validi:
- mario@example.com
- lisa.bianchi@azienda.it
- user+tag@domain.co.uk

### Telefono

Accetta formati internazionali:
- +39 123 456 7890
- +33123456789
- 123-456-7890
- 1234567890

Lunghezza: 10-15 cifre (senza spazi/segno)

## Esempio di Sessione

```
==================================================
BENVENUTO NELLA RUBRICA TELEFONICA!
==================================================

RUBRICA TELEFONICA - MENU PRINCIPALE
==================================================
1. Visualizza tutti i contatti
2. Aggiungi nuovo contatto
3. Cerca contatto
4. Modifica contatto
5. Elimina contatto
6. Controlla compleanni (prossimi 7 giorni)
7. Importa contatti da CSV
8. Esporta contatti in CSV
0. Esci
==================================================
Seleziona un'opzione (0-8): 2

[INFO] Inserimento nuovo contatto

>> Nome: Mario Rossi
>> Telefono: +39 123 456 7890
>> Email: mario@example.com
>> Indirizzo: Via Roma 1, Milano
>> Note: Amico del college
>> Compleanno (DD/MM/YYYY): 15/05/1990

[SUCCESSO] Contatto aggiunto!
```

## Promemoria Compleanni

Il programma controlla i compleanni nei prossimi 7 giorni e mostra:

```
==================================================
         PROMEMORIA COMPLEANNI
==================================================

[OGGI] Maria Verdi compie 35 anni!

[DOMANI] (1 giorni) Luca Bianchi compira 28 anni

[TRA 5 GIORNI] (5 giorni) Giulio Neri compira 42 anni

==================================================
Trovati 3 compleanni prossimi
==================================================
```

## Estensioni Suggerite

### Principiante
- [ ] Aggiungi foto profilo
- [ ] Gruppi (Lavoro, Amici, Famiglia)
- [ ] Campo "Azienda" per contatti lavoro
- [ ] Ordinamento alfabetico

### Intermedio
- [ ] Categorie/Tag personalizzati
- [ ] Campo "Preferito" per contatti frequenti
- [ ] Storia modifiche contatto
- [ ] Backup automatici

### Avanzato
- [ ] Sincronizzazione Google Contacts
- [ ] Interfaccia web con Flask
- [ ] API REST per integrazioni
- [ ] Database SQLite per performance

## Troubleshooting

### Errore: Email non valida
Assicurati che l'email abbia il formato `nome@dominio.ext`

### Errore: Telefono non valido
Il numero deve contenere tra 10 e 15 cifre. Puoi includere il prefisso internazionale (+39).

### Errore: Format data non valido
Usa il formato `DD/MM/YYYY` (es. 15/05/1990 per il 15 maggio 1990)

### CSV Import fallito
Verifica che il file CSV abbia le colonne corrette: Nome, Telefono, Email, Indirizzo, Note, Compleanno

## Formato CSV per Import

```csv
Nome,Telefono,Email,Indirizzo,Note,Compleanno
Mario Rossi,+391234567890,mario@example.com,Via Roma 1,Amico,15/05/1990
Lisa Bianchi,+390987654321,lisa@example.com,Via Milano 2,,20/08/1992
```

## Autore

Progetto didattico per studenti universitari di Python.

## Licenza

Questo progetto e disponibile a scopo educativo.

## Acknowledgments

Creato per aiutare gli studenti a imparare Python attraverso una rubrica completa e funzionale.
