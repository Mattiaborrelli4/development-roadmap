# Expense Tracker - Gestore di Spese

Un'applicazione CLI per tracciare e gestire le spese personali, progettata per studenti universitari che imparano Python.

## Descrizione

Expense Tracker e un programma a riga di comando che permette di:
- Aggiungere e gestire spese personali
- Visualizzare spese per categoria
- Creare riepiloghi mensili
- Gestire budget per categoria
- Visualizzare statistiche dettagliate

## Caratteristiche

- **Gestione Spese**: Aggiungi, visualizza, elimina spese
- **Categorie**: Cibo, Trasporti, Intrattenimento, Bollette, Altro
- **Budget Management**: Imposta e controlla budget per categoria
- **Statistiche**: Totale, media, spesa piu elevata
- **Report**: Esporta report in formato testo
- **Storage JSON**: Dati salvati in formato JSON leggibile

## Requisiti

- Python 3.7 o superiore
- Nessuna dipendenza esterna (solo libreria standard)

## Installazione

1. Clona o scarica questo repository
2. Naviga nella cartella del progetto:
   ```bash
   cd expense-tracker
   ```
3. Esegui il programma:
   ```bash
   python expense_tracker.py
   ```

## Utilizzo

### Menu Principale

```
============================================================
         EXPENSE TRACKER - GESTORE DI SPESE
============================================================

[1] Aggiungi una nuova spesa
[2] Visualizza tutte le spese
[3] Visualizza spese per categoria
[4] Visualizza riepilogo mensile
[5] Gestisci budget per categoria
[6] Visualizza statistiche
[7] Elimina una spesa
[8] Esporta report in formato testo
[9] Esci
============================================================
```

### Esempi di Utilizzo

#### Aggiungere una Spesa

1. Seleziona "Aggiungi una nuova spesa" dal menu
2. Inserisci l'importo (es. 25.50)
3. Seleziona la categoria (1-5)
4. Inserisci una descrizione
5. Inserisci la data (formato DD/MM/YYYY)

#### Visualizzare Riepilogo Mensile

1. Seleziona "Visualizza riepilogo mensile"
2. Inserisci mese e anno
3. Il programma mostra:
   - Totale spese del mese
   - Divisione per categoria
   - Numero di transazioni

#### Gestire Budget

1. Seleziona "Gestisci budget per categoria"
2. Scegli una categoria
3. Inserisci il budget mensile
4. Il programma avvisa se superi il budget

## Struttura del File

```
expense-tracker/
├── expense_tracker.py    # File principale dell'applicazione
├── expenses.json        # Database delle spese (auto-creato)
├── budget.json         # Budget per categoria (auto-creato)
└── README.md          # Questa documentazione
```

## Concetti Python Imparati

### Fondamentali
- **Funzioni**: Organizzazione del codice in blocchi riutilizzabili
- **Liste e Dizionari**: Strutture dati per memorizzare informazioni
- **Cicli**: `for` e `while` per iterare
- **Condizioni**: `if/elif/else` per decisioni
- **Input/Output**: `input()` e `print()` per interazione utente

### Intermedi
- **Gestione File**: Leggere e scrivere file JSON
- **Validazione**: Verificare input utente
- **Gestione Errori**: `try/except` per gestire eccezioni
- **Modulo datetime**: Lavorare con date e orari

### Best Practices
- **Docstrings**: Documentazione delle funzioni
- **Nomi descrittivi**: Variabili e funzioni con nomi chiari
- **Modularita**: Codice organizzato in funzioni specifiche
- **Gestione errori robusta**: Prevenire crash del programma

## Funzioni principali

```python
carica_spese_da_file()          # Carica spese da JSON
salva_spese_su_file(spese)      # Salva spese in JSON
aggiungi_spesa(spese)            # Aggiunge nuova spesa
visualizza_tutte_le_spese(spese) # Mostra tutte le spese
visualizza_per_categoria(spese)   # Filtra per categoria
visualizza_riepilogo_mensile(spese) # Riepilogo mensile
gestisci_budget(spese)           # Gestione budget
visualizza_statistiche(spese)     # Statistiche generali
```

## Formato Dati

### Struttura Spesa (JSON)

```json
{
  "id": 1,
  "importo": 25.50,
  "categoria": "Cibo",
  "descrizione": "Pizza",
  "data": "11/02/2026",
  "timestamp": "2026-02-11T14:30:00"
}
```

### Struttura Budget (JSON)

```json
{
  "Cibo": 500.00,
  "Trasporti": 100.00,
  "Intrattenimento": 150.00,
  "Bollette": 300.00,
  "Altro": 200.00
}
```

## Estensioni Suggerite

### Principiante
- [ ] Aggiungi modifica di spese esistenti
- [ ] Ordina spese per importo
- [ ] Aggiungi filtro per range di date

### Intermedio
- [ ] Export in formato CSV
- [ ] Grafici ASCII semplici
- [ ] Categorie personalizzabili
- [ ] Multi-valuta

### Avanzato
- [ ] Database SQLite invece di JSON
- [ ] Sincronizzazione cloud
- [ ] Dashboard web con Flask
- [ ] Machine learning per previsioni

## Troubleshooting

### Errore: File non trovato
Il programma crea automaticamente i file JSON alla prima esecuzione. Se ricevi questo errore, verifica i permessi della cartella.

### Errore: Format data non valido
Assicurati di inserire la data nel formato `DD/MM/YYYY` (es. 11/02/2026).

### Errore: Importo non valido
Usa il punto come separatore decimale (es. 25.50), non la virgola.

## Autore

Progetto didattico per studenti universitari di Python.

## Licenza

Questo progetto e disponibile a scopo educativo.

## Acknowledgments

Creato per aiutare gli studenti a imparare Python attraverso progetti pratici e reali.
