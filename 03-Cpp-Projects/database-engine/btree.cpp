#include "btree.h"
#include <iostream>
#include <algorithm>

// Implementazione KeyValue serialization
void KeyValue::serialize(std::ofstream& out) const {
    out.write(reinterpret_cast<const char*>(&key), sizeof(key));
    size_t size = value.size();
    out.write(reinterpret_cast<const char*>(&size), sizeof(size));
    out.write(value.c_str(), size);
}

void KeyValue::deserialize(std::ifstream& in) {
    in.read(reinterpret_cast<char*>(&key), sizeof(key));
    size_t size = 0;
    in.read(reinterpret_cast<char*>(&size), sizeof(size));
    value.resize(size);
    in.read(&value[0], size);
}

// Implementazione BTreeNode serialization
void BTreeNode::serialize(std::ofstream& out) const {
    // Scrivi is_leaf
    out.write(reinterpret_cast<const char*>(&is_leaf), sizeof(is_leaf));

    // Scrivi numero di chiavi
    size_t num_keys = keys.size();
    out.write(reinterpret_cast<const char*>(&num_keys), sizeof(num_keys));

    // Scrivi le chiavi
    for (const auto& kv : keys) {
        kv.serialize(out);
    }

    // Scrivi i figli (solo per nodi interni)
    if (!is_leaf) {
        size_t num_children = children.size();
        out.write(reinterpret_cast<const char*>(&num_children), sizeof(num_children));
        // I figli saranno serializzati ricorsivamente dal BTree
    }
}

void BTreeNode::deserialize(std::ifstream& in) {
    // Leggi is_leaf
    in.read(reinterpret_cast<char*>(&is_leaf), sizeof(is_leaf));

    // Leggi numero di chiavi
    size_t num_keys = 0;
    in.read(reinterpret_cast<char*>(&num_keys), sizeof(num_keys));

    // Leggi le chiavi
    keys.resize(num_keys);
    for (size_t i = 0; i < num_keys; ++i) {
        keys[i].deserialize(in);
    }

    // I figli verranno letti dal BTree
}

// Costruttore BTree
BTree::BTree() {
    root = std::make_shared<BTreeNode>(true);
}

BTree::BTree(std::shared_ptr<BTreeNode> r) : root(r) {}

// Split di un nodo figlio
void BTree::split_child(std::shared_ptr<BTreeNode> parent, int index) {
    auto child = parent->children[index];
    auto new_node = std::make_shared<BTreeNode>(child->is_leaf);

    // Trova il punto medio
    int mid = (BTREE_ORDER - 1) / 2;

    // Sposta le chiavi superiori al nuovo nodo
    for (int i = mid + 1; i < static_cast<int>(child->keys.size()); ++i) {
        new_node->keys.push_back(child->keys[i]);
    }
    child->keys.resize(mid);

    // Sposta i figli se non è foglia
    if (!child->is_leaf) {
        for (int i = mid + 1; i < static_cast<int>(child->children.size()); ++i) {
            new_node->children.push_back(child->children[i]);
        }
        child->children.resize(mid + 1);
    }

    // Inserisci la chiave mediana nel padre
    KeyValue mid_key = child->keys[mid];
    parent->keys.insert(parent->keys.begin() + index, child->keys[mid]);
    parent->children.insert(parent->children.begin() + index + 1, new_node);
}

// Inserimento in nodo non pieno
void BTree::insert_non_full(std::shared_ptr<BTreeNode> node, const KeyValue& kv) {
    int i = static_cast<int>(node->keys.size()) - 1;

    if (node->is_leaf) {
        // Trova la posizione e inserisci
        node->keys.push_back(kv);
        int j = static_cast<int>(node->keys.size()) - 2;
        while (j >= 0 && node->keys[j].key > kv.key) {
            node->keys[j + 1] = node->keys[j];
            --j;
        }
        node->keys[j + 1] = kv;
    } else {
        // Trova il figlio corretto
        while (i >= 0 && kv.key < node->keys[i].key) {
            --i;
        }
        ++i;

        // Split se necessario
        if (node->children[i]->is_full()) {
            split_child(node, i);
            if (kv.key > node->keys[i].key) {
                ++i;
            }
        }
        insert_non_full(node->children[i], kv);
    }
}

