import { useState, useEffect } from 'react';
import chatService from '../services/chatService';

export const useMessages = (roomId) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMessages();

    // Ascolta nuovi messaggi
    const handleNewMessage = (message) => {
      if (message.roomId === roomId) {
        setMessages(prev => [...prev, message]);
      }
    };

    chatService.on('message', handleNewMessage);

    return () => {
      chatService.off('message', handleNewMessage);
    };
  }, [roomId]);

  const loadMessages = async () => {
    setLoading(true);
    const msgs = await chatService.getMessages(roomId);
    setMessages(msgs || []);
    setLoading(false);
  };

  const sendMessage = async (text, type = 'text') => {
    const currentUserId = await chatService.getCurrentUserId();
    return await chatService.sendMessage(roomId, currentUserId, text, type);
  };

  const markAsRead = async (userId) => {
    await chatService.markAsRead(roomId, userId);
  };

  const clearChat = async () => {
    await chatService.clearChat(roomId);
    setMessages([]);
  };

  return {
    messages,
    loading,
    sendMessage,
    markAsRead,
    clearChat,
    reload: loadMessages
  };
};
