import React, { useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { useNotifications } from '../hooks/useNotifications';
import { usePosts } from '../hooks/usePosts';
import { THEME } from '../utils/constants';
import { formatDistanceToNow } from 'date-fns';
import { it } from 'date-fns/locale';

const NotificationsScreen = () => {
  const navigation = useNavigation();
  const { notifications, markAsRead, markAllAsRead, isLoading } = useNotifications();
  const { getPostById } = usePosts();

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'like':
        return 'heart';
      case 'comment':
        return 'chatbubble';
      case 'follow':
        return 'person-add';
      case 'mention':
        return 'at';
      default:
        return 'notifications';
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'like':
        return THEME.colors.like;
      case 'comment':
        return THEME.colors.primary;
      case 'follow':
        return THEME.colors.primary;
      case 'mention':
        return THEME.colors.success;
      default:
        return THEME.colors.text;
    }
  };

  const handleNotificationPress = useCallback(async (notification) => {
    await markAsRead(notification.id);

    if (notification.post) {
      navigation.navigate('PostDetail', { postId: notification.post.id });
    } else if (notification.type === 'follow') {
      navigation.navigate('Profile', { userId: notification.user.id });
    }
  }, [markAsRead, navigation]);

  const handleMarkAllRead = async () => {
    await markAllAsRead();
  };

  const renderNotification = ({ item }) => (
    <TouchableOpacity
      style={[styles.notificationItem, !item.read && styles.unreadNotification]}
      onPress={() => handleNotificationPress(item)}
    >
      <View style={styles.iconContainer}>
        <Ionicons
          name={getNotificationIcon(item.type)}
          size={24}
          color={getNotificationColor(item.type)}
        />
      </View>
      <Image source={{ uri: item.user.avatar }} style={styles.avatar} />
      <View style={styles.content}>
        <Text style={styles.text}>
          <Text style={styles.username}>{item.user.username}</Text>
          {' '}{item.message}
        </Text>
        <Text style={styles.timestamp}>
          {formatDistanceToNow(new Date(item.createdAt), {
            addSuffix: true,
            locale: it,
          })}
        </Text>
      </View>
      {item.post && (
        <Image source={{ uri: item.post.content.uri }} style={styles.postPreview} />
      )}
      {!item.read && <View style={styles.unreadDot} />}
    </TouchableOpacity>
  );

  const renderHeader = () => (
    <View style={styles.headerContainer}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Notifiche</Text>
        {notifications.some(n => !n.read) && (
          <TouchableOpacity onPress={handleMarkAllRead}>
            <Text style={styles.markAllRead}>Segna come lette</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Ionicons name="notifications-outline" size={64} color={THEME.colors.textSecondary} />
      <Text style={styles.emptyText}>Nessuna notifica</Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <FlatList
        data={notifications}
        keyExtractor={(item) => item.id}
        renderItem={renderNotification}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={renderEmpty}
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
  headerContainer: {
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: THEME.colors.text,
  },
  markAllRead: {
    fontSize: 14,
    color: THEME.colors.primary,
  },
  notificationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  unreadNotification: {
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  iconContainer: {
    marginRight: 12,
  },
  avatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    marginRight: 12,
  },
  content: {
    flex: 1,
  },
  text: {
    fontSize: 14,
    color: THEME.colors.text,
    lineHeight: 18,
  },
  username: {
    fontWeight: '600',
  },
  timestamp: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    marginTop: 2,
  },
  postPreview: {
    width: 44,
    height: 44,
    borderRadius: 4,
    marginLeft: 12,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: THEME.colors.primary,
    position: 'absolute',
    right: 12,
    top: 12,
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
});

export default NotificationsScreen;
