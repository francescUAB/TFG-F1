import React from 'react';
import { View, Image, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function StartScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Image
        source={require('./images/f1-logo.png')} 
        style={styles.logo}
        alt="logo"
      />
      <TouchableOpacity style={styles.button}  onPress={() => navigation.navigate('SelectionPrediction')}>
        <Text style={styles.buttonText}>Start</Text>
      </TouchableOpacity> 
      <View style={styles.footer}>
        <Text style={styles.footerText}>An application designed by Francesc Gallego</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  logo: {
    width: 300,
    height: 300,
    resizeMode: 'contain',
  },
  button: {
    marginTop: 20,
    padding: 10,
    backgroundColor: '#FF0000',
    borderRadius: 5,

    width: 200,
    height: 50,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign:'center',
  },
  footer: {
    marginTop: 50,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: '#888',
  },
});
