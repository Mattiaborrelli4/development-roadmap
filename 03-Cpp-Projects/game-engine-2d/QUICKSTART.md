# Quick Start - 2D Game Engine

## Compilazione Rapida (3 Modi)

### 1. Batch Script (Consigliato)
```bash
build.bat
```

### 2. G++ Diretto
```bash
g++ -std=c++17 main.cpp -o game.exe -static-libgcc -static-libstdc++
game.exe
```

### 3. Makefile
```bash
mingw32-make
mingw32-make run
```

## Primi Passi

### 1. Compila e Esegui
```bash
build.bat
```

### 2. Gioca la Demo
- Usa **WASD** o **frecce** per muoverti
- Raccogli le **$** monete
- Evita i **X** nemici rossi
- Premi **ESC** per uscire

### 3. Esplora il Codice

**Guarda `main.cpp`** per vedere come:
- Creare entità
- Aggiungere componenti
- Gestire input
- Rilevare collisioni
- Implementare game logic

**Guarda i file `.h` per l'API**:
- `vec2.h` - Matematica vettoriale
- `entity.h` - ECS (Entity-Component System)
- `engine.h` - Sistemi e game loop

## Creare il Tuo Gioco

### Step 1: Crea una Classe Game
```cpp
class MyGame : public Engine {
public:
    MyGame(int w, int h) : Engine(w, h) {}

    void init() {
        // Setup iniziale
    }

    void onUpdate(float dt) override {
        // Logica di gioco
    }
};
```

### Step 2: Crea Entità
```cpp
void init() {
    auto* player = getEntityManager().createEntity();

    // Aggiungi componenti
    player->addComponent<PositionComponent>()->position = Vec2(10, 10);
    player->addComponent<VelocityComponent>();
    player->addComponent<SpriteComponent>()->character = 'P';
    player->addComponent<ColliderComponent>()->size = Vec2(1, 1);
    player->addComponent<InputComponent>()->speed = 10.0f;
}
```

### Step 3: Implementa Logica
```cpp
void onUpdate(float dt) override {
    auto entities = getEntityManager().getActiveEntities();

    for (auto* entity : entities) {
        // Aggiorna entità
        auto* pos = entity->getComponent<PositionComponent>();
        auto* vel = entity->getComponent<VelocityComponent>();

        if (pos && vel) {
            pos->position += vel->velocity * dt;
        }
    }
}
```

### Step 4: Esegui
```cpp
int main() {
    MyGame game(80, 30);
    game.init();
    game.run();
    return 0;
}
```

## Snippet Utili

### Input Handling
```cpp
auto& input = getInputSystem();

if (input.isKeyDown(InputSystem::KEY_W)) {
    // Muovi su
}

if (input.isKeyPressed(InputSystem::KEY_SPACE)) {
    // Azione una tantum
}
```

### Collision Detection
```cpp
auto& physics = getPhysicsSystem();

if (physics.checkCollision(player, enemy)) {
    // Collisione!
}

auto collisions = physics.getCollisions(player, getEntityManager());
for (auto* other : collisions) {
    // Gestisci ogni collisione
}
```

### Muovere un'Entità
```cpp
auto* pos = entity->getComponent<PositionComponent>();
auto* vel = entity->getComponent<VelocityComponent>();

if (pos && vel) {
    pos->position += vel->velocity * deltaTime;
}
```

### Disegnare UI
```cpp
auto& render = getRenderSystem();
render.drawUI(fps, entityCount);
```

## Codici Carattere Utili

```cpp
// Giocatore/Nemici
'@' - Giocatore
'X' - Nemico
'$' - Moneta/Oggetto
'#' - Muro
'*' - Proiettile
'.' - Effetto particella

// Box Drawing (UTF-8)
'─' │ '┌' '┐' '└' '┘' - Bordi
'█' - Blocco pieno
'░' - Blocco mezzo pieno
```

## Codici Colore

```cpp
sprite->color = 7;  // Default bianco

// Colori comuni
0  - Nero          8  - Grigio scuro
1  - Blu           9  - Blu chiaro
2  - Verde         10 - Verde chiaro
3  - Ciano         11 - Ciano chiaro
4  - Rosso         12 - Rosso chiaro
5  - Magenta       13 - Magenta chiaro
14 - Giallo
7  - Bianco        15 - Bianco brillante
```

## Problemi Comuni

### Errore: "g++ non trovato"
**Soluzione**: Installa MinGW-w64 da https://www.mingw-w64.org/

### Console troppo piccola
**Soluzione**: Clic destro sulla barra del titolo → Proprietà → Layout → aumentare dimensioni

### Caratteri strani
**Soluzione**: Imposta encoding console a UTF-8 (già nel codice)

### Movimento troppo veloce/lento
**Soluzione**: Adjust `speed` in InputComponent o usa delta time

## Risorse

- **README.md** - Documentazione completa
- **STRUCTURE.md** - Architettura dettagliata
- **Codice sorgente** - Commentato in italiano

---

Buon sviluppo! 🚀
