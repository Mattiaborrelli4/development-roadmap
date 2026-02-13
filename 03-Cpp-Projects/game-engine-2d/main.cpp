/**
 * @file main.cpp
 * @brief Gioco di esempio con il 2D Game Engine
 *
 * Un semplice gioco demo con:
 * - Giocatore controllabile (WASD o frecce)
 * - Nemici che si muovono
 * - Sistema di collisioni
 * - Raccolta di oggetti
 */

#include "engine.h"
#include <random>
#include <iostream>

using namespace GameEngine;

/**
 * @class Game
 * @brief Gioco di esempio che estende Engine
 */
class Game : public Engine {
private:
    Entity* player;
    std::vector<Entity*> enemies;
    std::vector<Entity*> collectibles;
    int score;
    std::mt19937 rng;

public:
    Game(int width, int height) : Engine(width, height), score(0) {
        std::random_device rd;
        rng = std::mt19937(rd());
    }

    // Inizializza il gioco
    void init() {
        // Crea giocatore
        player = getEntityManager().createEntity();
        player->addComponent<PositionComponent>()->position = Vec2(20.0f, 10.0f);
        player->addComponent<VelocityComponent>()->velocity = Vec2(0.0f, 0.0f);
        player->addComponent<SpriteComponent>()->character = '@';
        player->addComponent<ColliderComponent>()->size = Vec2(1.0f, 1.0f);
        player->addComponent<InputComponent>()->speed = 15.0f;

        // Crea nemici
        for (int i = 0; i < 5; i++) {
            spawnEnemy();
        }

        // Crea collectibles
        for (int i = 0; i < 10; i++) {
            spawnCollectible();
        }

        std::cout << "=== 2D Game Engine Demo ===" << std::endl;
        std::cout << "Controlli: WASD o frecce per muoversi" << std::endl;
        std::cout << "Obiettivo: Raccogli le monete ($), evita i nemici (X)" << std::endl;
        std::cout << "ESC per uscire" << std::endl;
        std::cout << "=========================" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    // Spawn nemico
    void spawnEnemy() {
        auto* enemy = getEntityManager().createEntity();

        std::uniform_int_distribution<int> xDist(0, getRenderSystem().getWidth() - 2);
        std::uniform_int_distribution<int> yDist(2, getRenderSystem().getHeight() - 1);

        enemy->addComponent<PositionComponent>()->position =
            Vec2(static_cast<float>(xDist(rng)), static_cast<float>(yDist(rng)));

        std::uniform_real_distribution<float> velDist(-5.0f, 5.0f);
        enemy->addComponent<VelocityComponent>()->velocity =
            Vec2(velDist(rng), velDist(rng));

        enemy->addComponent<SpriteComponent>()->character = 'X';
        enemy->addComponent<SpriteComponent>()->color = 12; // Rosso
        enemy->addComponent<ColliderComponent>()->size = Vec2(1.0f, 1.0f);

        enemies.push_back(enemy);
    }

    // Spawn collectible
    void spawnCollectible() {
        auto* collectible = getEntityManager().createEntity();

        std::uniform_int_distribution<int> xDist(1, getRenderSystem().getWidth() - 3);
        std::uniform_int_distribution<int> yDist(3, getRenderSystem().getHeight() - 2);

        collectible->addComponent<PositionComponent>()->position =
            Vec2(static_cast<float>(xDist(rng)), static_cast<float>(yDist(rng)));

        auto* sprite = collectible->addComponent<SpriteComponent>();
        sprite->character = '$';
        sprite->color = 14; // Giallo

        collectible->addComponent<ColliderComponent>()->size = Vec2(1.0f, 1.0f);

        collectibles.push_back(collectible);
    }

    // Update custom del gioco
    void onUpdate(float deltaTime) override {
        // Input giocatore
        auto* input = player->getComponent<InputComponent>();
        auto* vel = player->getComponent<VelocityComponent>();
        auto* pos = player->getComponent<PositionComponent>();

        if (input && vel && pos) {
            Vec2 movement(0.0f, 0.0f);

            if (getInputSystem().isKeyDown(InputSystem::KEY_W) ||
                getInputSystem().isKeyDown(InputSystem::KEY_UP)) {
                movement.y -= 1.0f;
            }
            if (getInputSystem().isKeyDown(InputSystem::KEY_S) ||
                getInputSystem().isKeyDown(InputSystem::KEY_DOWN)) {
                movement.y += 1.0f;
            }
            if (getInputSystem().isKeyDown(InputSystem::KEY_A) ||
                getInputSystem().isKeyDown(InputSystem::KEY_LEFT)) {
                movement.x -= 1.0f;
            }
            if (getInputSystem().isKeyDown(InputSystem::KEY_D) ||
                getInputSystem().isKeyDown(InputSystem::KEY_RIGHT)) {
                movement.x += 1.0f;
            }

            // Normalizza e applica speed
            if (movement.length() > 0.0f) {
                movement = movement.normalized() * input->speed;
                vel->velocity = movement;
            } else {
                vel->velocity = Vec2(0.0f, 0.0f);
            }

            // Boundary check giocatore
            int width = getRenderSystem().getWidth();
            int height = getRenderSystem().getHeight();

            if (pos->position.x < 1.0f) {
                pos->position.x = 1.0f;
                vel->velocity.x = 0;
            }
            if (pos->position.x > width - 2.0f) {
                pos->position.x = width - 2.0f;
                vel->velocity.x = 0;
            }
            if (pos->position.y < 3.0f) {
                pos->position.y = 3.0f;
                vel->velocity.y = 0;
            }
            if (pos->position.y > height - 1.0f) {
                pos->position.y = height - 1.0f;
                vel->velocity.y = 0;
            }
        }

        // AI nemici - movimento casuale e bounce
        for (auto* enemy : enemies) {
            if (!enemy->active) continue;

            auto* enemyPos = enemy->getComponent<PositionComponent>();
            auto* enemyVel = enemy->getComponent<VelocityComponent>();
            auto* enemyCol = enemy->getComponent<ColliderComponent>();

            if (enemyPos && enemyVel && enemyCol) {
                int width = getRenderSystem().getWidth();
                int height = getRenderSystem().getHeight();

                // Bounce sui bordi
                if (enemyPos->position.x <= 1.0f || enemyPos->position.x >= width - 2.0f) {
                    enemyVel->velocity.x *= -1;
                }
                if (enemyPos->position.y <= 3.0f || enemyPos->position.y >= height - 1.0f) {
                    enemyVel->velocity.y *= -1;
                }

                // Clamp posizione
                enemyPos->position.x = std::max(1.0f, std::min(enemyPos->position.x, width - 2.0f));
                enemyPos->position.y = std::max(3.0f, std::min(enemyPos->position.y, height - 1.0f));
            }
        }

        // Collision detection: Player vs Collectibles
        auto& physics = getPhysicsSystem();
        for (auto* collectible : collectibles) {
            if (!collectible->active) continue;

            if (physics.checkCollision(player, collectible)) {
                collectible->active = false;
                score += 10;

                // Spawn nuovo collectible
                spawnCollectible();

                // Aumenta difficoltà ogni 50 punti
                if (score % 50 == 0) {
                    spawnEnemy();
                }
            }
        }

        // Collision detection: Player vs Enemies
        for (auto* enemy : enemies) {
            if (!enemy->active) continue;

            if (physics.checkCollision(player, enemy)) {
                // Game over - reset gioco
                resetGame();
                break;
            }
        }
    }

    // Reset gioco
    void resetGame() {
        // Pulisci tutto
        for (auto* e : enemies) {
            e->active = false;
        }
        for (auto* c : collectibles) {
            c->active = false;
        }

        enemies.clear();
        collectibles.clear();
        getEntityManager().cleanup();

        // Reset giocatore
        player->getComponent<PositionComponent>()->position = Vec2(20.0f, 10.0f);
        player->getComponent<VelocityComponent>()->velocity = Vec2(0.0f, 0.0f);
        score = 0;

        // Respawn
        for (int i = 0; i < 5; i++) {
            spawnEnemy();
        }
        for (int i = 0; i < 10; i++) {
            spawnCollectible();
        }
    }

    int getScore() const { return score; }
};

int main() {
    try {
        // Imposta console
        SetConsoleOutputCP(CP_UTF8);

        // Crea gioco (80x30 console)
        Game game(80, 30);

        // Inizializza
        game.init();

        // Esegui game loop
        game.run();

        std::cout << "\n\n=== Game Over ===" << std::endl;
        std::cout << "Grazie per aver giocato!" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Errore: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
