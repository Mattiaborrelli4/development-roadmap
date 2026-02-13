# Guida Rapida - Calcolatrice PWA 🚀

## Passo 1: Genera le Icone (Necessario)

L'app ha bisogno delle icone per funzionare come PWA. Hai due opzioni:

### Opzione A: Usare il Generatore Automatico (Consigliato) ⭐

1. Apri il file `generate-icons.html` nel tuo browser
2. Clicca sul pulsante **"🎨 Genera Tutte le Icone"**
3. Tutte le icone PNG verranno scaricate nella cartella Download
4. Sposta tutti i file `icon-*.png` nella cartella `calculator-app/`

### Opzione B: Creare Icone Personalizzate

1. Vai su [favicon.io](https://favicon.io) o [RealFaviconGenerator](https://realfavicongenerator.net)
2. Carica un'immagine o usa il testo "🧮"
3. Scarica le icone nelle dimensioni richieste
4. Rinomina i file come: `icon-72.png`, `icon-96.png`, `icon-192.png`, `icon-512.png`, ecc.

## Passo 2: Testare l'App Localmente

### Metodo 1: Python (Più Semplice)
```bash
# Apri il terminale nella cartella calculator-app
cd "C:\Users\matti\Desktop\Project Ideas Portfolio\08-Mobile-Projects\calculator-app"

# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

### Metodo 2: Node.js
```bash
# Prima installa http-server globalmente
npm install -g http-server

# Poi avvia il server
http-server -p 8000
```

### Metodo 3: Estensione VS Code
1. Installa l'estensione "Live Server"
2. Tasto destro su `index.html`
3. Seleziona "Open with Live Server"

## Passo 3: Apri nel Browser

Vai su: `http://localhost:8000`

## Passo 4: Testare come PWA

### Su Chrome/Edge (Desktop):
1. Apri DevTools (F12)
2. Vai al tab **Application**
3. Verifica:
   - **Manifest**: Controlla che non ci siano errori
   - **Service Workers**: Dovresti vedere "activated"
   - **Lighthouse**: Esegui audit PWA (punteggio ideale: 90+)

4. Se tutto è OK, vedrai l'icona di installazione nella barra degli indirizzi

### Su Mobile (Android):
1. Apri Chrome
2. Vai all'URL della tua app
3. Apri il menu (tre punti in alto a destra)
4. Seleziona "Aggiungi alla schermata Home"

### Su Mobile (iOS):
1. Apri Safari
2. Vai all'URL della tua app
3. Premi il pulsante Condividi (quadrato con freccia su)
4. Scorri in basso e seleziona "Aggiungi a Home"

## Passo 5: Distribuire Online (Opzionale)

### GitHub Pages (Gratis)
```bash
# Crea un nuovo repository su GitHub
# Nella cartella calculator-app:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main

# Vai su Settings > Pages
# Seleziona branch "main" e folder "/root"
```

### Netlify (Più Veloce)
1. Vai su [netlify.com](https://netlify.com)
2. Trascina la cartella `calculator-app` nel dashboard
3. Fatto! Avrai un URL istantaneo

### Vercel
1. Installa Vercel CLI: `npm i -g vercel`
2. Nella cartella: `vercel`
3. Segui le istruzioni

## Troubleshooting

### Le icone non appaiono?
- Assicurati di aver generato TUTTE le icone con `generate-icons.html`
- Verifica che i file siano nella cartella corretta

### Il Service Worker non funziona?
- Devi usare HTTPS o localhost (non file://)
- Ricarica la pagina e controlla la console (F12)

### Non posso installare l'app?
- Verifica il manifest.json con DevTools
- Assicurati di usare HTTPS online
- Alcuni browser richiedono interazione dell'utente prima dell'installazione

### L'app non funziona offline?
- Controlla che il Service Worker sia attivo
- Ricarica la pagina una volta online, poi prova offline
- Verifica la cache in DevTools > Application > Cache Storage

## Struttura File Finale

```
calculator-app/
├── index.html          ✅ Pagina principale
├── styles.css          ✅ Foglio di stile
├── app.js              ✅ Logica JavaScript
├── manifest.json       ✅ Configurazione PWA
├── sw.js               ✅ Service Worker
├── icon-72.png         ⚠️ Da generare
├── icon-96.png         ⚠️ Da generare
├── icon-128.png        ⚠️ Da generare
├── icon-144.png        ⚠️ Da generare
├── icon-152.png        ⚠️ Da generare
├── icon-192.png        ⚠️ Da generare
├── icon-384.png        ⚠️ Da generare
├── icon-512.png        ⚠️ Da generare
├── README.md           ✅ Documentazione
├── QUICKSTART.md       ✅ Questa guida
├── generate-icons.html 🛠️ Generatore icone
└── icon-generator.html 🛠️ Alternativa icone
```

## Funzionalità dell'App

✅ Calcolatrice completa con operazioni base
✅ Funzioni: percentuale, negazione, backspace
✅ Supporto tastiera completo
✅ Design mobile-first responsive
✅ PWA installabile
✅ Funziona offline
✅ Feedback aptico (su dispositivi supportati)
✅ Dark mode automatica
✅ Accessibile (screen reader, navigazione tastiera)

## Prossimi Passi

Dopo aver generato le icone e testato l'app:

1. **Personalizza i colori** in `styles.css` (variabili CSS)
2. **Aggiungi funzionalità** in `app.js`
3. **Distribuisci online** per condividerla
4. **Testa su dispositivi reali** per l'esperienza completa

Buon sviluppo! 🎉
