import { useState, useEffect } from 'react';
import chatService from '../services/chatService';

export const useUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUsers();

    const handleStatusChange = ({ userId, status }) => {
      setUsers(prevUsers =>
        prevUsers.map(user =>
          user.id === userId ? { ...user, status } : user
        )
      );
    };

    chatService.on('statusChange', handleStatusChange);

    return () => {
      chatService.off('statusChange', handleStatusChange);
    };
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    const usr = await chatService.getUsers();
    setUsers(usr || []);
    setLoading(false);
  };

  const getUserById = async (userId) => {
    return await chatService.getUser(userId);
  };

  const getCurrentUser = async () => {
    return await chatService.getCurrentUser();
  };

  const updateUserStatus = async (userId, status) => {
    await chatService.updateUserStatus(userId, status);
  };

  return {
    users,
    loading,
    reload: loadUsers,
    getUserById,
    getCurrentUser,
    updateUserStatus
  };
};
