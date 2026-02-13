import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { COLORS, SPACING, FONT_SIZES, BORDER_RADIUS } from '../styles/theme';

const FavoritesBar = ({ favorites, onSelect, currentPair }) => {
  if (!favorites || favorites.length === 0) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Preferiti</Text>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {favorites.map((fav, index) => {
          const isActive =
            currentPair &&
            fav.from === currentPair.from &&
            fav.to === currentPair.to;

          return (
            <TouchableOpacity
              key={index}
              style={[styles.item, isActive && styles.itemActive]}
              onPress={() => onSelect(fav.from, fav.to)}
              activeOpacity={0.7}
            >
              <Text style={[styles.itemText, isActive && styles.itemTextActive]}>
                {fav.from}/{fav.to}
              </Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: SPACING.md,
  },
  title: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
    marginLeft: SPACING.xs,
  },
  scrollContent: {
    paddingHorizontal: SPACING.xs,
  },
  item: {
    backgroundColor: COLORS.surface,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
    marginRight: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  itemActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  itemText: {
    fontSize: FONT_SIZES.sm,
    fontWeight: '600',
    color: COLORS.text,
  },
  itemTextActive: {
    color: COLORS.surface,
  },
});

export default FavoritesBar;
