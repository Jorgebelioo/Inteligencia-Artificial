import streamlit as st
import requests
import os

# Función para normalizar nombres de archivo (sin acentos)
def normalize_name(name):
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    name = name.lower().replace(" ", "_")
    for src, target in replacements.items():
        name = name.replace(src, target)
    return name

# Carpeta donde están las imágenes
image_folder = "ui/images"

st.title("Recomendador de Menú - Demo")

is_vegan = st.checkbox("Cliente vegano", value=False)
allergic_nuts = st.checkbox("Alergia a nueces", value=False)
ingredients_available = st.checkbox("Ingredientes del plato disponibles", value=True)
likes_spicy = st.checkbox("Le gusta picante", value=False)

if st.button("Obtener recomendación"):
    payload = {
        "IsVeganCustomer": int(is_vegan),
        "AllergicToNuts": int(allergic_nuts),
        "IngredientsAvailable": int(ingredients_available),
        "LikesSpicy": int(likes_spicy)
    }

    resp = requests.post("http://localhost:8000/recommend", json=payload)

    try:
        data = resp.json()
        st.subheader("Distribución de recomendación:")
        st.write(data["recommend_distribution"])

        # Plato más probable
        best_dish = max(data["recommend_distribution"], key=data["recommend_distribution"].get)
        st.success(f"🍴 Plato recomendado: **{best_dish}**")

        # Filtramos solo los platos con imagen existente
        platos_con_imagen = []
        for plato, prob in data["recommend_distribution"].items():
            filename = normalize_name(plato) + ".jpg"
            image_path = os.path.join(image_folder, filename)
            if os.path.exists(image_path):
                platos_con_imagen.append((plato, prob, image_path))

        # Mostrar imágenes en grid (3 por fila)
        n_cols = 3
        for i in range(0, len(platos_con_imagen), n_cols):
            cols = st.columns(n_cols)
            for j, (plato, prob, image_path) in enumerate(platos_con_imagen[i:i+n_cols]):
                with cols[j]:
                    st.image(image_path, caption=f"{plato} ({prob*100:.1f}%)", use_container_width=True)

    except Exception as e:
        st.error(f"Error al decodificar JSON: {e}")
        st.write("Respuesta cruda:", resp.text)
