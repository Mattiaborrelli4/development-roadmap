import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import GalleryScreen from './src/screens/GalleryScreen';
import AlbumDetailScreen from './src/screens/AlbumDetailScreen';
import CameraScreen from './src/screens/CameraScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { Colors } from './src/styles/theme';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <StatusBar style="auto" />
        <Stack.Navigator
          initialRouteName="Gallery"
          screenOptions={{
            headerStyle: {
              backgroundColor: Colors.background,
            },
            headerTintColor: Colors.text,
            headerTitleStyle: {
              fontWeight: '600',
              fontSize: 20,
            },
            headerShadowVisible: false,
          }}
        >
          <Stack.Screen
            name="Gallery"
            component={GalleryScreen}
            options={{
              title: 'Photo Gallery',
              headerRight: () => null,
            }}
          />
          <Stack.Screen
            name="AlbumDetail"
            component={AlbumDetailScreen}
            options={{
              title: 'Album',
            }}
          />
          <Stack.Screen
            name="Camera"
            component={CameraScreen}
            options={{
              headerShown: false,
              orientation: 'portrait',
              animation: 'fade',
            }}
          />
          <Stack.Screen
            name="Settings"
            component={SettingsScreen}
            options={{
              title: 'Impostazioni',
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}
