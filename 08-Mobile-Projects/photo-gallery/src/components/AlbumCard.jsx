import React from 'react';
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Text,
} from 'react-native';
import { Image } from 'expo-image';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../styles/theme';
import { formatDate } from '../utils/helpers';

const AlbumCard = ({
  album,
  onPress,
  onLongPress,
  size = 160,
}) => {
  return (
    <TouchableOpacity
      style={[styles.container, { width: size }]}
      onPress={() => onPress(album)}
      onLongPress={() => onLongPress && onLongPress(album)}
      activeOpacity={0.9}
    >
      <View style={[styles.coverContainer, { height: size * 0.8 }]}>
        {album.coverPhoto ? (
          <Image
            source={{ uri: album.coverPhoto }}
            style={styles.coverImage}
            contentFit="cover"
            transition={200}
          />
        ) : (
          <View style={styles.placeholder}>
            <Ionicons name="images" size={40} color={Colors.textSecondary} />
          </View>
        )}

        <View style={styles.countBadge}>
          <Text style={styles.countText}>{album.count}</Text>
        </View>
      </View>

      <View style={styles.info}>
        <Text style={styles.name} numberOfLines={1}>
          {album.name}
        </Text>
        <Text style={styles.date}>
          {formatDate(album.createdAt)}
        </Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.lg,
  },
  coverContainer: {
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    marginBottom: Spacing.sm,
    ...Shadows.sm,
  },
  coverImage: {
    width: '100%',
    height: '100%',
  },
  placeholder: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.backgroundSecondary,
  },
  countBadge: {
    position: 'absolute',
    bottom: Spacing.sm,
    right: Spacing.sm,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: Spacing.sm,
    paddingVertical: Spacing.xs,
    borderRadius: BorderRadius.round,
  },
  countText: {
    ...Typography.small,
    color: Colors.background,
    fontWeight: '600',
  },
  info: {
    paddingHorizontal: Spacing.xs,
  },
  name: {
    ...Typography.body,
    fontWeight: '600',
  },
  date: {
    ...Typography.small,
    marginTop: 2,
  },
});

export default AlbumCard;
