# 2D Game Engine - Struttura Progetto

## File Creati

### Core Engine
- **vec2.h** (97 righe)
  - Struttura Vec2 per matematica vettoriale 2D
  - Operatori: +, -, *, /, +=, -=, *=
  - Metodi: length(), normalized(), distanceTo(), dot()

- **entity.h** (175 righe)
  - Entity-Component System (ECS)
  - Componenti: Position, Velocity, Sprite, Collider, Input
  - Entity class con ID unico e gestione componenti
  - EntityManager per gestione lifecycle entità

- **engine.h** (430 righe)
  - InputSystem: Gestione tastiera in tempo reale
  - PhysicsSystem: Fisica base + collisioni AABB
  - RenderSystem: Rendering console con buffer e colori
  - Engine: Game loop con delta time, FPS cap

### Gioco Esempio
- **main.cpp** (220 righe)
  - Game class che estende Engine
  - Demo gioco completo con:
    * Giocatore controllabile (@)
    * Nemici con AI (X)
    * Sistema di punteggio
    * Collision detection
    * Respawn e difficulty progression

### Build System
- **CMakeLists.txt**: CMake configuration
- **Makefile**: MinGW make build
- **build.bat**: Windows batch script
- **.gitignore**: Git ignore rules

### Documentazione
- **README.md**: Documentazione completa in italiano

## Caratteristiche Tecniche

### ECS Architecture
```
Entity (ID + Active)
  └─ PositionComponent (Vec2)
  └─ VelocityComponent (Vec2)
  └─ SpriteComponent (char + color)
  └─ ColliderComponent (size + trigger)
  └─ InputComponent (speed)
```

### Game Loop
```
1. Calculate Delta Time
2. Update FPS counter
3. Input System Update
4. Physics System Update
5. Custom Game Logic (onUpdate)
6. Render System Clear
7. Render Entities
8. Draw UI
9. Present Buffer
10. Sleep (FPS Cap)
```

### Systems
- **Input**: Real-time keyboard polling
- **Physics**: Velocity integration + AABB collision
- **Render**: Double-buffered console rendering
- **Game Logic**: Virtual onUpdate() override

## Come Compilare

### Opzione 1: build.bat (Più Semplice)
```bash
build.bat
```

### Opzione 2: g++ Manual
```bash
g++ -std=c++17 main.cpp -o game.exe -static-libgcc -static-libstdc++
```

### Opzione 3: Makefile
```bash
mingw32-make
./game.exe
```

### Opzione 4: CMake
```bash
mkdir build
cd build
cmake ..
cmake --build .
./bin/game.exe
```

### Opzione 5: MSVC
```bash
cl /EHsc /std:c++17 main.cpp
main.exe
```

## Come Giocare

### Controlli
- **W/↑**: Muovi su
- **S/↓**: Muovi giù
- **A/←**: Muovi a sinistra
- **D/→**: Muovi a destra
- **ESC**: Esci dal gioco

### Gameplay
1. Controlli **@** (il giocatore)
2. Raccogli **$** (monete) per punti
3. Evita **X** (nemici rossi)
4. Ogni 50 punti: nuovo nemico
5. Tocchi un nemico = game over, reset

## API Quick Reference

### Creare Entità
```cpp
auto* entity = entityManager.createEntity();
entity->addComponent<PositionComponent>()->position = Vec2(x, y);
entity->addComponent<VelocityComponent>()->velocity = Vec2(vx, vy);
entity->addComponent<SpriteComponent>()->character = '@';
```

### Controllare Collisioni
```cpp
if (physics.checkCollision(entityA, entityB)) {
    // Handle collision
}
```

### Input Handling
```cpp
if (input.isKeyDown(InputSystem::KEY_W)) {
    // Move up
}
```

### Custom Game Loop
```cpp
class MyGame : public Engine {
    void onUpdate(float deltaTime) override {
        // Your game logic
    }
};
```

## Estendere l'Engine

### Aggiungere Componente
```cpp
struct HealthComponent {
    int current;
    int maximum;
};
```

### Aggiungere Sistema
```cpp
class AISystem {
public:
    void update(EntityManager& em, float dt) {
        // AI logic
    }
};
```

### Nuovi Livelli
```cpp
void loadLevel(int level) {
    // Clear entities
    // Spawn new entities
    // Set difficulty
}
```

## Note Tecniche

### Performance
- 60 FPS target
- Frame-rate indipendente con delta time
- ECS per cache efficiency
- Double-buffered rendering

### Limitazioni
- Windows only (WinAPI console)
- Rendering testuale
- No audio
- Physics base

### Possibili Miglioramenti
- Sprite rendering avanzato (ASCII art)
- Audio system
- Save/Load game
- Level editor
- Particle system
- Networking
- Scripting (Lua/Python)

---

Progetto creato con successo! Tutti i file sono pronti.
