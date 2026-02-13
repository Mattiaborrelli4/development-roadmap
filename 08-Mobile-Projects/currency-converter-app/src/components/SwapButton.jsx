import React from 'react';
import { View, TouchableOpacity, Animated } from 'react-native';
import { COLORS, SPACING } from '../styles/theme';

const SwapButton = ({ onPress }) => {
  const rotateAnim = React.useRef(new Animated.Value(0)).current;

  const handlePress = () => {
    // Animazione di rotazione
    Animated.sequence([
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.timing(rotateAnim, {
        toValue: 0,
        duration: 0,
        useNativeDriver: true,
      }),
    ]).start();

    onPress();
  };

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '180deg'],
  });

  return (
    <View style={{ alignItems: 'center', marginVertical: SPACING.xs }}>
      <Animated.View style={{ transform: [{ rotate }] }}>
        <TouchableOpacity
          onPress={handlePress}
          style={{
            backgroundColor: COLORS.primary,
            width: 50,
            height: 50,
            borderRadius: 25,
            justifyContent: 'center',
            alignItems: 'center',
            elevation: 4,
            shadowColor: COLORS.shadow,
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.3,
            shadowRadius: 4,
          }}
          activeOpacity={0.8}
        >
          <View
            style={{
              width: 24,
              height: 24,
              borderTopWidth: 3,
              borderRightWidth: 3,
              borderColor: COLORS.surface,
              transform: [{ rotate: '-45deg' }],
              marginTop: -4,
            }}
          />
          <View
            style={{
              width: 24,
              height: 24,
              borderTopWidth: 3,
              borderRightWidth: 3,
              borderColor: COLORS.surface,
              transform: [{ rotate: '135deg' }],
              marginTop: -20,
            }}
          />
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
};

export default SwapButton;
