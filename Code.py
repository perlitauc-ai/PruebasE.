import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# ---------------------------------------------------------
st.set_page_config(page_title="Cuestionario de Pruebas Estadísticas", layout="centered")

# ---------------------------------------------------------
# FUNCIÓN: Cargar ítems desde GitHub RAW
# ---------------------------------------------------------
@st.cache_data
def cargar_items(url):
    try:
        contenido = requests.get(url).text
        df = pd.read_csv(StringIO(contenido))
        return df
    except Exception as e:
        st.error(f"Error cargando los datos: {e}")
        return None

# ---------------------------------------------------------
# URL del archivo CSV en GitHub (RAW)
# ⚠️ REEMPLAZA ESTE LINK POR EL TUYO
# ---------------------------------------------------------
URL_GITHUB_RAW = "https://raw.githubusercontent.com/usuario/repositorio/rama/items.csv"

items = cargar_items(URL_GITHUB_RAW)

if items is None:
    st.stop()

# ---------------------------------------------------------
# Inicializar estados
# ---------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "correctas" not in st.session_state:
    st.session_state.correctas = 0

# ---------------------------------------------------------
# Mostrar progreso
# ---------------------------------------------------------
st.title("📊 Cuestionario para elegir una prueba estadística")
st.progress(st.session_state.indice / len(items))

# ---------------------------------------------------------
# Si ya terminó
# ---------------------------------------------------------
if st.session_state.indice >= len(items):
    st.success("🎉 ¡Has terminado todas las preguntas!")
    st.write(f"**Respuestas correctas: {st.session_state.correctas} de {len(items)}**")
    st.stop()

# ---------------------------------------------------------
# Mostrar ítem actual
# ---------------------------------------------------------
fila = items.iloc[st.session_state.indice]

pregunta = fila["pregunta"]
op1 = fila["opcion1"]
op2 = fila["opcion2"]
op3 = fila["opcion3"]
correcta = fila["correcta"]  # texto EXACTO de la opción correcta

st.subheader(f"Pregunta {st.session_state.indice + 1}")
st.write(pregunta)

respuesta = st.radio("Selecciona tu respuesta:", [op1, op2, op3])

# ---------------------------------------------------------
# Botón para enviar respuesta
# ---------------------------------------------------------
if st.button("Enviar respuesta"):
    if respuesta == correcta:
        st.success("✅ ¡Correcto!")
        st.session_state.correctas += 1
        st.session_state.indice += 1
    else:
        st.error("❌ Incorrecto. Intenta de nuevo.")

    st.rerun()

