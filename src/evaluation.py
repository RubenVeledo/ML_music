# Librerias
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


# Cargar datos de test
df_test = pd.read_csv("../data/test/test.csv")


# Cargar modelo XGBoost entrenado
with open('../models/finalmodel.pkl', 'rb') as file:
    best_model_xgb = pickle.load(file)


# Evaluación en test
X_xgb_nuevo = df_test[['duration_ms', 'acousticness', 'danceability', 'energy', 'instrumentalness',
          'loudness', 'speechiness', 'valence', 'tempo', 'popularity_normalized']]
y_xgb_nuevo = df_test['decade_label']

y_nuevos_pred_xgb = best_model_xgb.predict(X_xgb_nuevo)

accuracy_xgb_nuevo = accuracy_score(y_xgb_nuevo, y_nuevos_pred_xgb)
precision_xgb_nuevo = precision_score(y_xgb_nuevo, y_nuevos_pred_xgb, average='macro')
recall_xgb_nuevo = recall_score(y_xgb_nuevo, y_nuevos_pred_xgb, average='macro')
f1_xgb_nuevo = f1_score(y_xgb_nuevo, y_nuevos_pred_xgb, average='macro')
conf_matrix_xgb = confusion_matrix(y_xgb_nuevo, y_nuevos_pred_xgb)

print("Rendimiento en datos no vistos:")
print("Accuracy:", accuracy_xgb_nuevo)
print("Precision:", precision_xgb_nuevo)
print("Recall:", recall_xgb_nuevo)
print("F1-Score:", f1_xgb_nuevo)
print("----------------")
print("\nReporte de clasificación:")
print(classification_report(y_xgb_nuevo, y_nuevos_pred_xgb))
print("----------------")
print("\nMatriz de confusión:")
print(conf_matrix_xgb)
