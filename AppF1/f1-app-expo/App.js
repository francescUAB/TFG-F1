import { StyleSheet, View } from 'react-native';
import StartScreen from './StartScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import MenuScreen from './MenuScreen';
import SelectionPrediction from './SelectionPrediction';



const Stack = createStackNavigator();
function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Start" component={StartScreen} />
        <Stack.Screen name="SelectionPrediction" component={SelectionPrediction} />
        <Stack.Screen name="Prediction" component={MenuScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
});