import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { chatStyles, colors } from '../styles/theme';

const ChatInput = ({ onSend, onAttachment }) => {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (text.trim()) {
      onSend(text.trim());
      setText('');
    }
  };

  const handleAttachment = () => {
    Alert.alert(
      'Allegati',
      'Funzionalità di allegati simulata',
      [{ text: 'OK' }]
    );
    if (onAttachment) {
      onAttachment();
    }
  };

  return (
    <View style={chatStyles.chatInputContainer}>
      <TouchableOpacity style={chatStyles.iconButton} onPress={handleAttachment}>
        <Ionicons name="add-circle" size={28} color={colors.primary} />
      </TouchableOpacity>

      <View style={styles.inputWrapper}>
        <TextInput
          style={chatStyles.input}
          placeholder="Scrivi un messaggio..."
          placeholderTextColor={colors.textLight}
          value={text}
          onChangeText={setText}
          multiline
          maxLength={1000}
        />
      </View>

      {text.trim() ? (
        <TouchableOpacity style={chatStyles.iconButton} onPress={handleSend}>
          <Ionicons name="send" size={24} color={colors.primary} />
        </TouchableOpacity>
      ) : (
        <TouchableOpacity style={chatStyles.iconButton} onPress={handleAttachment}>
          <Ionicons name="camera" size={24} color={colors.primary} />
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  inputWrapper: {
    flex: 1,
    marginHorizontal: 8
  }
});

export default ChatInput;
