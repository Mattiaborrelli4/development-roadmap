import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  RefreshControl
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useChatRooms } from '../hooks/useChatRooms';
import { useUsers } from '../hooks/useUsers';
import UserAvatar from '../components/UserAvatar';
import { colors, spacing, chatStyles, globalStyles } from '../styles/theme';
import chatService from '../services/chatService';

const ChatsListScreen = ({ navigation }) => {
  const { rooms, loading, reload } = useChatRooms();
  const { users } = useUsers();
  const [currentUserId, setCurrentUserId] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadCurrentUserId();
  }, []);

  const loadCurrentUserId = async () => {
    const userId = await chatService.getCurrentUserId();
    setCurrentUserId(userId);
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Adesso';
    if (diffMins < 60) return `${diffMins}m`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `${diffDays}g`;

    return date.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' });
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await reload();
    setRefreshing(false);
  };

  const getUserForRoom = (room) => {
    if (room.type === 'direct') {
      const otherUserId = room.participants.find(id => id !== currentUserId);
      return users.find(u => u.id === otherUserId);
    }
    return null;
  };

  const renderChatItem = ({ item }) => {
    const user = getUserForRoom(item);

    return (
      <TouchableOpacity
        style={chatStyles.chatItem}
        onPress={() => navigation.navigate('ChatRoom', { roomId: item.id })}
      >
        {item.type === 'direct' && user ? (
          <UserAvatar user={user} size={56} />
        ) : (
          <View style={[chatStyles.chatAvatar, styles.groupAvatar]}>
            <Text style={styles.groupAvatarText}>
              {item.name.substring(0, 2).toUpperCase()}
            </Text>
          </View>
        )}

        <View style={chatStyles.chatInfo}>
          <View style={globalStyles.row}>
            <Text style={chatStyles.chatName} numberOfLines={1}>
              {item.name}
            </Text>
            <Text style={chatStyles.chatTime}>
              {formatTime(item.lastMessage?.timestamp)}
            </Text>
          </View>
          <Text style={chatStyles.chatPreview} numberOfLines={2}>
            {item.lastMessage
              ? item.lastMessage.senderId === currentUserId
                ? `Tu: ${item.lastMessage.text}`
                : item.lastMessage.text
              : 'Nessun messaggio'}
          </Text>
        </View>

        {item.unreadCount > 0 && (
          <View style={chatStyles.unreadBadge}>
            <Text style={chatStyles.unreadText}>
              {item.unreadCount > 99 ? '99+' : item.unreadCount}
            </Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  const ListEmptyComponent = () => (
    <View style={chatStyles.emptyContainer}>
      <Ionicons name="chatbubbles-outline" size={64} color={colors.textLight} />
      <Text style={chatStyles.emptyText}>Nessuna chat disponibile</Text>
    </View>
  );

  return (
    <View style={globalStyles.container}>
      <FlatList
        data={rooms}
        renderItem={renderChatItem}
        keyExtractor={(item) => item.id}
        refreshing={refreshing}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={ListEmptyComponent}
      />

      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('Users')}
      >
        <Ionicons name="add" size={28} color={colors.white} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  groupAvatar: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.primary
  },
  groupAvatarText: {
    fontSize: 20,
    fontWeight: '600',
    color: colors.white
  },
  fab: {
    position: 'absolute',
    bottom: spacing.lg,
    right: spacing.lg,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4
  }
});

export default ChatsListScreen;
