import React from 'react';
import { View, Image, Text, StyleSheet } from 'react-native';
import { colors, borderRadius } from '../styles/theme';
import OnlineStatus from './OnlineStatus';

const UserAvatar = ({ user, size = 56, showStatus = true }) => {
  const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  const getAvatarColor = (name) => {
    const colorsList = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
      '#FFEAA7', '#DFE6E9', '#74B9FF', '#A29BFE',
      '#FD79A8', '#00B894', '#E17055', '#0984E3'
    ];
    const index = name
      ? name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      : 0;
    return colorsList[index % colorsList.length];
  };

  const avatarColor = user?.avatar ? null : getAvatarColor(user?.username);

  return (
    <View style={[styles.avatarContainer, { width: size, height: size, borderRadius: size / 2 }]}>
      {user?.avatar ? (
        <Image
          source={{ uri: user.avatar }}
          style={[styles.avatarImage, { width: size, height: size, borderRadius: size / 2 }]}
        />
      ) : (
        <View style={[
          styles.avatarPlaceholder,
          { backgroundColor: avatarColor, width: size, height: size, borderRadius: size / 2 }
        ]}>
          <Text style={[styles.avatarText, { fontSize: size * 0.4 }]}>
            {getInitials(user?.username)}
          </Text>
        </View>
      )}

      {showStatus && user?.status && (
        <OnlineStatus status={user.status} size={size * 0.25} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  avatarContainer: {
    position: 'relative',
    overflow: 'hidden'
  },
  avatarImage: {
    resizeMode: 'cover'
  },
  avatarPlaceholder: {
    justifyContent: 'center',
    alignItems: 'center'
  },
  avatarText: {
    fontWeight: '600',
    color: colors.white
  }
});

export default UserAvatar;
