/**
 * ============================================================================
 * CONSOLE GAME ENGINE - SNAKE GAME
 * ============================================================================
 *
 * Un motore di gioco console semplice scritto in C++ moderno (C++17)
 * Questo progetto dimostra i concetti fondamentali della programmazione
 * orientata agli oggetti (OOP) e l'uso della STL (Standard Template Library)
 *
 * Autore: Progetto educativo per studenti universitari
 * Linguaggio: C++17
 * ============================================================================
 */

#include <iostream>
#include <vector>
#include <deque>
#include <random>
#include <chrono>
#include <string>
#include <algorithm>

// Utilizziamo le direttive using per semplificare il codice
// In progetti più grandi, evitare l'uso di "using namespace std;"
using std::cout;
using std::cin;
using std::endl;
using std::vector;
using std::deque;

/**
 * ============================================================================
 * CLASSE: Posizione
 * ============================================================================
 *
 * Scopo: Rappresenta una coordinata 2D (x, y) nella griglia di gioco
 *
 * Concetti OOP dimostrati:
 * - Incapsulamento: i dati membri sono privati
 * - Costruttore: inizializzazione dell'oggetto
 * - Operator overloading: ridefinizione dell'operatore ==
 *
 * Questo è un semplice "value object" - rappresenta un dato immutabile
 * ============================================================================
 */
class Posizione {
private:
    int x;
    int y;

public:
    // Costruttore con valori di default
    // C++11+: permette di creare Posizione() o Posizione(5, 10)
    Posizione(int x = 0, int y = 0) : x(x), y(y) {
        // Lista di inizializzazione: metodo preferito per inizializzare membri
        // È più efficiente dell'assegnazione nel corpo del costruttore
    }

    // Getter methods (accessor methods)
    // Forniscono accesso in sola lettura ai membri privati
    int getX() const { return x; }
    int getY() const { return y; }

    // Setter methods (mutator methods)
    void setX(int nuovoX) { x = nuovoX; }
    void setY(int nuovoY) { y = nuovoY; }

    // Operator overloading: confronto tra due posizioni
    bool operator==(const Posizione& altra) const {
        return x == altra.x && y == altra.y;
    }
};

/**
 * ============================================================================
 * CLASSE: GiocoSnake
 * ============================================================================
 *
 * Scopo: Gestisce tutta la logica del gioco Snake
 *
 * Concetti OOP dimostrati:
 * - Incapsulamento: tutti i dati sono privati
 * - Costruttore e Distruttore
 * - Metodi pubblici (interfaccia pubblica) e privati (implementazione interna)
 * - Gestione dello stato dell'oggetto
 * - Uso della STL (deque, vector, random)
 *
 * Design Pattern: Single Responsibility Principle
 * La classe si occupa SOLO della logica di gioco, non della visualizzazione
 * ============================================================================
 */
class GiocoSnake {
private:
    // ==================== MEMBRI PRIVATI (DATI) ====================

    // La griglia di gioco
    int larghezza;
    int altezza;

    // Stato del serpente: usiamo deque per efficienza
    // deque è preferito a vector per operazioni frequenti all'inizio/fine
    deque<Posizione> serpente;

    // Direzione corrente del serpente
    enum Direzione { SU, GIU, SINISTRA, DESTRA } direzione;

    // Posizione del cibo
    Posizione cibo;

    // Stato del gioco
    bool giocoTerminato;
    int punteggio;

    // Generatore di numeri casuali (C++11+)
    std::random_device rd;
    std::mt19937 gen;
    std::uniform_int_distribution<> distribuzioneX;
    std::uniform_int_distribution<> distribuzioneY;

    // ==================== METODI PRIVATI (HELPERS) ====================

    /**
     * Genera una nuova posizione casuale per il cibo
     * Evita di posizionare il cibo sul serpente
     */
    void generaCibo() {
        // Loop finché non troviamo una posizione valida
        bool posizioneValida = false;

        while (!posizioneValida) {
            // Genera coordinate casuali
            int newX = distribuzioneX(gen);
            int newY = distribuzioneY(gen);
            cibo = Posizione(newX, newY);

            // Verifica che il cibo non sia sul serpente
            posizioneValida = true;
            for (const auto& segmento : serpente) {
                if (segmento == cibo) {
                    posizioneValida = false;
                    break;
                }
            }
        }
    }

