/**
 * @file entity.h
 * @brief Entity-Component System (ECS) base
 */

#ifndef ENTITY_H
#define ENTITY_H

#include <vector>
#include <memory>
#include "vec2.h"

namespace GameEngine {

// ID unico per le entità
using EntityID = unsigned int;

// Componenti base

/**
 * @struct PositionComponent
 * @brief Componente posizione per le entità
 */
struct PositionComponent {
    Vec2 position;
    PositionComponent() : position(0.0f, 0.0f) {}
    PositionComponent(float x, float y) : position(x, y) {}
    PositionComponent(Vec2 pos) : position(pos) {}
};

/**
 * @struct VelocityComponent
 * @brief Componente velocità per le entità
 */
struct VelocityComponent {
    Vec2 velocity;
    VelocityComponent() : velocity(0.0f, 0.0f) {}
    VelocityComponent(float x, float y) : velocity(x, y) {}
    VelocityComponent(Vec2 vel) : velocity(vel) {}
};

/**
 * @struct SpriteComponent
 * @brief Componente sprite per renderizzare le entità
 */
struct SpriteComponent {
    char character;
    int color;

    SpriteComponent() : character('#'), color(7) {} // 7 = bianco default
    SpriteComponent(char c, int col = 7) : character(c), color(col) {}
};

/**
 * @struct ColliderComponent
 * @brief Componente collider per collision detection AABB
 */
struct ColliderComponent {
    Vec2 size;
    bool isTrigger;

    ColliderComponent() : size(1.0f, 1.0f), isTrigger(false) {}
    ColliderComponent(float width, float height, bool trigger = false)
        : size(width, height), isTrigger(trigger) {}
    ColliderComponent(Vec2 s, bool trigger = false)
        : size(s), isTrigger(trigger) {}
};

/**
 * @struct InputComponent
 * @brief Componente input per controllare le entità
 */
struct InputComponent {
    bool enabled;
    float speed;

    InputComponent() : enabled(true), speed(10.0f) {}
    InputComponent(float s) : enabled(true), speed(s) {}
};

/**
 * @class Entity
 * @brief Classe base per le entità del gioco
 */
class Entity {
public:
    EntityID id;
    bool active;

    // Componenti opzionali
    std::unique_ptr<PositionComponent> position;
    std::unique_ptr<VelocityComponent> velocity;
    std::unique_ptr<SpriteComponent> sprite;
    std::unique_ptr<ColliderComponent> collider;
    std::unique_ptr<InputComponent> input;

    Entity(EntityID entityID) : id(entityID), active(true) {}

    // Metodi helper per aggiungere componenti
    template<typename T>
    T* addComponent() {
        if constexpr (std::is_same_v<T, PositionComponent>) {
            position = std::make_unique<T>();
            return position.get();
        } else if constexpr (std::is_same_v<T, VelocityComponent>) {
            velocity = std::make_unique<T>();
            return velocity.get();
        } else if constexpr (std::is_same_v<T, SpriteComponent>) {
            sprite = std::make_unique<T>();
            return sprite.get();
        } else if constexpr (std::is_same_v<T, ColliderComponent>) {
            collider = std::make_unique<T>();
            return collider.get();
        } else if constexpr (std::is_same_v<T, InputComponent>) {
            input = std::make_unique<T>();
            return input.get();
        }
        return nullptr;
    }

    template<typename T>
    T* getComponent() {
        if constexpr (std::is_same_v<T, PositionComponent>) {
            return position.get();
        } else if constexpr (std::is_same_v<T, VelocityComponent>) {
            return velocity.get();
        } else if constexpr (std::is_same_v<T, SpriteComponent>) {
            return sprite.get();
        } else if constexpr (std::is_same_v<T, ColliderComponent>) {
            return collider.get();
        } else if constexpr (std::is_same_v<T, InputComponent>) {
            return input.get();
        }
        return nullptr;
    }

    template<typename T>
    bool hasComponent() const {
        if constexpr (std::is_same_v<T, PositionComponent>) {
            return position != nullptr;
        } else if constexpr (std::is_same_v<T, VelocityComponent>) {
            return velocity != nullptr;
        } else if constexpr (std::is_same_v<T, SpriteComponent>) {
            return sprite != nullptr;
        } else if constexpr (std::is_same_v<T, ColliderComponent>) {
            return collider != nullptr;
        } else if constexpr (std::is_same_v<T, InputComponent>) {
            return input != nullptr;
        }
        return false;
    }
};

/**
 * @class EntityManager
 * @brief Gestore delle entità del gioco
 */
class EntityManager {
private:
    std::vector<std::unique_ptr<Entity>> entities;
    EntityID nextID;

public:
    EntityManager() : nextID(0) {}

    // Crea una nuova entità
    Entity* createEntity() {
        auto entity = std::make_unique<Entity>(nextID++);
        entities.push_back(std::move(entity));
        return entities.back().get();
    }

    // Ottieni entità per ID
    Entity* getEntity(EntityID id) {
        for (auto& entity : entities) {
            if (entity->id == id && entity->active) {
                return entity.get();
            }
        }
        return nullptr;
    }

    // Rimuovi entità (soft delete)
    void destroyEntity(EntityID id) {
        for (auto& entity : entities) {
            if (entity->id == id) {
                entity->active = false;
                return;
            }
        }
    }

    // Ottieni tutte le entità attive
    std::vector<Entity*> getActiveEntities() {
        std::vector<Entity*> active;
        for (auto& entity : entities) {
            if (entity->active) {
                active.push_back(entity.get());
            }
        }
        return active;
    }

    // Pulisci entità inattive
    void cleanup() {
        entities.erase(
            std::remove_if(entities.begin(), entities.end(),
                [](const auto& entity) { return !entity->active; }),
            entities.end()
        );
    }

    // Numero di entità attive
    size_t getActiveCount() const {
        size_t count = 0;
        for (const auto& entity : entities) {
            if (entity->active) count++;
        }
        return count;
    }
};

} // namespace GameEngine

#endif // ENTITY_H
