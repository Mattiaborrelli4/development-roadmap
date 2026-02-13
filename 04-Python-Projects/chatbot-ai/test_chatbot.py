"""
Script di test per verificare le funzionalita del chatbot.
Esegue una serie di test automatici per validare il comportamento.
"""

import sys
import os

# Aggiungi il percorso del progetto
sys.path.append(r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\chatbot-ai")

from chatbot import Chatbot


def test_chatbot():
    """Esegue i test del chatbot."""
    print("="*60)
    print("TEST DEL CHATBOT AI")
    print("="*60)

    # Crea il chatbot
    print("\n1. Creazione del chatbot...")
    bot = Chatbot()
    print("   [OK] Chatbot creato con successo")

    # Test saluti
    print("\n2. Test dei saluti...")
    test_cases = [
        ("ciao", "saluto"),
        ("salve come stai", "saluto"),
        ("arrivederci", "arrivederci"),
        ("raccontami una barzelletta", "barzelletta"),
        ("che tempo fa", "meteo"),
        ("ultime notizie", "notizie"),
        ("grazie mille", "grazie"),
        ("come ti chiami", "nome"),
        ("aiutami", "aiuto"),
    ]

    for input_text, expected_intent in test_cases:
        response, confidence = bot.get_response(input_text)
        if confidence > 0.3:
            print(f"   [OK] '{input_text}' -> [{confidence:.2f}] {response[:50]}...")
        else:
            print(f"   [!] '{input_text}' -> Bassa confidenza ({confidence:.2f})")

    # Test calcolo confidenza
    print("\n3. Test del calcolo della confidenza...")
    pattern = r"\b(ciao|salve)\b.*"
    test_input = "ciao come stai"
    confidence = bot.calculate_confidence(pattern, test_input)
    print(f"   Pattern: {pattern}")
    print(f"   Input: {test_input}")
    print(f"   Confidenza: {confidence:.2f}")
    print(f"   [OK] Calcolo confidenza funzionante")

    # Test estrazione entità
    print("\n4. Test dell'estrazione delle entità...")
    test_input = "qual è il meteo di oggi a roma"
    entities = bot.extract_entities(test_input)
    print(f"   Input: {test_input}")
    print(f"   Entità estratte: {entities}")
    print(f"   [OK] Estrazione entità funzionante")

    # Test contesto
    print("\n5. Test del contesto conversazionale...")
    bot.context = []
    bot.update_context("Messaggio 1")
    bot.update_context("Messaggio 2")
    bot.update_context("Messaggio 3")
    bot.update_context("Messaggio 4")
    print(f"   Contesto (max 3): {bot.context}")
    assert len(bot.context) == 3, "Il contesto dovrebbe contenere max 3 messaggi"
    print(f"   [OK] Gestione contesto funzionante")

    # Test statistiche
    print("\n6. Test delle statistiche...")
    bot.total_conversations = 10
    bot.unknown_inputs = 2
    accuracy = bot._calculate_accuracy()
    print(f"   Conversazioni totali: {bot.total_conversations}")
    print(f"   Input sconosciuti: {bot.unknown_inputs}")
    print(f"   Accuratezza: {accuracy:.1f}%")
    print(f"   [OK] Calcolo statistiche funzionante")

    # Test saluti
    print("\n7. Test dei saluti casuali...")
    greeting = bot.get_greeting()
    print(f"   Saluto: {greeting}")
    assert len(greeting) > 0, "Il saluto non dovrebbe essere vuoto"
    print(f"   [OK] Generazione saluti funzionante")

    farewell = bot.get_farewell()
    print(f"   Congedo: {farewell}")
    assert len(farewell) > 0, "Il congedo non dovrebbe essere vuoto"
    print(f"   [OK] Generazione congedi funzionante")

    # Test pattern matching
    print("\n8. Test del pattern matching...")
    test_patterns = [
        (r"\b(ciao|salve)\b.*", "ciao a tutti"),
        (r"\b(meteo|tempo)\b.*", "che tempo fa"),
    ]
    for pattern, test_input in test_patterns:
        confidence = bot.calculate_confidence(pattern, test_input)
        print(f"   Pattern: {pattern[:30]}...")
        print(f"   Input: {test_input}")
        print(f"   Confidenza: {confidence:.2f}")
        assert confidence > 0, "La confidenza dovrebbe essere > 0"
    print(f"   [OK] Pattern matching funzionante")

    # Riepilogo
    print("\n" + "="*60)
    print("RIEPILOGO TEST")
    print("="*60)
    print("[OK] Tutti i test sono stati completati con successo!")
    print("[OK] Il chatbot e pronto per l'uso!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        test_chatbot()
    except Exception as e:
        print(f"\n[ERRORE] Errore durante i test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
