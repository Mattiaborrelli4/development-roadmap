import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Text } from 'react-native';

import DashboardScreen from './src/screens/DashboardScreen';
import WorkoutsScreen from './src/screens/WorkoutsScreen';
import ProgressScreen from './src/screens/ProgressScreen';
import GoalsScreen from './src/screens/GoalsScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { theme } from './src/styles/theme';

const Tab = createBottomTabNavigator();

const screenOptions = {
  headerShown: false,
  tabBarActiveTintColor: theme.colors.primary,
  tabBarInactiveTintColor: theme.colors.textSecondary,
  tabBarStyle: {
    backgroundColor: theme.colors.surface,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
    height: 60,
    paddingBottom: 8,
    paddingTop: 8,
  },
  tabBarLabelStyle: {
    fontSize: 12,
    fontWeight: '600',
  },
};

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar style="auto" />
        <Tab.Navigator screenOptions={screenOptions}>
          <Tab.Screen
            name="Dashboard"
            component={DashboardScreen}
            options={{
              tabBarLabel: 'Dashboard',
              tabBarIcon: ({ color }) => <TabIcon name="📊" color={color} />,
            }}
          />
          <Tab.Screen
            name="Workouts"
            component={WorkoutsScreen}
            options={{
              tabBarLabel: 'Allenamenti',
              tabBarIcon: ({ color }) => <TabIcon name="💪" color={color} />,
            }}
          />
          <Tab.Screen
            name="Progress"
            component={ProgressScreen}
            options={{
              tabBarLabel: 'Progressi',
              tabBarIcon: ({ color }) => <TabIcon name="📈" color={color} />,
            }}
          />
          <Tab.Screen
            name="Goals"
            component={GoalsScreen}
            options={{
              tabBarLabel: 'Obiettivi',
              tabBarIcon: ({ color }) => <TabIcon name="🎯" color={color} />,
            }}
          />
          <Tab.Screen
            name="Settings"
            component={SettingsScreen}
            options={{
              tabBarLabel: 'Impostazioni',
              tabBarIcon: ({ color }) => <TabIcon name="⚙️" color={color} />,
            }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

const TabIcon = ({ name, color }) => {
  return <Text style={{ fontSize: 24 }}>{name}</Text>;
};
