import { useState, useEffect } from 'react';
import chatService from '../services/chatService';

export const useTyping = (roomId) => {
  const [typingUsers, setTypingUsers] = useState([]);

  useEffect(() => {
    const handleTyping = ({ roomId: typingRoomId, username, isTyping }) => {
      if (typingRoomId === roomId) {
        setTypingUsers(prev => {
          if (isTyping) {
            return [...prev.filter(u => u.username !== username), { username }];
          } else {
            return prev.filter(u => u.username !== username);
          }
        });
      }
    };

    chatService.on('typing', handleTyping);

    return () => {
      chatService.off('typing', handleTyping);
    };
  }, [roomId]);

  return typingUsers;
};
