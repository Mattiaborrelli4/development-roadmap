/**
 * @file engine.h
 * @brief Engine di gioco principale con sistemi e game loop
 */

#ifndef ENGINE_H
#define ENGINE_H

#include "entity.h"
#include <chrono>
#include <map>
#include <windows.h>
#include <conio.h>

namespace GameEngine {

/**
 * @class InputSystem
 * @brief Sistema per gestire l'input da tastiera
 */
class InputSystem {
private:
    std::map<int, bool> keyStates;
    std::map<int, bool> previousKeyStates;

public:
    // Codici tasti
    static const int KEY_W = 119;
    static const int KEY_A = 97;
    static const int KEY_S = 115;
    static const int KEY_D = 100;
    static const int KEY_UP = 72;
    static const int KEY_DOWN = 80;
    static const int KEY_LEFT = 75;
    static const int KEY_RIGHT = 77;
    static const int KEY_SPACE = 32;
    static const int KEY_ESCAPE = 27;
    static const int KEY_ENTER = 13;

    InputSystem() {}

    // Aggiorna stati dei tasti
    void update() {
        previousKeyStates = keyStates;

        //_kbhit() controlla se c'è input disponibile
        while (_kbhit()) {
            int key = _getch();
            keyStates[key] = true;
        }

        // Resetta stati dei tasti (per input istantaneo)
        for (auto& pair : keyStates) {
            if (!previousKeyStates[pair.first]) {
                // Key pressed this frame
            }
            keyStates[pair.first] = false;
        }
    }

    // Controlla se un tasto è premuto
    bool isKeyPressed(int key) const {
        auto it = keyStates.find(key);
        return it != keyStates.end() && it->second;
    }

    // Controlla se un tasto è giù premuto
    bool isKeyDown(int key) const {
        return isKeyPressed(key);
    }
};

/**
 * @class PhysicsSystem
 * @brief Sistema per fisica base e collisioni
 */
class PhysicsSystem {
public:
    // Aggiorna posizioni basate su velocità
    void update(EntityManager& entityManager, float deltaTime) {
        auto entities = entityManager.getActiveEntities();

        for (auto* entity : entities) {
            if (!entity->active) continue;

            auto* pos = entity->getComponent<PositionComponent>();
            auto* vel = entity->getComponent<VelocityComponent>();

            if (pos && vel) {
                // Applica velocità alla posizione
                pos->position += vel->velocity * deltaTime;
            }
        }
    }

    // Collision detection AABB (Axis-Aligned Bounding Box)
    bool checkCollision(Entity* a, Entity* b) {
        if (!a->active || !b->active) return false;

        auto* colA = a->getComponent<ColliderComponent>();
        auto* colB = b->getComponent<ColliderComponent>();
        auto* posA = a->getComponent<PositionComponent>();
        auto* posB = b->getComponent<PositionComponent>();

        if (!colA || !colB || !posA || !posB) return false;

        // Calcola bounding box
        float aLeft = posA->position.x;
        float aRight = posA->position.x + colA->size.x;
        float aTop = posA->position.y;
        float aBottom = posA->position.y + colA->size.y;

        float bLeft = posB->position.x;
        float bRight = posB->position.x + colB->size.x;
        float bTop = posB->position.y;
        float bBottom = posB->position.y + colB->size.y;

        // Controlla sovrapposizione
        return (aLeft < bRight && aRight > bLeft &&
                aTop < bBottom && aBottom > bTop);
    }

