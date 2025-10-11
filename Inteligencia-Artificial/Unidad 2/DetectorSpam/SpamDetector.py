
import pandas as pd 
import re
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


MODEL='data/spam_model.pkl'
VECTORIZER='data/spam_vectorizer.pkl'
ACCURACY='model/precision.txt'


def load_model():
    if os.path.exists(MODEL) and os.path.exists(VECTORIZER):
        print('Loading model and vectorizer')
        return joblib.load(MODEL), joblib.load(VECTORIZER)
    return None, None

# 1. Cargar el dataset
file_path = "data/spam_assassin.csv"
df = pd.read_csv(file_path)

# 2. Función para limpiar el texto
def limpiar_texto(texto):
    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = re.sub(r'\d+', '', texto)
    return texto

def train_model():
    # Aplicar limpieza al texto
    df["text"] = df["text"].astype(str).apply(limpiar_texto)
    
    # 3. Convertir el texto en vectores numéricos
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["text"])
    y = df["target"]  # Etiquetas (1: spam, 0: no spam)

    # 4. Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Entrenar el modelo Naïve Bayes
    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)

    # 6. Evaluar el modelo
    y_pred = modelo.predict(X_test)
    precision = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo: {precision * 100:.2f}%")
    
    return modelo, vectorizer

# Cargar el modelo y el vectorizador si existen, de lo contrario, entrenar uno nuevo
model, vectorizer = load_model()
if model is None or vectorizer is None:
    model, vectorizer = train_model()

# 7. Probar el modelo con un mensaje nuevo
mensaje_prueba = ["Reminder: Your car service is scheduled for tomorrow at 10 AM."]

# 8. Limpiar el mensaje de prueba y predicir
mensaje_vectorizado = vectorizer.transform(mensaje_prueba)
prediccion = model.predict(mensaje_vectorizado)

# 9. Mostrar el resultado
if prediccion[0] == 1:
    print("El mensaje es SPAM")
else:
    print("El mensaje NO es spam")