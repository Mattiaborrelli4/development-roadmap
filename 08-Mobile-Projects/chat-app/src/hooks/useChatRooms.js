import { useState, useEffect } from 'react';
import chatService from '../services/chatService';

export const useChatRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRooms();

    const handleRoomUpdate = (updatedRoom) => {
      setRooms(prevRooms =>
        prevRooms.map(room =>
          room.id === updatedRoom.id ? updatedRoom : room
        )
      );
    };

    chatService.on('roomUpdate', handleRoomUpdate);

    return () => {
      chatService.off('roomUpdate', handleRoomUpdate);
    };
  }, []);

  const loadRooms = async () => {
    setLoading(true);
    const rms = await chatService.getChatRooms();
    setRooms(rms || []);
    setLoading(false);
  };

  const createGroup = async (name, participants) => {
    const room = await chatService.createGroup(name, participants);
    await loadRooms();
    return room;
  };

  const createDirectChat = async (targetUserId, currentUserId) => {
    const room = await chatService.createDirectChat(targetUserId, currentUserId);
    await loadRooms();
    return room;
  };

  return {
    rooms,
    loading,
    reload: loadRooms,
    createGroup,
    createDirectChat
  };
};
