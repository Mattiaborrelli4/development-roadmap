import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { COLORS, SPACING, FONT_SIZES, BORDER_RADIUS } from '../styles/theme';
import { formatCurrency } from '../services/currencyAPI';

const HistoryList = ({ history, onSelectItem, onClear }) => {
  if (!history || history.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>Nessuna conversione recente</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Conversioni Recenti</Text>
        {history.length > 0 && (
          <TouchableOpacity onPress={onClear}>
            <Text style={styles.clearText}>Pulisci</Text>
          </TouchableOpacity>
        )}
      </View>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {history.slice().reverse().map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.item}
            onPress={() => onSelectItem(item)}
            activeOpacity={0.7}
          >
            <View style={styles.itemHeader}>
              <Text style={styles.currencies}>
                {item.from} → {item.to}
              </Text>
              <Text style={styles.amount}>
                {formatCurrency(item.amount, item.from, '')}
              </Text>
            </View>
            <Text style={styles.result}>
              {formatCurrency(item.result, item.to, '')}
            </Text>
            <Text style={styles.rate}>
              1 {item.from} = {item.rate.toFixed(4)} {item.to}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: SPACING.lg,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
    paddingHorizontal: SPACING.xs,
  },
  title: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.text,
  },
  clearText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.primary,
    fontWeight: '600',
  },
  scrollContent: {
    paddingHorizontal: SPACING.xs,
  },
  item: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    padding: SPACING.md,
    marginRight: SPACING.sm,
    minWidth: 160,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.xs,
  },
  currencies: {
    fontSize: FONT_SIZES.sm,
    fontWeight: '600',
    color: COLORS.text,
  },
  amount: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  result: {
    fontSize: FONT_SIZES.lg,
    fontWeight: '700',
    color: COLORS.primary,
    marginBottom: SPACING.xs,
  },
  rate: {
    fontSize: FONT_SIZES.xs,
    color: COLORS.textSecondary,
  },
  emptyContainer: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    fontStyle: 'italic',
  },
});

export default HistoryList;
