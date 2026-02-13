import React, {useState} from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
  TextInput,
  ScrollView,
} from 'react-native';
import {useItems} from '../hooks/useItems';
import {useLists} from '../hooks/useLists';
import ListItem from '../components/ListItem';
import AddItemModal from '../components/AddItemModal';
import ShareButton from '../components/ShareButton';
import BarcodeScanner from '../components/BarcodeScanner';
import CategoryBadge from '../components/CategoryBadge';
import {CATEGORIES} from '../utils/constants';
import storageService from '../services/storageService';

const ListDetailScreen = ({route, navigation}) => {
  const {listId} = route.params;
  const {lists} = useLists();
  const {
    items,
    filter,
    setFilter,
    addItem,
    updateItem,
    toggleBought,
    deleteItem,
    moveItems,
    copyItems,
    clearBoughtItems,
    getItemsByCategory,
    getStatistics,
  } = useItems(listId);

  const list = lists.find(l => l.id === listId);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showScanner, setShowScanner] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [selectedItems, setSelectedItems] = useState([]);
  const [showMultiSelectActions, setShowMultiSelectActions] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const stats = getStatistics();
  const groupedItems = getItemsByCategory();

  const handleAddItem = async (itemData) => {
    try {
      await addItem(itemData);
    } catch (error) {
      Alert.alert('Errore', 'Impossibile aggiungere l\'elemento');
    }
  };

  const handleUpdateItem = async (itemId, updates) => {
    try {
      await updateItem(itemId, updates);
      setEditItem(null);
    } catch (error) {
      Alert.alert('Errore', 'Impossibile aggiornare l\'elemento');
    }
  };

  const handleDeleteItem = async (itemId) => {
    Alert.alert(
      'Elimina Elemento',
      'Sei sicuro di voler eliminare questo elemento?',
      [
        {text: 'Annulla', style: 'cancel'},
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteItem(itemId);
            } catch (error) {
              Alert.alert('Errore', 'Impossibile eliminare l\'elemento');
            }
          },
        },
      ]
    );
  };

  const handleLongPress = (itemId) => {
    if (selectedItems.includes(itemId)) {
      setSelectedItems(selectedItems.filter(id => id !== itemId));
    } else {
      setSelectedItems([...selectedItems, itemId]);
    }
    setShowMultiSelectActions(selectedItems.length > 0 || !selectedItems.includes(itemId));
  };

  const handleBarcodeScan = (data) => {
    setShowAddModal(true);
    setEditItem(data);
  };

  const handleClearBought = () => {
    Alert.alert(
      'Pulisci Lista',
      `Rimuovere ${stats.bought} elementi comprati?`,
      [
        {text: 'Annulla', style: 'cancel'},
        {
          text: 'Rimuovi',
          style: 'destructive',
          onPress: async () => {
            try {
              await clearBoughtItems();
            } catch (error) {
              Alert.alert('Errore', 'Impossibile pulire la lista');
            }
          },
        },
      ]
    );
  };

  const renderCategorySection = (categoryName, categoryItems) => {
    if (categoryItems.length === 0) return null;

    const filteredItems = searchQuery
      ? categoryItems.filter(item =>
          item.name.toLowerCase().includes(searchQuery.toLowerCase())
        )
      : categoryItems;

    if (filteredItems.length === 0) return null;

    return (
      <View key={categoryName} style={styles.categorySection}>
        <View style={styles.categoryHeader}>
          <CategoryBadge category={categoryName} />
          <Text style={styles.categoryCount}>
            {filteredItems.length}
          </Text>
        </View>

        {filteredItems.map(item => (
          <ListItem
            key={item.id}
            item={item}
            onToggleBought={toggleBought}
            onDelete={() => handleDeleteItem(item.id)}
            onPress={() => {
              setEditItem(item);
              setShowAddModal(true);
            }}
            onLongPress={() => handleLongPress(item.id)}
            style={selectedItems.includes(item.id) && styles.selectedItem}
          />
        ))}
      </View>
    );
  };

  const renderFilters = () => (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.filtersContainer}
      contentContainerStyle={styles.filtersContent}>
      <TouchableOpacity
        style={[styles.filterChip, filter === 'all' && styles.filterChipActive]}
        onPress={() => setFilter('all')}>
        <Text
          style={[
            styles.filterChipText,
            filter === 'all' && styles.filterChipTextActive,
          ]}>
          Tutti ({stats.total})
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.filterChip, filter === 'unbought' && styles.filterChipActive]}
        onPress={() => setFilter('unbought')}>
        <Text
          style={[
            styles.filterChipText,
            filter === 'unbought' && styles.filterChipTextActive,
          ]}>
          Da Comprare ({stats.unbought})
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.filterChip, filter === 'bought' && styles.filterChipActive]}
        onPress={() => setFilter('bought')}>
        <Text
          style={[
            styles.filterChipText,
            filter === 'bought' && styles.filterChipTextActive,
          ]}>
          Comprati ({stats.bought})
        </Text>
      </TouchableOpacity>

      {CATEGORIES.map(cat => (
        <TouchableOpacity
          key={cat.name}
          style={[styles.filterChip, filter === cat.name && styles.filterChipActive]}
          onPress={() => setFilter(cat.name)}>
          <Text
            style={[
              styles.filterChipText,
              filter === cat.name && styles.filterChipTextActive,
            ]}>
            {cat.icon} {cat.name}
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  if (!list) {
    return (
      <View style={styles.container}>
        <Text>Lista non trovata</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, {borderTopColor: list.color}]}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>←</Text>
        </TouchableOpacity>

        <View style={styles.headerInfo}>
          <Text style={styles.headerIcon}>{list.icon}</Text>
          <View>
            <Text style={styles.headerTitle}>{list.name}</Text>
            <Text style={styles.headerSubtitle}>
              {stats.completionRate}% completato
            </Text>
          </View>
        </View>

        <ShareButton list={list} onShare={async () => {}} onUnshare={async () => {}} />
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="🔍 Cerca elementi..."
          placeholderTextColor="#7F8C8D"
        />
      </View>

      {/* Filters */}
      {renderFilters()}

      {/* Multi-select Actions */}
      {showMultiSelectActions && selectedItems.length > 0 && (
        <View style={styles.multiSelectActions}>
          <Text style={styles.selectedCount}>{selectedItems.length} selezionati</Text>
          <View style={styles.actionButtons}>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => {
                setSelectedItems([]);
                setShowMultiSelectActions(false);
              }}>
              <Text style={styles.actionButtonText}>Annulla</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={async () => {
                // Implementa spostamento in altra lista
                Alert.alert('Info', 'Sposta in altra lista (da implementare)');
              }}>
              <Text style={styles.actionButtonText}>Sposta</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.actionButton, styles.deleteButton]}
              onPress={async () => {
                for (const itemId of selectedItems) {
                  await deleteItem(itemId);
                }
                setSelectedItems([]);
                setShowMultiSelectActions(false);
              }}>
              <Text style={styles.actionButtonText}>Elimina</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Items List */}
      <ScrollView
        style={styles.content}
        showsVerticalScrollIndicator={false}>
        {stats.total === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateIcon}>📝</Text>
            <Text style={styles.emptyStateTitle}>Lista Vuota</Text>
            <Text style={styles.emptyStateText}>
              Aggiungi elementi per iniziare
            </Text>
          </View>
        ) : (
          Object.entries(groupedItems).map(([category, items]) =>
            renderCategorySection(category, items)
          )
        )}
      </ScrollView>

      {/* Bottom Actions */}
      {stats.total > 0 && (
        <View style={styles.bottomActions}>
          <TouchableOpacity
            style={styles.bottomAction}
            onPress={handleClearBought}>
            <Text style={styles.bottomActionText}>🗑️ Pulisci comprati</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.bottomAction}
            onPress={() => setShowScanner(true)}>
            <Text style={styles.bottomActionText}>📊 Scanner</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* FAB */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => {
          setEditItem(null);
          setShowAddModal(true);
        }}>
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>

      {/* Modals */}
      <AddItemModal
        visible={showAddModal}
        onClose={() => {
          setShowAddModal(false);
          setEditItem(null);
        }}
        onAdd={handleAddItem}
        editItem={editItem}
        onUpdate={handleUpdateItem}
      />

      <BarcodeScanner
        visible={showScanner}
        onClose={() => setShowScanner(false)}
        onScan={handleBarcodeScan}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    paddingTop: 40,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
    borderTopWidth: 4,
  },
  backButton: {
    fontSize: 28,
    color: '#2C3E50',
    marginRight: 12,
  },
  headerInfo: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerIcon: {
    fontSize: 32,
    marginRight: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#7F8C8D',
  },
  searchContainer: {
    padding: 16,
    paddingBottom: 8,
  },
  searchInput: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  filtersContainer: {
    maxHeight: 50,
  },
  filtersContent: {
    paddingHorizontal: 16,
    paddingBottom: 8,
  },
  filterChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#F5F5F5',
    marginRight: 8,
  },
  filterChipActive: {
    backgroundColor: '#4ECDC4',
  },
  filterChipText: {
    fontSize: 14,
    color: '#2C3E50',
  },
  filterChipTextActive: {
    color: '#FFFFFF',
    fontWeight: '600',
  },
  multiSelectActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#F5F5F5',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  selectedCount: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
  },
  actionButtons: {
    flexDirection: 'row',
  },
  actionButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: '#4ECDC4',
    marginLeft: 8,
  },
  deleteButton: {
    backgroundColor: '#F44336',
  },
  actionButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  content: {
    flex: 1,
  },
  categorySection: {
    marginBottom: 16,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#F5F5F5',
  },
  categoryCount: {
    fontSize: 12,
    color: '#7F8C8D',
    marginLeft: 8,
  },
  selectedItem: {
    backgroundColor: '#E3F2FD',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 80,
  },
  emptyStateIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyStateTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 8,
  },
  emptyStateText: {
    fontSize: 14,
    color: '#7F8C8D',
    textAlign: 'center',
  },
  bottomActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 16,
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
  },
  bottomAction: {
    padding: 12,
  },
  bottomActionText: {
    fontSize: 14,
    color: '#4ECDC4',
    fontWeight: '600',
  },
  fab: {
    position: 'absolute',
    bottom: 80,
    right: 24,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#4ECDC4',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 4},
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  fabIcon: {
    fontSize: 32,
    color: '#FFFFFF',
    fontWeight: '300',
  },
});

export default ListDetailScreen;
