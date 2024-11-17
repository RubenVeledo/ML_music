import streamlit as st
import pickle
import numpy as np
import json

#Modelo entrenado
with open('../models/finalmodel.pkl', 'rb') as file:
    best_model_xgb = pickle.load(file)

#Estadísticas para normalización de canciones actuales (2020s)
with open("current_decade_stats.json", "r") as file:
    current_decade_stats = json.load(file)

current_decade_mean = current_decade_stats["mean"]
current_decade_std = current_decade_stats["std"]

#Función para normalizar la variable popularity
def normalize_popularity_current(popularity):
    return (popularity - current_decade_mean) / current_decade_std

#Diccionario de mapeo para convertir el número de la predicción en décadas
decade_mapping = {
    0: '50s-60s',
    1: '70s-80s',
    2: '90s-00s'} 

st.title('¿A qué época podría pertenecer una canción actual?')
st.write('Explora qué canciones actuales tienen la esencia de décadas pasadas.')


#Widgets para entrada de datos del usuario
duration_ms = st.number_input('Duración (ms)', min_value=0, max_value=800000, value=210000)
acousticness = st.slider('Acousticness', 0.0, 1.0, 0.5)
danceability = st.slider('Danceability', 0.0, 1.0, 0.5)
energy = st.slider('Energy', 0.0, 1.0, 0.5)
instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, 0.0)
loudness = st.number_input('Loudness (dB)', min_value=-60.0, max_value=0.0, value=-5.0)
speechiness = st.slider('Speechiness', 0.0, 1.0, 0.05)
valence = st.slider('Valence', 0.0, 1.0, 0.5)
tempo = st.slider('Tempo (BPM)', 50.0, 300.0, 120.0, step=0.1)
popularity = st.slider('Popularity', 0, 100, 50)


#Array de entrada para el modelo
datos_entrada = np.array([[duration_ms, acousticness, danceability, energy, instrumentalness,
                           loudness, speechiness, valence, tempo, popularity]])

if st.button('Predecir'):
    probabilidades = best_model_xgb.predict_proba(datos_entrada)
    prediccion = best_model_xgb.predict(datos_entrada)
    decada_predicha = decade_mapping.get(prediccion[0], '50s-60s')
    
    st.write(f'La canción probablemente pertenece a la década: {decada_predicha}')
    st.write('Probabilidades:')
    for i, prob in enumerate(probabilidades[0]):
        st.write(f"{decade_mapping.get(i, 'Desconocida')}: {prob:.2%}")
