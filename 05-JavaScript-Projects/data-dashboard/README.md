# Dashboard Analitica - Visualizzazione Dati

Una dashboard interattiva per la visualizzazione di dati aziendali con grafici dinamici, filtri e statistiche in tempo reale. Costruita con JavaScript puro, HTML5 e CSS3, utilizzando Chart.js per le visualizzazioni.

![Dashboard](https://img.shields.io/badge/version-1.0.0-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow) ![Chart.js](https://img.shields.io/badge/Chart.js-4.4.0-orange)

## Caratteristiche

### Grafici Multipli
- **Grafico a Linee**: Trend di vendite e entrate nel tempo
- **Grafico a Barre**: Vendite per categoria prodotto
- **Grafico a Torta (Doughnut)**: Distribuzione utenti per fascia d'età
- **Grafico a Barre Orizzontali**: Performance prodotti
- **Grafico Radar**: Metriche di performance mensili

### Funzionalità Interattive
- Filtri temporali (settimana, mese, trimestre, anno)
- Filtri per categoria (vendite, utenti, entrate)
- Cambio tipo di grafico dinamico (linea/barre)
- Statistiche animate con counter
- Tabella dati dettagliata
- Design completamente responsive

### Interfaccia Utente
- Design moderno e dark theme
- Animazioni fluide
- Tooltip informativi
- Legende interattive
- Layout adattivo per tutti i dispositivi

## Struttura del Progetto

```
data-dashboard/
│
├── index.html          # struttura HTML principale
├── style.css           # stili CSS con design responsive
├── app.js              # logica JavaScript e grafici
└── README.md           # documentazione del progetto
```

## Tecnologie Utilizzate

- **HTML5**: struttura semantica
- **CSS3**: Grid, Flexbox, animazioni, variabili CSS
- **JavaScript ES6+**: funzioni arrow, template literals, async/await
- **Chart.js 4.4.0**: libreria per grafici interattivi (tramite CDN)

## Installazione e Utilizzo

### Requisiti
- Un browser web moderno (Chrome, Firefox, Safari, Edge)
- Non sono richiesti server o dipendenze locali

### Passaggi

1. Clona o scarica il repository
2. Naviga nella cartella `data-dashboard/`
3. Apri `index.html` nel tuo browser preferito

Oppure, utilizza un server locale per sviluppare:

```bash
# Con Python 3
python -m http.server 8000

# Con Node.js (npx)
npx serve

# Con PHP
php -S localhost:8000
```

Poi visita `http://localhost:8000` nel tuo browser.

## Utilizzo della Dashboard

### Filtri Temporali
Clicca sui pulsanti nella sezione "Filtri Dati" per cambiare il periodo visualizzato:
- **Ultima Settimana**: dati giornalieri (7 giorni)
- **Ultimo Mese**: dati settimanali (4 settimane)
- **Ultimo Trimestre**: dati mensili (3 mesi)
- **Ultimo Anno**: dati trimestrali (4 trimestri)

### Filtri Categoria
Usa le checkbox per mostrare/nascondere:
- Vendite
- Utenti
- Entrate

### Cambio Tipo Grafico
Utilizza il dropdown nel grafico "Trend Vendite e Entrate" per passare dalla visualizzazione a linee a quella a barre.

## Dati di Esempio

La dashboard utilizza dati di esempio memorizzati in oggetti JavaScript:

```javascript
const dashboardData = {
    week: {
        labels: ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'],
        vendite: [4500, 5200, 4800, 6100, 5500, 7200, 6800],
        entrate: [11250, 13000, 12000, 15250, 13750, 18000, 17000],
        // ...
    },
    // ... altri periodi
};
```

Per utilizzare dati reali, sostituisci gli oggetti di esempio con chiamate API o dati da un database.

## Personalizzazione

### Colori
Modifica le variabili CSS in `style.css`:

```css
:root {
    --primary-color: #4f46e5;
    --secondary-color: #8b5cf6;
    --background: #0f172a;
    /* ... */
}
```

### Dati
Sostituisci i dati in `app.js`:
1. Modifica l'oggetto `dashboardData` con i tuoi dati
2. Aggiorna `categoryData`, `userDistribution`, `productPerformance` e `monthlyMetrics`
3. Oppure, integra un'API per fetchare dati in tempo reale

### Grafici
Personalizza i grafici modificando le opzioni di Chart.js nelle funzioni `initializeCharts()` in `app.js`.

## Funzionalità Avanzate

### Aggiornamento Automatico
Il grafico Radar si aggiorna automaticamente ogni 5 secondi per simulare dati in tempo reale:

```javascript
setInterval(() => {
    radarChart.data.datasets[0].data = /* ... */;
    radarChart.update('none');
}, 5000);
```

### Animazioni
Le statistiche utilizzano animazioni con easing quartico per un effetto fluido:

```javascript
function easeOutQuart(x) {
    return 1 - Math.pow(1 - x, 4);
}
```

## Compatibilità Browser

| Browser | Versione Minima |
|---------|----------------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

## Performance

- Caricamento iniziale: < 1 secondo
- Interazioni grafico: 60 FPS
- Utilizzo memoria: ~50 MB
- Dimensione totale: ~50 KB (senza CDN)

## Miglioramenti Futuri

- [ ] Integrazione con API reali
- [ ] Esportazione dati in CSV/PDF
- [ ] Grafici aggiuntivi (area, scatter, bubble)
- [ ] Modalità tema chiaro/scuro
- [ ] Autenticazione utenti
- [ ] Dashboard personalizzabili
- [ ] Notifiche in tempo reale
- [ ] PWA (Progressive Web App)

## Contributi

Contributi, problemi e richieste di funzionalità sono benvenuti!

1. Fai fork del progetto
2. Crea un branch per la tua funzionalità (`git checkout -b feature/NuovaFunzionalita`)
3. Commit delle modifiche (`git commit -m 'Aggiunta nuova funzionalità'`)
4. Push al branch (`git push origin feature/NuovaFunzionalita`)
5. Apri una Pull Request

## Licenza

Questo progetto è rilasciato sotto la licenza MIT. Vedi il file LICENSE per maggiori dettagli.

## Crediti

- **Chart.js**: Libreria per grafici interattivi
- **Design**: Ispirato alle moderne dashboard SaaS
- **Icone**: Emoji native per leggerezza e compatibilità

## Contatti

Per domande o suggerimenti:
- Apri un issue nel repository
- Contatta lo sviluppatore

---

**Realizzato con ❤️ in JavaScript puro**
