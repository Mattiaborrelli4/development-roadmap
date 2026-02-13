import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  TextInput
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useUsers } from '../hooks/useUsers';
import { useChatRooms } from '../hooks/useChatRooms';
import UserAvatar from '../components/UserAvatar';
import { colors, spacing, chatStyles, globalStyles } from '../styles/theme';
import chatService from '../services/chatService';

const UsersScreen = ({ navigation }) => {
  const { users } = useUsers();
  const { createDirectChat, createGroup } = useChatRooms();
  const [currentUserId, setCurrentUserId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [isCreatingGroup, setIsCreatingGroup] = useState(false);

  useEffect(() => {
    loadCurrentUserId();
  }, []);

  const loadCurrentUserId = async () => {
    const userId = await chatService.getCurrentUserId();
    setCurrentUserId(userId);
  };

  const filteredUsers = users.filter(user => {
    if (user.id === currentUserId) return false;
    if (searchQuery) {
      return user.username.toLowerCase().includes(searchQuery.toLowerCase());
    }
    return true;
  });

  const toggleUserSelection = (userId) => {
    setSelectedUsers(prev => {
      if (prev.includes(userId)) {
        return prev.filter(id => id !== userId);
      } else {
        return [...prev, userId];
      }
    });
  };

  const handleUserPress = async (user) => {
    if (isCreatingGroup) {
      toggleUserSelection(user.id);
    } else {
      // Create direct chat
      const room = await createDirectChat(user.id, currentUserId);
      if (room) {
        navigation.navigate('ChatRoom', { roomId: room.id });
      }
    }
  };

  const handleCreateGroup = async () => {
    if (selectedUsers.length < 1) {
      return;
    }

    const groupName = `Gruppo ${selectedUsers.length + 1}`;
    const participants = [currentUserId, ...selectedUsers];

    const room = await createGroup(groupName, participants);
    if (room) {
      setSelectedUsers([]);
      setIsCreatingGroup(false);
      navigation.navigate('ChatRoom', { roomId: room.id });
    }
  };

  const isUserSelected = (userId) => selectedUsers.includes(userId);

  const renderUserItem = ({ item }) => {
    const isSelected = isUserSelected(item.id);

    return (
      <TouchableOpacity
        style={[chatStyles.chatItem, isSelected && styles.selectedItem]}
        onPress={() => handleUserPress(item)}
      >
        <UserAvatar user={item} size={56} showStatus={!isCreatingGroup} />

        <View style={chatStyles.chatInfo}>
          <Text style={chatStyles.chatName}>{item.username}</Text>
          <Text style={[chatStyles.chatPreview, styles.statusText]}>
            {item.status === 'online'
              ? 'Online'
              : `Ultimo accesso: ${new Date(item.lastSeen).toLocaleString('it-IT')}`}
          </Text>
        </View>

        {isCreatingGroup && (
          <View style={[styles.checkbox, isSelected && styles.checkboxSelected]}>
            {isSelected && (
              <Ionicons name="checkmark" size={20} color={colors.white} />
            )}
          </View>
        )}
      </TouchableOpacity>
    );
  };

  return (
    <View style={globalStyles.container}>
      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Ionicons name="search" size={20} color={colors.textLight} style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Cerca utenti..."
            placeholderTextColor={colors.textLight}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {selectedUsers.length > 0 && (
          <TouchableOpacity style={styles.createButton} onPress={handleCreateGroup}>
            <Text style={styles.createButtonText}>Crea ({selectedUsers.length})</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Mode Toggle */}
      {filteredUsers.length > 0 && (
        <View style={styles.modeToggle}>
          <TouchableOpacity
            style={[styles.modeButton, !isCreatingGroup && styles.modeButtonActive]}
            onPress={() => {
              setIsCreatingGroup(false);
              setSelectedUsers([]);
            }}
          >
            <Text style={[styles.modeButtonText, !isCreatingGroup && styles.modeButtonTextActive]}>
              Chat Dirette
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.modeButton, isCreatingGroup && styles.modeButtonActive]}
            onPress={() => setIsCreatingGroup(true)}
          >
            <Text style={[styles.modeButtonText, isCreatingGroup && styles.modeButtonTextActive]}>
              Crea Gruppo
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Users List */}
      <FlatList
        data={filteredUsers}
        renderItem={renderUserItem}
        keyExtractor={(item) => item.id}
        ListEmptyComponent={
          <View style={chatStyles.emptyContainer}>
            <Ionicons name="people-outline" size={64} color={colors.textLight} />
            <Text style={chatStyles.emptyText}>
              {searchQuery ? 'Nessun utente trovato' : 'Nessun utente disponibile'}
            </Text>
          </View>
        }
      />

      {isCreatingGroup && selectedUsers.length > 0 && (
        <View style={styles.selectionBar}>
          <Text style={styles.selectionText}>
            {selectedUsers.length} {selectedUsers.length === 1 ? 'utente' : 'utenti'} selezionati
          </Text>
          <TouchableOpacity
            style={[styles.createButton, styles.createButtonFull]}
            onPress={handleCreateGroup}
          >
            <Text style={styles.createButtonText}>Crea Gruppo</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.divider
  },
  searchBar: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.backgroundLight,
    borderRadius: 24,
    paddingHorizontal: spacing.md,
    height: 40
  },
  searchIcon: {
    marginRight: spacing.sm
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: colors.text
  },
  createButton: {
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 20,
    marginLeft: spacing.sm
  },
  createButtonText: {
    color: colors.white,
    fontWeight: '600',
    fontSize: 14
  },
  createButtonFull: {
    flex: 1,
    alignItems: 'center'
  },
  modeToggle: {
    flexDirection: 'row',
    backgroundColor: colors.backgroundLight,
    margin: spacing.md,
    borderRadius: 8,
    overflow: 'hidden'
  },
  modeButton: {
    flex: 1,
    paddingVertical: spacing.sm,
    alignItems: 'center'
  },
  modeButtonActive: {
    backgroundColor: colors.white
  },
  modeButtonText: {
    fontSize: 14,
    color: colors.textSecondary
  },
  modeButtonTextActive: {
    color: colors.primary,
    fontWeight: '600'
  },
  selectedItem: {
    backgroundColor: `${colors.primary}10`
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.divider,
    justifyContent: 'center',
    alignItems: 'center'
  },
  checkboxSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary
  },
  statusText: {
    fontStyle: 'italic'
  },
  selectionBar: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.divider
  },
  selectionText: {
    flex: 1,
    fontSize: 14,
    color: colors.textSecondary
  }
});

export default UsersScreen;
