import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  Modal,
  TouchableOpacity,
  Text,
  ScrollView,
  Alert,
} from 'react-native';
import { Image } from 'expo-image';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius } from '../styles/theme';
import { formatDate, formatFileSize } from '../utils/helpers';
import FilterSelector from './FilterSelector';

const PhotoView = ({
  visible,
  photo,
  onClose,
  onDelete,
  onShare,
  onApplyFilter,
  onViewDetails,
}) => {
  const [currentFilter, setCurrentFilter] = useState(photo?.filter || 'none');

  if (!photo) return null;

  const handleDelete = () => {
    Alert.alert(
      'Elimina foto',
      'Sei sicuro di voler eliminare questa foto?',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: () => {
            onDelete(photo.id);
            onClose();
          },
        },
      ]
    );
  };

  const handleShare = async () => {
    try {
      await onShare(photo.uri);
    } catch (error) {
      Alert.alert('Errore', 'Impossibile condividere la foto');
    }
  };

  const handleFilterChange = async (filter) => {
    setCurrentFilter(filter);
    if (onApplyFilter) {
      await onApplyFilter(photo.id, filter);
    }
  };

  return (
    <Modal
      visible={visible}
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.headerButton}>
            <Ionicons name="close" size={28} color={Colors.text} />
          </TouchableOpacity>

          <Text style={styles.headerTitle}>Foto</Text>

          <TouchableOpacity onPress={handleDelete} style={styles.headerButton}>
            <Ionicons name="trash-outline" size={28} color={Colors.danger} />
          </TouchableOpacity>
        </View>

        {/* Photo */}
        <ScrollView style={styles.content}>
          <View style={styles.photoContainer}>
            <Image
              source={{ uri: photo.uri }}
              style={styles.photo}
              contentFit="contain"
            />
          </View>

          {/* Photo Info */}
          <View style={styles.infoContainer}>
            <Text style={styles.infoTitle}>Informazioni</Text>
            <InfoRow label="Dimensione" value={formatFileSize(photo.size)} />
            <InfoRow label="Data" value={formatDate(photo.createdAt)} />
            {photo.width > 0 && (
              <InfoRow
                label="Risoluzione"
                value={`${photo.width} x ${photo.height}`}
              />
            )}
            <InfoRow
              label="Filtro"
              value={currentFilter !== 'none' ? currentFilter : 'Nessuno'}
            />
          </View>

          {/* Filter Selector */}
          {onApplyFilter && (
            <View style={styles.filterContainer}>
              <Text style={styles.filterTitle}>Applica Filtro</Text>
              <FilterSelector
                selectedFilter={currentFilter}
                onFilterSelect={handleFilterChange}
                previewUri={photo.uri}
              />
            </View>
          )}
        </ScrollView>

        {/* Bottom Actions */}
        <View style={styles.footer}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleShare}
          >
            <Ionicons name="share-outline" size={24} color={Colors.primary} />
            <Text style={styles.actionButtonText}>Condividi</Text>
          </TouchableOpacity>

          {onViewDetails && (
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => onViewDetails(photo)}
            >
              <Ionicons name="information-circle-outline" size={24} color={Colors.primary} />
              <Text style={styles.actionButtonText}>Dettagli</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    </Modal>
  );
};

const InfoRow = ({ label, value }) => (
  <View style={styles.infoRow}>
    <Text style={styles.infoLabel}>{label}:</Text>
    <Text style={styles.infoValue}>{value}</Text>
  </View>
);

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
  headerButton: {
    padding: Spacing.sm,
  },
  headerTitle: {
    ...Typography.subtitle,
  },
  content: {
    flex: 1,
  },
  photoContainer: {
    width: '100%',
    height: 400,
    backgroundColor: Colors.backgroundSecondary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  photo: {
    width: '100%',
    height: '100%',
  },
  infoContainer: {
    padding: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  infoTitle: {
    ...Typography.subtitle,
    marginBottom: Spacing.md,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: Spacing.sm,
  },
  infoLabel: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  infoValue: {
    ...Typography.body,
    fontWeight: '600',
  },
  filterContainer: {
    padding: Spacing.lg,
  },
  filterTitle: {
    ...Typography.subtitle,
    marginBottom: Spacing.md,
  },
  footer: {
    flexDirection: 'row',
    padding: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    gap: Spacing.md,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: Spacing.md,
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: BorderRadius.md,
    gap: Spacing.sm,
  },
  actionButtonText: {
    ...Typography.body,
    color: Colors.primary,
    fontWeight: '600',
  },
});

export default PhotoView;