// Inserimento pubblico
void BTree::insert(int key, const std::string& value) {
    KeyValue kv(key, value);

    if (root->is_full()) {
        auto new_root = std::make_shared<BTreeNode>(false);
        new_root->children.push_back(root);
        split_child(new_root, 0);
        insert_non_full(new_root, kv);
        root = new_root;
    } else {
        insert_non_full(root, kv);
    }
}

// Search helper
std::shared_ptr<BTreeNode> BTree::search(std::shared_ptr<BTreeNode> node, int key) {
    int i = 0;
    while (i < static_cast<int>(node->keys.size()) && key > node->keys[i].key) {
        ++i;
    }

    if (i < static_cast<int>(node->keys.size()) && key == node->keys[i].key) {
        return node;
    }

    if (node->is_leaf) {
        return nullptr;
    }

    return search(node->children[i], key);
}

// Search pubblico
std::string BTree::search(int key) {
    auto node = search(root, key);
    if (node) {
        for (const auto& kv : node->keys) {
            if (kv.key == key) {
                return kv.value;
            }
        }
    }
    return "";
}

bool BTree::exists(int key) {
    return search(root, key) != nullptr;
}

// Ottieni indice di una chiave
int BTree::get_key_index(std::shared_ptr<BTreeNode> node, int key) {
    for (size_t i = 0; i < node->keys.size(); ++i) {
        if (node->keys[i].key == key) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

// Merge di nodi
void BTree::merge_nodes(std::shared_ptr<BTreeNode> parent, int index) {
    auto left = parent->children[index];
    auto right = parent->children[index + 1];

    // Sposta la chiave del padre nel figlio sinistro
    left->keys.push_back(parent->keys[index]);

    // Sposta le chiavi del figlio destro
    for (const auto& kv : right->keys) {
        left->keys.push_back(kv);
    }

    // Sposta i figli
    if (!left->is_leaf) {
        for (const auto& child : right->children) {
            left->children.push_back(child);
        }
    }

    // Rimuovi la chiave e il figlio dal padre
    parent->keys.erase(parent->keys.begin() + index);
    parent->children.erase(parent->children.begin() + index + 1);
}

// Borrow from previous sibling
void BTree::borrow_from_prev(std::shared_ptr<BTreeNode> node, int index) {
    auto child = node->children[index];
    auto sibling = node->children[index - 1];

    // Sposta la chiave dal padre al figlio
    child->keys.insert(child->keys.begin(), node->keys[index - 1]);

    // Sposta l'ultima chiave del fratello al padre
    node->keys[index - 1] = sibling->keys.back();
    sibling->keys.pop_back();

    // Sposta il figlio se non è foglia
    if (!child->is_leaf) {
        child->children.insert(child->children.begin(), sibling->children.back());
        sibling->children.pop_back();
    }
}

// Borrow from next sibling
void BTree::borrow_from_next(std::shared_ptr<BTreeNode> node, int index) {
    auto child = node->children[index];
    auto sibling = node->children[index + 1];

    // Sposta la chiave dal padre al figlio
    child->keys.push_back(node->keys[index]);

    // Sposta la prima chiave del fratello al padre
    node->keys[index] = sibling->keys.front();
    sibling->keys.erase(sibling->keys.begin());

    // Sposta il figlio se non è foglia
    if (!child->is_leaf) {
        child->children.push_back(sibling->children.front());
        sibling->children.erase(sibling->children.begin());
    }
}

// Remove from leaf
void BTree::remove_from_leaf(std::shared_ptr<BTreeNode> node, int index) {
    node->keys.erase(node->keys.begin() + index);
}

// Remove from internal node
void BTree::remove_from_internal(std::shared_ptr<BTreeNode> node, int index) {
    int key = node->keys[index].key;

    if (node->children[index]->keys.size() >= (BTREE_ORDER - 1) / 2) {
        // Predecessore
        auto pred = node->children[index];
        while (!pred->is_leaf) {
            pred = pred->children.back();
        }
        node->keys[index] = pred->keys.back();
        node->children[index]->keys.pop_back();
    } else if (node->children[index + 1]->keys.size() >= (BTREE_ORDER - 1) / 2) {
        // Successore
        auto succ = node->children[index + 1];
        while (!succ->is_leaf) {
            succ = succ->children.front();
        }
        node->keys[index] = succ->keys.front();
        succ->keys.erase(succ->keys.begin());
    } else {
        // Merge
        merge_nodes(node, index);
        remove(node->children[index]->keys.back().key);
    }
}

// Remove pubblico
void BTree::remove(int key) {
    // Implementazione semplificata - in produzione servirebbe più complessa
    auto node = search(root, key);
    if (node) {
        int idx = get_key_index(node, key);
        if (idx != -1) {
            if (node->is_leaf) {
                remove_from_leaf(node, idx);
            } else {
                remove_from_internal(node, idx);
            }
        }
    }
}

// Update
bool BTree::update(int key, const std::string& new_value) {
    auto node = search(root, key);
    if (node) {
        for (auto& kv : node->keys) {
            if (kv.key == key) {
                kv.value = new_value;
                return true;
            }
        }
    }
    return false;
}

// Get all keys
std::vector<KeyValue> BTree::get_all() {
    std::vector<KeyValue> result;

    std::function<void(std::shared_ptr<BTreeNode>)> traverse =
        [&](std::shared_ptr<BTreeNode> node) {
            if (!node) return;

            size_t i = 0;
            for (; i < node->keys.size(); ++i) {
                if (!node->is_leaf) {
                    traverse(node->children[i]);
                }
                result.push_back(node->keys[i]);
            }
            if (!node->is_leaf && i < node->children.size()) {
                traverse(node->children[i]);
            }
        };

    traverse(root);
    return result;
}

// Serialize tree
void BTree::serialize(std::ofstream& out) const {
    std::function<void(std::shared_ptr<BTreeNode>)> serialize_node =
        [&](std::shared_ptr<BTreeNode> node) {
            if (!node) return;

            node->serialize(out);

            if (!node->is_leaf) {
                for (const auto& child : node->children) {
                    serialize_node(child);
                }
            }
        };

    serialize_node(root);
}

// Deserialize tree
void BTree::deserialize(std::ifstream& in) {
    std::function<std::shared_ptr<BTreeNode>()> deserialize_node =
        [&]() -> std::shared_ptr<BTreeNode> {
            auto node = std::make_shared<BTreeNode>();
            node->deserialize(in);

            if (!node->is_leaf) {
                size_t num_children = 0;
                in.read(reinterpret_cast<char*>(&num_children), sizeof(num_children));
                for (size_t i = 0; i < num_children; ++i) {
                    node->children.push_back(deserialize_node());
                }
            }

            return node;
        };

    root = deserialize_node();
}

// Print tree
void BTree::print() const {
    std::cout << "B-Tree Structure:\n";
    print_node(root);
}

void BTree::print_node(std::shared_ptr<BTreeNode> node, int level) const {
    if (!node) return;

    std::string indent(level * 2, ' ');
    std::cout << indent << "Level " << level << ": [";
    for (size_t i = 0; i < node->keys.size(); ++i) {
        std::cout << node->keys[i].key;
        if (i < node->keys.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << (node->is_leaf ? " (leaf)" : "") << "\n";

    if (!node->is_leaf) {
        for (const auto& child : node->children) {
            print_node(child, level + 1);
        }
    }
}
