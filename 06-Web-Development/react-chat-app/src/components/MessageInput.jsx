import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../contexts/ChatContext';
import './MessageInput.css';

export default function MessageInput() {
  const [message, setMessage] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const { currentRoom, sendMessage, sendTyping, user } = useChat();
  const inputRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const emojis = [
    '😀', '😂', '😍', '🥰', '😎', '🤔', '😴', '🥳',
    '❤️', '👍', '👎', '👏', '🙌', '🤝', '✌️', '🤟',
    '🎉', '🎊', '🔥', '✨', '💯', '⭐', '💫', '🌟',
    '💻', '🎮', '🎵', '📚', '🎯', '🚀', '💡', '🔧'
  ];

  // Focus sull'input quando cambia stanza
  useEffect(() => {
    if (currentRoom) {
      inputRef.current?.focus();
    }
  }, [currentRoom]);

  // Gestisci digitazione
  useEffect(() => {
    if (message.trim()) {
      sendTyping(true);

      // Cancella timeout precedente
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }

      // Smetti di digitare dopo 2 secondi
      typingTimeoutRef.current = setTimeout(() => {
        sendTyping(false);
      }, 2000);
    } else {
      sendTyping(false);
    }

    return () => {
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, [message]);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!message.trim() || !currentRoom) return;

    sendMessage(message.trim());
    setMessage('');
    sendTyping(false);
    setShowEmojiPicker(false);
  };

  const handleKeyDown = (e) => {
    // Invia con Enter (ma Shift+Enter va a capo)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }

    // Chiudi emoji picker con Escape
    if (e.key === 'Escape') {
      setShowEmojiPicker(false);
    }
  };

  const addEmoji = (emoji) => {
    setMessage(prev => prev + emoji);
    inputRef.current?.focus();
  };

  if (!currentRoom) {
    return null;
  }

  return (
    <div className="message-input-container">
      <form onSubmit={handleSubmit} className="message-input-form">
        <button
          type="button"
          className="emoji-button"
          onClick={() => setShowEmojiPicker(!showEmojiPicker)}
          title="Aggiungi emoji"
        >
          😊
        </button>

        <input
          ref={inputRef}
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Scrivi in #${currentRoom.name}...`}
          className="message-input"
          maxLength={500}
          disabled={!user}
        />

        <div className="input-actions">
          <span className="char-count">{message.length}/500</span>
          <button
            type="submit"
            className="send-button"
            disabled={!message.trim()}
            title="Invia messaggio"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
          </button>
        </div>

        {showEmojiPicker && (
          <div className="emoji-picker">
            <div className="emoji-grid">
              {emojis.map((emoji, index) => (
                <button
                  key={index}
                  type="button"
                  className="emoji-item"
                  onClick={() => addEmoji(emoji)}
                  title={emoji}
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
        )}
      </form>

      <div className="input-footer">
        <span className="footer-text">
          Premi Enter per inviare, Shift + Enter per andare a capo
        </span>
      </div>
    </div>
  );
}
