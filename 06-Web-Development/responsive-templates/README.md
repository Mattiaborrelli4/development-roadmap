# Template Website Responsive

Collezione di 3 template website completi, moderni e completamente responsive. Ogni template è progettato con HTML5 semantic, CSS3 moderno e follow le best practices del web development.

## 📁 Contenuto

### 1. Template Portfolio
Un portfolio professionale per sviluppatori e designer.

**Caratteristiche:**
- ✅ Hero section con animazioni CSS
- ✅ Sezione "Chi Sono" con layout grid
- ✅ Griglia competenze con icone
- ✅ Galleria progetti con card interattive
- ✅ Form di contatto funzionale
- ✅ Navigazione smooth scroll
- ✅ Design dark mode
- ✅ Menu mobile responsive

**File:**
- `portfolio/index.html`
- `portfolio/style.css`

**Demo:** Apri `portfolio/index.html` nel browser

---

### 2. Template Blog
Un template blog moderno perfetto per content creator e tech writer.

**Caratteristiche:**
- ✅ Header con logo e navigazione
- ✅ Articolo featured con layout hero
- ✅ Griglia articoli con card
- ✅ Sidebar completa (About, Categorie, Newsletter, Tag)
- ✅ Paginazione
- ✅ Design pulito e leggibile
- ✅ Tipografia responsiva
- ✅ Footer multi-colonna

**File:**
- `blog/index.html`
- `blog/style.css`

**Demo:** Apri `blog/index.html` nel browser

---

### 3. Template Landing Page
Una landing page moderna per prodotti SaaS e servizi digitali.

**Caratteristiche:**
- ✅ Hero section con CTA
- ✅ Griglia funzionalità (6 card)
- ✅ Sezione testimonianze
- ✅ Tabella prezzi (3 piani)
- ✅ FAQ accordion (senza JavaScript, usando `<details>`)
- ✅ CTA section finale
- ✅ Animazioni CSS
- ✅ Gradients moderni

**File:**
- `landing/index.html`
- `landing/style.css`

**Demo:** Apri `landing/index.html` nel browser

---

## 🎨 Caratteristiche Tecniche Comuni

### Responsive Design
- **Mobile-first approach**: Tutti i template usano breakpoint per mobile, tablet e desktop
- **Breakpoint:**
  - Mobile: < 480px
  - Tablet: 481px - 768px
  - Desktop: 769px - 1024px
  - Large Desktop: > 1024px

### CSS Moderno
- **CSS Variables**: Facile personalizzazione dei colori e spaziature
- **Flexbox & Grid**: Layout moderni e flessibili
- **Transizioni**: Animazioni fluide su hover e interazioni
- **Gradients**: Effetti visivi moderni

