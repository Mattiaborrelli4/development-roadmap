import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useMessages } from '../hooks/useMessages';
import { useUsers } from '../hooks/useUsers';
import { useTyping } from '../hooks/useTyping';
import MessageBubble from '../components/MessageBubble';
import ChatInput from '../components/ChatInput';
import UserAvatar from '../components/UserAvatar';
import TypingIndicator from '../components/TypingIndicator';
import { colors, spacing, chatStyles, globalStyles } from '../styles/theme';
import chatService from '../services/chatService';

const ChatRoomScreen = ({ route, navigation }) => {
  const { roomId } = route.params;
  const { messages, sendMessage, markAsRead, clearChat } = useMessages(roomId);
  const { users } = useUsers();
  const typingUsers = useTyping(roomId);
  const [room, setRoom] = useState(null);
  const [currentUserId, setCurrentUserId] = useState(null);
  const flatListRef = useRef(null);

  useEffect(() => {
    loadRoomData();
    markMessagesAsRead();
  }, [roomId]);

  useEffect(() => {
    // Scroll to bottom quando arrivano nuovi messaggi
    if (messages.length > 0) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages.length]);

  const loadRoomData = async () => {
    const roomIdValue = typeof roomId === 'string' ? roomId : roomId?.id;
    const roomData = await chatService.getChatRoomById(roomIdValue);
    const userId = await chatService.getCurrentUserId();

    setRoom(roomData);
    setCurrentUserId(userId);

    if (roomData) {
      if (roomData.type === 'direct') {
        const otherUserId = roomData.participants.find(id => id !== userId);
        const otherUser = users.find(u => u.id === otherUserId);
        navigation.setOptions({
          title: otherUser?.username || roomData.name
        });
      } else {
        navigation.setOptions({
          title: roomData.name
        });
      }
    }
  };

  const markMessagesAsRead = async () => {
    const userId = await chatService.getCurrentUserId();
    await markAsRead(userId);
  };

  const handleSend = async (text) => {
    await sendMessage(text);
  };

  const handleClearChat = () => {
    Alert.alert(
      'Cancella Chat',
      'Sei sicuro di voler cancellare tutti i messaggi?',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Cancella',
          style: 'destructive',
          onPress: async () => {
            await clearChat();
          }
        }
      ]
    );
  };

  const renderMessage = ({ item }) => {
    const isSent = item.senderId === currentUserId;
    return (
      <MessageBubble
        message={item}
        isSent={isSent}
        showReadReceipt={true}
      />
    );
  };

  const renderHeader = () => {
    if (room?.type === 'direct') {
      const otherUserId = room.participants.find(id => id !== currentUserId);
      const otherUser = users.find(u => u.id === otherUserId);

      if (!otherUser) return null;

      return (
        <View style={styles.headerContent}>
          <UserAvatar user={otherUser} size={48} />
          <View style={styles.headerText}>
            <Text style={styles.headerName}>{otherUser.username}</Text>
            <Text style={styles.headerStatus}>
              {otherUser.status === 'online'
                ? 'Online'
                : `Ultimo accesso: ${new Date(otherUser.lastSeen).toLocaleString('it-IT')}`}
            </Text>
          </View>
        </View>
      );
    }

    return (
      <View style={styles.headerContent}>
        <View style={[styles.groupAvatar, { width: 48, height: 48 }]}>
          <Text style={styles.groupAvatarText}>
            {room?.name.substring(0, 2).toUpperCase()}
          </Text>
        </View>
        <View style={styles.headerText}>
          <Text style={styles.headerName}>{room?.name}</Text>
          <Text style={styles.headerStatus}>
            {room?.participants?.length || 0} partecipanti
          </Text>
        </View>
      </View>
    );
  };

  const renderListHeader = () => {
    return (
      <>
        {renderHeader()}
        {typingUsers.length > 0 && <TypingIndicator users={typingUsers} />}
      </>
    );
  };

  return (
    <View style={globalStyles.container}>
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        contentContainerStyle={[styles.messagesList, messages.length === 0 && styles.emptyList]}
        ListHeaderComponent={renderListHeader}
        ListEmptyComponent={
          <View style={chatStyles.emptyContainer}>
            <Ionicons name="chatbubble-outline" size={64} color={colors.textLight} />
            <Text style={chatStyles.emptyText}>Inizia la conversazione!</Text>
          </View>
        }
        onScrollBeginDrag={() => {
          // Marca come letti quando si scorre
          markMessagesAsRead();
        }}
      />

      <ChatInput onSend={handleSend} />
    </View>
  );
};

const styles = StyleSheet.create({
  messagesList: {
    padding: spacing.md
  },
  emptyList: {
    flex: 1
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.divider
  },
  groupAvatar: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.primary,
    borderRadius: 24
  },
  groupAvatarText: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.white
  },
  headerText: {
    flex: 1,
    marginLeft: spacing.md
  },
  headerName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text
  },
  headerStatus: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2
  }
});

export default ChatRoomScreen;
