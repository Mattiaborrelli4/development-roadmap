import React from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {CATEGORIES} from '../utils/constants';

const CategoryBadge = ({category, style}) => {
  const cat = CATEGORIES.find(c => c.name === category) || CATEGORIES[CATEGORIES.length - 1];

  return (
    <View
      style={[
        styles.container,
        {backgroundColor: cat.color},
        style,
      ]}>
      <Text style={styles.icon}>{cat.icon}</Text>
      <Text style={styles.text}>{cat.name}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    alignSelf: 'flex-start',
  },
  icon: {
    fontSize: 14,
    marginRight: 4,
  },
  text: {
    fontSize: 12,
    fontWeight: '600',
    color: '#FFFFFF',
  },
});

export default CategoryBadge;
