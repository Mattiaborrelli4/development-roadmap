import React, { useState } from 'react';
import {
  View,
  TouchableOpacity,
  StyleSheet,
  CheckBox,
} from 'react-native';
import { Image } from 'expo-image';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, BorderRadius } from '../styles/theme';

const PhotoItem = ({
  photo,
  size,
  selected,
  onSelect,
  onPress,
  onLongPress,
  showCheckbox = false,
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);

  const handlePress = () => {
    if (showCheckbox && onSelect) {
      onSelect(photo.id);
    } else if (onPress) {
      onPress(photo);
    }
  };

  return (
    <TouchableOpacity
      style={[
        styles.container,
        {
          width: size,
          height: size,
        },
        selected && styles.selectedContainer,
      ]}
      onPress={handlePress}
      onLongPress={onLongPress}
      activeOpacity={0.9}
    >
      <Image
        source={{ uri: photo.uri }}
        style={styles.image}
        contentFit="cover"
        transition={200}
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setIsLoading(false);
          setError(true);
        }}
      />

      {error && (
        <View style={styles.errorContainer}>
          <Ionicons name="image-outline" size={32} color={Colors.textSecondary} />
        </View>
      )}

      {showCheckbox && (
        <View style={styles.checkboxContainer}>
          <View style={[
            styles.checkbox,
            selected && styles.checkboxSelected,
          ]}>
            {selected && (
              <Ionicons name="checkmark" size={16} color={Colors.background} />
            )}
          </View>
        </View>
      )}

      {photo.filter !== 'none' && (
        <View style={styles.filterBadge}>
          <Ionicons name="color-filter" size={12} color={Colors.background} />
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: BorderRadius.md,
    overflow: 'hidden',
    marginBottom: Spacing.sm,
  },
  selectedContainer: {
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  errorContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.backgroundSecondary,
  },
  checkboxContainer: {
    position: 'absolute',
    top: Spacing.sm,
    left: Spacing.sm,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderWidth: 2,
    borderColor: Colors.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxSelected: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  filterBadge: {
    position: 'absolute',
    bottom: Spacing.sm,
    right: Spacing.sm,
    backgroundColor: Colors.primary,
    borderRadius: BorderRadius.round,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default PhotoItem;
