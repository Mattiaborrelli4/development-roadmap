import React from 'react';
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
} from 'react-native';
import { COLORS, SPACING, FONT_SIZES, BORDER_RADIUS } from '../styles/theme';
import { CURRENCIES } from '../utils/constants';

const CurrencyPicker = ({
  visible,
  onClose,
  onSelect,
  selectedCurrency,
  title,
}) => {
  const renderCurrency = ({ item }) => {
    const isSelected = item.code === selectedCurrency;

    return (
      <TouchableOpacity
        style={[styles.currencyItem, isSelected && styles.currencyItemSelected]}
        onPress={() => {
          onSelect(item.code);
          onClose();
        }}
        activeOpacity={0.7}
      >
        <Text style={styles.flag}>{item.flag}</Text>
        <View style={styles.currencyInfo}>
          <Text style={[styles.code, isSelected && styles.codeSelected]}>
            {item.code}
          </Text>
          <Text style={styles.name}>{item.name}</Text>
        </View>
        <Text style={styles.symbol}>{item.symbol}</Text>
      </TouchableOpacity>
    );
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={false}
      onRequestClose={onClose}
    >
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>{title}</Text>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Text style={styles.closeText}>Chiudi</Text>
          </TouchableOpacity>
        </View>

        <FlatList
          data={CURRENCIES}
          renderItem={renderCurrency}
          keyExtractor={(item) => item.code}
          style={styles.list}
          showsVerticalScrollIndicator={false}
        />
      </SafeAreaView>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    backgroundColor: COLORS.surface,
  },
  title: {
    fontSize: FONT_SIZES.lg,
    fontWeight: '600',
    color: COLORS.text,
  },
  closeButton: {
    padding: SPACING.sm,
  },
  closeText: {
    fontSize: FONT_SIZES.md,
    color: COLORS.primary,
    fontWeight: '600',
  },
  list: {
    flex: 1,
    padding: SPACING.sm,
  },
  currencyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.md,
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  currencyItemSelected: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  flag: {
    fontSize: FONT_SIZES.xxl,
    marginRight: SPACING.md,
  },
  currencyInfo: {
    flex: 1,
  },
  code: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 2,
  },
  codeSelected: {
    color: COLORS.surface,
  },
  name: {
    fontSize: FONT_SIZES.sm,
    color: COLORS.textSecondary,
  },
  symbol: {
    fontSize: FONT_SIZES.md,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
});

export default CurrencyPicker;
