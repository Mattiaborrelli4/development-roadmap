# 2D Game Engine

Un motore di gioco 2D scritto in C++17 con rendering su console e Entity-Component System (ECS).

## Caratteristiche

### Core Systems
- **Vec2**: Struttura vettoriale 2D con operatori aritmetici completi
- **Entity-Component System (ECS)**: Architettura flessibile per game objects
- **Physics System**: Fisica base con movimento e collisioni
- **Render System**: Rendering console-based con buffer e colori
- **Input System**: Gestione input da tastiera in tempo reale
- **Game Loop**: Loop principale con delta time per frame-rate indipendente

### Componenti Disponibili
- `PositionComponent`: Posizione dell'entità (Vec2)
- `VelocityComponent`: Velocità dell'entità (Vec2)
- `SpriteComponent`: Aspetto visuale (carattere + colore)
- `ColliderComponent`: AABB collision box per rilevamento collisioni
- `InputComponent`: Controlli input per entità giocabile

### Funzionalità
- Collision detection AABB (Axis-Aligned Bounding Box)
- Rendering console con supporto colori
- FPS counter e entity counter UI
- Sistema di coordinate mondo
- Boundary checking per confini schermo
- Input multi-tasto simultaneo

## Struttura Progetto

```
game-engine-2d/
├── vec2.h          # Struttura Vec2 per matematica vettoriale
├── entity.h        # ECS: Entity, Componenti, EntityManager
├── engine.h        # Engine, Systems, Game loop
├── main.cpp        # Gioco di esempio
└── README.md       # Questo file
```

## Requisiti

- **Compilatore**: C++17 compatibile (MSVC, GCC, Clang)
- **OS**: Windows (per console rendering)
- **Librerie**: Standard Library solo

## Compilazione

### MinGW/G++
```bash
g++ -std=c++17 main.cpp -o game.exe -lkernel32 -static-libgcc -static-libstdc++
```

### MSVC (Visual Studio)
```bash
cl /EHsc /std:c++17 main.cpp
```

### CMake (opzionale)
```cmake
cmake_minimum_required(VERSION 3.10)
project(GameEngine2D)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(game main.cpp)
target_link_libraries(game kernel32)
```

## Utilizzo

### Gioco Demo
Il progetto include un gioco demo completo con:
- **@**: Giocatore (controllabile con WASD o frecce)
- **X**: Nemici (rossi, si muovono e rimbalzano)
- **$**: Monete da raccogliere (gialle)

**Obiettivo**: Raccogli quante più monete possibili evitando i nemici!

### Creare un Gioco Custom

```cpp
#include "engine.h"
using namespace GameEngine;

class MyGame : public Engine {
public:
    MyGame(int width, int height) : Engine(width, height) {}

    void init() {
        // Crea entità giocatore
        auto* player = getEntityManager().createEntity();
        player->addComponent<PositionComponent>()->position = Vec2(10.0f, 10.0f);
        player->addComponent<VelocityComponent>();
        player->addComponent<SpriteComponent>()->character = 'P';
        player->addComponent<ColliderComponent>()->size = Vec2(1.0f, 1.0f);
        player->addComponent<InputComponent>()->speed = 10.0f;
    }

    void onUpdate(float deltaTime) override {
        // Logica di gioco personalizzata
        auto entities = getEntityManager().getActiveEntities();

        for (auto* entity : entities) {
            // Aggiorna entità
        }
    }
};

int main() {
    MyGame game(80, 30);
    game.init();
    game.run();
    return 0;
}
```

## Architettura ECS

### Entity
Le entità sono container "vuoti" con un ID unico:
```cpp
Entity* entity = entityManager.createEntity();
```

### Componenti
I componenti contengono dati puri:
```cpp
entity->addComponent<PositionComponent>()->position = Vec2(5.0f, 10.0f);
entity->addComponent<VelocityComponent>()->velocity = Vec2(1.0f, 0.0f);
entity->addComponent<SpriteComponent>()->character = '@';
```

### Sistemi
I sistemi operano su entità con componenti specifici:
```cpp
auto* pos = entity->getComponent<PositionComponent>();
auto* vel = entity->getComponent<VelocityComponent>();

if (pos && vel) {
    pos->position += vel->velocity * deltaTime;
}
```

## API Reference

### Vec2
```cpp
Vec2 v(3.0f, 4.0f);
v.length();           // 5.0
v.normalized();        // (0.6, 0.8)
v.distanceTo(other);   // Distanza euclidea
v.dot(other);          // Prodotto scalare

// Operatori
v + other;            // Addizione
v - other;            // Sottrazione
v * 2.0f;             // Moltiplicazione scalare
```

### Engine
```cpp
Engine game(width, height, fps);

// Accesso ai sistemi
game.getEntityManager();
game.getInputSystem();
game.getPhysicsSystem();
game.getRenderSystem();
```

### PhysicsSystem
```cpp
// Collision detection
bool collides = physics.checkCollision(entityA, entityB);

// Trova collisioni
auto collisions = physics.getCollisions(entity, entityManager);
```

### InputSystem
```cpp
// Controlla input
if (input.isKeyPressed(InputSystem::KEY_W)) {
    // Muovi su
}

// Tasti disponibili
InputSystem::KEY_W / A / S / D
InputSystem::KEY_UP / DOWN / LEFT / RIGHT
InputSystem::KEY_SPACE
InputSystem::KEY_ESCAPE
InputSystem::KEY_ENTER
```

## Codici Colore Console

```
0 = Nero        8 = Grigio scuro
1 = Blu         9 = Blu chiaro
2 = Verde       10 = Verde chiaro
3 = Ciano       11 = Ciano chiaro
4 = Rosso       12 = Rosso chiaro
5 = Magenta     13 = Magenta chiaro
6 = Giallo scuro 14 = Giallo
7 = Bianco      15 = Bianco brillante
```

## Performance

- Target FPS: 60 (configurabile)
- Delta time per movimento frame-rate indipendente
- Rendering ottimizzato con buffer
- ECS per cache-friendly data access

## Limitazioni

- Windows-only (per WinAPI console)
- Rendering testuale semplice (pixel = carattere)
- Nessun audio
- Nessun networking
- Physics base (no gravity, friction advanced)

## Estensioni Possibili

- **Audio**: Sistema sound con Beep() o libreria esterna
- **Grafica**: Supporto bitmap/ASCII art
- **Physics**: Gravity, friction, rotazione
- **AI**: Pathfinding (A*), state machine
- **Networking**: Multiplayer
- **Scripting**: Lua/Python integration
- **Assets**: Loader per sprites, mappe

## License

Questo progetto è a scopo educativo. Codice libero per uso personale e commerciale.

## Autore

Creato come progetto portfolio per C++ Game Development.

---

Buon sviluppo! 🎮
