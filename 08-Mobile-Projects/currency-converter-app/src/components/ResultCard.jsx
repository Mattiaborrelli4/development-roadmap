import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { COLORS, SPACING, FONT_SIZES, BORDER_RADIUS, SHADOWS } from '../styles/theme';
import { formatCurrency } from '../services/currencyAPI';

const ResultCard = ({ result, currencyInfo, onToggleFavorite, isFavorite }) => {
  if (!result) {
    return null;
  }

  const fromInfo = currencyInfo(result.from);
  const toInfo = currencyInfo(result.to);

  return (
    <View style={styles.container}>
      <View style={styles.resultHeader}>
        <Text style={styles.resultLabel}>Risultato</Text>
        <TouchableOpacity
          onPress={onToggleFavorite}
          style={[styles.favoriteButton, isFavorite && styles.favoriteButtonActive]}
          activeOpacity={0.7}
        >
          <Text style={[styles.favoriteText, isFavorite && styles.favoriteTextActive]}>
            {isFavorite ? '★ Salva' : '☆ Salva'}
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.resultRow}>
        <Text style={styles.resultAmount}>
          {formatCurrency(result.result, result.to, toInfo.symbol)}
        </Text>
      </View>

      <View style={styles.details}>
        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Tasso di cambio:</Text>
          <Text style={styles.detailValue}>
            1 {result.from} = {result.rate.toFixed(4)} {result.to}
          </Text>
        </View>

        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Importo:</Text>
          <Text style={styles.detailValue}>
            {formatCurrency(result.amount, result.from, fromInfo.symbol)}
          </Text>
        </View>

        <View style={styles.detailRow}>
          <Text style={styles.detailLabel}>Commissione:</Text>
          <Text style={styles.detailValue}>0.00 €</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginTop: SPACING.md,
    ...SHADOWS.md,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  resultLabel: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  favoriteButton: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  favoriteButtonActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  favoriteText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  favoriteTextActive: {
    color: COLORS.surface,
  },
  resultRow: {
    alignItems: 'center',
    paddingVertical: SPACING.md,
  },
  resultAmount: {
    fontSize: FONT_SIZES.xxl,
    fontWeight: '700',
    color: COLORS.primary,
  },
  details: {
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: SPACING.md,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.sm,
  },
  detailLabel: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  detailValue: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.text,
    fontWeight: '500',
  },
});

export default ResultCard;
