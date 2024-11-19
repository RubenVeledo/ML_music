import streamlit as st
import pickle
import numpy as np
import json
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# Modelo entrenado
with open('../models/finalmodel.pkl', 'rb') as file:
    best_model_xgb = pickle.load(file)

# Normalización de canciones actuales (2020s)
with open("current_decade_stats.json", "r") as file:
    current_decade_stats = json.load(file)

current_decade_mean = current_decade_stats["mean"]
current_decade_std = current_decade_stats["std"]

# Función para normalizar la variable popularity
def normalize_popularity_current(popularity):
    return (popularity - current_decade_mean) / current_decade_std

# Función para convertir el DataFrame a CSV
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Función para limpiar el texto del PDF
def clean_text(text):
    if isinstance(text, str):
        return text.encode('latin-1', 'ignore').decode('latin-1')
    return text

# Función para crear un informe PDF
def generar_informe_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Informe de Predicciones", ln=True, align="C")
    pdf.ln(10)

    # Agregar contenido al PDF
    pdf.set_font("Arial", size=12)
    for index, row in data.iterrows():
        pdf.cell(0, 10, txt=f"Canción: {clean_text(row['name'])}", ln=True)
        pdf.cell(0, 10, txt=f"Artista: {clean_text(row['artists'])}", ln=True)
        pdf.cell(0, 10, txt=f"Época Predicha: {clean_text(row['Época'])}", ln=True)
        pdf.cell(0, 10, txt=f"Probabilidades: 50s-60s={row['prob_50s_60s']:.2%}, "
                            f"70s-80s={row['prob_70s_80s']:.2%}, "
                            f"90s-00s={row['prob_90s_00s']:.2%}", ln=True)
        pdf.ln(10)
    
    # Guardar el PDF en memoria
    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

# Diccionario de mapeo para convertir el número de la predicción en décadas
decade_mapping = {
    0: '50s-60s',
    1: '70s-80s',
    2: '90s-00s'} 

# Título y descripción de la app
st.title('¿A qué época podría pertenecer una canción actual?')
st.write('Explora qué canciones actuales tienen la esencia de décadas pasadas.')

# Pestañas
tab1, tab2 = st.tabs(["Predicción individual", "Predicciones en lote"])

# **Tab 1: Predicción Individual**
with tab1:
    st.subheader("Predicción individual")
    # Widgets para entrada de datos del usuario
    duration_ms = st.number_input('Duración (ms)', min_value=0, max_value=800000, value=210000)
    acousticness = st.slider('Acousticness', 0.0, 1.0, 0.5)
    danceability = st.slider('Danceability', 0.0, 1.0, 0.5)
    energy = st.slider('Energy', 0.0, 1.0, 0.5)
    instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, 0.0)
    loudness = st.number_input('Loudness (dB)', min_value=-60.0, max_value=0.0, value=-5.0)
    valence = st.slider('Valence', 0.0, 1.0, 0.5)
    popularity = st.slider('Popularity', 0, 100, 50)

    #Normalización de popularity
    popularity_normalized = normalize_popularity_current(popularity)

    #Array de entrada para el modelo
    datos_entrada = np.array([[duration_ms, acousticness, danceability, energy, instrumentalness,
                               loudness, valence, popularity_normalized]])

    #Predicción
    if st.button('Predecir'):
        probabilidades = best_model_xgb.predict_proba(datos_entrada)
        prediccion = best_model_xgb.predict(datos_entrada)
        decada_predicha = decade_mapping[prediccion[0]]

        st.write(f'La canción podría incluirse en la playlist: {decada_predicha}')

        prob_values = probabilidades[0]
        prob_df = {
            'Época': [decade_mapping[i] for i in range(len(prob_values))],
            'Probabilidad': prob_values,
        }

        custom_colors = {
            '50s-60s': '#85C1E9',  
            '70s-80s': '#F1948A',  
            '90s-00s': '#82E0AA',}
        
        image_mapping = {
            '50s-60s': 'img/grease.jpg',  
            '70s-80s': 'img/locomia.jpg',  
            '90s-00s': 'img/spice.jpg'}

        # Gráfico de barras con épocas como etiquetas y texto personalizado
        fig = px.bar(prob_df, x='Época', y='Probabilidad', 
                    title='Probabilidades por época',
                    labels={'Probabilidad': 'Probabilidad', 'Época': 'Época'},
                    text='Probabilidad',
                    color='Época',  # Colorear las barras según la época
                    color_discrete_map=custom_colors) 

        #Texto en las barras estático e interactivo
        fig.update_traces(
            texttemplate='Probabilidad: %{y:.2%}', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Probabilidad: %{y:.2%}<extra></extra>'
        )
        
        #Ajustar formato del eje Y
        fig.update_layout(yaxis=dict(tickformat=".0%"))

        st.plotly_chart(fig)

         # Mostrar imagen correspondiente a la década
        image_path = image_mapping.get(decada_predicha, None)
        if image_path:
            st.image(image_path, caption=f"Época: {decada_predicha}", use_container_width=True)
        else:
            st.write("No hay imagen disponible para esta época.")

