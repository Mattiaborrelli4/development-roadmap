# 📝 Esercizi Pratici - Snake Game

Questa guida contiene esercizi pratici con codice di esempio per migliorare il gioco Snake.

---

## 🟢 Esercizio 1: Aggiungi un High Score System

### Obiettivo
Salva il punteggio più alto su file e mostralo all'avvio del gioco.

### Codice da Aggiungere

In cima al file, aggiungi:
```cpp
#include <fstream>   // Per file I/O
#include <sstream>   // Per string stream
```

### Classe HighScoreManager (da aggiungere)

```cpp
/**
 * Gestisce il salvataggio e caricamento del punteggio più alto
 */
class HighScoreManager {
private:
    std::string filename;
    int highScore;

public:
    HighScoreManager(const std::string& file = "highscore.txt")
        : filename(file), highScore(0) {
        caricaHighScore();
    }

    void caricaHighScore() {
        std::ifstream file(filename);
        if (file.is_open()) {
            file >> highScore;
            file.close();
        }
    }

    void salvaHighScore() {
        std::ofstream file(filename);
        if (file.is_open()) {
            file << highScore;
            file.close();
        }
    }

    bool aggiornaPunteggio(int nuovoPunteggio) {
        if (nuovoPunteggio > highScore) {
            highScore = nuovoPunteggio;
            salvaHighScore();
            return true;  // Nuovo record!
        }
        return false;
    }

    int getHighScore() const {
        return highScore;
    }
};
```

### Modifiche al main()

```cpp
int main() {
    // Crea il gestore del high score
    HighScoreManager highScore;

    // ... codice esistente ...

    cout << "High Score: " << highScore.getHighScore() << "\n\n";

    // ... game loop ...

    // Quando il gioco finisce:
    if (highScore.aggiornaPunteggio(gioco.getPunteggio())) {
        cout << "\n🎉 NUOVO RECORD! 🎉\n";
    } else {
        cout << "\nHigh Score: " << highScore.getHighScore() << "\n";
    }
}
```

---

## 🟢 Esercizio 2: Aggiungi Livelli di Difficoltà

### Obiettivo
Lascia l'utente scegliere tra Easy, Medium, Hard.

### Codice da Aggiungere

```cpp
enum LivelloDifficolta {
    FACILE,      // FPS: 8
    MEDIO,       // FPS: 12
    DIFFICILE    // FPS: 20
};

LivelloDifficolta menuDifficolta() {
    int scelta;
    cout << "\nSeleziona la difficoltà:\n";
    cout << "1. Facile\n";
    cout << "2. Medio\n";
    cout << "3. Difficile\n";
    cout << "Scelta: ";
    cin >> scelta;

    switch(scelta) {
        case 1: return FACILE;
        case 2: return MEDIO;
        case 3: return DIFFICILE;
        default: return MEDIO;
    }
}

int getFPS(LivelloDifficolta livello) {
    switch(livello) {
        case FACILE: return 8;
        case MEDIO: return 12;
        case DIFFICILE: return 20;
        default: return 12;
    }
}
```

### Modifiche al game loop

```cpp
int main() {
    // ... benvenuto ...

    LivelloDifficolta difficolta = menuDifficolta();
    int fps = getFPS(difficolta);
    const auto durataFrame = std::chrono::milliseconds(1000 / fps);

    // ... resto del codice ...
}
```

---

## 🟡 Esercizio 3: Aggiungi Ostacoli

### Obiettivo
Genera ostacoli casuali sulla griglia.

### Codice da Aggiungere

Nella classe `GiocoSnake`, aggiungi:

```cpp
private:
    vector<Posizione> ostacoli;

    void generaOstacoli(int numero) {
        for (int i = 0; i < numero; ++i) {
            bool posizioneValida = false;
            while (!posizioneValida) {
                int x = distribuzioneX(gen);
                int y = distribuzioneY(gen);
                Posizione ostacolo(x, y);

                // Verifica non sia sul serpente
                bool sulSerpente = false;
                for (const auto& segmento : serpente) {
                    if (segmento == ostacolo) {
                        sulSerpente = true;
                        break;
                    }
                }

                // Verifica non sia sul cibo
                if (!sulSerpente && !(ostacolo == cibo)) {
                    ostacoli.push_back(ostacolo);
                    posizioneValida = true;
                }
            }
        }
    }

    bool verificaOstacolo(const Posizione& pos) const {
        for (const auto& ostacolo : ostacoli) {
            if (pos == ostacolo) {
                return true;
            }
        }
        return false;
    }
```

### Nel costruttore

```cpp
GiocoSnake(int w, int h, int numOstacoli = 5)
    : /* ... inizializzazione esistente ... */ {

    // ... codice esistente ...

    generaOstacoli(numOstacoli);
}
```

### In aggiorna()

