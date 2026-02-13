import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Text,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius } from '../styles/theme';
import { calculateGridColumns, SCREEN_WIDTH } from '../utils/helpers';
import PhotoItem from './PhotoItem';

const PhotoGrid = ({
  photos,
  numColumns = 3,
  onPhotoPress,
  onPhotoLongPress,
  selectedPhotos = [],
  onToggleSelect,
  selectionMode = false,
  onRefresh,
  refreshing = false,
}) => {
  const [itemSize, setItemSize] = useState(0);

  // Calcola la dimensione degli item
  React.useEffect(() => {
    const spacing = Spacing.md;
    const availableWidth = SCREEN_WIDTH - (spacing * 2) - (spacing * (numColumns - 1));
    const size = Math.floor(availableWidth / numColumns);
    setItemSize(size);
  }, [numColumns]);

  const renderItem = ({ item }) => (
    <PhotoItem
      photo={item}
      size={itemSize}
      selected={selectedPhotos.includes(item.id)}
      onSelect={onToggleSelect}
      onPress={onPhotoPress}
      onLongPress={() => onPhotoLongPress && onPhotoLongPress(item)}
      showCheckbox={selectionMode}
    />
  );

  const renderEmptyState = () => (
    <View style={styles.emptyContainer}>
      <Ionicons name="images-outline" size={64} color={Colors.textSecondary} />
      <Text style={styles.emptyTitle}>Nessuna foto</Text>
      <Text style={styles.emptyText}>
        {selectionMode ? 'Seleziona delle foto' : 'Inizia aggiungendo delle foto'}
      </Text>
    </View>
  );

  if (photos.length === 0) {
    return renderEmptyState();
  }

  return (
    <FlatList
      data={photos}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      numColumns={numColumns}
      key={numColumns.toString()}
      contentContainerStyle={styles.gridContainer}
      columnWrapperStyle={numColumns > 1 ? styles.row : undefined}
      refreshControl={
        onRefresh ? (
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={Colors.primary}
          />
        ) : undefined
      }
    />
  );
};

const styles = StyleSheet.create({
  gridContainer: {
    padding: Spacing.md,
  },
  row: {
    justifyContent: 'space-between',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xxl,
  },
  emptyTitle: {
    ...Typography.subtitle,
    marginTop: Spacing.lg,
  },
  emptyText: {
    ...Typography.caption,
    marginTop: Spacing.sm,
    textAlign: 'center',
  },
});

export default PhotoGrid;
