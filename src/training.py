# Librerias
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier


# Lectura de archivo procesado
df_processed = pd.read_csv("../data/processed/processed.csv")

# División y guardado train/test data processed
train, test = train_test_split(df_processed, test_size=0.2, random_state=42, stratify=df['decade_label'])
train.to_csv("train.csv", index=False) 
test.to_csv("test.csv", index=False) 

# DataFrame de train
df = pd.read_csv("../data/train/train.csv")

#Entrenamiento XGBoost hiperparametrizado
X_xgb = df[['duration_ms', 'acousticness', 'danceability', 'energy', 'instrumentalness',
          'loudness', 'speechiness', 'valence', 'tempo', 'popularity_normalized']]
y_xgb = df['decade_label']

X_train, X_test, y_train, y_test = train_test_split(X_xgb, y_xgb, test_size=0.2, random_state=42)

param_grid = {
    'reg_alpha': [0, 0.1, 1, 10],
    'reg_lambda': [1, 10, 100],
    'max_depth': [3, 5],
    'learning_rate': [0.05, 0.1],
    'n_estimators': [50, 100]}

model_xgb_2 = XGBClassifier(random_state=42)

grid_search_xgb = GridSearchCV(estimator=model_xgb_2, param_grid=param_grid, scoring='accuracy', cv=3)
grid_search_xgb.fit(X_train, y_train)
print("Mejores hiperparámetros:", grid_search_xgb.best_params_)
