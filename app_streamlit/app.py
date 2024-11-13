import streamlit as st
import pickle
import numpy as np

#Cargar el modelo entrenado
with open('basicmodel2.pkl', 'rb') as file:
    model_2 = pickle.load(file)

#Diccionario de mapeo para convertir el número de la predicción en décadas
decade_mapping = {
    0: '50s-60s',
    1: '70s-80s',
    2: '90s-00s'
}

#Título de la app
st.title('Predicción de Década de Canciones')
st.write('Ingresa las características de una canción para predecir a qué década pertenece.')

#Widgets para entrada de datos del usuario
duration_ms = st.number_input('Duración (ms)', min_value=0, max_value=800000, value=210000)
acousticness = st.slider('Acousticness', 0.0, 1.0, 0.5)
danceability = st.slider('Danceability', 0.0, 1.0, 0.5)
energy = st.slider('Energy', 0.0, 1.0, 0.5)
instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, 0.0)
liveness = st.slider('Liveness', 0.0, 1.0, 0.3)
loudness = st.number_input('Loudness (dB)', min_value=-60.0, max_value=0.0, value=-5.0)
speechiness = st.slider('Speechiness', 0.0, 1.0, 0.05)
tempo = st.slider('Tempo (BPM)', 50.0, 300.0, 120.0, step=0.1)
valence = st.slider('Valence', 0.0, 1.0, 0.5)
mode = st.selectbox('Mode (Escala)', [0, 1], format_func=lambda x: 'Mayor' if x == 1 else 'Menor')
key = st.slider('Key (Nota musical)', 0, 11, 5) 
popularity = st.slider('Popularity', 0, 100, 50)

 


#Crear el array de entrada para el modelo
datos_entrada = np.array([[duration_ms, acousticness, danceability, energy, instrumentalness,
                           liveness, loudness, speechiness, tempo, valence, mode,
                           key, popularity]])

#Hacer la predicción y mostrar el resultado
if st.button('Predecir'):
    prediccion = model_2.predict(datos_entrada)
    st.write(f'La canción podría incluirse en la playlist: {prediccion[0]}')
    #decada_predicha = decade_mapping.get(prediccion[0], 'Desconocida')
    #st.write(f'La canción probablemente pertenece a la década: {decada_predicha}')





