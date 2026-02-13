# 🚀 INIZIA QUI - Calcolatrice PWA

Benvenuto! Questa guida ti aiuterà a far funzionare la tua calcolatrice PWA in meno di 5 minuti.

## Stato Attuale: ✅ PRONTO (con un piccolo passaggio aggiuntivo)

L'app è completamente funzionante. Hai solo bisogno di **generare le icone** per abilitare la funzionalità PWA completa.

## ⚡ Avvio Rapido (3 Passaggi)

### Passo 1: Genera le Icone (2 minuti)
Apri il file `generate-icons.html` nel tuo browser e clicca il pulsante grande **"🎨 Genera Tutte le Icone"**. Tutte le icone PNG verranno scaricate automaticamente.

### Passo 2: Sposta le Icone (30 secondi)
Sposta tutti i file `icon-*.png` dalla cartella Download alla cartella `calculator-app/`.

### Passo 3: Avvia l'App (30 secondi)
```bash
# Nella cartella calculator-app, esegui:
python -m http.server 8000
# oppure
npx http-server -p 8000
```

Poi apri: **http://localhost:8000**

## 📚 Documentazione Disponibile

- **QUICKSTART.md** - Guida rapida completa con troubleshooting
- **README.md** - Documentazione tecnica dettagliata
- **PROJECT_SUMMARY.md** - Panoramica architettura e features

## 🎯 Cosa Puoi Fare Subito

### Testare le Funzionalità
- ✅ Calcoli: +, -, ×, ÷, %
- ✅ Tastiera: usa numeri e operatori
- ✅ Touch: clicca sui pulsanti
- ✅ Backspace e Clear

### Testare come PWA
Su Chrome/Edge desktop:
1. Apri DevTools (F12)
2. Vai su "Application" > "Manifest"
3. Verifica che non ci siano errori
4. Vedi l'icona installazione nella barra indirizzi

### Distribuire Online
- **GitHub Pages**: Push del codice e abilita Pages
- **Netlify**: Trascina la cartella sul sito
- **Vercel**: Esegui `vercel` nella cartella

## 🛠️ Strumenti Inclusi

- `generate-icons.html` - Generatore automatico icone (usa questo!)
- `icon-generator.html` - Alternativa per icone SVG
- `package.json` - Configurazione per `npm start`

## 📱 Compatibilità

| Piattaforma | Stato |
|-------------|-------|
| Chrome Desktop | ✅ Perfetto |
| Chrome Mobile | ✅ Perfetto |
| Firefox | ✅ Buono |
| Safari Desktop | ⚠️ Limitato |
| Safari iOS | ⚠️ Limitato |

## ⚠️ Nota Importante

Le icone sono NECESSARIE per:
- Visualizzazione nella home screen
- Icona app quando installata
- Splash screen
- PWA completo funzionamento

Senza icone, l'app funziona normalmente nel browser ma non può essere installata come PWA.

## 🎨 Personalizzazione

Vuoi cambiare i colori? Apri `styles.css` e modifica:
```css
:root {
    --operator-bg: #ff9f0a;  /* Cambia questo colore */
}
```

## 💡 Consigli

1. **Prima volta**: Segui i 3 passaggi sopra
2. **Testing**: Usa `http-server` per testing locale
3. **Deploy**: Usa Netlify per deployment istantaneo
4. **Debug**: Usa DevTools > Application per debug PWA

## ❓ Hai Problemi?

Vedi `QUICKSTART.md` per la sezione Troubleshooting completa.

---

**Buon divertimento con la tua calcolatrice PWA!** 🧮✨

Prossimo passo: Apri `generate-icons.html` nel browser!
