import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import TabNavigator from './src/navigation/TabNavigator';
import { DataProvider } from './src/hooks/usePosts';
import { AuthProvider } from './src/hooks/useAuth';
import { NotificationProvider } from './src/hooks/useNotifications';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <AuthProvider>
        <DataProvider>
          <NotificationProvider>
            <NavigationContainer>
              <TabNavigator />
              <StatusBar style="dark" />
            </NavigationContainer>
          </NotificationProvider>
        </DataProvider>
      </AuthProvider>
    </GestureHandlerRootView>
  );
}
