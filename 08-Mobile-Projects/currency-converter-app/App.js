import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaView } from 'react-native';
import ConverterScreen from './src/screens/ConverterScreen';

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ConverterScreen />
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}