# **Tab 2: Predicciones en lote**
with tab2:
    st.subheader("Predicciones en lote")
    # Subida de archivo CSV
    uploaded_file = st.file_uploader("Sube un archivo CSV con canciones", type=["csv"])

    if uploaded_file is not None:
        # Leer el archivo cargado
        data = pd.read_csv(uploaded_file)

        # Verificar si las columnas necesarias están en el archivo
        required_columns = ['name', 'artists', 'duration_ms', 'acousticness', 'danceability', 
                            'energy', 'instrumentalness', 'loudness', 'valence', 'popularity']
        
        if not all(col in data.columns for col in required_columns):
            st.error(f"El archivo debe contener las siguientes columnas: {', '.join(required_columns)}")
        else:
            # Normalizar la popularidad
            data['popularity_normalized'] = data['popularity'].apply(normalize_popularity_current)

            # Crear el array de entrada para el modelo
            features = ['duration_ms', 'acousticness', 'danceability', 'energy', 
                        'instrumentalness', 'loudness', 'valence', 'popularity_normalized']
            X = data[features].values

            # Realizar predicciones
            data['Predicción'] = best_model_xgb.predict(X)
            data['Época'] = data['Predicción'].map(decade_mapping)

            # Obtener las probabilidades de cada década
            probabilidades = best_model_xgb.predict_proba(X)
            data['prob_50s_60s'] = probabilidades[:, 0]
            data['prob_70s_80s'] = probabilidades[:, 1]
            data['prob_90s_00s'] = probabilidades[:, 2]

            # Seleccionar columnas para visualización
            output_columns = ['name', 'artists', 'Época', 'prob_50s_60s', 
                              'prob_70s_80s', 'prob_90s_00s'] + features

            # Función para aplicar estilos a las filas
            def highlight_high_probabilities(row):
                if row['prob_50s_60s'] > 0.75 or row['prob_70s_80s'] > 0.75 or row['prob_90s_00s'] > 0.75:
                    return ['background-color: #dafbe1'] * len(row)
                return [''] * len(row)

            styled_data = data[output_columns].style.apply(highlight_high_probabilities, axis=1)

            st.write("Resultados de las predicciones:")
            st.dataframe(styled_data, use_container_width=True)

            # Botón para generar CSV
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(data[output_columns])

            st.download_button(
                label="Descargar predicciones en CSV",
                data=csv,
                file_name='predicciones_canciones.csv',
                mime='text/csv',
            )

            # Botón para generar PDF
            if st.button("Generar Informe en PDF"):
                pdf_data = generar_informe_pdf(data[output_columns])
                st.download_button(
                    label="Descargar Informe en PDF",
                    data=pdf_data,
                    file_name="informe_predicciones.pdf",
                    mime="application/pdf",
                )

