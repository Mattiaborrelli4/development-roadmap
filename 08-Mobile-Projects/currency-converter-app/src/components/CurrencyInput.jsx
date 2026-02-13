import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';
import { COLORS, SPACING, FONT_SIZES, BORDER_RADIUS } from '../styles/theme';

const CurrencyInput = ({
  label,
  amount,
  onAmountChange,
  currency,
  onPress,
  disabled = false,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>

      <View style={styles.inputRow}>
        <TextInput
          style={[styles.input, disabled && styles.inputDisabled]}
          value={amount}
          onChangeText={onAmountChange}
          placeholder="0.00"
          keyboardType="decimal-pad"
          editable={!disabled}
          selectTextOnFocus
        />

        <View style={styles.currencyButton} onPress={onPress}>
          <Text style={styles.currencyText}>{currency}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: SPACING.md,
  },
  label: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
    marginLeft: SPACING.xs,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    overflow: 'hidden',
  },
  input: {
    flex: 1,
    fontSize: FONT_SIZES.xl,
    fontWeight: '600',
    color: COLORS.text,
    padding: SPACING.md,
    textAlign: 'right',
  },
  inputDisabled: {
    backgroundColor: COLORS.background,
    color: COLORS.textSecondary,
  },
  currencyButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
    borderLeftWidth: 1,
    borderLeftColor: COLORS.border,
  },
  currencyText: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.surface,
  },
});

export default CurrencyInput;
