import React, { useState, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import dataService from '../services/dataService';
import { THEME } from '../utils/constants';
import { formatDistanceToNow } from 'date-fns';
import { it } from 'date-fns/locale';

const MessagesScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { userId } = route.params || {};

  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      // Open conversation with specific user
      openConversation(userId);
    } else {
      loadConversations();
    }
  }, [userId]);

  const loadConversations = async () => {
    setIsLoading(true);
    try {
      const data = await dataService.getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Errore caricamento conversazioni:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const openConversation = async (targetUserId) => {
    try {
      const user = await dataService.getUserById(targetUserId);
      setSelectedConversation({
        id: `conv_${targetUserId}`,
        user,
      });
      loadMessages(`conv_${targetUserId}`);
    } catch (error) {
      console.error('Errore apertura conversazione:', error);
    }
  };

  const loadMessages = async (conversationId) => {
    try {
      const data = await dataService.getMessages(conversationId);
      setMessages(data);
    } catch (error) {
      console.error('Errore caricamento messaggi:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!messageText.trim() || !selectedConversation) return;

    try {
      const newMessage = await dataService.sendMessage(
        selectedConversation.id,
        messageText
      );
      setMessages(prev => [...prev, newMessage]);
      setMessageText('');
    } catch (error) {
      console.error('Errore invio messaggio:', error);
    }
  };

  const renderConversation = ({ item }) => (
    <TouchableOpacity
      style={styles.conversationItem}
      onPress={() => {
        setSelectedConversation(item);
        loadMessages(item.id);
      }}
    >
      <Image source={{ uri: item.user.avatar }} style={styles.avatar} />
      <View style={styles.conversationContent}>
        <View style={styles.conversationHeader}>
          <Text style={styles.username}>{item.user.username}</Text>
          <Text style={styles.timestamp}>
            {formatDistanceToNow(new Date(item.lastMessageTime), {
              addSuffix: true,
              locale: it,
            })}
          </Text>
        </View>
        <Text style={styles.lastMessage} numberOfLines={1}>
          {item.lastMessage}
        </Text>
      </View>
    </TouchableOpacity>
  );

  const renderMessage = ({ item }) => {
    const isMe = item.sender === 'me';
    return (
      <View
        style={[
          styles.messageContainer,
          isMe ? styles.messageMe : styles.messageOther
        ]}
      >
        <Text
          style={[
            styles.messageText,
            isMe ? styles.messageTextMe : styles.messageTextOther
          ]}
        >
          {item.text}
        </Text>
      </View>
    );
  };

  if (selectedConversation) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        {/* Chat Header */}
        <View style={styles.chatHeader}>
          <TouchableOpacity onPress={() => setSelectedConversation(null)}>
            <Ionicons name="arrow-back" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
          <Image
            source={{ uri: selectedConversation.user.avatar }}
            style={styles.chatAvatar}
          />
          <View style={styles.chatInfo}>
            <Text style={styles.chatUsername}>{selectedConversation.user.username}</Text>
          </View>
          <TouchableOpacity>
            <Ionicons name="videocam-outline" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.headerIcon}>
            <Ionicons name="call-outline" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
        </View>

        {/* Messages */}
        <FlatList
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={renderMessage}
          contentContainerStyle={styles.messagesContent}
          showsVerticalScrollIndicator={false}
        />

        {/* Input */}
        <View style={styles.inputContainer}>
          <TouchableOpacity>
            <Ionicons name="camera-outline" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.input}
              placeholder="Messaggio..."
              placeholderTextColor={THEME.colors.textSecondary}
              value={messageText}
              onChangeText={setMessageText}
              multiline
            />
            <TouchableOpacity>
              <Ionicons name="happy-outline" size={24} color={THEME.colors.text} />
            </TouchableOpacity>
          </View>
          <TouchableOpacity
            style={[
              styles.sendButton,
              messageText.trim() && styles.sendButtonActive
            ]}
            onPress={handleSendMessage}
            disabled={!messageText.trim()}
          >
            <Ionicons
              name="send"
              size={20}
              color={messageText.trim() ? THEME.colors.primary : THEME.colors.textSecondary}
            />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={24} color={THEME.colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Messaggi</Text>
        <TouchableOpacity onPress={() => navigation.navigate('NewMessage')}>
          <Ionicons name="create-outline" size={24} color={THEME.colors.text} />
        </TouchableOpacity>
      </View>

      {/* Conversations */}
      <FlatList
        data={conversations}
        keyExtractor={(item) => item.id}
        renderItem={renderConversation}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="paper-plane-outline" size={64} color={THEME.colors.textSecondary} />
            <Text style={styles.emptyText}>Nessun messaggio</Text>
          </View>
        }
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: THEME.colors.text,
  },
  conversationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
  },
  conversationContent: {
    flex: 1,
    marginLeft: 12,
  },
  conversationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  username: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  timestamp: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
  },
  lastMessage: {
    fontSize: 14,
    color: THEME.colors.textSecondary,
    marginTop: 2,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 16,
    color: THEME.colors.textSecondary,
    marginTop: 16,
  },
  chatHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  chatAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    marginLeft: 12,
  },
  chatInfo: {
    flex: 1,
    marginLeft: 12,
  },
  chatUsername: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  headerIcon: {
    marginLeft: 16,
  },
  messagesContent: {
    paddingVertical: 16,
    paddingHorizontal: 16,
    flexGrow: 1,
  },
  messageContainer: {
    maxWidth: '75%',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 4,
  },
  messageMe: {
    alignSelf: 'flex-end',
    backgroundColor: THEME.colors.primary,
  },
  messageOther: {
    alignSelf: 'flex-start',
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  messageText: {
    fontSize: 14,
    lineHeight: 18,
  },
  messageTextMe: {
    color: '#fff',
  },
  messageTextOther: {
    color: THEME.colors.text,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: THEME.colors.border,
  },
  inputWrapper: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: THEME.colors.backgroundSecondary,
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginHorizontal: 8,
  },
  input: {
    flex: 1,
    fontSize: 14,
    color: THEME.colors.text,
    maxHeight: 100,
  },
  sendButton: {
    padding: 8,
  },
  sendButtonActive: {
    opacity: 1,
  },
});

export default MessagesScreen;
