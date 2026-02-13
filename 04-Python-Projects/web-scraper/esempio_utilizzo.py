#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
ESEMPI DI UTILIZZO DEL WEB SCRAPER
==============================================================================
Questo file contiene esempi pratici per iniziare a usare il web scraper.

Contenuti:
- Esempio 1: Scraping base di una singola pagina
- Esempio 2: Scraping multi-pagina con rate limiting
- Esempio 3: Estrazione di prodotti da e-commerce
- Esempio 4: Monitoraggio notizie
==============================================================================
"""

from web_scraper import (
    download_page,
    download_multiple_pages,
    parse_html_basic,
    parse_products_demo,
    extract_text_content,
    save_to_csv,
    save_to_json,
    validate_url,
    check_robots_txt
)


def esempio_1_scraping_base():
    """
    ESEMPIO 1: Scraping Base di una Singola Pagina
    -----------------------------------------------
    Scarica una pagina web, estrae i dati di base e li salva in JSON.
    """
    print("\n" + "="*70)
    print("ESEMPIO 1: Scraping Base di una Singola Pagina")
    print("="*70)

    # URL da scaricare (siti demo per scraping)
    url = "https://books.toscrape.com/"

    print(f"\n[1] Target URL: {url}")

    # Controlla robots.txt (best practice!)
    check_robots_txt(url)

    # Download della pagina
    print("\n[2] Download pagina in corso...")
    html = download_page(url)

    if not html:
        print("[ERRORE] Download fallito!")
        return

    # Parsing HTML
    print("\n[3] Parsing HTML...")
    dati = parse_html_basic(html)

    # Mostra risultati
    print("\n[4] Risultati:")
    if dati['title']:
        print(f"  - Titolo: {dati['title']}")
    print(f"  - Link trovati: {len(dati['links'])}")
    print(f"  - Heading H1: {len(dati['headings']['h1'])}")
    print(f"  - Heading H2: {len(dati['headings']['h2'])}")
    print(f"  - Immagini: {len(dati['images'])}")

    # Salvataggio JSON
    print("\n[5] Salvataggio in JSON...")
    dati['url'] = url
    save_to_json(dati, 'esempio_1_output.json')

    print("\n[OK] Esempio 1 completato! Controlla 'esempio_1_output.json'")


def esempio_2_multi_pagina():
    """
    ESEMPIO 2: Scraping Multi-Pagina
    ---------------------------------
    Scarica multiple pagine con rate limiting.
    """
    print("\n" + "="*70)
    print("ESEMPIO 2: Scraping Multi-Pagina")
    print("="*70)

    # Lista di URL da scaricare (siti demo)
    urls = [
        "https://books.toscrape.com/",
        "https://quotes.toscrape.com/",
        "https://toscrape.com/"
    ]

    print(f"\n[1] Target: {len(urls)} pagine")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")

    # Download con rate limiting
    print(f"\n[2] Download con delay di 2 secondi tra le richieste...")
    results = download_multiple_pages(urls, delay=2.0)

    # Parsing e salvataggio
    print("\n[3] Parsing e salvataggio...")
    all_data = []

    for result in results:
        if result['status'] == 'success':
            print(f"  Parsing: {result['url']}")
            dati = parse_html_basic(result['html'])
            dati['url'] = result['url']
            all_data.append(dati)

    # Salvataggio
    if all_data:
        save_to_json(all_data, 'esempio_2_multi_output.json')

        # Creiamo anche un CSV semplificato
        csv_data = []
        for dati in all_data:
            csv_data.append({
                'url': dati['url'],
                'titolo': dati.get('title', ''),
                'n_link': len(dati.get('links', [])),
                'n_h1': len(dati.get('headings', {}).get('h1', [])),
                'n_img': len(dati.get('images', []))
            })

        save_to_csv(csv_data, 'esempio_2_multi_output.csv')

        print("\n[OK] Esempio 2 completato!")
        print("     File creati:")
        print("     - esempio_2_multi_output.json")
        print("     - esempio_2_multi_output.csv")


def esempio_3_estrazione_testo():
    """
    ESEMPIO 3: Estrazione Contenuto Testuale
    -----------------------------------------
    Scarica una pagina e estrae solo il contenuto testuale pulito.
    Utile per analisi testo, NLP, etc.
    """
    print("\n" + "="*70)
    print("ESEMPIO 3: Estrazione Contenuto Testuale")
    print("="*70)

    # URL di un articolo o pagina testuale
    url = "https://quotes.toscrape.com/"

    print(f"\n[1] Target: {url}")

    # Download
    html = download_page(url)
    if not html:
        print("[ERRORE] Download fallito!")
        return

    # Estrazione testo
    print("\n[2] Estrazione contenuto testuale...")
    text_data = extract_text_content(html)

    # Mostra statistiche
    print("\n[3] Statistiche:")
    print(f"  - Titolo: {text_data['title']}")
    print(f"  - Paragrafi trovati: {len(text_data['paragraphs'])}")
    print(f"  - Totale parole: {text_data['word_count']}")

    # Mostra primi paragrafi
    print("\n[4] Prime 3 paragrafi:")
    for i, p in enumerate(text_data['paragraphs'][:3], 1):
        print(f"  {i}. {p[:100]}...")

    # Salvataggio
    text_data['url'] = url
    save_to_json(text_data, 'esempio_3_testo.json')

    print("\n[OK] Esempio 3 completato!")


def esempio_4_csv_personalizzato():
    """
    ESEMPIO 4: Export CSV Personalizzato
    -------------------------------------
    Scarica dati e crea un CSV con colonne personalizzate.
    """
    print("\n" + "="*70)
    print("ESEMPIO 4: Export CSV Personalizzato")
    print("="*70)

    url = "https://quotes.toscrape.com/"

    print(f"\n[1] Target: {url}")

    # Download e parsing
    html = download_page(url)
    if not html:
        print("[ERRORE] Download fallito!")
        return

    # Parsing
    soup = __import__('bs4').BeautifulSoup(html, 'html.parser')

    # Estrazione quote specifiche per questo sito
    quotes = []
    quote_elements = soup.find_all('div', class_='quote')

    print(f"\n[2] Trovate {len(quote_elements)} citazioni")

    for i, q_elem in enumerate(quote_elements, 1):
        text = q_elem.find('span', class_='text').get_text(strip=True)
        author = q_elem.find('small', class_='author').get_text(strip=True)
        tags = [t.get_text(strip=True) for t in q_elem.find_all('a', class_='tag')]

        quote = {
            'id': i,
            'text': text,
            'author': author,
            'tags': ', '.join(tags),
            'tags_count': len(tags)
        }
        quotes.append(quote)
        print(f"  [{i}] {author}: {text[:50]}...")

    # Salvataggio CSV
    if quotes:
        # Specifica l'ordine delle colonne
        fieldnames = ['id', 'author', 'text', 'tags_count', 'tags']
        save_to_csv(quotes, 'esempio_4_quotes.csv', fieldnames=fieldnames)

        print(f"\n[OK] Salvate {len(quotes)} citazioni in 'esempio_4_quotes.csv'")


def main():
    """
    Menu principale per scegliere quale esempio eseguire.
    """
    print("\n" + "="*70)
    print(" ESEMPI DI UTILIZZO WEB SCRAPER")
    print("="*70)
    print("\nScegli quale esempio eseguire:\n")
    print("  1. Scraping base di una singola pagina")
    print("  2. Scraping multi-pagina con rate limiting")
    print("  3. Estrazione contenuto testuale")
    print("  4. Export CSV personalizzato")
    print("  0. Esci")

    while True:
        choice = input("\nScelta [0-4]: ").strip()

        if choice == '1':
            esempio_1_scraping_base()
            break
        elif choice == '2':
            esempio_2_multi_pagina()
            break
        elif choice == '3':
            esempio_3_estrazione_testo()
            break
        elif choice == '4':
            esempio_4_csv_personalizzato()
            break
        elif choice == '0':
            print("\nArrivederci!")
            break
        else:
            print("[!] Scelta non valida. Riprova.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interruzione dall'utente")
        print("[*] Chiusura programma...\n")