    // Trova tutte le collisioni per un'entità
    std::vector<Entity*> getCollisions(Entity* entity, EntityManager& entityManager) {
        std::vector<Entity*> collisions;
        auto entities = entityManager.getActiveEntities();

        for (auto* other : entities) {
            if (entity->id != other->id && checkCollision(entity, other)) {
                collisions.push_back(other);
            }
        }

        return collisions;
    }
};

/**
 * @class RenderSystem
 * @brief Sistema per renderizzare su console
 */
class RenderSystem {
private:
    int width;
    int height;
    std::vector<std::vector<char>> buffer;
    std::vector<std::vector<int>> colorBuffer;
    HANDLE consoleHandle;

public:
    RenderSystem(int w, int h) : width(w), height(h) {
        buffer.resize(height, std::vector<char>(width, ' '));
        colorBuffer.resize(height, std::vector<int>(width, 7));

        // Setup console
        consoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);
        CONSOLE_CURSOR_INFO cursorInfo;
        GetConsoleCursorInfo(consoleHandle, &cursorInfo);
        cursorInfo.bVisible = FALSE;
        SetConsoleCursorInfo(consoleHandle, &cursorInfo);

        // Imposta dimensioni console
        COORD bufferSize = {static_cast<SHORT>(width), static_cast<SHORT>(height + 5)};
        SetConsoleScreenBufferSize(consoleHandle, bufferSize);

        SMALL_RECT windowSize = {0, 0, static_cast<SHORT>(width - 1), static_cast<SHORT>(height + 4)};
        SetConsoleWindowInfo(consoleHandle, TRUE, &windowSize);
    }

    // Pulisci buffer
    void clear() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                buffer[y][x] = ' ';
                colorBuffer[y][x] = 7;
            }
        }
    }

    // Disegna entità
    void drawEntity(Entity* entity) {
        if (!entity->active) return;

        auto* pos = entity->getComponent<PositionComponent>();
        auto* sprite = entity->getComponent<SpriteComponent>();
        auto* col = entity->getComponent<ColliderComponent>();

        if (!pos || !sprite) return;

        int entityWidth = 1;
        int entityHeight = 1;

        if (col) {
            entityWidth = static_cast<int>(col->size.x);
            entityHeight = static_cast<int>(col->size.y);
        }

        // Disegna entità nel buffer
        for (int dy = 0; dy < entityHeight && dy < height; dy++) {
            for (int dx = 0; dx < entityWidth && dx < width; dx++) {
                int x = static_cast<int>(pos->position.x) + dx;
                int y = static_cast<int>(pos->position.y) + dy;

                if (x >= 0 && x < width && y >= 0 && y < height) {
                    buffer[y][x] = sprite->character;
                    colorBuffer[y][x] = sprite->color;
                }
            }
        }
    }

    // Disegna UI
    void drawUI(int fps, int entityCount) {
        // FPS counter in alto a sinistra
        std::string fpsText = "FPS: " + std::to_string(fps);
        std::string countText = "Entities: " + std::to_string(entityCount);
        std::string controlsText = "WASD/Arrows: Move | ESC: Exit";

        SetConsoleTextAttribute(consoleHandle, 14); // Giallo
        COORD pos = {0, 0};
        SetConsoleCursorPosition(consoleHandle, pos);
        std::cout << std::setw(width) << std::left << fpsText;

        pos.Y = 1;
        SetConsoleCursorPosition(consoleHandle, pos);
        std::cout << std::setw(width) << std::left << countText;

        pos.Y = height + 2;
        SetConsoleCursorPosition(consoleHandle, pos);
        std::cout << std::setw(width) << std::left << controlsText;
    }

    // Renderizza buffer su console
    void present() {
        COORD pos;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                pos.X = x;
                pos.Y = y + 2; // Offset per spazio UI
                SetConsoleCursorPosition(consoleHandle, pos);
                SetConsoleTextAttribute(consoleHandle, colorBuffer[y][x]);
                std::cout << buffer[y][x];
            }
        }
        SetConsoleTextAttribute(consoleHandle, 7); // Reset a bianco
    }

    // Disegna bordo
    void drawBorder() {
        SetConsoleTextAttribute(consoleHandle, 8); // Grigio

        // Linee orizzontali
        for (int x = 0; x < width; x++) {
            COORD pos;
            pos.X = x;
            pos.Y = 2;
            SetConsoleCursorPosition(consoleHandle, pos);
            std::cout << "-";

            pos.Y = height + 1;
            SetConsoleCursorPosition(consoleHandle, pos);
            std::cout << "-";
        }

        // Linee verticali
        for (int y = 2; y <= height + 1; y++) {
            COORD pos;
            pos.X = 0;
            pos.Y = y;
            SetConsoleCursorPosition(consoleHandle, pos);
            std::cout << "|";

            pos.X = width;
            SetConsoleCursorPosition(consoleHandle, pos);
            std::cout << "|";
        }

        // Angoli
        SetConsoleTextAttribute(consoleHandle, 7);
    }

    int getWidth() const { return width; }
    int getHeight() const { return height; }
};

