import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Image, Alert } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { Button } from 'react-native-elements';

const MenuScreen = () => {
  const [circuitos, setCircuitos] = useState([]);
  const [selectedCircuit, setSelectedCircuit] = useState('');
  const [years, setYears] = useState(
    Array.from({ length: 2024 - 1950 + 1 }, (_, i) => 1950 + i)
  );
  const [selectedSeason, setSelectedSeason] = useState('');
  const [filteredPilotos, setFilteredPilotos] = useState([]);
  const [selectedPiloto, setSelectedPiloto] = useState('');
  const [pilotoInfo, setPilotoInfo] = useState(null);
  const [predictedPosition, setPredictedPosition] = useState(null);
  const [selectedModel, setSelectedModel] = useState('Random Forest'); 

  const pilotoImages = {
    1: require('./images/1.png'),
    4: require('./images/4.png'),
    815: require('./images/815.png'),
    822: require('./images/822.png'),
    830: require('./images/830.png'),
    839: require('./images/839.png'),
    840: require('./images/840.png'),
    842: require('./images/842.png'),
    844: require('./images/844.png'),
    846: require('./images/846.png'),
    847: require('./images/847.png'),
    848: require('./images/848.png'),
    852: require('./images/852.png'),
    855: require('./images/855.png'),
    857: require('./images/857.png'),
    default: require('./images/4.png'),
};

  const getPilotoImage = (driverid) =>
    pilotoImages[driverid] || pilotoImages.default;

  const fetchCircuitos = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/circuits');
      const data = await response.json();
      setCircuitos(data || []);
    } catch (error) {
      console.error('Error al obtener circuitos:', error);
      setCircuitos([]);
    }
  };

  const fetchPilotos = async () => {
    if (!selectedCircuit || !selectedSeason) {
      setFilteredPilotos([]);
      return;
    }
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/pilots?circuit=${selectedCircuit}&season=${selectedSeason}`
      );
      const data = await response.json();
      if (!response.ok) {
        console.error('Error al filtrar pilotos:', data);
        setFilteredPilotos([]);
        return;
      }
      setFilteredPilotos(data || []);
    } catch (error) {
      console.error('Error al filtrar pilotos:', error);
      setFilteredPilotos([]);
    }
  };


  const fetchPilotoInfo = async () => {
    if (!selectedPiloto || !selectedCircuit || !selectedSeason) {
      setPilotoInfo(null);
      return;
    }
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/pilots?circuit=${selectedCircuit}&season=${selectedSeason}`
      );
      const data = await response.json();
      const pilotoData = data.find(
        (p) => String(p.driverid) === String(selectedPiloto)
      );
      setPilotoInfo(pilotoData || null);
    } catch (error) {
      console.error('Error al obtener información del piloto:', error);
      setPilotoInfo(null);
    }
  };

  const handlePrediction = async () => {
    if (!pilotoInfo) {
      Alert.alert('Error', 'Selecciona un piloto para predecir.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel,
          constructorid: pilotoInfo.constructorid,
          circuitid: selectedCircuit,
          grid: pilotoInfo.position,               
          experience: pilotoInfo.experience_scaled,  
          hability: pilotoInfo.habilidad,        
          constructor_experience: pilotoInfo.constructor_experience,
          constructor_fiability: pilotoInfo.constructor_fiability,
          constructor_performance: pilotoInfo.constructor_performance,
          gap_to_best_time: pilotoInfo.time_difference,
          age: pilotoInfo.age
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setPredictedPosition(data.predicted_position);
      } else {
        console.error('Error al predecir:', data);
        Alert.alert('Error', 'Error al predecir la posición.');
      }
    } catch (error) {
      console.error('Error al conectar con el modelo:', error);
      Alert.alert('Error', 'Error al conectar con el modelo.');
    }
  };

  useEffect(() => {
    setPredictedPosition(null);
  }, [selectedCircuit, selectedSeason, selectedPiloto, selectedModel]);

  useEffect(() => {
    fetchCircuitos();
  }, []);

  useEffect(() => {
    fetchPilotos();
  }, [selectedCircuit, selectedSeason]);

  useEffect(() => {
    fetchPilotoInfo();
  }, [selectedPiloto]);

  useEffect(() => {
    if (!filteredPilotos.some((p) => p.driverid === selectedPiloto)) {
      setSelectedPiloto('');
    }
  }, [filteredPilotos]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Select a circuit</Text>
      <Picker
        selectedValue={selectedCircuit}
        style={styles.picker}
        onValueChange={(itemValue) => setSelectedCircuit(itemValue || '')}
      >
        <Picker.Item label="Select a circuit" value="" />
        {circuitos.map((circuito) => (
          <Picker.Item
            key={circuito.circuitid}
            label={`${circuito.name} - ${circuito.location}`}
            value={circuito.circuitid}
          />
        ))}
      </Picker>

      <Text style={styles.title}>Select a season</Text>
      <Picker
        selectedValue={selectedSeason}
        style={styles.picker}
        onValueChange={(itemValue) => setSelectedSeason(itemValue || '')}
      >
        <Picker.Item label="Select a year" value="" />
        {years.map((year) => (
          <Picker.Item key={year} label={year.toString()} value={year} />
        ))}
      </Picker>

      <Text style={styles.title}>Select a driver</Text>
      <Picker
        selectedValue={selectedPiloto || ''}
        style={styles.picker}
        onValueChange={(itemValue) => {
          if (itemValue && itemValue !== selectedPiloto) {
            setSelectedPiloto(itemValue);
          }
        }}
      >
        <Picker.Item label="Select a driver" value="" />
        {filteredPilotos.map((piloto) => (
          <Picker.Item
            key={piloto.driverid}
            label={`${piloto.surname} (${piloto.constructorid})`}
            value={piloto.driverid}
          />
        ))}
      </Picker>

      {/* Nuevo selector para el modelo */}
      <Text style={styles.title}>Select a model</Text>
      <Picker
        selectedValue={selectedModel}
        style={styles.picker}
        onValueChange={(itemValue) => setSelectedModel(itemValue)}
      >
        <Picker.Item label="Random Forest" value="Random Forest" />
        <Picker.Item label="SVM" value="SVM" />
      </Picker>

      {pilotoInfo && (
        <Button
          title="Predict position"
          onPress={handlePrediction}
          buttonStyle={styles.button}
        />
      )}

      {pilotoInfo && predictedPosition !== null && (
        <View style={styles.resultContainer}>
          <Image
            source={getPilotoImage(pilotoInfo.driverid)}
            style={styles.pilotoImage}
          />
          <Text style={styles.prediction}>Predicted Position:</Text>
          <Text style={styles.predictedNumber}>{predictedPosition}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  picker: {
    height: 50,
    width: '80%',
    marginBottom: 20,
  },
  pilotoImage: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 10,
  },
  prediction: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  predictedNumber: {
    fontSize: 60,
    fontWeight: 'bold',
    color: '#ff0000',
  },
  resultContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'red',
    padding: 10,
    borderRadius: 5,
    width: 200,
  },
});

export default MenuScreen;
