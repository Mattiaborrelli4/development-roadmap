import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { chatStyles } from '../styles/theme';

const TypingIndicator = ({ users }) => {
  if (!users || users.length === 0) return null;

  const getTypingText = () => {
    if (users.length === 1) {
      return `${users[0].username} sta scrivendo...`;
    } else if (users.length === 2) {
      return `${users[0].username} e ${users[1].username} stanno scrivendo...`;
    } else {
      return `${users.length} persone stanno scrivendo...`;
    }
  };

  return (
    <View style={chatStyles.typingContainer}>
      <View style={chatStyles.typingBubble}>
        <Text style={chatStyles.typingText}>{getTypingText()}</Text>
        <View style={chatStyles.typingDots}>
          <AnimatedDot />
          <AnimatedDot delay={200} />
          <AnimatedDot delay={400} />
        </View>
      </View>
    </View>
  );
};

const AnimatedDot = ({ delay = 0 }) => {
  const opacityAnim = React.useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(opacityAnim, {
          toValue: 1,
          duration: 800,
          delay,
          useNativeDriver: true
        }),
        Animated.timing(opacityAnim, {
          toValue: 0.3,
          duration: 800,
          useNativeDriver: true
        })
      ])
    );

    animation.start();

    return () => animation.stop();
  }, []);

  return (
    <Animated.View
      style={[
        chatStyles.dot,
        { opacity: opacityAnim }
      ]}
    />
  );
};

export default TypingIndicator;