```cpp
void aggiorna() {
    // ... codice esistente ...

    Posizione nuovaTesta = calcolaNuovaTesta();

    // Verifica ostacoli
    if (verificaOstacolo(nuovaTesta)) {
        giocoTerminato = true;
        return;
    }

    // ... resto del codice ...
}
```

### In renderizza()

```cpp
// Aggiungi dopo il cibo:
else if (std::find(ostacoli.begin(), ostacoli.end(), current)
         != ostacoli.end()) {
    cout << " X ";  // Ostacolo
    trovato = true;
}
```

---

## 🟡 Esercizio 4: Sistema di Vite

### Obiettivo
Invece di Game Over immediato, dai 3 vite al giocatore.

### Modifiche alla classe GiocoSnake

```cpp
private:
    int vite;

public:
    GiocoSnake(int w, int h)
        : /* ... inizializzazione ... */, vite(3) {
        // ...
    }

    void perdiVita() {
        vite--;
        if (vite <= 0) {
            giocoTerminato = true;
        } else {
            // Resetta il serpente
            serpente.clear();
            int startX = larghezza / 2;
            int startY = altezza / 2;
            serpente.push_back(Posizione(startX, startY));
            direzione = DESTRA;
        }
    }

    int getVite() const { return vite; }
```

### In aggiorna()

```cpp
if (èFuoriBordi(nuovaTesta) || verificaCollisione()) {
    perdiVita();  // Invece di giocoTerminato = true
    if (!giocoTerminato) {
        return;  // Continua il gioco
    }
}
```

### In renderizza()

```cpp
cout << "Vite: ";
for (int i = 0; i < vite; ++i) {
    cout << "❤️ ";
}
cout << "\n";
```

---

## 🟠 Esercizio 5: Cibo Speciale (Bonus)

### Obiettivo
Diversi tipi di cibo con effetti diversi.

### Codice da Aggiungere

```cpp
enum TipoCibo {
    NORMALE,   // +10 punti
    BONUS,     // +50 punti
    VELOCE     // +20 punti, ma aumenta velocità
};

struct CiboSpecial {
    Posizione posizione;
    TipoCibo tipo;
};

private:
    CiboSpecial ciboSpeciale;
    int velocitaBonus;  // 0 = normale, >0 = extra velocità

    void generaCiboSpeciale() {
        // 20% di probabilità di cibo bonus
        bool isBonus = (rand() % 100) < 20;

        ciboSpeciale.posizione = Posizione(
            distribuzioneX(gen),
            distribuzioneY(gen)
        );
        ciboSpeciale.tipo = isBonus ? BONUS : NORMALE;
    }
```

### In aggiorna()

```cpp
if (nuovaTesta == ciboSpeciale.posizione) {
    switch(ciboSpeciale.tipo) {
        case NORMALE:
            punteggio += 10;
            break;
        case BONUS:
            punteggio += 50;
            break;
        case VELOCE:
            punteggio += 20;
            velocitaBonus = 50;  // Durata del bonus in frame
            break;
    }
    generaCiboSpeciale();
} else {
    serpente.pop_back();
}

// Decrementa velocità bonus
if (velocitaBonus > 0) {
    velocitaBonus--;
}
```

---

## 🔴 Esercizio 6: Pause Game

### Obiettivo
Permetti di mettere in pausa il gioco con P.

### Codice da Aggiungere

```cpp
private:
    bool inPausa;

public:
    void togglePause() {
        inPausa = !inPausa;
    }

    bool isInPausa() const {
        return inPausa;
    }
```

### In processaInput()

```cpp
case 'p': case 'P':
    togglePause();
    break;
```

### Nel game loop

```cpp
if (gioco.isInPausa()) {
    cout << "\n⏸️  IN PAUSA - Premi P per continuare\n";
    continue;  // Skip update e render
}
```

---

## 💡 Suggerimenti per Completare gli Esercizi

1. **Leggi prima di codificare**
   - Capisci come funziona il codice esistente
   - Identifica dove inserire il nuovo codice

2. **Testa frequentemente**
   - Compila dopo ogni cambiamento significativo
   - Verifica che il gioco funzioni ancora

3. **Usa il debugger**
   - Se qualcosa non va, usa il debugger passo-passo
   - Guarda i valori delle variabili

4. **Commenta il tuo codice**
   - Spiega cosa fa il tuo nuovo codice
   - Sarà utile se ci ritornerai dopo

5. **Non avere paura di sperimentare**
   - Prova diverse combinazioni
   - Impara dagli errori

---

## ✅ Soluzioni

Le soluzioni complete non sono fornite intenzionalmente - parte dell'apprendimento è sperimentare e trovare la propria soluzione!

Se sei davvero bloccato:
- Controlla la documentazione C++ su cppreference.com
- Chiedi aiuto su Stack Overflow
- Consulta il tuo manuale di C++

Buon coding! 🚀
