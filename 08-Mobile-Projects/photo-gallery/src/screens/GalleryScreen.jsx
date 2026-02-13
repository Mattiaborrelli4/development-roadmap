import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Text,
  Alert,
  ActionSheetIOS,
  Platform,
  Modal,
  ScrollView,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../styles/theme';
import { usePhotos } from '../hooks/usePhotos';
import { useAlbums } from '../hooks/useAlbums';
import PhotoGrid from '../components/PhotoGrid';
import PhotoView from '../components/PhotoView';
import AlbumCard from '../components/AlbumCard';

const GalleryScreen = ({ navigation }) => {
  const {
    photos,
    loading,
    refresh,
    addPhoto,
    addPhotos,
    deletePhotos,
    applyFilter,
    sharePhoto,
    sortPhotos,
  } = usePhotos();

  const { albums, createAlbum } = useAlbums();

  const [viewMode, setViewMode] = useState('photos'); // 'photos' or 'albums'
  const [selectedPhotos, setSelectedPhotos] = useState([]);
  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [showPhotoView, setShowPhotoView] = useState(false);
  const [showAlbumSelect, setShowAlbumSelect] = useState(false);
  const [gridColumns, setGridColumns] = useState(3);

  const handleTakePhoto = async () => {
    try {
      // Implementazione con ImagePicker
      const { photoService } = require('../services/photoService');
      const photo = await photoService.takePhoto();
      if (photo) {
        await addPhoto(photo);
      }
    } catch (error) {
      Alert.alert('Errore', 'Impossibile scattare la foto');
    }
  };

  const handlePickFromGallery = async () => {
    try {
      const { photoService } = require('../services/photoService');
      const newPhotos = await photoService.pickFromGallery(true);
      if (newPhotos && newPhotos.length > 0) {
        await addPhotos(newPhotos);
      }
    } catch (error) {
      Alert.alert('Errore', 'Impossibile selezionare le foto');
    }
  };

  const handleAddPhotos = () => {
    if (Platform.OS === 'ios') {
      ActionSheetIOS.showActionSheetWithOptions(
        {
          options: ['Annulla', 'Scatta Foto', 'Scegli dalla Galleria'],
          cancelButtonIndex: 0,
        },
        (buttonIndex) => {
          if (buttonIndex === 1) {
            navigation.navigate('Camera');
          }
          if (buttonIndex === 2) handlePickFromGallery();
        }
      );
    } else {
      // Per Android, mostra un semplice alert o usa BottomSheet
      Alert.alert(
        'Aggiungi Foto',
        'Come vuoi aggiungere foto?',
        [
          { text: 'Annulla', style: 'cancel' },
          { text: 'Scatta Foto', onPress: () => navigation.navigate('Camera') },
          { text: 'Galleria', onPress: handlePickFromGallery },
        ]
      );
    }
  };

  const handleCreateAlbum = () => {
    Alert.prompt(
      'Nuovo Album',
      'Inserisci il nome dell\'album',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Crea',
          onPress: async (name) => {
            if (name && name.trim()) {
              await createAlbum(name.trim());
            }
          },
        },
      ],
      'plain-text'
    );
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

  const handleDeleteSelected = () => {
    Alert.alert(
      'Elimina Foto',
      `Sei sicuro di voler eliminare ${selectedPhotos.length} foto?`,
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            await deletePhotos(selectedPhotos);
            exitSelectionMode();
          },
        },
      ]
    );
  };

  const handleMoveToAlbum = async (albumId) => {
    const { photoService } = require('../services/photoService');
    for (const photoId of selectedPhotos) {
      await photoService.movePhotoToAlbum(photoId, albumId);
    }
    await refresh();
    exitSelectionMode();
  };

  const exitSelectionMode = () => {
    setSelectionMode(false);
    setSelectedPhotos([]);
  };

  const handleApplyFilter = async (photoId, filter) => {
    await applyFilter(photoId, filter);
    // Aggiorna la foto selezionata
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
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>
          {viewMode === 'photos' ? 'Galleria' : 'Album'}
        </Text>

        <View style={styles.headerActions}>
          {viewMode === 'photos' && (
            <TouchableOpacity
              style={styles.headerButton}
              onPress={() => setGridColumns(gridColumns === 3 ? 2 : 3)}
            >
              <Ionicons
                name={gridColumns === 3 ? 'grid-outline' : 'square-outline'}
                size={24}
                color={Colors.text}
              />
            </TouchableOpacity>
          )}

          <TouchableOpacity
            style={styles.headerButton}
            onPress={() => setViewMode(viewMode === 'photos' ? 'albums' : 'photos')}
          >
            <Ionicons
              name={viewMode === 'photos' ? 'albums-outline' : 'images-outline'}
              size={24}
              color={Colors.text}
            />
          </TouchableOpacity>
        </View>
      </View>

      {/* Selection Mode Bar */}
      {selectionMode && (
        <View style={styles.selectionBar}>
          <Text style={styles.selectionText}>
            {selectedPhotos.length} selezionate
          </Text>

          <View style={styles.selectionActions}>
            <TouchableOpacity
              style={styles.selectionButton}
              onPress={() => setShowAlbumSelect(true)}
            >
              <Ionicons name="folder-outline" size={20} color={Colors.primary} />
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

      {/* Content */}
      {viewMode === 'photos' ? (
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
      ) : (
        <ScrollView
          style={styles.albumsContainer}
          contentContainerStyle={styles.albumsContent}
        >
          <TouchableOpacity
            style={styles.createAlbumCard}
            onPress={handleCreateAlbum}
          >
            <View style={styles.createAlbumIcon}>
              <Ionicons name="add" size={40} color={Colors.primary} />
            </View>
            <Text style={styles.createAlbumText}>Crea Album</Text>
          </TouchableOpacity>

          {albums.map((album) => (
            <AlbumCard
              key={album.id}
              album={album}
              onPress={(album) => navigation.navigate('AlbumDetail', { albumId: album.id })}
              size={(SCREEN_WIDTH - Spacing.md * 3) / 2}
            />
          ))}
        </ScrollView>
      )}

      {/* FAB */}
      {viewMode === 'photos' && !selectionMode && (
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

      {/* Album Selection Modal */}
      {showAlbumSelect && (
        <Modal
          visible={showAlbumSelect}
          transparent
          animationType="slide"
          onRequestClose={() => setShowAlbumSelect(false)}
        >
          <View style={styles.albumModal}>
            <View style={styles.albumModalContent}>
              <Text style={styles.albumModalTitle}>Scegli Album</Text>

              {albums.map((album) => (
                <TouchableOpacity
                  key={album.id}
                  style={styles.albumOption}
                  onPress={() => handleMoveToAlbum(album.id)}
                >
                  <Text style={styles.albumOptionText}>{album.name}</Text>
                  <Ionicons name="chevron-forward" size={20} color={Colors.textSecondary} />
                </TouchableOpacity>
              ))}

              <TouchableOpacity
                style={styles.albumOption}
                onPress={() => handleMoveToAlbum(null)}
              >
                <Text style={styles.albumOptionText}>Nessun Album</Text>
                <Ionicons name="chevron-forward" size={20} color={Colors.textSecondary} />
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.albumModalClose}
                onPress={() => setShowAlbumSelect(false)}
              >
                <Text style={styles.albumModalCloseText}>Annulla</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      )}
    </View>
  );
};

const { width: SCREEN_WIDTH } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  title: {
    ...Typography.title,
  },
  headerActions: {
    flexDirection: 'row',
    gap: Spacing.sm,
  },
  headerButton: {
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
  albumsContainer: {
    flex: 1,
  },
  albumsContent: {
    padding: Spacing.md,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  createAlbumCard: {
    width: (SCREEN_WIDTH - Spacing.md * 3) / 2,
    height: (SCREEN_WIDTH - Spacing.md * 3) / 2 * 0.8 + 50,
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: BorderRadius.lg,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  createAlbumIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: Colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  createAlbumText: {
    ...Typography.body,
    fontWeight: '600',
    marginTop: Spacing.md,
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
    ...Shadows.lg,
  },
  albumModal: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  albumModalContent: {
    backgroundColor: Colors.background,
    borderTopLeftRadius: BorderRadius.xl,
    borderTopRightRadius: BorderRadius.xl,
    padding: Spacing.lg,
  },
  albumModalTitle: {
    ...Typography.subtitle,
    marginBottom: Spacing.md,
  },
  albumOption: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  albumOptionText: {
    ...Typography.body,
  },
  albumModalClose: {
    marginTop: Spacing.md,
    padding: Spacing.md,
    alignItems: 'center',
  },
  albumModalCloseText: {
    ...Typography.body,
    color: Colors.primary,
    fontWeight: '600',
  },
});

export default GalleryScreen;