    /**
     * Verifica se una posizione è fuori dai bordi della griglia
     */
    bool èFuoriBordi(const Posizione& pos) const {
        return pos.getX() < 0 || pos.getX() >= larghezza ||
               pos.getY() < 0 || pos.getY() >= altezza;
    }

    /**
     * Verifica se il serpente collide con se stesso
     */
    bool verificaCollisione() const {
        // La testa è serpente.front()
        // Iniziamo da 1 per evitare di controllare la testa contro se stessa
        for (size_t i = 1; i < serpente.size(); ++i) {
            if (serpente[0] == serpente[i]) {
                return true;
            }
        }
        return false;
    }

    /**
     * Calcola la nuova posizione della testa basata sulla direzione
     */
    Posizione calcolaNuovaTesta() const {
        Posizione testa = serpente.front();
        int newX = testa.getX();
        int newY = testa.getY();

        // Aggiorna le coordinate in base alla direzione
        switch (direzione) {
            case SU:        newY--; break;
            case GIU:       newY++; break;
            case SINISTRA:  newX--; break;
            case DESTRA:    newX++; break;
        }

        return Posizione(newX, newY);
    }

public:
    // ==================== METODI PUBBLICI (INTERFACCIA) ====================

    /**
     * Costruttore: inizializza il gioco
     *
     * Concetto: Il costruttore inizializza l'oggetto in uno stato valido
     * Usa la lista di inizializzazione per i membri
     */
    GiocoSnake(int w, int h)
        : larghezza(w),
          altezza(h),
          direzione(DESTRA),
          giocoTerminato(false),
          punteggio(0),
          gen(rd()),
          distribuzioneX(0, w - 1),
          distribuzioneY(0, h - 1) {

        // Inizializza il serpente al centro della griglia
        int startX = w / 2;
        int startY = h / 2;
        serpente.push_back(Posizione(startX, startY));
        serpente.push_back(Posizione(startX - 1, startY));
        serpente.push_back(Posizione(startX - 2, startY));

        // Genera il primo cibo
        generaCibo();
    }

    /**
     * Distruttore: pulizia delle risorse
     *
     * Concetto: Il distruttore viene chiamato quando l'oggetto viene distrutto
     * In questo caso semplice, non abbiamo risorse da liberare
     */
    ~GiocoSnake() {
        // Nessuna risorsa da pulire (no memoria dinamica, no file aperti)
        // In C++ moderno, usiamo smart pointers per gestire la memoria automaticamente
    }

    /**
     * Aggiorna lo stato del gioco di un frame
     *
     * Questo metodo implementa la "logica di gioco" core
     */
    void aggiorna() {
        if (giocoTerminato) {
            return;
        }

        // Calcola la nuova posizione della testa
        Posizione nuovaTesta = calcolaNuovaTesta();

        // Verifica collisioni
        if (èFuoriBordi(nuovaTesta)) {
            giocoTerminato = true;
            return;
        }

        // Aggiungi temporaneamente la nuova testa per verificare la collisione
        serpente.push_front(nuovaTesta);

        if (verificaCollisione()) {
            giocoTerminato = true;
            return;
        }

        // Verifica se il serpente ha mangiato il cibo
        if (nuovaTesta == cibo) {
            // Ha mangiato: incrementa il punteggio e genera nuovo cibo
            punteggio += 10;
            generaCibo();
            // NON rimuoviamo la coda: il serpente cresce
        } else {
            // Non ha mangiato: rimuoviamo la coda per mantenere la lunghezza
            serpente.pop_back();
        }
    }

    /**
     * Processa l'input dell'utente
     *
     * Concetto: Separazione tra input processing e game logic
     */
    void processaInput(char tasto) {
        // Evita di andare nella direzione opposta (suicide prevention)
        switch (tasto) {
            case 'w': case 'W':
                if (direzione != GIU) direzione = SU;
                break;
            case 's': case 'S':
                if (direzione != SU) direzione = GIU;
                break;
            case 'a': case 'A':
                if (direzione != DESTRA) direzione = SINISTRA;
                break;
            case 'd': case 'D':
                if (direzione != SINISTRA) direzione = DESTRA;
                break;
            case 'q': case 'Q':
                giocoTerminato = true;
                break;
        }
    }

