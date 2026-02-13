import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {GestureHandlerRootView} from 'react-native-gesture-handler';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import ListsScreen from './src/screens/ListsScreen';
import ListDetailScreen from './src/screens/ListDetailScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import {createTheme} from './src/styles/theme';

const Stack = createStackNavigator();

export default function App() {
  const theme = createTheme(false);

  return (
    <GestureHandlerRootView style={{flex: 1}}>
      <SafeAreaProvider>
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Lists"
            screenOptions={{
              headerShown: false,
              cardStyle: {backgroundColor: '#FFFFFF'},
              cardStyleInterpolator: ({current, layouts}) => {
                return {
                  cardStyle: {
                    transform: [
                      {
                        translateX: current.progress.interpolate({
                          inputRange: [0, 1],
                          outputRange: [layouts.screen.width, 0],
                        }),
                      },
                    ],
                  },
                };
              },
            }}>
            <Stack.Screen name="Lists" component={ListsScreen} />
            <Stack.Screen name="ListDetail" component={ListDetailScreen} />
            <Stack.Screen name="Settings" component={SettingsScreen} />
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
