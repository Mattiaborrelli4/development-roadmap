"""
========================================
CHATBOT AI - Semplice Chatbot in Python
========================================

Un chatbot educativo che utilizza pattern matching e un sistema di
apprendimento semplice. Progettato per studenti universitari principianti.

Autore: Progetto Educativo
Linguaggio: Python 3.x
"""

import json
import random
import re
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class Chatbot:
    """
    Classe principale del Chatbot.

    Gestisce la conversazione, l'apprendimento e il matching dei pattern.
    """

    def __init__(self):
        """Inizializza il chatbot con i dati di training e la conversazione."""
        # Percorsi dei file (assoluti per compatibilita Windows)
        self.base_path = r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\chatbot-ai"
        self.training_file = os.path.join(self.base_path, "training_data.json")
        self.learned_file = os.path.join(self.base_path, "learned_data.json")

        # Dati del chatbot
        self.intents = {}  # Struttura: {intent: {'patterns': [], 'responses': []}}
        self.learned_intents = {}  # Pattern appresi durante le conversazioni

        # Contesto della conversazione (ultimi 3 messaggi)
        self.context: List[str] = []

        # Statistiche
        self.total_conversations = 0
        self.unknown_inputs = 0

        # Carica i dati di training
        self.load_training_data()
        self.load_learned_data()

        print("Chatbot inizializzato con successo!")

    def load_training_data(self) -> None:
        """
        Carica i dati di training dal file JSON.

        Se il file non esiste, crea i dati di training di default.
        """
        # Se esiste il file, caricalo
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, 'r', encoding='utf-8') as f:
                    self.intents = json.load(f)
                print(f"Dati di training caricati da {self.training_file}")
                return
            except Exception as e:
                print(f"Errore nel caricamento: {e}")

        # Altrimenti, crea i dati di training di default
        print("Creazione dati di training di default...")
        self.intents = self._get_default_intents()

        # Salva i dati di default
        self._save_training_data()

    def _get_default_intents(self) -> Dict:
        """
        Restituisce i dati di training di default.

        Ritorna:
            Dict: Dizionario con intenti, pattern e risposte predefiniti
        """
        return {
            "saluto": {
                "patterns": [
                    r"\b(ciao|salve|hey|buongiorno|buonasera|buon pomeriggio)\b.*",
                    r"\bhola\b",
                    r"\bcome stai\b.*",
                    r"\bcome va\b.*"
                ],
                "responses": [
                    "Ciao! Come posso aiutarti oggi?",
                    "Salve! Sono qui per assisterti.",
                    "Ciao! Dimmi tutto, sono pronto ad ascoltarti.",
                    "Hey! Cosa vuoi sapere?"
                ]
            },
            "arrivederci": {
                "patterns": [
                    r"\b(arrivederci|addio|ciao ciao|alla prossima|a presto)\b.*",
                    r"\bbye\b",
                    r"\besci\b.*",
                    r"\bchiudi.*\b"
                ],
                "responses": [
                    "Arrivederci! È stato un piacere chattare con te.",
                    "A presto! Torna presto a trovarmi.",
                    "Ciao ciao! Alla prossima conversazione!",
                    "Addio! Ha una bellissima giornata!"
                ]
            },
            "meteo": {
                "patterns": [
                    r"\b(meteo|tempo|temperature|previsioni)\b.*",
                    r"\b(piove|sole|nuvolo|freddo|caldo)\b.*",
                    r"\bche tempo\b.*",
                    r"\bcom'e' il tempo\b.*"
                ],
                "responses": [
                    "Non posso controllare il meteo reale, ma spero sia bello!",
                    "Per il meteo preciso, ti consiglio di controllare un'app meteo.",
                    "Sarebbe bello se ci fosse il sole oggi, non trovi?",
                    "Il meteo è imprevedibile, ma portati sempre un ombrello!"
                ]
            },
            "notizie": {
                "patterns": [
                    r"\b(notizie|news|attualita|giornale)\b.*",
                    r"\bsuccede\b.*",
                    r"\bultime notizie\b.*",
                    r"\bcosa c'e' di nuovo\b.*"
                ],
                "responses": [
                    "Non ho accesso alle notizie in tempo reale, ma il mondo è sempre pieno di eventi!",
                    "Per le ultime notizie, ti consiglio di visitare siti di informazione.",
                    "Ci sono sempre molte cose che accadono nel mondo!",
                    "Il mondo cambia ogni giorno, rimani informato!"
                ]
            },
            "barzelletta": {
                "patterns": [
                    r"\b(barzelletta|raccontami|fami ridere|joke)\b.*",
                    r"\b(barze|scherzo)\b.*",
                    r"\bchi ha detto\b.*"
                ],
                "responses": [
                    "Perché i programmatori preferiscono il mode scuro? Perché la luce attira i bug!",
                    "Cosa dice un informatico a un altro? 'Hai 1000 problemi, ma la soluzione non è tra di loro'.",
                    "Perché gli informatici confondono Natale e Halloween? Perché OCT 31 = DEC 25!",
                    "Un uomo entra in un bar e chiede: 'Quanto costa un Wi-Fi?' Il barista risponde: 'Per te è gratis!'"
                ]
            },
            "aiuto": {
                "patterns": [
                    r"\b(aiuto|help|aiutami|cos sai fare)\b.*",
                    r"\b(istruzioni|come funzioni|guida)\b.*",
                    r"\b(cosa puoi fare|capabilities)\b.*"
                ],
                "responses": [
                    "Posso chattare con te, raccontare barzellette, e rispondere a domande semplici!",
                    "Sono un chatbot educativo. Chiedimi del meteo, notizie, o dì semplicemente ciao!",
                    "Scrivi 'impara' per insegnarmi nuove risposte!",
                    "Posso fare molte cose: salutare, rispondere, e imparare da te!"
                ]
            },
            "grazie": {
                "patterns": [
                    r"\b(grazie|grazie mille|thank you|thanks)\b.*",
                    r"\b(apprezzo|gentile)\b.*"
                ],
                "responses": [
                    "Prego! Sempre felice di aiutare!",
                    "Di nulla! Sono qui per questo.",
                    "Il piacere è tutto mio!",
                    "Prego! C'è altro che posso fare?"
                ]
            },
            "nome": {
                "patterns": [
                    r"\b(come ti chiami|chi sei|il tuo nome|ti chiami)\b.*",
                    r"\b(presentati|presentazione)\b.*"
                ],
                "responses": [
                    "Sono ChatbotAI, il tuo assistente virtuale educativo!",
                    "Mi chiamo ChatbotAI, creato per aiutarti a imparare Python!",
                    "Sono un chatbot semplice ma potente. Chiamami ChatbotAI!",
                    "ChatbotAI è il mio nome, chiacchierare è il mio gioco!"
                ]
            },
            "tempo": {
                "patterns": [
                    r"\b(che ore|ora|orario|clock)\b.*",
                    r"\b(ora attuale)\b.*"
                ],
                "responses": [
                    f"Adesso sono le {datetime.now().strftime('%H:%M')}.",
                    "Non ho un orologio integrato, ma il tuo computer sa l'ora!",
                    "Controlla l'ora sul tuo dispositivo!"
                ]
            }
        }

    def _save_training_data(self) -> None:
        """Salva i dati di training nel file JSON."""
        try:
            with open(self.training_file, 'w', encoding='utf-8') as f:
                json.dump(self.intents, f, ensure_ascii=False, indent=2)
            print(f"Dati di training salvati in {self.training_file}")
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")

    def load_learned_data(self) -> None:
        """
        Carica i pattern appresi dal file JSON.

        Permette al chatbot di ricordare ciò che ha appreso nelle sessioni precedenti.
        """
        if os.path.exists(self.learned_file):
            try:
                with open(self.learned_file, 'r', encoding='utf-8') as f:
                    self.learned_intents = json.load(f)
                print(f"Dati appresi caricati da {self.learned_file}")
            except Exception as e:
                print(f"Errore nel caricamento dati appresi: {e}")
                self.learned_intents = {}
        else:
            self.learned_intents = {}

    def save_learning(self) -> None:
        """
        Salva i nuovi pattern appresi nel file JSON.

        Questo permette al chatbot di "ricordare" ciò che ha imparato
        tra una sessione e l'altra.
        """
        try:
            with open(self.learned_file, 'w', encoding='utf-8') as f:
                json.dump(self.learned_intents, f, ensure_ascii=False, indent=2)
            print(f"Nuovi apprendimenti salvati in {self.learned_file}")
        except Exception as e:
            print(f"Errore nel salvataggio degli apprendimenti: {e}")

    def calculate_confidence(self, pattern: str, user_input: str) -> float:
        """
        Calcola quanto bene un pattern corrisponde all'input dell'utente.

        Utilizza espressioni regolari per il pattern matching e calcola
        un punteggio di confidenza basato sulla corrispondenza.

        Args:
            pattern: Il pattern regex da confrontare
            user_input: L'input dell'utente

        Ritorna:
            float: Punteggio di confidenza tra 0.0 e 1.0
        """
        try:
            # Tenta di fare il match del pattern
            match = re.search(pattern, user_input, re.IGNORECASE)

            if not match:
                return 0.0

            # Calcola la confidenza base
            confidence = 0.5

            # Aumenta la confidenza se il match è completo
            if match.group() == user_input.strip():
                confidence += 0.3

            # Aumenta la confidenza per match più lunghi
            matched_length = len(match.group())
            input_length = len(user_input.strip())
            if input_length > 0:
                confidence += (matched_length / input_length) * 0.2

            # Bonus per parole chiave multiple
            word_count = len(user_input.split())
            if word_count >= 3:
                confidence += 0.1

            # Assicurati che la confidenza sia tra 0 e 1
            return min(confidence, 1.0)

        except Exception as e:
            print(f"Errore nel calcolo della confidenza: {e}")
            return 0.0

    def extract_entities(self, user_input: str) -> List[str]:
        """
        Estrae le parole chiave (entità) dall'input dell'utente.

        Utilizza una semplice tecnica NLP: rimozione di stopword
        e estrazione delle parole significative.

        Args:
            user_input: L'input dell'utente

        Ritorna:
            List[str]: Lista di parole chiave estratte
        """
        # Stopword italiane comuni da ignorare
        stopword = {
            "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
            "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
            "e", "o", "ma", "perche", "quindi", "poi", "anche",
            "essere", "avere", "fare", "dire", "andare", "venire",
            "questo", "quello", "questa", "quella", "cio", "cioe"
        }

        # Tokenizzazione semplice: dividi per spazi e punteggiatura
        words = re.findall(r'\b\w+\b', user_input.lower())

        # Rimuovi stopword e parole corte
        entities = [
            word for word in words
            if word not in stopword and len(word) > 2
        ]

        return entities

    def get_greeting(self) -> str:
        """
        Genera un saluto casuale all'avvio della conversazione.

        Ritorna:
            str: Un saluto casuale
        """
        greetings = [
            "Ciao! Sono il tuo assistente virtuale. Come posso aiutarti?",
            "Salve! Sono pronto a chattare con te. Cosa vuoi sapere?",
            "Hey! Benvenuto nella mia conversazione. Dimmi tutto!",
            "Buongiorno! Sono qui per rispondere alle tue domande.",
            "Ciao! Scrivi 'aiuto' per vedere cosa so fare."
        ]
        return random.choice(greetings)

    def get_farewell(self) -> str:
        """
        Genera un saluto di chiusura casuale.

        Ritorna:
            str: Un congedo casuale
        """
        farewells = [
            "Grazie per la chiacchierata! A presto!",
            "È stato un piacere parlarti. Alla prossima!",
            "Arrivederci! Torna presto a trovarmi!",
            "Ciao ciao! Buona giornata!",
            "Alla prossima conversazione!"
        ]
        return random.choice(farewells)

    def update_context(self, message: str) -> None:
        """
        Aggiorna il contesto della conversazione.

        Mantiene gli ultimi 3 messaggi per dare coerenza alla conversazione.

        Args:
            message: Il messaggio da aggiungere al contesto
        """
        self.context.append(message)

        # Mantiene solo gli ultimi 3 messaggi
        if len(self.context) > 3:
            self.context = self.context[-3:]

    def get_response(self, user_input: str, context: Optional[List[str]] = None) -> Tuple[str, float]:
        """
        Trova la risposta migliore per l'input dell'utente.

        Utilizza il pattern matching con scoring di confidenza.

        Args:
            user_input: L'input dell'utente
            context: Il contesto della conversazione (opzionale)

        Ritorna:
            Tuple[str, float]: (risposta, punteggio di confidenza)
        """
        if not user_input.strip():
            return "Non hai scritto nulla. Come posso aiutarti?", 0.0

        # Normalizza l'input
        user_input = user_input.strip().lower()

        # Combina entrambe le fonti di dati
        all_intents = {**self.intents, **self.learned_intents}

        best_response = None
        best_confidence = 0.0
        best_intent = None

        # Cerca attraverso tutti gli intenti
        for intent_name, intent_data in all_intents.items():
            patterns = intent_data.get('patterns', [])

            for pattern in patterns:
                confidence = self.calculate_confidence(pattern, user_input)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent_name

                    # Scegli una risposta casuale per questo intent
                    responses = intent_data.get('responses', [])
                    if responses:
                        best_response = random.choice(responses)

        # Se trovato una buona corrispondenza
        if best_response and best_confidence >= 0.3:
            return best_response, best_confidence

        # Risposte di fallback per input sconosciuti
        fallback_responses = [
            "Non sono sicuro di aver capito. Puoi ripetere in modo diverso?",
            "Interessante! Dimmi di più su questo argomento.",
            "Non ho una risposta pronta per questo. Vuoi insegnarmelo? Scrivi 'impara'.",
            "Hmm, non sono sicuro di cosa intendi. Prova con 'aiuto' per vedere cosa so fare!",
            "Non conosco questa domanda. Forse potresti reformularla?",
            "Questa è nuova per me! Scrivi 'impara' per insegnarmi una risposta."
        ]

        # Considera il contesto per risposte migliori
        if context and len(context) > 0:
            # Se l'utente continua su un argomento sconosciuto
            fallback_responses.append(
                f"Ho capito che stai parlando di questo, ma ho bisogno di più dettagli."
            )

        self.unknown_inputs += 1
        return random.choice(fallback_responses), 0.1

    def learn_mode(self) -> None:
        """
        Modalità di apprendimento per aggiungere nuovi pattern.

        Permette all'utente di insegnare al chatbot nuove risposte.
        """
        print("\n" + "="*50)
        print("MODALITA DI APPRENDIMENTO")
        print("="*50)
        print("Insegnerai al chatbot nuove risposte!")
        print("Scrivi 'annulla' in qualsiasi momento per uscire.\n")

        # Ottieni il pattern
        while True:
            pattern_input = input("Inserisci il pattern (es: 'ciao come stai'): ").strip()

            if pattern_input.lower() == 'annulla':
                print("Apprendimento annullato.")
                return

            if pattern_input:
                break
            print("Il pattern non può essere vuoto. Riprova.")

        # Ottieni l'intento
        while True:
            intent_input = input("Inserisci il nome dell'intento (es: 'saluto'): ").strip()

            if intent_input.lower() == 'annulla':
                print("Apprendimento annullato.")
                return

            if intent_input:
                break
            print("L'intento non può essere vuoto. Riprova.")

        # Ottieni la risposta
        while True:
            response_input = input("Inserisci la risposta del chatbot: ").strip()

            if response_input.lower() == 'annulla':
                print("Apprendimento annullato.")
                return

            if response_input:
                break
            print("La risposta non può essere vuota. Riprova.")

        # Crea il pattern regex
        pattern_regex = self._create_pattern_from_input(pattern_input)

        # Aggiungi agli intenti appresi
        if intent_input not in self.learned_intents:
            self.learned_intents[intent_input] = {
                'patterns': [],
                'responses': []
            }

        self.learned_intents[intent_input]['patterns'].append(pattern_regex)
        self.learned_intents[intent_input]['responses'].append(response_input)

        # Salva
        self.save_learning()

        print("\n" + "="*50)
        print("APPRENDIMENTO COMPLETATO!")
        print("="*50)
        print(f"Pattern: {pattern_input}")
        print(f"Intento: {intent_input}")
        print(f"Risposta: {response_input}")
        print(f"Pattern Regex: {pattern_regex}")
        print("\nGrazie per avermi insegnato qualcosa di nuovo!")

    def _create_pattern_from_input(self, user_input: str) -> str:
        """
        Crea un pattern regex dall'input dell'utente.

        Args:
            user_input: L'input dell'utente

        Ritorna:
            str: Pattern regex creato
        """
        # Estrae le parole chiave
        entities = self.extract_entities(user_input)

        if not entities:
            # Fallback: usa l'intero input con wildcard
            return rf"\b{re.escape(user_input)}\b.*"

        # Crea pattern con le parole chiave
        pattern_words = []
        for word in entities[:3]:  # Max 3 parole chiave
            pattern_words.append(word)

        # Crea il pattern regex
        if len(pattern_words) == 1:
            pattern = rf"\b{pattern_words[0]}\b.*"
        else:
            pattern = r"\b(" + "|".join(pattern_words) + r")\b.*"

        return pattern

    def show_statistics(self) -> None:
        """Mostra le statistiche della conversazione."""
        print("\n" + "="*50)
        print("STATISTICHE DELLA CONVERSAZIONE")
        print("="*50)
        print(f"Totale scambi: {self.total_conversations}")
        print(f"Input non riconosciuti: {self.unknown_inputs}")
        print(f"Tasso di riconoscimento: {self._calculate_accuracy():.1f}%")

        total_intents = len(self.intents) + len(self.learned_intents)
        print(f"Intenti conosciuti: {total_intents}")
        print(f"Intenti base: {len(self.intents)}")
        print(f"Intenti appresi: {len(self.learned_intents)}")

        if self.learned_intents:
            print(f"\nIntenti appresi:")
            for intent in self.learned_intents.keys():
                print(f"  - {intent}")

        print("="*50 + "\n")

    def _calculate_accuracy(self) -> float:
        """
        Calcola la percentuale di input riconosciuti.

        Ritorna:
            float: Percentuale di riconoscimento
        """
        if self.total_conversations == 0:
            return 0.0

        recognized = self.total_conversations - self.unknown_inputs
        return (recognized / self.total_conversations) * 100

    def show_help(self) -> None:
        """Mostra le informazioni di aiuto."""
        print("\n" + "="*50)
        print("AIUTO - COMANDI DISPONIBILI")
        print("="*50)
        print("Comandi speciali:")
        print("  'impara'     - Entra in modalità apprendimento")
        print("  'statistiche' - Mostra le statistiche della conversazione")
        print("  'aiuto'      - Mostra questo messaggio di aiuto")
        print("  'esci'       - Termina la conversazione")
        print("\nArgomenti che conosco:")
        print("  - Saluti e presentazioni")
        print("  - Meteo (informazioni generali)")
        print("  - Notizie (informazioni generali)")
        print("  - Barzellette")
        print("  - Aiuto e istruzioni")
        print("  - Orario")
        print("\nSuggerimento: Scrivi in italiano e sii specifico!")
        print("="*50 + "\n")

    def main(self) -> None:
        """
        Loop principale della conversazione.

        Gestisce l'interazione con l'utente fino alla chiusura.
        """
        print("\n" + "="*50)
        print("CHATBOT AI - Conversazione")
        print("="*50)
        print("\nDigitare 'esci' per terminare la conversazione.")
        print("Digitare 'aiuto' per vedere i comandi disponibili.\n")

        # Saluto iniziale
        print(f"Chatbot: {self.get_greeting()}\n")

        # Loop principale
        while True:
            try:
                # Ottieni l'input dell'utente
                user_input = input("Tu: ").strip()

                if not user_input:
                    continue

                # Controlla i comandi speciali
                if user_input.lower() in ['esci', 'exit', 'quit', 'bye', 'arrivederci']:
                    print(f"\nChatbot: {self.get_farewell()}")
                    break

                elif user_input.lower() in ['impara', 'learn', 'insegna']:
                    self.learn_mode()
                    print("\nChatbot: Torno alla conversazione normale.\n")
                    continue

                elif user_input.lower() in ['statistiche', 'stats', 'info']:
                    self.show_statistics()
                    continue

                elif user_input.lower() in ['aiuto', 'help', '?']:
                    self.show_help()
                    continue

                # Ottieni la risposta normale
                response, confidence = self.get_response(user_input, self.context)

                # Aggiorna il contesto
                self.update_context(user_input)

                # Mostra la risposta
                print(f"\nChatbot: {response}")

                # Mostra la confidenza per scopi educativi
                if confidence < 0.3:
                    print(f"[Confidenza: {confidence:.2f} - Non molto sicuro]")

                self.total_conversations += 1
                print()

            except KeyboardInterrupt:
                print("\n\nInterruzione rilevata.")
                print(f"Chatbot: {self.get_farewell()}")
                break

            except Exception as e:
                print(f"\nErrore: {e}")
                print("Per favore, riprova.\n")

        # Mostra le statistiche finali
        self.show_statistics()


def main():
    """
    Funzione principale per avviare il chatbot.

    Crea un'istanza del chatbot e avvia la conversazione.
    """
    try:
        # Crea il chatbot
        chatbot = Chatbot()

        # Avvia la conversazione
        chatbot.main()

    except Exception as e:
        print(f"Errore critico: {e}")
        print("Impossibile avviare il chatbot.")


if __name__ == "__main__":
    """
    Punto di ingresso del programma.

    Esegue la funzione main quando lo script viene eseguito direttamente.
    """
    main()
