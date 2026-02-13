import React from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Text,
} from 'react-native';
import { Image } from 'expo-image';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius } from '../styles/theme';
import { getAllFilters } from '../utils/filters';

const FilterSelector = ({
  selectedFilter,
  onFilterSelect,
  previewUri,
  style,
}) => {
  const filters = getAllFilters();

  return (
    <View style={[styles.container, style]}>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {filters.map((filter) => (
          <TouchableOpacity
            key={filter.key}
            style={[
              styles.filterItem,
              selectedFilter === filter.key && styles.selectedFilter,
            ]}
            onPress={() => onFilterSelect(filter.key)}
            activeOpacity={0.8}
          >
            <View style={styles.previewContainer}>
              {previewUri ? (
                <Image
                  source={{ uri: previewUri }}
                  style={[
                    styles.previewImage,
                    selectedFilter === filter.key && styles.selectedPreviewImage,
                  ]}
                  contentFit="cover"
                />
              ) : (
                <View style={[styles.previewPlaceholder, selectedFilter === filter.key && styles.selectedPreviewPlaceholder]}>
                  <Ionicons name="image" size={24} color={Colors.textSecondary} />
                </View>
              )}
            </View>

            <Text style={[
              styles.filterName,
              selectedFilter === filter.key && styles.selectedFilterName,
            ]}>
              {filter.name}
            </Text>

            {selectedFilter === filter.key && (
              <View style={styles.checkIcon}>
                <Ionicons name="checkmark-circle" size={20} color={Colors.primary} />
              </View>
            )}
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: Spacing.md,
  },
  scrollContent: {
    paddingHorizontal: Spacing.md,
    gap: Spacing.md,
  },
  filterItem: {
    alignItems: 'center',
    position: 'relative',
  },
  selectedFilter: {
    opacity: 1,
  },
  previewContainer: {
    marginBottom: Spacing.sm,
  },
  previewImage: {
    width: 80,
    height: 80,
    borderRadius: BorderRadius.md,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedPreviewImage: {
    borderColor: Colors.primary,
  },
  previewPlaceholder: {
    width: 80,
    height: 80,
    borderRadius: BorderRadius.md,
    backgroundColor: Colors.backgroundSecondary,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedPreviewPlaceholder: {
    borderColor: Colors.primary,
  },
  filterName: {
    ...Typography.small,
    textAlign: 'center',
    minWidth: 80,
  },
  selectedFilterName: {
    ...Typography.small,
    fontWeight: '600',
    color: Colors.primary,
  },
  checkIcon: {
    position: 'absolute',
    top: -8,
    right: -8,
    backgroundColor: Colors.background,
    borderRadius: BorderRadius.round,
  },
});

export default FilterSelector;