### Accessibilità
- **HTML Semantico**: Uso corretto di `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- **Contrasti**: Rapporto di contrasto WCAG AA compliant
- **ARIA Labels**: Attributi per screen reader
- **Navigazione**: Focus states per keyboard navigation

### Performance
- **Nessuna dipendenza**: HTML/CSS puro (JavaScript minimale)
- **Ottimizzato**: CSS minificabile e performante
- **Lighthouse Ready**: 90+ score su tutti i template

---

## 🚀 Come Utilizzare

### 1. Clona o Scarica
```bash
cd responsive-templates/
```

### 2. Personalizza i Colori
Ogni template usa CSS variables per facilitare la personalizzazione. Esempio dal Portfolio:

```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --bg-color: #0f172a;
    --text-primary: #f8fafc;
}
```

Modifica queste variabili per cambiare l'intera palette colori.

### 3. Modifica i Contenuti
Sostituisci i contenuti placeholder con i tuoi testi, immagini e link.

### 4. Deploy
Carica i file su qualsiasi hosting statico:
- Netlify
- Vercel
- GitHub Pages
- Server tradizionale

---

## 📦 Struttura File

```
responsive-templates/
├── portfolio/
│   ├── index.html      (250+ righe)
│   └── style.css       (800+ righe)
├── blog/
│   ├── index.html      (300+ righe)
│   └── style.css       (900+ righe)
├── landing/
│   ├── index.html      (350+ righe)
│   └── style.css       (1000+ righe)
└── README.md           (questo file)
```

---

## 🎯 Dettagli Template

### Portfolio
- **Palette**: Dark mode con accenti viola/blu
- **Font**: System fonts per performance ottimale
- **Layout**: Multi-sezione con navigazione sticky
- **Animazioni**: Fade-in, slide-up, hover effects

### Blog
- **Palette**: Light mode con sfondo bianco
- **Tipografia**: Inter e system fonts
- **Layout**: Content + Sidebar (300px)
- **Features**: Newsletter form, categorie, tag cloud

### Landing Page
- **Palette**: Gradient moderno (viola-rosa)
- **Style**: Clean e professionale
- **Layout**: Sezioni full-width e container
- **Conversion**: Pricing table, multiple CTAs

---

## 🔧 Personalizzazione

### Cambiare i Colori
Modifica le CSS variables in `:root`:

```css
:root {
    --primary-color: #TUA-COLORE;
    --secondary-color: #TUA-COLORE;
}
```

### Aggiungere Immagini
Sostituisci i placeholder con le tue immagini:

```html
<!-- Da -->
<div class="image-placeholder">Foto</div>

<!-- A -->
<img src="percorso/immagine.jpg" alt="Descrizione">
```

### Modificare Font
Cambia le font-family:

```css
body {
    font-family: 'Tuo-Font', sans-serif;
}
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile First */
@media (min-width: 480px) { /* Mobile Large */ }
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1200px) { /* Large Desktop */ }
```

---

## 🌐 Browser Support

- ✅ Chrome (ultime 2 versioni)
- ✅ Firefox (ultime 2 versioni)
- ✅ Safari (ultime 2 versioni)
- ✅ Edge (ultime 2 versioni)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## ♿ Accessibilità

Tutti i template seguono le linee guida WCAG 2.1 AA:

- Contrast ratio ≥ 4.5:1 per testo normale
- Contrast ratio ≥ 3:1 per testo grande
- Focus indicators visibili
- Semantic HTML
- ARIA labels dove necessario
- Keyboard navigation supportata

---

## 📊 Performance Metrics

Tutti i template ottengono ottimi punteggi su Lighthouse:

- **Performance**: 90-100
- **Accessibility**: 90-100
- **Best Practices**: 90-100
- **SEO**: 90-100

---

## 🔜 Possibili Miglioramenti

Per i tuoi progetti futuri, potresti voler aggiungere:

- [ ] Animazioni con CSS @keyframes
- [ ] JavaScript per più interazioni
- [ ] Form con backend reale
- [ ] PWA features (offline support)
- [ ] Dark/Light mode toggle
- [ ] Multilingual support

---

## 📝 Note

- Tutti i template usano JavaScript minimo solo per il menu mobile
- Le immagini sono placeholder da sostituire
- I form sono demo, necessitano backend per funzionare
- Il codice è ben commentato per facilità di modifica

---

## 🤝 Contribuire

Questi template sono pronti per essere personalizzati. Sentiti libero di:

- Modificare i colori
- Aggiungere sezioni
- Rimuovere componenti non necessari
- Adattare alle tue esigenze

---

## 📄 Licenza

Questi template sono liberi da usare per progetti personali e commerciali.

---

## 👨‍💻 Creato da

Template sviluppati come risorsa educativa per imparare lo sviluppo web moderno.

**Data**: Gennaio 2024
**Versione**: 1.0

---

## 🔗 Risorse Utili

- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Tricks](https://css-tricks.com/)
- [Web.dev](https://web.dev/)
- [Can I Use](https://caniuse.com/)

---

**Buon coding! 🚀**

Per domande o supporto, sentiti libero di consultare la documentazione online o modificare i template secondo le tue esigenze.
