import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import dataService from '../services/dataService';
import storageService from '../services/storageService';

const NotificationsContext = createContext({});

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    setIsLoading(true);
    try {
      const [notificationsData, unread] = await Promise.all([
        dataService.getNotifications(),
        dataService.getUnreadCount(),
      ]);

      setNotifications(notificationsData);
      setUnreadCount(unread);

      await storageService.saveNotifications(notificationsData);
    } catch (error) {
      console.error('Errore caricamento notifiche:', error);

      // Fallback to local storage
      const saved = await storageService.getNotifications();
      if (saved) {
        setNotifications(saved);
        setUnreadCount(saved.filter(n => !n.read).length);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const markAsRead = useCallback(async (notificationId) => {
    try {
      await dataService.markNotificationAsRead(notificationId);

      setNotifications(prev =>
        prev.map(notif =>
          notif.id === notificationId ? { ...notif, read: true } : notif
        )
      );

      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (error) {
      console.error('Errore marca notifica come letta:', error);
    }
  }, []);

  const markAllAsRead = useCallback(async () => {
    try {
      await dataService.markAllNotificationsAsRead();

      setNotifications(prev =>
        prev.map(notif => ({ ...notif, read: true }))
      );

      setUnreadCount(0);
    } catch (error) {
      console.error('Errore marca tutte come lette:', error);
    }
  }, []);

  const addNotification = useCallback((notification) => {
    setNotifications(prev => [notification, ...prev]);
    setUnreadCount(prev => prev + 1);
  }, []);

  const refreshNotifications = useCallback(async () => {
    await loadNotifications();
  }, []);

  return (
    <NotificationsContext.Provider
      value={{
        notifications,
        unreadCount,
        isLoading,
        markAsRead,
        markAllAsRead,
        addNotification,
        refresh: refreshNotifications,
      }}
    >
      {children}
    </NotificationsContext.Provider>
  );
};

export const useNotifications = () => {
  const context = useContext(NotificationsContext);
  if (!context) {
    throw new Error('useNotifications deve essere usato dentro NotificationProvider');
  }
  return context;
};
