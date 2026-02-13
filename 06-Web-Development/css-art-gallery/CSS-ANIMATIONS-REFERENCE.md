# 🎬 CSS Animations Reference

## Tutte le Animazioni del Progetto

## 📋 Indice
1. [Blink Animation](#1-blink-animation)
2. [Float Animation](#2-float-animation)
3. [Pulse Animation](#3-pulse-animation)
4. [Cloud Move Animation](#4-cloud-move-animation)
5. [Heartbeat Animation](#5-heartbeat-animation)
6. [Rotate Star Animation](#6-rotate-star-animation)
7. [Bounce Animation](#7-bounce-animation)
8. [Morph Animations](#8-morph-animations)
9. [Spin Animation](#9-spin-animation)
10. [Dot Bounce Animation](#10-dot-bounce-animation)
11. [Gradient Move Animation](#11-gradient-move-animation)
12. [Bounce Ball Animation](#12-bounce-ball-animation)
13. [Wave Move Animation](#13-wave-move-animation)
14. [Dance Animation](#14-dance-animation)
15. [Flag Wave Animation](#15-flag-wave-animation)
16. [Glow Animation](#16-glow-animation)

---

## 1. BLINK ANIMATION

**Uso:** Effetto ammiccamento occhi
**Elementi:** `.eye`

```css
@keyframes blink {
    0%, 90%, 100% {
        transform: scaleY(1);
    }
    95% {
        transform: scaleY(0.1);
    }
}

.eye {
    animation: blink 4s infinite;
}
```

**Come Funziona:**
- 90% del tempo: occhio aperto (scaleY: 1)
- 5% del tempo: occhio chiuso (scaleY: 0.1)
- Ciclo ogni 4 secondi

---

## 2. FLOAT ANIMATION

**Uso:** Levitazione forme geometriche
**Elementi:** `.geo-shape`

```css
@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

.geo-shape {
    animation: float 3s ease-in-out infinite;
}
```

**Come Funziona:**
- Movimento verticale su asse Y
- ±10px spostamento
- Easing fluido (ease-in-out)

---

## 3. PULSE ANIMATION

**Uso:** Sole pulsante nel paesaggio
**Elementi:** `.sun`

```css
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
    }
    50% {
        transform: scale(1.1);
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.8);
    }
}

.sun {
    animation: pulse 3s ease-in-out infinite;
}
```

**Come Funziona:**
- Scale 1 → 1.1 → 1
- Shadow contemporaneamente ingrandita
- Effetto bagliore solare

---

## 4. CLOUD MOVE ANIMATION

**Uso:** Nuvole che si muovono nel cielo
**Elementi:** `.cloud`, `.cloud-2`

```css
@keyframes cloudMove {
    0% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(20px);
    }
    100% {
        transform: translateX(0);
    }
}

.cloud {
    animation: cloudMove 20s linear infinite;
}

.cloud-2 {
    animation: cloudMove 20s linear infinite;
    animation-delay: -10s;
}
```

**Come Funziona:**
- Movimento orizzontale 0 → 20px → 0
- Durata 20 secondi (lento)
- Seconda cloud parte a metà ciclo

---

## 5. HEARTBEAT ANIMATION

**Uso:** Cuore che batte
**Elementi:** `.heart`

```css
@keyframes heartbeat {
    0%, 100% {
        transform: scale(1);
    }
    10%, 30% {
        transform: scale(0.9);
    }
    20%, 40% {
        transform: scale(1.1);
    }
}

.heart {
    animation: heartbeat 1.5s ease-in-out infinite;
}
```

**Come Funziona:**
- Simula battito cardiaco reale
- Doppio battito: scale 1 → 0.9 → 1.1 → 0.9 → 1
    - **0%** scale(1) - stato normale
    - **10%** scale(0.9) - contrazione
    - **20%** scale(1.1) - espansione
    - **30%** scale(0.9) - seconda contrazione
    - **40%** scale(1.1) - seconda espansione
    - **100%** scale(1) - ritorno normale

---

## 6. ROTATE STAR ANIMATION

**Uso:** Rotazione continua stella
**Elementi:** `.star`

```css
@keyframes rotateStar {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

.star {
    animation: rotateStar 4s linear infinite;
}
```

**Come Funziona:**
- Rotazione completa 0° → 360°
- Linear easing (costante)
- 4 secondi per rotazione completa

---

## 7. BOUNCE ANIMATION

**Uso:** Rimbalzo personaggio cartoon
**Elementi:** `.character`

```css
@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-15px);
    }
}

.character {
    animation: bounce 2s ease-in-out infinite;
}
```

**Come Funziona:**
- Movimento verticale -15px
- Simula salto con gravity
- Easing smooth per effetto naturale

---

## 8. MORPH ANIMATIONS

**Uso:** Trasformazione forme astratte
**Elementi:** `.abstract-shape`

```css
@keyframes morph1 {
    0%, 100% {
        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
        transform: translate(20px, 20px) rotate(180deg);
    }
}

.shape-1 {
    animation: morph1 8s ease-in-out infinite;
}
```

**Come Funziona:**
- **border-radius** con 8 valori per morphing forma
- **Format:** `top-left top-right bottom-right bottom-left / ...`
- **Transform simultaneo:** translate + rotate
- 4 varianti con delay diversi

**Sintassi Border-radius:**
```css
/* Senza slash */
border-radius: 60% 40% 30% 70%;
/* Angoli orizzontali: TL TR BR BR */

/* Con slash */
border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
/* Prima slash: angoli orizzontali */
/* Dopo slash: angoli verticali */
```

---

## 9. SPIN ANIMATION

**Uso:** Rotazione loading spinner
**Elementi:** `.spinner`

```css
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

.spinner {
    animation: spin 1s linear infinite;
}

.spinner::after {
    animation: spin 1.5s linear infinite reverse;
}
```

**Come Funziona:**
- Spinner principale: clockwise
- Pseudo-elemento `::after`: counter-clockwise
- Velocità diverse (1s vs 1.5s)

---

## 10. DOT BOUNCE ANIMATION

**Uso:** Punti rimbalzanti loader
**Elementi:** `.dot`

```css
@keyframes dotBounce {
    0%, 80%, 100% {
        transform: scale(0.6);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
```

**Come Funziona:**
- Scale + opacity sincronizzate
- **0%, 80%, 100%**: piccolo, semi-trasparente
- **40%**: grande, opaco
- Delay sequenziale per effetto onda

---

## 11. GRADIENT MOVE ANIMATION

**Uso:** Gradiente animato pulsante
**Elementi:** `.btn-gradient`

```css
@keyframes gradientMove {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

.btn-gradient {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
    background-size: 200% 200%;
    animation: gradientMove 3s ease infinite;
}

.btn-gradient:hover {
    animation: gradientMove 0.5s ease infinite;
}
```

**Come Funziona:**
- `background-size: 200%` crea gradiente più grande del container
- Animazione sposta `background-position`
- Hover: velocità aumentata da 3s → 0.5s

---

## 12. BOUNCE BALL ANIMATION

**Uso:** Palla che rimbalza
**Elementi:** `.bouncing-ball`

```css
@keyframes bounceBall {
    0%, 100% {
        transform: translateY(0) scale(1.1, 0.9);
    }
    50% {
        transform: translateY(-50px) scale(0.9, 1.1);
    }
}

.bouncing-ball {
    animation: bounceBall 1s ease-in-out infinite;
}
```

**Come Funziona:**
- **0%, 100%** (a terra):
  - `translateY(0)` - posizione base
  - `scale(1.1, 0.9)` - schiacciata orizzontalmente
- **50%** (in aria):
  - `translateY(-50px)` - alzata
  - `scale(0.9, 1.1)` - allungata verticalmente

**Effetto fisica:** Simula compressione palla al suolo

---

## 13. WAVE MOVE ANIMATION

**Uso:** Onde marine animate
**Elementi:** `.wave`, `.wave-2`, `.wave-3`

```css
@keyframes waveMove {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}

.wave {
    animation: waveMove 3s linear infinite;
}

.wave-2 {
    animation: waveMove 5s linear infinite reverse;
}

.wave-3 {
    animation: waveMove 7s linear infinite;
}
```

**Come Funziona:**
- SVG wave background
- Translazione orizzontale infinita
- 3 layer con:
  - Velocità diverse (3s, 5s, 7s)
  - Opacità diverse (0.6, 0.4, 0.3)
  - Direzione: 2 orizzontali, 1 reverse

---

## 14. DANCE ANIMATION

**Uso:** Nota musicale che balla
**Elementi:** `.music-note`

```css
@keyframes dance {
    0%, 100% {
        transform: rotate(-10deg) translateY(0);
    }
    25% {
        transform: rotate(10deg) translateY(-10px);
    }
    50% {
        transform: rotate(-10deg) translateY(0);
    }
    75% {
        transform: rotate(5deg) translateY(-5px);
    }
}

.music-note {
    animation: dance 1s ease-in-out infinite;
}
```

**Come Funziona:**
- Combina rotazione + spostamento
- Pattern irregolare per effetto naturale
- **0%, 50%**: rotazione -10°, posizione base
- **25%**: rotazione +10°, alzata 10px
- **75%**: rotazione +5°, alzata 5px

---

## 15. FLAG WAVE ANIMATION

**Uome:** Bandiera nota musicale
**Elementi:** `.note-flag`

```css
@keyframes flagWave {
    0%, 100% {
        transform: scaleY(1);
    }
    50% {
        transform: scaleY(1.2);
    }
}

.note-flag {
    animation: flagWave 1s ease-in-out infinite;
}
```

**Come Funziona:**
- `transform-origin: left center` (già nel CSS)
- Scale verticale da 1 → 1.2 → 1
- Simula onda bandiera

---

## 16. GLOW ANIMATION

**Uso:** Effetto bagliore stella
**Elementi:** `.star::after`

```css
@keyframes glow {
    0%, 100% {
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    }
    50% {
        text-shadow: 0 0 20px rgba(255, 255, 255, 1),
                    0 0 30px rgba(255, 215, 0, 0.8);
    }
}

.star::after {
    content: '⭐';
    animation: glow 2s ease-in-out infinite;
}
```

**Come Funziona:**
- `text-shadow` con multipli layer
- **0%, 100%**: 1 layer, 10px blur
- **50%**: 2 layer, 20px + 30px blur
- Transizione graduale per effetto pulsante

---

## 🎯 Animation Properties Reference

### Shorthand Syntax

```css
animation: [name] [duration] [timing-function] [delay] [iteration-count] [direction] [fill-mode] [play-state];
```

### Complete Example

```css
.element {
    animation:
        bounce 2s        /* name duration */
        ease-in-out      /* timing-function */
        0.5s             /* delay */
        infinite         /* iteration-count */
        alternate        /* direction */
        forwards         /* fill-mode */
        running;         /* play-state */
}
```

### Properties Breakdown

| Property | Values | Default |
|----------|--------|---------|
| `animation-name` | keyframe name | none |
| `animation-duration` | time (s, ms) | 0s |
| `animation-timing-function` | ease, linear, ease-in-out, cubic-bezier() | ease |
| `animation-delay` | time (s, ms) | 0s |
| `animation-iteration-count` | number, infinite | 1 |
| `animation-direction` | normal, reverse, alternate, alternate-reverse | normal |
| `animation-fill-mode` | none, forwards, backwards, both | none |
| `animation-play-state` | running, paused | running |

---

## 📊 Performance Tips

### 1. Usa Transform e Opacity
```css
/* ✅ GOOD - GPU accelerated */
.animated {
    transform: translateX(100px);
    opacity: 0.5;
}

/* ❌ BAD - CPU intensive */
.animated {
    left: 100px;
    filter: blur(5px);
}
```

### 2. Minimizza Repaints
```css
/* ✅ GOOD */
.box {
    will-change: transform;
}

/* ❌ BAD - Overuse */
* {
    will-change: transform;
}
```

### 3. Usa Animation Compositing
```css
/* ✅ GOOD - Separate animations */
.element {
    animation: rotate 2s linear infinite,
               scale 1s ease-in-out infinite;
}

/* ⚠️ WARNING - May cause performance issues */
.element {
    animation: complex 5s ease-in-out infinite;
}
```

---

## 🎨 Timing Functions

### Built-in
```css
/* Linear - Velocità costante */
animation-timing-function: linear;

/* Ease - Start slow, fast, end slow */
animation-timing-function: ease;

/* Ease-in - Start slow */
animation-timing-function: ease-in;

/* Ease-out - End slow */
animation-timing-function: ease-out;

/* Ease-in-out - Start e end lenti */
animation-timing-function: ease-in-out;
```

### Cubic Bezier
```css
/* Custom curve */
animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Generator: https://cubic-bezier.com/ */
```

---

## 🔄 Iteration Patterns

### Infinite
```css
animation: bounce 1s infinite;
```

### Specific Count
```css
animation: bounce 1s 3; /* 3 volte */
```

### Alternate
```css
animation: bounce 1s infinite alternate;
/* Forward, then reverse */
```

### Reverse
```css
animation: bounce 1s infinite reverse;
/* Backward first */
```

---

## 🎭 Fill Modes

### Forwards
```css
/* Mantiene stato finale */
.element {
    animation: fadeOut 1s forwards;
}
```

### Backwards
```css
/* Applica stato iniziale prima delay */
.element {
    animation: fadeIn 1s 2s backwards;
}
```

### Both
```css
/* Combina forwards + backwards */
.element {
    animation: fade 1s both;
}
```

---

## 🚀 Advanced Techniques

### 1. Stagger Animations
```css
.item:nth-child(1) { animation-delay: 0s; }
.item:nth-child(2) { animation-delay: 0.1s; }
.item:nth-child(3) { animation-delay: 0.2s; }
```

### 2. Multi-step Keyframes
```css
@keyframes complex {
    0% { transform: translateX(0); }
    25% { transform: translateX(100px); }
    50% { transform: translateX(100px) rotate(180deg); }
    75% { transform: translateX(0) rotate(180deg); }
    100% { transform: translateX(0); }
}
```

### 3. Conditional Animation
```css
/* Start on hover */
.element {
    animation: rotate 2s linear infinite;
    animation-play-state: paused;
}

.element:hover {
    animation-play-state: running;
}
```

---

## 📚 Resources

### Tools
- [Cubic-bezier.com](https://cubic-bezier.com/) - Timing functions
- [CSS Animation Generator](https://cssgenerator.org/) - Visual tools
- [Animista](https://animista.net/) - Animation presets

### References
- [MDN: CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [CSS-Tricks: Animation](https://css-tricks.com/almanac/properties/a/animation/)

---

## 💡 Best Practices

### ✅ DO
- Usa `transform` per movimento
- Specifica `will-change` per animazioni complesse
- Usa prefissi vendor solo se necessario
- Testa su browser multipli
- Considera `prefers-reduced-motion`

### ❌ DON'T
- Animare `width`, `height`, `top`, `left`
- Usare troppe animazioni simultanee
- Dimenticarsi del fallback
- Ignorare performance
- Osservareccessivamente

---

## 🎯 Prefers Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

## 🔥 Quick Copy Examples

### Fade In
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### Slide Up
```css
@keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
}
```

### Pulse
```css
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
```

### Shake
```css
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-10px); }
    75% { transform: translateX(10px); }
}
```

---

**Creato per CSS Art Gallery Project**
*Tutte le animazioni sono testate e ottimizzate*
