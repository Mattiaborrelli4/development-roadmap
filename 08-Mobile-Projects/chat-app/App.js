import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import ChatsListScreen from './src/screens/ChatsListScreen';
import ChatRoomScreen from './src/screens/ChatRoomScreen';
import UsersScreen from './src/screens/UsersScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import { colors } from './src/styles/theme';
import chatService from './src/services/chatService';

// Stack Navigator per Chat
const Stack = createNativeStackNavigator();
const ChatStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: colors.primary
      },
      headerTintColor: colors.white,
      headerTitleStyle: {
        fontWeight: 'bold'
      }
    }}
  >
    <Stack.Screen
      name="ChatsList"
      component={ChatsListScreen}
      options={{ title: 'Chat' }}
    />
    <Stack.Screen
      name="ChatRoom"
      component={ChatRoomScreen}
      options={({ route }) => ({
        title: route.params?.name || 'Chat'
      })}
    />
    <Stack.Screen
      name="Users"
      component={UsersScreen}
      options={{ title: 'Nuova Chat' }}
    />
  </Stack.Navigator>
);

// Bottom Tab Navigator
const Tab = createBottomTabNavigator();

export default function App() {
  useEffect(() => {
    // Inizializza il servizio chat
    chatService.initialize();

    return () => {
      // Cleanup on unmount
      chatService.cleanup();
    };
  }, []);

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <StatusBar style="light" />
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;

              if (route.name === 'ChatTab') {
                iconName = focused ? 'chatbubbles' : 'chatbubbles-outline';
              } else if (route.name === 'PeopleTab') {
                iconName = focused ? 'people' : 'people-outline';
              } else if (route.name === 'ProfileTab') {
                iconName = focused ? 'person' : 'person-outline';
              }

              return <Ionicons name={iconName} size={size} color={color} />;
            },
            tabBarActiveTintColor: colors.primary,
            tabBarInactiveTintColor: colors.textLight,
            tabBarStyle: {
              paddingBottom: 5,
              paddingTop: 5,
              height: 60
            },
            headerShown: false
          })}
        >
          <Tab.Screen
            name="ChatTab"
            component={ChatStack}
            options={{ tabBarLabel: 'Chat' }}
          />
          <Tab.Screen
            name="PeopleTab"
            component={UsersScreen}
            options={{ tabBarLabel: 'Persone' }}
          />
          <Tab.Screen
            name="ProfileTab"
            component={ProfileScreen}
            options={{ tabBarLabel: 'Profilo' }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}
