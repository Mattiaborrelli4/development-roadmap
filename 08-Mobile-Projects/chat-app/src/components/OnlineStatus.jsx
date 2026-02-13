import React from 'react';
import { View, StyleSheet } from 'react-native';
import { colors, borderRadius } from '../styles/theme';

const OnlineStatus = ({ status, size = 14 }) => {
  const getStatusColor = () => {
    switch (status) {
      case 'online':
        return colors.statusOnline;
      case 'away':
        return colors.statusAway;
      case 'offline':
      default:
        return colors.statusOffline;
    }
  };

  const styles = StyleSheet.create({
    indicator: {
      position: 'absolute',
      bottom: 0,
      right: 0,
      width: size,
      height: size,
      borderRadius: borderRadius.round,
      backgroundColor: getStatusColor(),
      borderWidth: 2,
      borderColor: '#FFFFFF'
    }
  });

  return <View style={styles.indicator} />;
};

export default OnlineStatus;
