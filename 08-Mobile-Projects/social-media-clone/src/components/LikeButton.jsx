import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withSequence,
  withTiming,
} from 'react-native-reanimated';
import { THEME } from '../../utils/constants';

const AnimatedHeart = Animated.createAnimatedComponent(Text);

const LikeButton = ({ liked, onToggle, size = 24 }) => {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scale: scale.value }],
    };
  });

  const handlePress = () => {
    if (!liked) {
      scale.value = withSequence(
        withTiming(0.5, { duration: 100 }),
        withSpring(1.3, { damping: 3 }),
        withSpring(1, { damping: 3 })
      );
    }
    onToggle();
  };

  return (
    <TouchableOpacity
      onPress={handlePress}
      activeOpacity={0.7}
      hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
    >
      <Animated.View style={animatedStyle}>
        <Text style={[styles.heart, { fontSize: size }]}>
          {liked ? '❤️' : '🤍'}
        </Text>
      </Animated.View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  heart: {
    color: THEME.colors.text,
  },
});

export default LikeButton;
