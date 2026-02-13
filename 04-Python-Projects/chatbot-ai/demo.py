"""
Script demo per mostrare come usare il chatbot.
Esegue una conversazione di esempio automatica.
"""

import sys
sys.path.append(r"C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\chatbot-ai")

from chatbot import Chatbot


def demo_conversation():
    """Esegue una conversazione demo con il chatbot."""
    print("="*70)
    print("DEMO CONVERSAZIONE CHATBOT")
    print("="*70)

    # Crea il chatbot
    bot = Chatbot()

    # Messaggi demo
    messages = [
        "ciao",
        "come ti chiami",
        "raccontami una barzelletta",
        "che tempo fa",
        "grazie",
        "arrivederci"
    ]

    print("\n--- INIZIO CONVERSAZIONE ---\n")

    # Saluto iniziale
    print(f"Chatbot: {bot.get_greeting()}\n")

    # Simula la conversazione
    for i, msg in enumerate(messages, 1):
        print(f"Utente [{i}]: {msg}")

        response, confidence = bot.get_response(msg, bot.context)
        bot.update_context(msg)

        print(f"Chatbot: {response}")
        print(f"[Confidenza: {confidence:.2f}]\n")

    print("--- FINE CONVERSAZIONE ---\n")

    # Mostra le statistiche
    bot.total_conversations = len(messages)
    bot.show_statistics()


if __name__ == "__main__":
    try:
        demo_conversation()
    except Exception as e:
        print(f"\nErrore durante la demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
