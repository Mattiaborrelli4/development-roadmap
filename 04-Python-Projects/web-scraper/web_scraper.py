#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
WEB SCRAPER DIDATTICO
==============================================================================
Un web scraper completo con scopo educativo per imparare il web scraping.

Questo script dimostra:
- Download di pagine web con requests
- Parsing HTML con BeautifulSoup4
- Gestione errori robusta
- Salvataggio dati in CSV e JSON
- Rate limiting per evitare di sovraccaricare i server
- CLI interattiva per l'utente

Autore: Project Didattico
Licenza: Educational Use Only
==============================================================================
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import sys
from typing import List, Dict, Optional


# ============================================================================
# COSTANTI GLOBALI
# ============================================================================

# User-Agent per simulare un browser reale
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Timeout predefinito per le richieste (in secondi)
DEFAULT_TIMEOUT = 10

# Delay predefinito tra le richieste (in secondi)
DEFAULT_DELAY = 2

# Numero massimo di retry per le richieste fallite
MAX_RETRIES = 3


# ============================================================================
# FUNZIONI DI DOWNLOAD
# ============================================================================

def download_page(url: str, timeout: int = DEFAULT_TIMEOUT,
                  max_retries: int = MAX_RETRIES) -> Optional[str]:
    """
    Scarica il contenuto HTML di una pagina web con gestione errori robusta.

    Implementa:
    - Retry con backoff esponenziale
    - Timeout configurabile
    - Gestione di tutti gli errori comuni di rete
    - Headers realistici per evitare blocchi

    Args:
        url: URL della pagina da scaricare
        timeout: Tempo massimo di attesa in secondi
        max_retries: Numero massimo di tentativi in caso di fallimento

    Returns:
        Contenuto HTML della pagina come stringa, oppure None se fallito

    Esempio:
        >>> html = download_page("https://example.com")
        >>> if html:
        ...     print("Pagina scaricata con successo")
    """
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Mostra progresso
            print(f"[*] Scaricamento: {url}")
            if retry_count > 0:
                print(f"    Tentativo {retry_count + 1}/{max_retries}")

            # Effettua la richiesta HTTP GET
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=timeout
            )

            # Verifica che la risposta sia positiva (codice 200)
            response.raise_for_status()

            # Verifica che il contenuto sia HTML
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                print(f"[!] Attenzione: Content-Type non HTML: {content_type}")

            print(f"[OK] Download completato ({len(response.content)} bytes)")
            return response.text

        except requests.exceptions.Timeout:
            retry_count += 1
            if retry_count < max_retries:
                # Backoff esponenziale: 2^retry_count secondi
                wait_time = 2 ** retry_count
                print(f"[!] Timeout - Attendo {wait_time}s prima di riprovare...")
                time.sleep(wait_time)
            else:
                print(f"[ERRORE] Timeout dopo {max_retries} tentativi")

        except requests.exceptions.ConnectionError:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                print(f"[!] Errore connessione - Attendo {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"[ERRORE] Impossibile connettersi dopo {max_retries} tentativi")

        except requests.exceptions.HTTPError as e:
            # Gestione specifica per diversi codici HTTP
            status_code = e.response.status_code

            if status_code == 404:
                print(f"[ERRORE] Pagina non trovata (404)")
            elif status_code == 403:
                print(f"[ERRORE] Accesso negato (403) - Possibile blocco anti-bot")
            elif status_code == 500:
                print(f"[ERRORE] Errore interno del server (500)")
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    print(f"    Attendo {wait_time}s prima di riprovare...")
                    time.sleep(wait_time)
                    continue
            else:
                print(f"[ERRORE] Codice HTTP: {status_code}")

            # Per errori HTTP non facciamo retry
            return None

        except requests.exceptions.RequestException as e:
            print(f"[ERRORE] Errore nella richiesta: {e}")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(2 ** retry_count)
            else:
                return None

        except Exception as e:
            print(f"[ERRORE] Errore imprevisto: {type(e).__name__}: {e}")
            return None

    return None


def download_multiple_pages(urls: List[str], delay: float = DEFAULT_DELAY,
                           timeout: int = DEFAULT_TIMEOUT,
                           max_pages: Optional[int] = None) -> List[Dict]:
    """
    Scarica multiple pagine web con rate limiting.

    Implementa:
    - Delay tra le richieste per rispettare il server
    - Limite opzionale sul numero di pagine
    - Progress indicator
    - Raccolta dei risultati con statistiche

    Args:
        urls: Lista di URL da scaricare
        delay: Secondi di attesa tra ogni richiesta
        timeout: Timeout per ogni singola richiesta
        max_pages: Numero massimo di pagine da scaricare (None = tutte)

    Returns:
        Lista di dizionari con url, html, e status per ogni pagina

    Esempio:
        >>> urls = ["https://site1.com", "https://site2.com"]
        >>> results = download_multiple_pages(urls, delay=1)
    """
    results = []
    successful = 0
    failed = 0

    # Applica il limite se specificato
    if max_pages:
        urls = urls[:max_pages]

    total = len(urls)
    print(f"\n[*] Inizio download di {total} pagine...")
    print(f"[*] Delay tra richieste: {delay} secondi\n")

    for i, url in enumerate(urls, 1):
        print(f"--- Pagina {i}/{total} ---")

        # Scarica la pagina
        html = download_page(url, timeout=timeout)

        if html:
            results.append({
                'url': url,
                'html': html,
                'status': 'success'
            })
            successful += 1
        else:
            results.append({
                'url': url,
                'html': None,
                'status': 'failed'
            })
            failed += 1

        # Rate limiting: attendi prima della prossima richiesta
        if i < total:  # Non attendere dopo l'ultima
            print(f"[*] Attendo {delay} secondi...\n")
            time.sleep(delay)

    # Stampa statistiche finali
    print(f"\n{'='*60}")
    print(f"RIEPILOGO DOWNLOAD")
    print(f"{'='*60}")
    print(f"[+] Totale pagine processate: {total}")
    print(f"[+] Successi: {successful}")
    print(f"[+] Fallimenti: {failed}")
    print(f"{'='*60}\n")

    return results


# ============================================================================
# FUNZIONI DI PARSING
# ============================================================================

def parse_html_basic(html: str) -> Dict[str, any]:
    """
    Effettua il parsing base di un documento HTML.

    Estrae informazioni comuni presenti nella maggior parte delle pagine:
    - Titolo della pagina
    - Meta description
    - Tutti i link
    - Tutti gli headings (h1, h2, h3)
    - Tutte le immagini

    Args:
        html: Contenuto HTML come stringa

    Returns:
        Dizionario con tutti i dati estratti

    Esempio:
        >>> html = "<html><head><title>Test</title></head></html>"
        >>> data = parse_html_basic(html)
        >>> print(data['title'])
        'Test'
    """
    # Crea l'oggetto BeautifulSoup per il parsing
    soup = BeautifulSoup(html, 'html.parser')

    result = {
        'title': None,
        'description': None,
        'links': [],
        'headings': {
            'h1': [],
            'h2': [],
            'h3': []
        },
        'images': []
    }

    # Estrai il titolo della pagina
    try:
        title_tag = soup.find('title')
        if title_tag:
            result['title'] = title_tag.get_text(strip=True)
            print(f"[+] Titolo trovato: {result['title']}")
        else:
            print("[!] Nessun titolo trovato")
    except Exception as e:
        print(f"[!] Errore nell'estrazione del titolo: {e}")

    # Estrai la meta description
    try:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            result['description'] = meta_desc['content']
            print(f"[+] Description trovata: {result['description'][:50]}...")
    except Exception as e:
        print(f"[!] Errore nell'estrazione della description: {e}")

    # Estrai tutti i link (anchor tags)
    try:
        links = soup.find_all('a', href=True)
        result['links'] = [link['href'].strip() for link in links]
        print(f"[+] Trovati {len(result['links'])} link")
    except Exception as e:
        print(f"[!] Errore nell'estrazione dei link: {e}")

    # Estrai gli headings
    for level in ['h1', 'h2', 'h3']:
        try:
            headings = soup.find_all(level)
            result['headings'][level] = [
                h.get_text(strip=True) for h in headings
            ]
            if result['headings'][level]:
                print(f"[+] Trovati {len(result['headings'][level])} tag {level.upper()}")
        except Exception as e:
            print(f"[!] Errore nell'estrazione dei {level}: {e}")

    # Estrai le immagini
    try:
        images = soup.find_all('img', src=True)
        result['images'] = [
            {
                'src': img['src'],
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            }
            for img in images
        ]
        print(f"[+] Trovate {len(result['images'])} immagini")
    except Exception as e:
        print(f"[!] Errore nell'estrazione delle immagini: {e}")

    return result


def parse_products_demo(html: str) -> List[Dict]:
    """
    Funzione demo per estrarre dati di prodotti da HTML.

    Questa e' una funzione didattica che mostra come estrarre:
    - Nomi dei prodotti
    - Prezzi
    - Descrizioni
    - Link ai prodotti

    NOTA: I selector CSS dipendono dalla struttura del sito target.
    Questa e' una struttura generica a scopo dimostrativo.

    Args:
        html: Contenuto HTML della pagina con prodotti

    Returns:
        Lista di dizionari, uno per prodotto

    Esempio:
        >>> products = parse_products_demo(html)
        >>> for p in products:
        ...     print(f"{p['name']}: {p['price']}")
    """
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    # STRUTTURA GENERICA DA ADATTARE:
    # I selector vanno modificati in base al sito reale!

    try:
        # Cerca container di prodotti (varia da sito a sito)
        # Esempi di selector comuni:
        # - soup.find_all('div', class_='product')
        # - soup.select('.product-item')
        # - soup.find_all('article', class_='product-card')

        # Per questa demo, cerchiamo elementi con classe 'product'
        product_containers = soup.find_all('div', class_=lambda x: x and (
            'product' in x.lower() or
            'item' in x.lower() or
            'card' in x.lower()
        ), limit=20)  # Limitiamo a 20 per la demo

        if not product_containers:
            print("[!] Nessun prodotto trovato con i selector generici")
            print("[*] Suggerimento: Ispeziona il HTML e adatta i selector")
            return products

        print(f"[*] Trovati {len(product_containers)} potenziali prodotti")

        for i, container in enumerate(product_containers, 1):
            product = {
                'name': None,
                'price': None,
                'description': None,
                'link': None
            }

            # Estrai nome prodotto (cerca in vari tag comuni)
            for tag in ['h2', 'h3', 'h4', 'span', 'div']:
                name_elem = container.find(tag, class_=lambda x: x and (
                    'name' in x.lower() or 'title' in x.lower()
                ))
                if name_elem:
                    product['name'] = name_elem.get_text(strip=True)
                    break

            # Se non trovato con class, prova il primo heading
            if not product['name']:
                for tag in ['h2', 'h3', 'h4']:
                    name_elem = container.find(tag)
                    if name_elem:
                        product['name'] = name_elem.get_text(strip=True)
                        break

            # Estrai prezzo (cerca pattern comuni)
            for tag in ['span', 'div', 'p']:
                price_elem = container.find(tag, class_=lambda x: x and (
                    'price' in x.lower() or 'cost' in x.lower()
                ))
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Verifica che contenga numeri o simboli di valuta
                    if any(c in price_text for c in ['EUR', '€', '$', '£', '¥']) or \
                       any(c.isdigit() for c in price_text):
                        product['price'] = price_text
                        break

            # Estrai link prodotto
            link_elem = container.find('a', href=True)
            if link_elem:
                product['link'] = link_elem['href']

            # Aggiungi solo se abbiamo almeno un nome
            if product['name']:
                products.append(product)
                print(f"[+] Prodotto {i}: {product['name'][:50]}")

    except Exception as e:
        print(f"[!] Errore nel parsing dei prodotti: {e}")

    return products


def extract_text_content(html: str) -> Dict[str, any]:
    """
    Estrae solo il contenuto testuale da una pagina HTML.

    Utile per analizzare il contenuto di articoli, blog, documenti.

    Args:
        html: Contenuto HTML

    Returns:
        Dizionario con testo strutturato
    """
    soup = BeautifulSoup(html, 'html.parser')

    result = {
        'title': '',
        'paragraphs': [],
        'word_count': 0
    }

    try:
        # Rimuovi script e style (non ci interessano)
        for script in soup(['script', 'style']):
            script.decompose()

        # Estrai titolo
        if soup.title:
            result['title'] = soup.title.get_text(strip=True)

        # Estrai tutti i paragrafi
        paragraphs = soup.find_all('p')
        result['paragraphs'] = [
            p.get_text(strip=True) for p in paragraphs
            if p.get_text(strip=True)
        ]

        # Conta le parole totali
        all_text = ' '.join(result['paragraphs'])
        result['word_count'] = len(all_text.split())

        print(f"[+] Estratti {len(result['paragraphs'])} paragrafi")
        print(f"[+] Totale parole: {result['word_count']}")

    except Exception as e:
        print(f"[!] Errore nell'estrazione del testo: {e}")

    return result


# ============================================================================
# FUNZIONI DI SALVATAGGIO
# ============================================================================

def save_to_csv(data: List[Dict], filename: str,
                fieldnames: Optional[List[str]] = None) -> bool:
    """
    Salva i dati in un file CSV con encoding UTF-8.

    Args:
        data: Lista di dizionari da salvare
        filename: Nome del file CSV
        fieldnames: Lista ordinata di colonne (opzionale)

    Returns:
        True se salvataggio riuscito, False altrimenti

    Esempio:
        >>> data = [{'name': 'A', 'price': '10€'}, {'name': 'B', 'price': '20€'}]
        >>> save_to_csv(data, 'output.csv')
    """
    if not data:
        print("[!] Nessun dato da salvare")
        return False

    try:
        # Se non specificato, deduci le colonne dai dati
        if fieldnames is None:
            fieldnames = list(data[0].keys())

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Scrivi l'header
            writer.writeheader()

            # Scrivi le righe
            writer.writerows(data)

        print(f"[OK] Salvati {len(data)} record in: {filename}")
        return True

    except PermissionError:
        print(f"[ERRORE] Permesso negato: impossibile scrivere {filename}")
        print("    Chiudi il file se e' aperto in un altro programma")
        return False

    except Exception as e:
        print(f"[ERRORE] Impossibile salvare CSV: {e}")
        return False


def save_to_json(data: any, filename: str, indent: int = 2) -> bool:
    """
    Salva i dati in un file JSON con encoding UTF-8.

    Args:
        data: Dati da salvare (dict, list, etc.)
        filename: Nome del file JSON
        indent: Numero di spazi per indentazione (default: 2)

    Returns:
        True se salvataggio riuscito, False altrimenti

    Esempio:
        >>> data = {'products': [{'name': 'A', 'price': 10}]}
        >>> save_to_json(data, 'output.json')
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=indent)

        print(f"[OK] Dati salvati in: {filename}")
        return True

    except PermissionError:
        print(f"[ERRORE] Permesso negato: impossibile scrivere {filename}")
        return False

    except TypeError as e:
        print(f"[ERRORE] Dati non serializzabili in JSON: {e}")
        return False

    except Exception as e:
        print(f"[ERRORE] Impossibile salvare JSON: {e}")
        return False


def save_scraping_results(results: List[Dict], output_format: str,
                          base_filename: str = 'scraping_results') -> List[str]:
    """
    Salva i risultati dello scraping nel formato specificato.

    Args:
        results: Lista di risultati con dati estratti
        output_format: 'csv', 'json', o 'both'
        base_filename: Nome base per i file (senza estensione)

    Returns:
        Lista dei file creati con successo
    """
    saved_files = []

    if output_format in ['csv', 'both']:
        csv_filename = f"{base_filename}.csv"

        # Appiattisci i dati per CSV
        csv_data = []
        for result in results:
            flat_data = {
                'url': result.get('url', ''),
                'title': result.get('title', ''),
                'description': result.get('description', ''),
                'link_count': len(result.get('links', [])),
                'h1_count': len(result.get('headings', {}).get('h1', [])),
                'h2_count': len(result.get('headings', {}).get('h2', [])),
                'image_count': len(result.get('images', []))
            }
            csv_data.append(flat_data)

        if save_to_csv(csv_data, csv_filename):
            saved_files.append(csv_filename)

    if output_format in ['json', 'both']:
        json_filename = f"{base_filename}.json"

        if save_to_json(results, json_filename):
            saved_files.append(json_filename)

    return saved_files


# ============================================================================
# FUNZIONI DI UTILITA'
# ============================================================================

def validate_url(url: str) -> bool:
    """
    Validazione base di un URL.

    Args:
        url: URL da validare

    Returns:
        True se l'URL sembra valido, False altrimenti
    """
    if not url:
        return False

    # Controllo base: deve iniziare con http:// o https://
    if not url.startswith(('http://', 'https://')):
        print(f"[!] URL non valido: deve iniziare con http:// o https://")
        return False

    # Controllo base lunghezza
    if len(url) < 10 or len(url) > 2000:
        print(f"[!] URL non valido: lunghezza non valida")
        return False

    return True


def check_robots_txt(url: str) -> None:
    """
    Controlla robots.txt per verificare se lo scraping e' permesso.

    NOTA: Questa e' una versione semplificata a scopo didattico.
    Per produzione, usa la libreria 'urllib.robotparser'.

    Args:
        url: URL del sito da controllare
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        print(f"[*] Controllo robots.txt: {robots_url}")
        response = requests.get(robots_url, timeout=5, headers=HEADERS)

        if response.status_code == 200:
            print("[+] robots.txt trovato:")
            print("-" * 60)
            # Mostra prime righe
            lines = response.text.split('\n')[:10]
            for line in lines:
                print(f"  {line}")
            if len(response.text.split('\n')) > 10:
                print("  ...")
            print("-" * 60)
            print("[!] Ricorda di rispettare le regole del robots.txt!")
        else:
            print("[*] Nessun robots.txt trovato")

    except Exception as e:
        print(f"[!] Impossibile controllare robots.txt: {e}")


def print_banner() -> None:
    """Mostra il banner del programma."""
    banner = """
==============================================================================
                    WEB SCRAPER DIDATTICO v1.0
==============================================================================
Un tool educativo per imparare il web scraping in Python

Funzionalita':
  - Download di pagine web con retry e gestione errori
  - Parsing HTML con BeautifulSoup
  - Estrazione di titoli, link, headings, immagini
  - Salvataggio in CSV e JSON
  - Rate limiting per non sovraccaricare i server

AVVERTENZA: Usa questo scraper in modo responsabile!
  - Rispetta robots.txt
  - Non fare troppe richieste in poco tempo
  - Non usare per scopi commerciali senza permesso
==============================================================================
"""
    print(banner)


# ============================================================================
# INTERFACCIA CLI INTERATTIVA
# ============================================================================

def interactive_mode() -> None:
    """
    Modalita' interattiva con menu per l'utente.

    Guida l'utente attraverso:
    1. Inserimento URL
    2. Scelta formato output
    3. Esecuzione scraping
    4. Salvataggio risultati
    """
    print_banner()

    print("\n[MODALITA' INTERATTIVA]")
    print("-" * 60)

    # 1. Richiedi URL
    while True:
        print("\nInserisci l'URL da analizzare (o 'quit' per uscire):")
        url = input("URL> ").strip()

        if url.lower() in ['quit', 'exit', 'q']:
            print("\n[*] Uscita dal programma...")
            return

        if validate_url(url):
            break

    # 2. Check robots.txt (opzionale ma consigliato)
    print("\nVuoi controllare robots.txt prima di procedere? (raccomandato)")
    check = input("Controllare robots.txt? [s/N]: ").strip().lower()
    if check in ['s', 'si', 'y', 'yes']:
        check_robots_txt(url)
        print("\nPremi Invio per continuare...")
        input()

    # 3. Scegli formato output
    print("\nFormato di output desiderato:")
    print("  1. CSV")
    print("  2. JSON")
    print("  3. Entrambi (CSV + JSON)")

    while True:
        choice = input("\nScelta [1-3]: ").strip()
        if choice == '1':
            output_format = 'csv'
            break
        elif choice == '2':
            output_format = 'json'
            break
        elif choice == '3':
            output_format = 'both'
            break
        else:
            print("[!] Scelta non valida. Riprova.")

    # 4. Scegli delay tra richieste
    print("\nImposta il delay tra le richieste (in secondi):")
    print("  Raccomandato: 2-5 secondi")
    print("  Minimo: 1 secondo")

    while True:
        try:
            delay = float(input("Delay [default: 2]: ").strip() or "2")
            if delay >= 1:
                break
            else:
                print("[!] Il delay deve essere almeno 1 secondo")
        except ValueError:
            print("[!] Inserisci un numero valido")

    # 5. Conferma e avvia
    print("\n" + "=" * 60)
    print("RIEPILOGO CONFIGURAZIONE")
    print("=" * 60)
    print(f"  URL: {url}")
    print(f"  Output: {output_format.upper()}")
    print(f"  Delay: {delay} secondi")
    print("=" * 60)

    confirm = input("\nProcedere con lo scraping? [s/N]: ").strip().lower()
    if confirm not in ['s', 'si', 'y', 'yes']:
        print("\n[*] Operazione annullata dall'utente")
        return

    # 6. ESECUZIONE SCRAPER
    print("\n" + "=" * 60)
    print("INIZIO SCRAPER")
    print("=" * 60 + "\n")

    # Download pagina
    html = download_page(url)

    if not html:
        print("\n[ERRORE] Impossibile procedere senza il contenuto HTML")
        return

    # Parsing HTML
    print("\n[*] Inizio parsing HTML...")
    parsed_data = parse_html_basic(html)

    # Mostra risultati
    print("\n" + "=" * 60)
    print("RISULTATI PARSING")
    print("=" * 60)

    if parsed_data['title']:
        print(f"\n[+] TITOLO:")
        print(f"    {parsed_data['title']}")

    if parsed_data['description']:
        print(f"\n[+] DESCRIPTION:")
        print(f"    {parsed_data['description'][:100]}...")

    print(f"\n[+] STATISTICHE:")
    print(f"    Link trovati: {len(parsed_data['links'])}")
    print(f"    H1 trovati: {len(parsed_data['headings']['h1'])}")
    print(f"    H2 trovati: {len(parsed_data['headings']['h2'])}")
    print(f"    Immagini trovate: {len(parsed_data['images'])}")

    # Mostra alcuni link come esempio
    if parsed_data['links']:
        print(f"\n[+] PRIMI 5 LINK:")
        for i, link in enumerate(parsed_data['links'][:5], 1):
            print(f"    {i}. {link}")

    # 7. Salvataggio
    print("\n" + "=" * 60)
    print("SALVATAGGIO RISULTATI")
    print("=" * 60)

    # Prepara i dati per il salvataggio
    save_data = [{
        'url': url,
        'title': parsed_data.get('title', ''),
        'description': parsed_data.get('description', ''),
        'links': parsed_data.get('links', []),
        'headings': parsed_data.get('headings', {}),
        'images': parsed_data.get('images', [])
    }]

    saved_files = save_scraping_results(save_data, output_format)

    if saved_files:
        print(f"\n[OK] Salvataggio completato!")
        print(f"[+] File creati:")
        for filename in saved_files:
            print(f"    - {filename}")
    else:
        print("\n[ERRORE] Nessun file creato")

    print("\n" + "=" * 60)
    print("SCRAPER COMPLETATO")
    print("=" * 60 + "\n")


def batch_mode(urls: List[str], output_format: str = 'json',
               delay: float = DEFAULT_DELAY) -> None:
    """
    Modalita' batch per processare multiple URL.

    Args:
        urls: Lista di URL da processare
        output_format: Formato di output ('csv', 'json', 'both')
        delay: Secondi tra le richieste
    """
    print(f"\n[MODALITA' BATCH] - {len(urls)} URL da processare\n")

    # Download pagine
    results = download_multiple_pages(urls, delay=delay)

    # Parsing dei risultati
    print("\n[*] Inizio parsing HTML...")
    all_data = []

    for result in results:
        if result['status'] == 'success' and result['html']:
            print(f"\n[*] Parsing: {result['url']}")
            parsed = parse_html_basic(result['html'])
            parsed['url'] = result['url']
            all_data.append(parsed)

    # Salvataggio
    if all_data:
        saved_files = save_scraping_results(all_data, output_format)
        print(f"\n[OK] Batch completato! File creati: {saved_files}")
    else:
        print("\n[!] Nessun dato da salvare")


def main():
    """
    Funzione principale del programma.

    Gestisce:
    - Argomenti da riga di comando
    - Modalita' interattiva
    - Modalita' batch
    """
    # Se ci sono argomenti da riga di comando
    if len(sys.argv) > 1:
        # Modalita' batch: python web_scraper.py url1 url2 url3 ...
        urls = sys.argv[1:]
        valid_urls = [u for u in urls if validate_url(u)]

        if valid_urls:
            batch_mode(valid_urls)
        else:
            print("[ERRORE] Nessun URL valido fornito")
    else:
        # Modalita' interattiva
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n[!] Interruzione dall'utente (Ctrl+C)")
            print("[*] Chiusura programma...\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Punto di ingresso dello script.

    Esempi di utilizzo:

    # Modalita' interattiva:
    python web_scraper.py

    # Modalita' batch con URL specifici:
    python web_scraper.py https://example.com https://example.org

    # Nota: Questo script e' a scopo didattico.
    # Usare sempre robots.txt e rispettare i Termini di Servizio.
    """
    main()