/**
 * @class Engine
 * @brief Engine principale con game loop
 */
class Engine {
private:
    EntityManager entityManager;
    InputSystem inputSystem;
    PhysicsSystem physicsSystem;
    std::unique_ptr<RenderSystem> renderSystem;

    bool running;
    float targetFPS;

    std::chrono::high_resolution_clock::time_point lastFrameTime;
    int currentFPS;
    int frameCount;
    float fpsTimer;

public:
    Engine(int width, int height, float fps = 60.0f)
        : running(false), targetFPS(fps), currentFPS(0), frameCount(0), fpsTimer(0.0f) {

        renderSystem = std::make_unique<RenderSystem>(width, height);
        lastFrameTime = std::chrono::high_resolution_clock::now();
    }

    // Avvia il game loop
    void run() {
        running = true;
        lastFrameTime = std::chrono::high_resolution_clock::now();

        while (running) {
            // Calcola delta time
            auto currentTime = std::chrono::high_resolution_clock::now();
            std::chrono::duration<float> deltaTime = currentTime - lastFrameTime;
            lastFrameTime = currentTime;

            float dt = deltaTime.count();

            // Limita delta time per evitare salti enormi
            if (dt > 0.1f) dt = 0.1f;

            // Calcola FPS
            frameCount++;
            fpsTimer += dt;
            if (fpsTimer >= 1.0f) {
                currentFPS = frameCount;
                frameCount = 0;
                fpsTimer = 0.0f;
            }

            // Update
            update(dt);

            // Render
            render();

            // Cap FPS
            float frameTime = 1000.0f / targetFPS;
            std::chrono::duration<float, std::milli> elapsed =
                std::chrono::high_resolution_clock::now() - currentTime;
            if (elapsed.count() < frameTime) {
                std::this_thread::sleep_for(
                    std::chrono::duration<float, std::milli>(frameTime - elapsed.count())
                );
            }
        }
    }

    // Stop engine
    void stop() {
        running = false;
    }

    // Update loop
    void update(float deltaTime) {
        // Input
        inputSystem.update();

        // Esci con ESC
        if (inputSystem.isKeyPressed(InputSystem::KEY_ESCAPE)) {
            stop();
            return;
        }

        // Physics
        physicsSystem.update(entityManager, deltaTime);

        // Custom update override
        onUpdate(deltaTime);
    }

    // Render loop
    void render() {
        renderSystem->clear();

        // Disegna tutte le entità
        auto entities = entityManager.getActiveEntities();
        for (auto* entity : entities) {
            renderSystem->drawEntity(entity);
        }

        // Disegna UI
        renderSystem->drawUI(currentFPS, entityManager.getActiveCount());

        // Present
        renderSystem->present();
    }

    // Metodi accessor
    EntityManager& getEntityManager() { return entityManager; }
    InputSystem& getInputSystem() { return inputSystem; }
    PhysicsSystem& getPhysicsSystem() { return physicsSystem; }
    RenderSystem& getRenderSystem() { return *renderSystem; }

    // Override per custom logic
    virtual void onUpdate(float deltaTime) {}
    virtual void onInit() {}
};

} // namespace GameEngine

#endif // ENGINE_H
