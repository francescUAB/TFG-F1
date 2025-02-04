import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const SelectionPrediction = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Select Prediction</Text>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Prediction')}>
                <Text style={styles.buttonText}>Prediction position group by 1</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('')}>
                <Text style={styles.buttonText}>Prediction position group by 2</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('')}>
                <Text style={styles.buttonText}>Prediction position group by 4</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={() =>navigation.navigate('Start')}>
                <Text style={styles.buttonText}>Start Page</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    text: {
        fontSize: 20,
        color: '#000',
        marginBottom: 20, 
    },
    button: {
        marginTop: 10,
        padding: 10,
        backgroundColor: 'red',
        borderRadius: 5,
        alignItems: 'center',
        width: 200, 
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
    },
});

export default SelectionPrediction;