    /**
     * Renderizza il gioco nella console
     *
     * Concetto: Separazione tra logica e visualizzazione (MVC pattern)
     * Questo metodo si occupa solo della "View", non della logica
     */
    void renderizza() const {
        // Pulisci lo schermo (platform-specific)
        // Su Windows: system("cls")
        // Su Unix: system("clear")
        // Per compatibilità, usiamo solo nuove righe

        // Header del gioco
        cout << "\n\n";
        cout << "============================================\n";
        cout << "          SNAKE GAME - C++ ENGINE          \n";
        cout << "============================================\n";
        cout << "Punteggio: " << punteggio << "\n\n";

        // Disegna la griglia
        for (int y = 0; y < altezza; ++y) {
            // Disegna il bordo superiore
            if (y == 0) {
                cout << "+";
                for (int x = 0; x < larghezza; ++x) {
                    cout << "---";
                }
                cout << "+\n";
            }

            // Disegna la riga
            cout << "|";
            for (int x = 0; x < larghezza; ++x) {
                Posizione current(x, y);

                // Verifica cosa c'è in questa posizione
                bool trovato = false;

                // È la testa del serpente?
                if (serpente.front() == current) {
                    cout << " O ";  // Testa
                    trovato = true;
                }
                // È un segmento del corpo?
                else if (std::find(serpente.begin() + 1, serpente.end(), current)
                         != serpente.end()) {
                    cout << " o ";  // Corpo
                    trovato = true;
                }
                // È il cibo?
                else if (cibo == current) {
                    cout << " * ";  // Cibo
                    trovato = true;
                }
                // Spazio vuoto
                else {
                    cout << "   ";
                }
            }
            cout << "|\n";

            // Disegna il bordo inferiore
            if (y == altezza - 1) {
                cout << "+";
                for (int x = 0; x < larghezza; ++x) {
                    cout << "---";
                }
                cout << "+\n";
            }
        }

        // Istruzioni di gioco
        cout << "\nControlli:\n";
        cout << "  W/A/S/D - Muovi il serpente\n";
        cout << "  Q - Esci dal gioco\n";
        cout << "\nPremi un tasto per continuare...\n";
    }

    /**
     * Verifica se il gioco è terminato
     *
     * Concetto: Getter method - fornisce accesso allo stato interno
     */
    bool èTerminato() const {
        return giocoTerminato;
    }

    /**
     * Ottieni il punteggio
     */
    int getPunteggio() const {
        return punteggio;
    }
};

/**
 * ============================================================================
 * FUNZIONE: main
 * ============================================================================
 *
 * Punto di ingresso del programma
 *
 * Concetti dimostrati:
 * - Gestione del flusso del programma
 * - Loop di gioco (game loop)
 * - Gestione dell'input utente
 * - I/O stream
 * ============================================================================
 */
