# Quiz App - Applicazione Quiz Python

Un'applicazione CLI per quiz a scelta multipla, progettata per studenti universitari che imparano Python.

## Descrizione

Quiz App e un programma interattivo che permette di:
- Svolgere quiz su diverse categorie
- Mettere alla prova le proprie conoscenze
- Tener traccia dei punteggi piu alti
- Competere contro il tempo

## Caratteristiche

- **4 Categorie**: Conoscenza Generale, Scienza, Storia, Programmazione
- **5 Domande per categoria**: Quiz completi e bilanciati
- **Timer 30 secondi**: Tempo limitato per ogni domanda
- **Ordine casuale**: Domande mescolate ogni volta
- **Feedback immediato**: Sap subito se hai risposto correttamente
- **Sistema punteggi**: Salva i migliori 10 punteggi
- **Valutazione**: Eccellente, Buono, Medio, Scarso

## Requisiti

- Python 3.7 o superiore
- Nessuna dipendenza esterna (solo libreria standard)

## Installazione

1. Clona o scarica questo repository
2. Naviga nella cartella del progetto:
   ```bash
   cd quiz-app
   ```
3. E maggere il programma:
   ```bash
   python quiz_app.py
   ```

## Utilizzo

### Menu Principale

```
======================================================================
               BENVENUTO ALL'APP QUIZ PYTHON!
======================================================================

 MENU PRINCIPALE

 [1] Nuovo Quiz
 [2] Punteggi Più Alti
 [3] Esci

======================================================================
```

### Esempi di Utilizzo

#### Svolgere un Quiz

1. Seleziona "Nuovo Quiz"
2. Scegli una categoria:
   ```
   =================== SELEZIONA CATEGORIA ==================

   [1] Conoscenza Generale
   [2] Scienza
   [3] Storia
   [4] Programmazione

   ================================================================
   ```
3. Rispondi alle domande entro 30 secondi
4. Visualizza il punteggio finale con valutazione

#### Visualizzare Punteggi

1. Seleziona "Punteggi Più Alti"
2. Vedi i migliori 10 punteggi per categoria

## Struttura del File

```
quiz-app/
├── quiz_app.py         # File principale dell'applicazione
├── high_scores.json    # Database punteggi (auto-creato)
└── README.md          # Questa documentazione
```

## Concetti Python Imparati

### Fondamentali
- **Funzioni**: Organizzazione del codice in blocchi riutilizzabili
- **Dizionari**: Strutture dati per domande e opzioni
- **Liste**: Collezioni di domande e risposte
- **Cicli**: `for` e `while` per iterare
- **Condizioni**: `if/elif/else` per decisioni

### Intermedi
- **Modulo random**: Generare numeri casuali e mescolare liste
- **Modulo time**: Gestire timer e countdown
- **Modulo json**: Salvare e caricare dati
- **Gestione Errori**: `try/except` per robustezza

### Best Practices
- **Docstrings**: Documentazione delle funzioni
- **Validazione input**: Verificare risposte utente
- **Codice modulare**: Funzioni specializzate
- **Chiarezza**: Nomi descrittivi per variabili e funzioni

## Funzioni principali

```python
mostra_menu_principale()        # Mostra menu principale
seleziona_categoria()           # Seleziona categoria quiz
inizia_quiz(categoria)          # Avvia quiz nella categoria
mostra_domanda(...)             # Visualizza domanda corrente
ottieni_risposta_utente()      # Ottiene risposta con timer
calcola_punteggio(risultati)   # Calcola punteggio finale
ottieni_valutazione(percentuale) # Restituisce valutazione
salva_punteggio_alto(...)      # Salva punteggio in JSON
mostra_punteggi_alti()        # Visualizza classifica
mescola_domande(domande)        # Mescola ordine domande
```

## Struttura Dati

### Formato Domanda

```python
{
    "domanda": "Testo della domanda?",
    "opzioni": [
        "Opzione 1",
        "Opzione 2",
        "Opzione 3",
        "Opzione 4"
    ],
    "corretta": 2,  # Indice risposta corretta (0-3)
    "punti": 10
}
```

### Formato Punteggio JSON

```json
[
    {
        "nome": "Mario",
        "punteggio": 40,
        "percentuale": 80.0,
        "corrette": 4,
        "totali": 5,
        "categoria": "Programmazione",
        "data": "2026-02-11T15:30:00"
    }
]
```

## Sistema di Valutazione

| Percentuale | Valutazione  |
|-------------|---------------|
| 80-100%     | Eccellente    |
| 60-79%      | Buono         |
| 40-59%      | Medio         |
| 0-39%       | Scarso        |

## Esempio di Sessione

```
========================== APP QUIZ PYTHON ===========================

Benvenuto nell'Applicazione Quiz Python!
Testa le tue conoscenze in diverse categorie.

======================================================================

 MENU PRINCIPALE

 [1] Nuovo Quiz
 [2] Punteggi Più Alti
 [3] Esci

======================================================================
>> Seleziona un'opzione: 1

================== SELEZIONA CATEGORIA ==================

[1] Conoscenza Generale
[2] Scienza
[3] Storia
[4] Programmazione

===============================================================
>> Seleziona una categoria (1-4): 4

====================== QUIZ: Programmazione ======================

[Domanda 1/5]

Qual e la keyword corretta per definire una funzione in Python?

[1] function
[2] def
[3] define
[4] func

Tempo rimanente: 25s
>> La tua risposta (1-4): 2

[CORRETTO!] Hai guadagnato 10 punti!

...

=========================== RISULTATO FINALE ===========================

Punteggio Totale: 40 su 50 punti
Percentuale: 80.0%
Risposte Corrette: 4 su 5

Valutazione: Eccellente

======================================================================
Vuoi salvare il tuo punteggio? (s/n): s
>> Inserisci il tuo nome: Mario

[SUCCESSO] Punteggio salvato!
```

## Estensioni Suggerite

### Principiante
- [ ] Aggiungi altre categorie (Geografia, Arte, Sport)
- [ ] Difficoltà (Facile, Medio, Difficile)
- [ ] Più opzioni per risposta (5 invece di 4)

### Intermedio
- [ ] Multiplayer (2 giocatori sfidano)
- [ ] Domande True/False
- [ ] Sound effects con winsound
- [ ] Timer configurabile

### Avanzato
- [ ] Editor domande (aggiungi/rimuovi/modifica)
- [ ] Import domande da file JSON
- [ ] Database SQLite per statistiche
- [ ] Web interface con Flask

## Troubleshooting

### Errore: File non trovato
Il programma crea automaticamente `high_scores.json` alla prima esecuzione.

### Errore: Input non valido
Inserisci solo numeri da 1 a 4 per le risposte.

### Timeout
Se il tempo scade, la risposta viene considerata errata. Rispondi prima che il timer arrivi a 0!

## Autore

Progetto didattico per studenti universitari di Python.

## Licenza

Questo progetto è disponibile a scopo educativo.

## Acknowledgments

Creato per aiutare gli studenti a imparare Python attraverso quiz interattivi.
