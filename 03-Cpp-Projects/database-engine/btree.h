#ifndef BTREE_H
#define BTREE_H

#include <vector>
#include <string>
#include <memory>

// Ordine del B-tree (numero massimo di figli per nodo)
constexpr int BTREE_ORDER = 4;

// Struct per rappresentare una chiave con il suo valore associato
struct KeyValue {
    int key;
    std::string value;

    KeyValue() : key(0) {}
    KeyValue(int k, const std::string& v) : key(k), value(v) {}

    // Serializzazione per file I/O
    void serialize(std::ofstream& out) const;
    void deserialize(std::ifstream& in);
};

// Nodo del B-tree
struct BTreeNode {
    std::vector<KeyValue> keys;
    std::vector<std::shared_ptr<BTreeNode>> children;
    bool is_leaf;

    BTreeNode(bool leaf = true) : is_leaf(leaf) {
        keys.reserve(BTREE_ORDER - 1);
        children.reserve(BTREE_ORDER);
    }

    // Verifica se il nodo è pieno
    bool is_full() const {
        return keys.size() >= BTREE_ORDER - 1;
    }

    // Verifica se il nodo è sotto il minimo (underflow)
    bool is_underflow() const {
        return keys.size() < (BTREE_ORDER - 1) / 2;
    }

    // Serializzazione
    void serialize(std::ofstream& out) const;
    void deserialize(std::ifstream& in);
};

// Classe principale del B-tree
class BTree {
private:
    std::shared_ptr<BTreeNode> root;

    void split_child(std::shared_ptr<BTreeNode> parent, int index);
    void insert_non_full(std::shared_ptr<BTreeNode> node, const KeyValue& kv);
    void merge_nodes(std::shared_ptr<BTreeNode> parent, int index);
    std::shared_ptr<BTreeNode> search(std::shared_ptr<BTreeNode> node, int key);
    void remove_from_leaf(std::shared_ptr<BTreeNode> node, int index);
    void remove_from_internal(std::shared_ptr<BTreeNode> node, int index);
    int get_key_index(std::shared_ptr<BTreeNode> node, int key);
    void borrow_from_prev(std::shared_ptr<BTreeNode> node, int index);
    void borrow_from_next(std::shared_ptr<BTreeNode> node, int index);

public:
    BTree();
    explicit BTree(std::shared_ptr<BTreeNode> r);

    // Inserisce una chiave-valore
    void insert(int key, const std::string& value);

    // Cerca una chiave
    std::string search(int key);
    bool exists(int key);

    // Rimuove una chiave
    void remove(int key);

    // Aggiorna una chiave
    bool update(int key, const std::string& new_value);

    // Ottiene tutte le chiavi (per SELECT *)
    std::vector<KeyValue> get_all();

    // Ottieni la radice (per serializzazione)
    std::shared_ptr<BTreeNode> get_root() const { return root; }

    // Serializzazione dell'albero intero
    void serialize(std::ofstream& out) const;
    void deserialize(std::ifstream& in);

    // Stampa l'albero (per debug)
    void print() const;
    void print_node(std::shared_ptr<BTreeNode> node, int level = 0) const;
};

#endif // BTREE_H
