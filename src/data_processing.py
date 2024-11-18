# Librerias
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Lectura de archivo
df = pd.read_csv("../data/raw/dataset.csv")


# Extracción de target, no está implícita en el dataset
df['decade'] = (df['year'] // 10) * 10


# Frequent Label Encoding (artist)
artist_counts = df['artists'].value_counts()
df['artists_frequency'] = df['artists'].map(artist_counts)


# Clasificar canciones en función de diferentes versiones
def asignar_version(nombre):
    if 'remix' in nombre.lower():
        return 'Remix'
    elif 'remastered' in nombre.lower():
        return 'Remaster'
    elif 'live' in nombre.lower():
        return 'Live'
    else:
        return 'Original'

df['version_type'] = df['name'].apply(asignar_version)

df['base_name'] = df['name'].str.replace(r'(?i)(remix|remastered|live)', '', regex=True).str.strip()
versiones_diferentes = df[df.duplicated(subset='base_name', keep=False)]


# Variables para dummis sobre 'version_type'
dummies = pd.get_dummies(df['version_type'], prefix='version', dtype=int)
df = pd.concat([df, dummies], axis=1)


# Variables para label encoding sobre 'version_type'
le = LabelEncoder()
df['version_type_encoded'] = le.fit_transform(df['version_type'])


# Variable target al final
decade_col = df['decade']
df = df.drop(columns=['decade'])
df['decade'] = decade_col


# Filtrado por canciones entre las décadas de 1950 y 2010 (ésta última no incluida)
df = df[(df['decade'] >= 1950) & (df['decade'] < 2010)]


# Agrupación de variable target en rangos más amplios
def asignar_rango_decada(decade):
    if 1950 <= decade <= 1969:
        return '50s-60s'
    elif 1970 <= decade <= 1989:
        return '70s-80s'
    elif 1990 <= decade <= 2009:
        return '90s-00s' 
    
df['decade_range'] = df['decade'].apply(asignar_rango_decada)


# Creación de nuevas variables a partir de las existentes
df['energy_danceability_valence'] = df['energy'] * df['danceability'] * df['valence']
df['acoustic_intensity'] = df['acousticness'] * df['loudness']
df['popularity_energy_ratio'] = df['popularity'] / (df['energy'] + 1e-5)
df['valence_energy_dif'] = df['valence'] - df['energy']


#Transformación de la variable target a numérica
decade_mapping = {}
for idx, decade in enumerate(sorted(df['decade_range'].unique())):
    decade_mapping[decade] = idx
df['decade_label'] = df['decade_range'].map(decade_mapping)


# Normalización de la variable popularity en función de la popularidad de su época
df['popularity_normalized'] = (df['popularity'] - df.groupby('decade_label')['popularity'].transform('mean')) / df.groupby('decade_label')['popularity'].transform('std')


# Guardar dataframe processed
df.to_csv("processed.csv") 