int main() {
    // Configurazione della console per UTF-8 (per Windows)
    // Questo permette di visualizzare correttamente i caratteri
    setlocale(LC_ALL, "");

    // Messaggio di benvenuto
    cout << "============================================\n";
    cout << "   SNAKE GAME - Motore di Gioco Console    \n";
    cout << "   C++ Moderno (C++17) - OOP Demo          \n";
    cout << "============================================\n\n";

    cout << "Benvenuto nel Snake Game!\n";
    cout << "Questo progetto dimostra i concetti della programmazione\n";
    cout << "orientata agli oggetti in C++.\n\n";

    cout << "Premi INVIO per iniziare...";
    cin.get();

    // Crea l'istanza del gioco
    // La griglia è 20x15 per adattarsi bene alla console
    GiocoSnake gioco(20, 15);

    // ==================== GAME LOOP ====================
    // Il game loop è il cuore di ogni gioco
    // Structure: Update -> Render -> Repeat

    // Variabile per tracciare il tempo
    auto ultimoAggiornamento = std::chrono::steady_clock::now();
    const int FPS = 10;  // Frame per secondo
    const auto durataFrame = std::chrono::milliseconds(1000 / FPS);

    while (!gioco.èTerminato()) {
        // 1. INPUT
        // Verifica se c'è input disponibile
        if (_kbhit()) {  // Funzione Windows-specifica
            char tasto = _getch();
            gioco.processaInput(tasto);
        }

        // 2. UPDATE
        // Aggiorna la logica di gioco a intervalli regolari
        auto ora = std::chrono::steady_clock::now();
        auto tempoTrascorso = ora - ultimoAggiornamento;

        if (tempoTrascorso >= durataFrame) {
            gioco.aggiorna();
            ultimoAggiornamento = ora;
        }

        // 3. RENDER
        // Disegna lo stato corrente del gioco
        gioco.renderizza();

        // Piccola pausa per evitare di consumare troppo CPU
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    // ==================== GAME OVER ====================
    cout << "\n\n============================================\n";
    cout << "              GIOCO TERMINATO!             \n";
    cout << "============================================\n";
    cout << "Punteggio finale: " << gioco.getPunteggio() << "\n";
    cout << "\nGrazie per aver giocato!\n";

    // Concetto C++: return 0 indica esecuzione riuscita
    return 0;
}

/**
 * ============================================================================
 * NOTE EDUCATIVE PER STUDENTI
 * ============================================================================
 *
 * CONCETTI OOP DIMOSTRATI:
 *
 * 1. ENCAPSULATION (Incapsulamento):
 *    - Tutti i dati membri sono privati (private)
 *    - L'accesso ai dati avviene tramite metodi pubblici (getter/setter)
 *    - L'implementazione interna è nascosta all'utente della classe
 *
 * 2. ABSTRACTION (Astrazione):
 *    - Le classi nascondono complessità dietro interfacce semplici
 *    - L'utente di GiocoSnake non deve sapere come è memorizzato il serpente
 *
 * 3. CLASSI & OGGETTI:
 *    - Posizione: semplice value object
 *    - GiocoSnake: gestisce la logica completa del gioco
 *    - Ogni istanza ha il proprio stato indipendente
 *
 * 4. COSTRUTTORI & DISTRUTTORI:
 *    - Il costruttore inizializza l'oggetto
 *    - Il distruttore pulisce le risorse
 *    - Usa la lista di inizializzazione per efficienza
 *
 * 5. OPERATOR OVERLOADING:
 *    - Ridefinizione dell'operatore == per confrontare posizioni
 *    - Rende il codice più naturale e leggibile
 *
 * CONCETTI C++ MODERNI:
 *
 * 1. STL (Standard Template Library):
 *    - deque: container efficiente per operazioni all'inizio/fine
 *    - vector: container dinamico per array ridimensionabili
 *    - random: generatore di numeri casuali moderno (C++11+)
 *
 * 2. SMART POINTERS (menzionati):
 *    - In C++ moderno, preferisci smart pointers (unique_ptr, shared_ptr)
 *    - Gestione automatica della memoria
 *
 * 3. AUTO TYPE DEDUCTION:
 *    - auto keyword: il compilatore deduce il tipo automaticamente
 *    - Riduce la verbosità del codice
 *
 * 4. CHRONO LIBRARY:
 *    - Gestione moderna del tempo
 *    - Type-safe e precisione garantita
 *
 * 5. REFERENCE SEMANTICS:
 *    - Passaggio per riferimento (const T&) per efficienza
 *    - Evita copie non necessarie di oggetti
 *
 * BEST PRACTICES:
 *
 * 1. const CORRETNESS:
 *    - Marca i metodi che non modificano lo stato come const
 *    - Permette ottimizzazioni del compilatore
 *    - Rende il codice più chiaro e sicuro
 *
 * 2. SEPARATION OF CONCERNS:
 *    - Logica separata dalla visualizzazione
 *    - Input processing separato dalla logica
 *    - Ogni classe/metodo ha una singola responsabilità
 *
 * 3. MODERN C++ STYLE:
 *    - Preferisci member initialization list
 *    - Usa {} initialization quando possibile
 *    - Evita raw pointers, usa smart pointers
 *
 * PER APPROFONDIRE:
 *
 * - Design Patterns: Singleton, Factory, Observer
 * - STL Algorithms: std::find, std::for_each, std::transform
 * - Lambda expressions (C++11+)
 * - Move semantics (C++11+)
 * - Template metaprogramming
 *
 * ============================================================================
 */
