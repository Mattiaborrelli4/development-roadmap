import React, {useState} from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
  RefreshControl,
  TextInput,
} from 'react-native';
import {useLists} from '../hooks/useLists';
import {createTheme} from '../styles/theme';
import {LIST_ICONS, LIST_COLORS} from '../utils/constants';

const ListsScreen = ({navigation}) => {
  const {lists, loading, createList, deleteList, duplicateList, refresh} = useLists();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [showNewListModal, setShowNewListModal] = useState(false);
  const [newListName, setNewListName] = useState('');
  const [selectedIcon, setSelectedIcon] = useState(LIST_ICONS[0]);
  const [selectedColor, setSelectedColor] = useState(LIST_COLORS[0]);
  const theme = createTheme(false);

  const onRefresh = async () => {
    setIsRefreshing(true);
    await refresh();
    setIsRefreshing(false);
  };

  const handleCreateList = async () => {
    if (!newListName.trim()) {
      Alert.alert('Errore', 'Inserisci un nome per la lista');
      return;
    }

    try {
      const newList = await createList({
        name: newListName.trim(),
        icon: selectedIcon,
        color: selectedColor,
      });
      setShowNewListModal(false);
      setNewListName('');
      navigation.navigate('ListDetail', {listId: newList.id});
    } catch (error) {
      Alert.alert('Errore', 'Impossibile creare la lista');
    }
  };

  const handleDeleteList = (list) => {
    Alert.alert(
      'Elimina Lista',
      `Sei sicuro di voler eliminare "${list.name}"?`,
      [
        {text: 'Annulla', style: 'cancel'},
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteList(list.id);
            } catch (error) {
              Alert.alert('Errore', 'Impossibile eliminare la lista');
            }
          },
        },
      ]
    );
  };

  const handleDuplicateList = async (list) => {
    try {
      await duplicateList(list.id);
      Alert.alert('Successo', 'Lista duplicata con successo');
    } catch (error) {
      Alert.alert('Errore', 'Impossibile duplicare la lista');
    }
  };

  const renderListCard = ({item: list}) => {
    const items = list.items || [];
    const boughtCount = items.filter(i => i.bought).length;
    const progress = items.length > 0 ? boughtCount / items.length : 0;

    return (
      <TouchableOpacity
        style={[styles.card, {borderLeftColor: list.color}]}
        onPress={() => navigation.navigate('ListDetail', {listId: list.id})}
        onLongPress={() => {
          Alert.alert(
            list.name,
            'Cosa vuoi fare?',
            [
              {text: 'Annulla', style: 'cancel'},
              {
                text: 'Duplica',
                onPress: () => handleDuplicateList(list),
              },
              {
                text: 'Elimina',
                style: 'destructive',
                onPress: () => handleDeleteList(list),
              },
            ]
          );
        }}>
        <View style={styles.cardHeader}>
          <View style={[styles.iconContainer, {backgroundColor: list.color + '20'}]}>
            <Text style={styles.icon}>{list.icon}</Text>
          </View>
          <View style={styles.cardInfo}>
            <Text style={styles.cardTitle}>{list.name}</Text>
            <View style={styles.cardMeta}>
              {list.shared && <Text style={styles.sharedBadge}>👥 Condivisa</Text>}
              <Text style={styles.cardMetaText}>
                {items.length} elementi
              </Text>
            </View>
          </View>
        </View>

        {items.length > 0 && (
          <View style={styles.progressContainer}>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFill,
                  {width: `${progress * 100}%`, backgroundColor: list.color},
                ]}
              />
            </View>
            <Text style={styles.progressText}>
              {boughtCount}/{items.length}
            </Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Text style={styles.emptyStateIcon}>🛒</Text>
      <Text style={styles.emptyStateTitle}>Nessuna Lista</Text>
      <Text style={styles.emptyStateText}>
        Crea la tua prima lista della spesa
      </Text>
    </View>
  );

  const renderNewListModal = () => (
    <View style={styles.modalOverlay}>
      <View style={styles.modalContainer}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Nuova Lista</Text>
          <TouchableOpacity onPress={() => setShowNewListModal(false)}>
            <Text style={styles.modalClose}>✕</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.modalContent}>
          <Text style={styles.label}>Nome *</Text>
          <TextInput
            style={styles.input}
            value={newListName}
            onChangeText={setNewListName}
            placeholder="Es: Spesa settimanale"
            autoFocus
          />

          <Text style={styles.label}>Icona</Text>
          <View style={styles.iconsContainer}>
            {LIST_ICONS.map(icon => (
              <TouchableOpacity
                key={icon}
                style={[
                  styles.iconOption,
                  selectedIcon === icon && styles.iconOptionSelected,
                ]}
                onPress={() => setSelectedIcon(icon)}>
                <Text style={styles.iconOptionText}>{icon}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>Colore</Text>
          <View style={styles.colorsContainer}>
            {LIST_COLORS.map(color => (
              <TouchableOpacity
                key={color}
                style={[
                  styles.colorOption,
                  selectedColor === color && styles.colorOptionSelected,
                  {backgroundColor: color},
                ]}
                onPress={() => setSelectedColor(color)}>
                {selectedColor === color && (
                  <Text style={styles.colorCheck}>✓</Text>
                )}
              </TouchableOpacity>
            ))}
          </View>

          <TouchableOpacity style={styles.createButton} onPress={handleCreateList}>
            <Text style={styles.createButtonText}>Crea Lista</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  if (showNewListModal) {
    return renderNewListModal();
  }

  return (
    <View style={[theme.container, styles.container]}>
      <View style={styles.header}>
        <Text style={styles.title}>Le Mie Liste</Text>
        <TouchableOpacity onPress={() => setShowNewListModal(true)}>
          <Text style={styles.addButton}>+ Nuova</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={lists}
        renderItem={renderListCard}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={!loading ? renderEmptyState : null}
        showsVerticalScrollIndicator={false}
      />

      <TouchableOpacity
        style={styles.fab}
        onPress={() => setShowNewListModal(true)}>
        <Text style={styles.fabIcon}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 40,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  addButton: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4ECDC4',
  },
  listContent: {
    padding: 16,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 56,
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  icon: {
    fontSize: 28,
  },
  cardInfo: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 4,
  },
  cardMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sharedBadge: {
    fontSize: 12,
    color: '#4ECDC4',
    marginRight: 8,
  },
  cardMetaText: {
    fontSize: 14,
    color: '#7F8C8D',
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
  },
  progressBar: {
    flex: 1,
    height: 6,
    backgroundColor: '#E0E0E0',
    borderRadius: 3,
    overflow: 'hidden',
    marginRight: 8,
  },
  progressFill: {
    height: '100%',
  },
  progressText: {
    fontSize: 12,
    color: '#7F8C8D',
    fontWeight: '600',
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
  fab: {
    position: 'absolute',
    bottom: 24,
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
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    width: '90%',
    maxWidth: 400,
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  modalClose: {
    fontSize: 24,
    color: '#7F8C8D',
  },
  modalContent: {
    padding: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 8,
    marginTop: 12,
  },
  input: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  iconsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  iconOption: {
    width: 48,
    height: 48,
    borderRadius: 8,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
    marginBottom: 8,
  },
  iconOptionSelected: {
    backgroundColor: '#4ECDC4',
  },
  iconOptionText: {
    fontSize: 24,
  },
  colorsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  colorOption: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 8,
    marginBottom: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  colorOptionSelected: {
    borderWidth: 3,
    borderColor: '#2C3E50',
  },
  colorCheck: {
    color: '#2C3E50',
    fontSize: 18,
    fontWeight: 'bold',
  },
  createButton: {
    backgroundColor: '#4ECDC4',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  createButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default ListsScreen;
