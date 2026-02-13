import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { chatStyles, colors } from '../styles/theme';

const MessageBubble = ({ message, isSent, showReadReceipt }) => {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();

    if (isToday) {
      return date.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
    }

    return date.toLocaleDateString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const isRead = message.read && (message.readBy?.length > 0 || isSent);

  return (
    <View
      style={[
        chatStyles.messageBubble,
        isSent ? chatStyles.messageSent : chatStyles.messageReceived
      ]}
    >
      <Text style={chatStyles.messageText}>{message.text}</Text>

      <View style={chatStyles.messageMeta}>
        {showReadReceipt && isSent && (
          <Text style={[
            chatStyles.readReceipt,
            !isRead && { color: colors.textLight }
          ]}>
            ✓✓
          </Text>
        )}
        <Text style={chatStyles.messageTime}>{formatTime(message.timestamp)}</Text>
      </View>
    </View>
  );
};

export default MessageBubble;
