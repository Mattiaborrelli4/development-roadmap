import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import {CATEGORIES} from '../utils/constants';

const ListItem = ({
  item,
  onToggleBought,
  onDelete,
  onPress,
  style,
}) => {
  const category = CATEGORIES.find(cat => cat.name === item.category) || CATEGORIES[CATEGORIES.length - 1];

  return (
    <View style={styles.swipeContainer}>
      <TouchableOpacity
        style={[styles.container, item.bought && styles.bought, style]}
        onPress={onPress}
        onLongPress={() => {
          // Long press could open options menu
          if (onDelete) {
            onDelete();
          }
        }}
        activeOpacity={0.7}>
        <View
          style={[
            styles.iconContainer,
            {backgroundColor: category.color + '20'},
          ]}>
          <Text style={styles.icon}>{category.icon}</Text>
        </View>

        <View style={styles.content}>
          <View style={styles.header}>
            <Text style={[styles.name, item.bought && styles.nameBought]}>
              {item.name}
            </Text>
            {item.quantity > 1 && (
              <View style={styles.quantityBadge}>
                <Text style={styles.quantityText}>x{item.quantity}</Text>
              </View>
            )}
          </View>

          <View style={styles.meta}>
            <Text style={styles.category}>{category.name}</Text>
            {item.notes && (
              <>
                <Text style={styles.separator}>•</Text>
                <Text style={styles.notes} numberOfLines={1}>
                  {item.notes}
                </Text>
              </>
            )}
          </View>

          {item.barcode && (
            <Text style={styles.barcode}>📊 {item.barcode}</Text>
          )}
        </View>

        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.deleteButton}
            onPress={onDelete}>
            <Text style={styles.deleteIcon}>🗑️</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.checkButton}
            onPress={() => onToggleBought(item.id)}>
            <Text style={styles.checkIcon}>{item.bought ? '✅' : '⬜'}</Text>
          </TouchableOpacity>
        </View>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  swipeContainer: {
    backgroundColor: '#FFFFFF',
  },
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  bought: {
    opacity: 0.6,
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  icon: {
    fontSize: 24,
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2C3E50',
    flex: 1,
  },
  nameBought: {
    textDecorationLine: 'line-through',
  },
  quantityBadge: {
    backgroundColor: '#4ECDC4',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginLeft: 8,
  },
  quantityText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  meta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  category: {
    fontSize: 14,
    color: '#7F8C8D',
  },
  separator: {
    marginHorizontal: 8,
    color: '#7F8C8D',
  },
  notes: {
    fontSize: 14,
    color: '#7F8C8D',
    flex: 1,
  },
  barcode: {
    fontSize: 12,
    color: '#95A5A6',
    marginTop: 4,
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkButton: {
    padding: 8,
    marginLeft: 4,
  },
  deleteButton: {
    padding: 8,
  },
  checkIcon: {
    fontSize: 24,
  },
  deleteIcon: {
    fontSize: 20,
  },
});

export default ListItem;
