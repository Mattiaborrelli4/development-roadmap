import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Text,
  Alert,
  ActionSheetIOS,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius } from '../styles/theme';
import { usePhotos } from '../hooks/usePhotos';
import { albumService } from '../services/albumService';
import PhotoGrid from '../components/PhotoGrid';
import PhotoView from '../components/PhotoView';

const AlbumDetailScreen = ({ route, navigation }) => {
  const { albumId } = route.params;
  const [album, setAlbum] = useState(null);
  const [selectedPhotos, setSelectedPhotos] = useState([]);
  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [showPhotoView, setShowPhotoView] = useState(false);
  const [gridColumns, setGridColumns] = useState(3);

  const {
    photos,
    loading,
    refresh,
    deletePhotos,
    applyFilter,
    sharePhoto,
  } = usePhotos(albumId);

  React.useEffect(() => {
    loadAlbum();
  }, [albumId]);

  const loadAlbum = async () => {
    const albumData = await albumService.getAlbumById(albumId);
    setAlbum(albumData);
    navigation.setOptions({ title: albumData?.name || 'Album' });
  };

  const handleRenameAlbum = () => {
    if (!album) return;

    Alert.prompt(
      'Rinomina Album',
      'Inserisci il nuovo nome',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Salva',
          onPress: async (name) => {
            if (name && name.trim()) {
              await albumService.renameAlbum(album.id, name.trim());
              await loadAlbum();
            }
          },
        },
      ],
      'plain-text',
      album.name
    );
  };

  const handleDeleteAlbum = () => {
    if (!album) return;

    Alert.alert(
      'Elimina Album',
      'Sei sicuro di voler eliminare questo album? Le foto verranno spostate fuori dall\'album.',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            await albumService.deleteAlbum(album.id);
            navigation.goBack();
          },
        },
      ]
    );
  };

  const handleMenuPress = () => {
    if (Platform.OS === 'ios') {
      ActionSheetIOS.showActionSheetWithOptions(
        {
          options: ['Annulla', 'Rinomina Album', 'Elimina Album'],
          cancelButtonIndex: 0,
          destructiveButtonIndex: 2,
        },
        (buttonIndex) => {
          if (buttonIndex === 1) handleRenameAlbum();
          if (buttonIndex === 2) handleDeleteAlbum();
        }
      );
    } else {
      Alert.alert(
        'Opzioni Album',
        'Cosa vuoi fare?',
        [
          { text: 'Annulla', style: 'cancel' },
          { text: 'Rinomina', onPress: handleRenameAlbum },
          { text: 'Elimina', style: 'destructive', onPress: handleDeleteAlbum },
        ]
      );
    }
  };

  const handleAddPhotos = async () => {
    const { photoService } = require('../services/photoService');
    const newPhotos = await photoService.pickFromGallery(true);
    if (newPhotos && newPhotos.length > 0) {
      for (const photo of newPhotos) {
        await photoService.movePhotoToAlbum(photo.id, albumId);
      }
      await refresh();
      await loadAlbum();
    }
  };

  const handlePhotoPress = (photo) => {
    if (selectionMode) {
      togglePhotoSelection(photo.id);
    } else {
      setSelectedPhoto(photo);
      setShowPhotoView(true);
    }
  };

  const handlePhotoLongPress = (photo) => {
    setSelectionMode(true);
    setSelectedPhotos([photo.id]);
  };

  const togglePhotoSelection = (photoId) => {
    setSelectedPhotos(prev =>
      prev.includes(photoId)
        ? prev.filter(id => id !== photoId)
        : [...prev, photoId]
    );
  };

  const handleRemoveFromAlbum = async () => {
    const { photoService } = require('../services/photoService');
    for (const photoId of selectedPhotos) {
      await photoService.movePhotoToAlbum(photoId, null);
    }
    await refresh();
    await loadAlbum();
    exitSelectionMode();
  };

  const handleDeleteSelected = async () => {
    await deletePhotos(selectedPhotos);
    exitSelectionMode();
    await loadAlbum();
  };

  const exitSelectionMode = () => {
    setSelectionMode(false);
    setSelectedPhotos([]);
  };

  const handleApplyFilter = async (photoId, filter) => {
    await applyFilter(photoId, filter);
    const updated = photos.find(p => p.id === photoId);
    if (updated) {
      setSelectedPhoto(updated);
    }
  };

  const handleShare = async (uri) => {
    await sharePhoto(uri);
  };

  const handleDelete = async (photoId) => {
    const { photoService } = require('../services/photoService');
    await photoService.deletePhoto(photoId);
    await refresh();
    await loadAlbum();
  };

  React.useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <TouchableOpacity onPress={handleMenuPress}>
          <Ionicons name="ellipsis-horizontal" size={24} color={Colors.text} />
        </TouchableOpacity>
      ),
    });
  }, [navigation, album]);

  return (
    <View style={styles.container}>
      {/* Album Info */}
      {album && (
        <View style={styles.albumInfo}>
          <Text style={styles.photoCount}>{album.count} foto</Text>
          <View style={styles.actions}>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => setGridColumns(gridColumns === 3 ? 2 : 3)}
            >
              <Ionicons
                name={gridColumns === 3 ? 'grid-outline' : 'square-outline'}
                size={20}
                color={Colors.text}
              />
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Selection Mode Bar */}
      {selectionMode && (
        <View style={styles.selectionBar}>
          <Text style={styles.selectionText}>
            {selectedPhotos.length} selezionate
          </Text>

          <View style={styles.selectionActions}>
            <TouchableOpacity
              style={styles.selectionButton}
              onPress={handleRemoveFromAlbum}
            >
              <Ionicons name="folder-open-outline" size={20} color={Colors.warning} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.selectionButton}
              onPress={handleDeleteSelected}
            >
              <Ionicons name="trash" size={20} color={Colors.danger} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.selectionButton}
              onPress={exitSelectionMode}
            >
              <Ionicons name="close" size={20} color={Colors.text} />
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Photo Grid */}
      <PhotoGrid
        photos={photos}
        numColumns={gridColumns}
        selectedPhotos={selectedPhotos}
        selectionMode={selectionMode}
        onPhotoPress={handlePhotoPress}
        onPhotoLongPress={handlePhotoLongPress}
        onToggleSelect={togglePhotoSelection}
        onRefresh={refresh}
        refreshing={loading}
      />

      {/* Add Photos FAB */}
      {!selectionMode && (
        <TouchableOpacity style={styles.fab} onPress={handleAddPhotos}>
          <Ionicons name="add" size={28} color={Colors.background} />
        </TouchableOpacity>
      )}

      {/* Photo View Modal */}
      <PhotoView
        visible={showPhotoView}
        photo={selectedPhoto}
        onClose={() => setShowPhotoView(false)}
        onShare={handleShare}
        onDelete={handleDelete}
        onApplyFilter={handleApplyFilter}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  albumInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  photoCount: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  actions: {
    flexDirection: 'row',
    gap: Spacing.sm,
  },
  actionButton: {
    padding: Spacing.sm,
  },
  selectionBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    backgroundColor: Colors.primary,
  },
  selectionText: {
    ...Typography.body,
    color: Colors.background,
    fontWeight: '600',
  },
  selectionActions: {
    flexDirection: 'row',
    gap: Spacing.md,
  },
  selectionButton: {
    padding: Spacing.sm,
  },
  fab: {
    position: 'absolute',
    bottom: Spacing.xl,
    right: Spacing.xl,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default AlbumDetailScreen;
