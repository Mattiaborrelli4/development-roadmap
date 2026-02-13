# 🕷️ Web Scraper - Python Project

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production-ready-brightgreen.svg)

> **Utility Python professionale per estrarre dati da siti web in modo etico ed efficiente**

Una soluzione completa per il web scraping che combina semplicità d'uso con best practices industriali. Ideale per studenti che vogliono imparare l'automazione web e per sviluppatori che cercano un tool affidabile per il proprio portfolio.

---

## 📋 Indice

- [Introduzione](#introduzione)
- [Perché questo Progetto](#perché-questo-progetto)
- [Caratteristiche](#caratteristiche)
- [Installazione](#installazione)
- [Utilizzo Rapido](#utilizzo-rapido)
- [Spiegazione del Codice](#spiegazione-del-codice)
- [Moduli e Librerie](#moduli-e-librerie)
- [Esempi Pratici](#esempi-pratici)
- [Etica dello Scraping](#etica-dello-scraping)
- [Troubleshooting](#troubleshooting)
- [Esercizi Proposti](#esercizi-proposti)
- [Risorse Utili](#risorse-utili)

---

## 🎯 Introduzione

### Cos'è il Web Scraping?

Il **Web Scraping** (o web harvesting) è la tecnica di estrarre automaticamente dati da siti web. Immagina di poter copiare-incollare informazioni da migliaia di pagine web in pochi secondi: questo è ciò che fa un web scraper.

### Cosa fa questo progetto?

Questo script Python ti permette di:

- 📥 **Scaricare** pagine web automaticamente
- 🔍 **Estrarre** testo, link e immagini
- 💾 **Salvare** i dati in formato JSON o CSV
- ⏱️ **Gestire** il rate limiting per essere gentili con i server
- 🛡️ **Rispettare** le best practices etiche

### Output Esempio

```json
{
  "url": "https://example.com",
  "status_code": 200,
  "timestamp": "2024-01-15 14:30:22",
  "title": "Example Domain",
  "description": "",
  "body": "Example Domain This domain is for use in illustrative...",
  "links_count": 1,
  "links": [
    {
      "text": "More information...",
      "href": "https://www.iana.org/domains/example"
    }
  ],
  "images_count": 0,
  "images": []
}
```

---

## 💡 Perché questo Progetto

### Valore Didattico

Per **studenti e principianti**:

- ✅ Impara la programmazione Python con un progetto pratico
- ✅ Capisci come funziona il web (HTTP, HTML, DOM)
- ✅ Sviluppa competenze richieste nel mercato del lavoro
- ✅ Prepara base per Data Science e Machine Learning

**Tempo stimato per completarlo**: 2-4 ore
**Difficoltà**: ⭐⭐☆☆☆ (Intermedia)

### Valore Portfolio

Per **sviluppatori junior**:

- 🎨 Dimostra capacità di automazione
- 🌐 Mostra competenze web e API
- 📊 Esperti a estrazione e analisi dati
- 🚀 Progetto reale da mostrare ai recruiter

### Casi d'Uso Reali

| Settore | Applicazione |
|---------|--------------|
| **Marketing** | Monitoraggio prezzi competitor |
| **Journalism** | Analisi tendenze e fact-checking |
| **Finance** | Raccolta dati finanziari |
| **Research** | Analisi social media e opinioni |
| **E-commerce** | Comparazione prezzi prodotti |

---

## ⭐ Caratteristiche

### Funzionalità Principali

```python
✅ Download pagine web con requests
✅ Parsing HTML con BeautifulSoup
✅ Estrazione link, immagini e testo
✅ Export JSON e CSV
✅ Rate limiting configurabile
✅ Gestione errori robusta
✅ Supporto multi-pagina
✅ User-Agent personalizzabile
```

### Cosa NON fare

- ❌ Violare Termini di Servizio
- ❌ Scraping senza autorizzazione
- ❌ Overload dei server
- ❌ Accesso a dati personali senza consenso
- ❌ Bypassare sistemi di sicurezza

---

## 🚀 Installazione

### Prerequisiti

- **Python 3.7+** installato ([Scarica Python](https://www.python.org/downloads/))
- Accesso a internet
- Un editor di codice (VS Code, PyCharm, o anche Notepad++)

### Setup del Progetto

```bash
# 1. Clona o scarica il progetto
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\web-scraper"

# 2. Crea un ambiente virtuale (raccomandato)
python -m venv venv

# 3. Attiva l'ambiente virtuale
# Su Windows:
venv\Scripts\activate
# Su Linux/Mac:
source venv/bin/activate

# 4. Installa le dipendenze
pip install requests beautifulsoup4

# 5. Verifica l'installazione
python -c "import requests; import bs4; print('Pronto!')"
```

### Installazione Rapida

```bash
pip install requests beautifulsoup4
```

---

## 💻 Utilizzo Rapido

### 1. Scraping Singola Pagina (JSON)

```python
from web_scraper import scrape_page

# Scarica e salva in JSON
scrape_page("https://example.com", output_format='json')
```

**Output**: `scrape_20240115_143022.json`

### 2. Scraping Singola Pagina (CSV - solo link)

```python
from web_scraper import scrape_page

# Scarica e salva i link in CSV
scrape_page("https://example.com", output_format='csv')
```

**Output**: `links_20240115_143022.csv`

### 3. Scraping Multi-Pagina

```python
from web_scraper import scrape_multiple_pages

# Lista di URL da scaricare
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

# Scarica con 2 secondi di delay
scrape_multiple_pages(urls, delay=2.0)
```

### 4. Esecuzione Diretta

```bash
# Esegui lo script principale
python web_scraper.py
```

### Esempio Completo con Sito Reale

```python
#!/usr/bin/env python3
from web_scraper import get_page, parse_html, extract_text_content, save_to_json

# Scraping di un articolo di notizie
url = "https://www.reuters.com/world/europe/"

# 1. Download
response = get_page(url)

if response:
    # 2. Parsing
    soup = parse_html(response.text)

    # 3. Estrazione dati
    data = extract_text_content(soup)

    # 4. Salvataggio
    save_to_json(data, "notizie.json")
    print("Scraping completato!")
```

---

## 📚 Spiegazione del Codice

### Architettura del Codice

```
web_scraper.py
├── get_page()              # HTTP Client - Scarica le pagine
├── parse_html()            # Parser - Converte HTML in oggetto navigabile
├── extract_links()         # Estrattore link
├── extract_images()        # Estrattore immagini
├── extract_text_content()  # Estrattore contenuto testuale
├── save_to_csv()           # Export CSV
├── save_to_json()          # Export JSON
├── scrape_page()           # Funzione principale (orchestrator)
├── scrape_multiple_pages() # Batch processing
└── main()                  # Entry point
```

### Analisi Funzione per Funzione

#### 1. `get_page(url, headers)` - HTTP Client

```python
def get_page(url: str, headers: Optional[Dict] = None) -> Optional[requests.Response]:
    """Effettua una richiesta HTTP GET"""
    headers = headers or {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Solleva errore per 4xx/5xx
        return response
    except requests.RequestException as e:
        print(f"Errore: {e}")
        return None
```

**Concetti Python**:
- Type hints (`str`, `Optional`, `Dict`)
- Gestione errori con try-except
- Short-circuit evaluation (`or` operator)

#### 2. `parse_html(html_content)` - HTML Parser

```python
def parse_html(html_content: str) -> BeautifulSoup:
    """Parsa il contenuto HTML"""
    return BeautifulSoup(html_content, 'html.parser')
```

**Cos'è BeautifulSoup?**
Libreria che trasforma HTML in un albero navigabile, come il DOM di JavaScript.

```python
# Prima: HTML grezzo
html = "<html><body><h1>Ciao!</h1></body></html>"

# Dopo: Oggetto navigabile
soup = parse_html(html)
soup.h1.text  # "Ciao!"
```

#### 3. `extract_links(soup, base_url)` - Estrazione Link

```python
def extract_links(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """Estrae tutti i link dalla pagina"""
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(base_url, href)  # Converte URL relativi
        links.append({
            'text': link.get_text(strip=True),
            'href': absolute_url
        })
    return links
```

**Concetti chiave**:
- `soup.find_all()` - Trova tutti gli elementi matching
- `urljoin()` - Converte URL relativi in assoluti
- List comprehension pattern

#### 4. `extract_text_content(soup)` - Estrazione Testo

```python
def extract_text_content(soup: BeautifulSoup) -> Dict[str, str]:
    """Estrae il contenuto testuale principale"""
    # Titolo
    title = soup.find('title')
    title_text = title.get_text(strip=True) if title else "Nessun titolo"

    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '') if meta_desc else ''

    # Rimuovi script e style
    for script in soup(['script', 'style']):
        script.decompose()  # Rimuove elemento dal DOM

    # Testo pulito
    body_text = soup.get_text(separator='\n', strip=True)

    return {
        'title': title_text,
        'description': description,
        'body': body_text[:1000]  # Prime 1000 lettere
    }
```

#### 5. `save_to_json(data, filename)` - Export JSON

```python
def save_to_json(data: Dict, filename: str) -> bool:
    """Salva i dati in un file JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Dati salvati in {filename}")
        return True
    except IOError as e:
        print(f"Errore nel salvataggio JSON: {e}")
        return False
```

**Concetti Python**:
- Context manager (`with statement`)
- File I/O con encoding UTF-8
- Gestione errori

#### 6. `scrape_multiple_pages(urls, delay)` - Rate Limiting

```python
def scrape_multiple_pages(urls: List[str], delay: float = 1.0) -> None:
    """Scarica più pagine con un ritardo tra le richieste"""
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Elaborazione: {url}")
        scrape_page(url)

        # Rate limiting con jitter casuale
        if i < len(urls):
            sleep_time = delay + random.uniform(0, 0.5)
            print(f"In attesa di {sleep_time:.1f} secondi...")
            time.sleep(sleep_time)
```

**Perché il Jitter?**
Il jitter (ritardo casuale) previene pattern di traffico sospetti e riduce il rischio di essere bloccati.

---

## 🛠️ Moduli e Librerie

### Requests - HTTP Client

**Installazione**: `pip install requests`

```python
import requests

# GET request
response = requests.get('https://example.com')

# Con headers personalizzati
headers = {'User-Agent': 'MyBot 1.0'}
response = requests.get('https://example.com', headers=headers)

# Gestione errori
try:
    response = requests.get('https://example.com', timeout=10)
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.Timeout:
    print("Timeout!")
```

**Documentazione**: [https://requests.readthedocs.io/](https://requests.readthedocs.io/)

### BeautifulSoup4 - HTML Parser

**Installazione**: `pip install beautifulsoup4`

```python
from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <h1 id="main-title">Benvenuto</h1>
        <div class="content">
            <p>Primo paragrafo</p>
            <p>Secondo paragrafo</p>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Trova per ID
title = soup.find(id='main-title')

# Trova per classe
content = soup.find('div', class_='content')

# Trova tutti i paragrafi
paragraphs = soup.find_all('p')

# CSS Selectors
first_p = soup.select_one('.content p')
all_p = soup.select('.content p')

# Navigazione DOM
parent = title.parent
sibling = title.next_sibling
```

**Selettori CSS comuni**:

| Selettore | Descrizione | Esempio |
|-----------|-------------|---------|
| `tag` | Elemento per tag | `soup.find('a')` |
| `#id` | Elemento per ID | `soup.find(id='header')` |
| `.class` | Elemento per classe | `soup.find(class_='btn')` |
| `[attr]` | Elemento per attributo | `soup.find(href=True)` |
| `parent child` | Discendente | `soup.select('div a')` |

**Documentazione**: [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### CSV - Export Tabellare

```python
import csv

data = [
    {'name': 'Mario', 'age': 30, 'city': 'Roma'},
    {'name': 'Luca', 'age': 25, 'city': 'Milano'}
]

# Scrittura CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
    writer.writeheader()
    writer.writerows(data)

# Lettura CSV
with open('output.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'])
```

### JSON - Export Strutturato

```python
import json

# Dump (Python → JSON)
data = {
    'name': 'Mario',
    'age': 30,
    'hobbies': ['calcio', 'lettura']
}

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Load (JSON → Python)
with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Time - Rate Limiting

```python
import time
import random

# Sleep semplice
time.sleep(2)  # Pausa 2 secondi

# Sleep con jitter
delay = 2 + random.uniform(0, 1)  # 2-3 secondi casuali
time.sleep(delay)

# Timestamp
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
print(timestamp)  # 2024-01-15 14:30:22
```

---

## 🌐 Esempi Pratici

### Siti Consigliati per Praticare

| Categoria | Sito | Difficoltà | Note |
|-----------|------|------------|------|
| **Tutorial** | https://toscrape.com | ⭐☆☆☆☆ | Sito creato apposta per scraping! |
| **Notizie** | https://news.ycombinator.com | ⭐⭐☆☆☆ | Ottimo per testare parsing |
| **Libri** | https://books.toscrape.com | ⭐⭐☆☆☆ | E-commerce demo |
| **Quotes** | https://quotes.toscrape.com | ⭐⭐☆☆☆ | Quotes con autori e tag |
| **Quotazioni** | https://finance.yahoo.com | ⭐⭐⭐☆☆ | Dati finanziari (check TOS) |

### Esempio 1: Scraping Blog Post

```python
from web_scraper import get_page, parse_html, save_to_json

def scrape_blog_post(url):
    response = get_page(url)
    if not response:
        return

    soup = parse_html(response.text)

    # Estrai articolo
    article = {
        'title': soup.find('h1').get_text(strip=True),
        'author': soup.find(class_='author').get_text(strip=True),
        'date': soup.find(class_='date').get_text(strip=True),
        'content': soup.find(class_='article-content').get_text(strip=True)
    }

    save_to_json(article, 'blog_post.json')
```

### Esempio 2: Monitoraggio Prezzi

```python
def scrape_price(url):
    """Scraping prezzo prodotto (pseudo-codice)"""
    response = get_page(url)
    soup = parse_html(response.text)

    # Adatta selettori al sito specifico
    product = {
        'name': soup.find(class_='product-title').get_text(strip=True),
        'price': soup.find(class_='price').get_text(strip=True),
        'availability': soup.find(class_='stock').get_text(strip=True),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    return product

# Loop di monitoraggio
while True:
    price_data = scrape_price("https://example.com/product")
    save_to_json(price_data, 'prices.json')
    time.sleep(3600)  # Ogni ora
```

### Esempio 3: Aggregatore Notizie

```python
def scrape_news_aggregator(urls):
    """Raccogli notizie da più fonti"""
    all_news = []

    for url in urls:
        response = get_page(url)
        soup = parse_html(response.text)

        # Trova tutti gli articoli
        articles = soup.find_all(class_='article')

        for article in articles:
            news_item = {
                'title': article.find('h2').get_text(strip=True),
                'link': article.find('a')['href'],
                'summary': article.find(class_='summary').get_text(strip=True),
                'source': url
            }
            all_news.append(news_item)

        time.sleep(2)  # Rispetta il server!

    return all_news
```

---

## 🛡️ Etica dello Scraping

### Robots.txt - Il File delle Regole

Prima di scraping, **SEMPRE** controlla `https://sito.com/robots.txt`

```
# Esempio robots.txt
User-agent: *
Disallow: /admin/
Disallow: /private/
Crawl-delay: 5

Allow: /public/
```

**Come interpretarlo**:
- `User-agent: *` - Regole per tutti i bot
- `Disallow: /path/` - NON accedere a questi path
- `Crawl-delay: 5` - Attendi 5 secondi tra le richieste
- `Allow: /path/` - Questi path sono permessi

### Controlla il robots.txt

```python
import requests
from urllib.robotparser import RobotFileParser

def can_scrape(url, user_agent='*'):
    """Verifica se lo scraping è permesso dal robots.txt"""
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    return rp.can_fetch(user_agent, url)

# Uso
if can_scrape("https://example.com/page"):
    print("Scraping permesso!")
else
    print("Scraping NON permesso dal robots.txt")
```

### Rate Limiting - Sii Gentile

```python
import time
import random

def polite_request(url):
    """Richiesta HTTP con rate limiting"""
    # Base delay
    delay = 2

    # Jitter casuale (+/- 50%)
    actual_delay = delay * random.uniform(0.5, 1.5)

    print(f"In attesa di {actual_delay:.1f} secondi...")
    time.sleep(actual_delay)

    return get_page(url)
```

### User-Agent - Identificati

```python
# ❌ MALE - Si nasconde
headers = {
    'User-Agent': 'python-requests/2.28.0'
}

# ✅ BENE - Si identifica
headers = {
    'User-Agent': 'MyBot/1.0 (+https://mysite.com/bot; contact@mysite.com)'
}
```

### Checklist Etica

Prima di scraping:

- [ ] Ho letto il `robots.txt`
- [ ] Ho letto i Termini di Servizio
- [ ] Ho implementato rate limiting (1-2 secondi minimo)
- [ ] Uso un User-Agent identificabile
- [ ] Non intasco il server con troppe richieste
- [ ] Non accedo a dati personali senza consenso
- [ ] Non bypasso sistemi di sicurezza
- [ ] I dati sono pubblici e non protetti da copyright
- [ ] Ho un contatto (email) nel User-Agent

---

## 🔧 Troubleshooting

### Errori Comuni

#### 1. ConnectionError - Connessione Fallita

```
requests.exceptions.ConnectionError: HTTPConnectionPool
```

**Cause**:
- Nessuna connessione internet
- Sito offline
- Firewall bloccante
- URL sbagliato

**Soluzioni**:
```python
# Verifica connessione
import requests
try:
    requests.get('https://www.google.com')
    print("Internet OK")
except:
    print("Problema di connessione")

# Prova con timeout
response = requests.get(url, timeout=30)
```

#### 2. HTTPError - Codice di Errore HTTP

```
requests.exceptions.HTTPError: 403 Client Error: Forbidden
```

**Codici comuni**:
- **403 Forbidden** - Accesso negato, probabilmente bloccato
- **404 Not Found** - URL inesistente
- **429 Too Many Requests** - Rate limit superato
- **500 Server Error** - Errore lato server

**Soluzioni**:
```python
# Gestione errori HTTP
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.HTTPError as e:
    if response.status_code == 403:
        print("Bloccato! Prova a cambiare User-Agent o usa API")
    elif response.status_code == 429:
        print("Rate limit! Aumenta il delay tra le richieste")
    else:
        print(f"Errore HTTP: {e}")
```

#### 3. Timeout - Richiesta Lenta

```
requests.exceptions.Timeout: HTTPConnectionPool
```

**Soluzioni**:
```python
# Aumenta timeout
response = requests.get(url, timeout=30)  # 30 secondi

# Timeout separati per connect e read
response = requests.get(url, timeout=(10, 30))
```

#### 4. AttributeError - Parsing Fallito

```python
AttributeError: 'NoneType' object has no attribute 'get_text'
```

**Causa**: L'elemento non esiste nella pagina

**Soluzioni**:
```python
# ❌ Non safe
title = soup.find('h1').get_text()

# ✅ Safe
title_elem = soup.find('h1')
title = title_elem.get_text() if title_elem else "Nessun titolo"

# ✅ Oppure
title = soup.find('h1')
if title:
    print(title.get_text())
```

#### 5. UnicodeEncodeError - Encoding Problem

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Soluzioni**:
```python
# Specifica encoding UTF-8
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

# Per ensure_ascii in JSON
json.dump(data, f, ensure_ascii=False)
```

### Debug Tips

```python
# Abilita logging per requests
import logging
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# Stampa HTML grezzo per debug
response = get_page(url)
print(response.text[:500])  # Prime 500 lettere

# Salva HTML per ispezione manuale
with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
```

---

## ⚖️ Legalità e Considerazioni

### È Legale il Web Scraping?

**Risposta breve**: Dipende.

**Legittimo** quando:
- ✅ Dati sono pubblici
- ✅ Non violi Termini di Servizio
- ✅ Rispetti copyright e database rights
- ✅ Non competa direttamente con il sito
- ✅ Non intasi il server

**Illegale** quando:
- ❌ Accedi a dati riservati/privati
- ❌ Bypassi autenticazione/autorizzazione
- ❌ Violi copyright (riproduzione integrale)
- ❌ Violi CFAA (Computer Fraud and Abuse Act - USA)
- ❌ Scraping massivo per competizione diretta

### Caso Studio: hiQ v. LinkedIn (2019)

**Caso**: hiQ Labs faceva scraping di profili LinkedIn pubblici

**Risultato**: Corte ha stabilito che il scraping di dati **pubblici** è legale

**Ma**:
- LinkedIn ha modificato i ToS per proibirlo
- Serve sempre verificare ToS specifici
- Giurisprudenza varia per paese

### GDPR - Privacy Europe

Se scraping coinvolge dati personali:

- ✅ Base giuridica richiesta (consenso, interesse legittimo)
- ✅ Minimizzazione dati (solo dati necessari)
- ✅ Diritti dell'interessato (accesso, cancellazione)
- ✅ Misure di sicurezza appropriate

### Copyright

**Regola generale**:
- Fatti non sono copyright (dati grezzi)
- Struttura e presentazione possono essere copyright
- Riutilizzo integrale = rischio
- Analisi e aggregazione = generalmente OK

**Best practice**:
- Attribuzione della fonte
- Non riprodurre contenuti integralmente
- Trasforma i dati (analisi, aggregazione)
- Considera fair use per scopi educativi/ricerca

### Responsabilità

**Sei responsabile per**:
- Uso dei dati scaricati
- Danni al server target (overload)
- Violazione ToS e copyright
- Uso improprio dei dati personali

**Disclaimer**: Questo progetto è a scopo educativo. L'autore non è responsabile dell'uso improprio dello script.

---

## 📝 Esercizi Proposti

### Livello 1 - Base (Per Principianti)

#### Esercizio 1.1: Scraping Quotes
Obiettivo: Estrarre tutte le citazioni da https://quotes.toscrape.com

```python
from web_scraper import get_page, parse_html, save_to_json

url = "https://quotes.toscrape.com"

# TODO: Scarica la pagina
response = get_page(url)

# TODO: Parsa l'HTML
soup = parse_html(response.text)

# TODO: Trova tutte le quote
quotes = soup.find_all(class_='quote')

# TODO: Crea lista di dizionari con 'text', 'author', 'tags'
quote_data = []
for quote in quotes:
    # Il tuo codice qui
    pass

# TODO: Salva in JSON
```

#### Esercizio 1.2: Monitoraggio Prezzo Libro
Obiettivo: Tracciare prezzi di libri da https://books.toscrape.com

```python
# TODO: Scrivi funzione che:
# - Scarica pagina di un libro
# - Estrae titolo e prezzo
# - Salva in CSV con timestamp

# TODO: Crea loop che ripete ogni ora
# (usando time.sleep())
```

### Livello 2 - Intermedio

#### Esercizio 2.1: Scraping Multi-Pagina
Obiettivo: Scraping tutte le pagine di un blog

```python
def scrape_all_pages(base_url):
    """Scraping di tutte le pagine con paginazione"""

    page = 1
    all_data = []

    while True:
        # TODO: Costruisci URL della pagina
        url = f"{base_url}?page={page}"

        # TODO: Scarica e parsa
        response = get_page(url)
        if not response:
            break

        soup = parse_html(response.text)

        # TODO: Estrai contenuti
        items = soup.find_all(class_='item')

        if not items:
            break  # Fine paginazione

        # TODO: Aggiungi a all_data
        all_data.extend(extract_items(items))

        page += 1
        time.sleep(2)  # Rate limiting

    return all_data
```

#### Esercizio 2.2: Export Multi-Formato
Obiettivo: Salva dati in tutti e tre i formati

```python
def export_all_formats(data, base_filename):
    """Esporta in JSON, CSV e TXT"""

    # TODO: Salva JSON
    save_to_json(data, f"{base_filename}.json")

    # TODO: Salva CSV
    # (usa csv.DictWriter)

    # TODO: Salva TXT leggibile
    # (formatto testo, non raw dump)
```

### Livello 3 - Avanzato

#### Esercizio 3.1: Schedulazione con Cron
Obiettivo: Automatizza scraping periodico

```python
import schedule
import time

def job():
    """Job da eseguire periodicamente"""
    print("Esecuzione scheduled job...")
    scrape_page("https://example.com")

# TODO: Schedula ogni ora
# schedule.every().hour.do(job)

# TODO: Loop infinito con schedule.run_pending()
```

#### Esercizio 3.2: Analisi Dati
Obiettivo: Analizza i dati scaricati

```python
import json
from collections import Counter

def analyze_scraped_data(json_file):
    """Analizza i dati scaricati"""

    # TODO: Carica JSON
    with open(json_file) as f:
        data = json.load(f)

    # TODO: Statistiche base
    # - Numero totale link
    # - Link più comuni domini
    # - Numero immagini

    # TODO: Visualizza risultati
    # Prova a creare grafici con matplotlib
```

#### Esercizio 3.3: Bot Telegram
Obiettivo: Notifiche Telegram quando trovi nuovi dati

```python
# TODO: Integra con Telegram Bot API
# Quando trovi nuovi dati, invia notifica

# Pseudocodice:
# 1. Scarica dati attuali
# 2. Confronta con dati salvati precedentemente
# 3. Se ci sono differenze, invia notifica
# 4. Salva nuovi dati come "baseline"
```

### Soluzioni

Soluzioni complete disponibili in `exercises/` directory.

---

## 📚 Risorse Utili

### Documentazione Ufficiale

| Libreria | Link |
|---------|------|
| **Requests** | [https://requests.readthedocs.io/](https://requests.readthedocs.io/) |
| **BeautifulSoup** | [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| **Python CSV** | [https://docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html) |
| **Python JSON** | [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html) |

### Tutorial Consigliati

**Italiano**:
- [Python Italia - Web Scraping](https://www.python.it/)
- [DigitalOcean: Web Scraping con Python](https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3)

**Inglese**:
- [Real Python - Web Scraping with BeautifulSoup](https://realpython.com/beautiful-soup-web-scraper-python/)
- [ScrapeCenter - Blog](https://www.scrapehero.com/)
- [Web Scraping with Python (O'Reilly Book)](https://www.oreilly.com/library/view/web-scraping-with/9781491910285/)

### Siti per Praticare

- [http://toscrape.com/](http://toscrape.com/) - Siti demo per scraping
- [https://www.web-scraping-playground.com/](https://www.web-scraping-playground.com/) - Playground interattivo

### Community

- [Reddit - r/webscraping](https://www.reddit.com/r/webscraping/)
- [Stack Overflow - Tag 'web-scraping'](https://stackoverflow.com/questions/tagged/web-scraping)
- [Python Discord](https://discord.gg/python)

### Framework Avanzati

Quando questo progetto diventa troppo limitato:

- **Scrapy** - Framework completo per scraping su larga scala
- **Selenium** - Automazione browser (JavaScript-heavy sites)
- **Playwright** - Modern browser automation
- **APIs** - Quando disponibili, usa APIs invece di scraping!

---

## 🤝 Contributing

Questo è un progetto educativo. Suggerimenti e miglioramenti sono benvenuti!

### Come Contribuire

1. Fork il progetto
2. Crea branch per la feature (`git checkout -b feature/AwesomeFeature`)
3. Commit (`git commit -m 'Add AwesomeFeature'`)
4. Push (`git push origin feature/AwesomeFeature`)
5. Apri Pull Request

### Idee di Miglioramento

- [ ] Aggiungere supporto proxy
- [ ] Implementare retry automatico
- [ ] Aggiungere logging strutturato
- [ ] Supporto CAPTCHA solving
- [ ] Integrazione con database (SQLite)
- [ ] Dashboard web con Flask
- [ ] Testing automatico con pytest

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

---

## 👨‍💻 Autore

Creato da [Tuo Nome] - Portfolio Project

**Contatto**: [tua-email@example.com]

---

## 🙏 Ringraziamenti

- Librerie requests e BeautifulSoup
- Comunità Python italiana
- Tutti i contributori open-source

---

<div align="center">

**⭐ Se questo progetto ti è stato utile, lascia una star! ⭐**

Made with ❤️ and Python

</div>
