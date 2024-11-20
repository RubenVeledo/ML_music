![encabezado](https://github.com/user-attachments/assets/a48c7ed6-481d-42c8-95ef-064d43758ca8)

<h1 align="center">🎶 Ecos del pasado: estrategias de clasificación musical para aumentar el engagement de usuarios en Spotify 🎵</h1>

<br><br>

## 📋 Descripción del proyecto 📋


Este proyecto combina la música con el Machine Learning para abordar un reto interesante: clasificar canciones modernas según su esencia en décadas pasadas. Utilizando avanzadas técnicas de Machine Learning y un exhaustivo análisis de datos, hemos desarrollado un modelo que analiza características musicales como la energía, el tempo y el valence, entre otras, y determina en qué época se podría clasificar una canción actual.

El proyecto tiene aplicaciones tanto recreativas como profesionales. Desde crear playlists nostálgicas que conecten generaciones, hasta servir como una herramienta útil para DJs y curadores de música interesados en explorar la evolución de los estilos musicales. Además, este enfoque también abre la posibilidad de redescubrir cómo podrían resonar las canciones actuales en un contexto histórico.

Con una interfaz interactiva desarrollada en Streamlit, cualquier usuario puede experimentar con el modelo, ingresando datos de canciones modernas y explorando su clasificador para descubrir a qué época musical pertenecerían.

<br><br>

## 🧩 Características principales 🧩


- **Modelo de Machine Learning:** Clasifica canciones por época basándose en características musicales como energía, tempo, valence o danceability, entre otras.
- **Interfaz interactiva:** Aplicación construida con Streamlit para explorar y clasificar canciones de forma sencilla.
- **Dataset amplio:** Más de 160.000 canciones de múltiples décadas y géneros.
- **Técnicas de Machine Learning avanzadas:** Incluye modelos supervisados, y preprocesados con modelos no supervisados como clustering y selección de características.


<p align="center">
  <img src="https://github.com/user-attachments/assets/b6a1d85b-29f1-4b77-b7c5-3900deb25fa3" alt="streamlit" width="600">
</p>


<br><br>

## 📦 Estructura del repositorio 📦


📁-- Ecos_del_pasado
   - 📁-- app_streamlit
   - 📁-- data
   - 📁-- docs
   - 📁-- img
   - 📁-- models
   - 📁-- notebooks
     - 📁-- drafts
   - 📁-- src
   - 📃-- README.md

<br><br>

## ⚙️ Enfoque técnico ⚙️


**Descripción:** Datos de canciones desde 1921 hasta 2020, ampliado con canciones actuales mediante extracción de más de 300 canciones desde 2020 hasta la actualidad a través de la API de Spotify.

**Preprocesamiento:** EDA y feature engineering.

**Algoritmos utilizados:** 
- Modelos supervisados: Decision Trees, Random Forest, XGBoost, SVM y KNN.
- Modelos no supervisados (preprocesamiento): PCA, Kmeans.

**Enfoque final:** El modelo seleccionado para la integración en la app es un XGBoost con 8 variables. Este modelo ha sido hiperparametrizado para asegurar que generalice bien a datos nuevos.

<br><br>

## 📊 Resultados 📊


 **Reporte de Clasificación para datos no vistos**

| Clase  | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| 0      | 0.84      | 0.91   | 0.87     | 7990    |
| 1      | 0.90      | 0.87   | 0.88     | 8000    |
| 2      | 0.93      | 0.88   | 0.90     | 8000    |

**Accuracy:** 0.89  
**Macro Avg:**  
- Precision: 0.89  
- Recall: 0.89  
- F1-Score: 0.89  

**Weighted Avg:**  
- Precision: 0.89  
- Recall: 0.89  
- F1-Score: 0.89  

**Total Support:** 23990

<br><br>


<p align="center">
  <img src="https://github.com/user-attachments/assets/74567f0b-bc92-4172-a3ed-0964a55c909c" alt="tablaejemplo" width="900">
</p>

<br><br>

## 🛠️ Construido con 🛠️


[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/Numpy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-003b57?style=flat-square&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-9A1B30?style=flat-square&logo=seaborn&logoColor=white)](https://seaborn.pydata.org/)
[![Sklearn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white)](https://keras.io/)

<br><br>

## ✒️ Créditos ✒️

**Autor:** Rubén Veledo

**Dataset:** Spotify Songs (1921-2020), ampliado con datos actuales de extracción propia.

**Inspiración:** La nostalgia.
