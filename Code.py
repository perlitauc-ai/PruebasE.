import streamlit as st
import pandas as pd
import requests
from io import StringIO

# -----------------------------------------------
# CONFIGURACIÓN
# -----------------------------------------------
st.set_page_config(page_title="Cuestionario de Pruebas Estadísticas", layout="centered")

# -----------------------------------------------
# FUNCIÓN PARA CARGAR ÍTEMS DESDE GITHUB RAW
# -----------------------------------------------
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
# ⚠️ REEMPLAZA ESTE LINK POR TU ENLACE RAW DE GITHUB
# ---------------------------------------------------------
URL_GITHUB_RAW = "https://raw.githubusercontent.com/usuario/repositorio/rama/items.csv"

items = cargar_items(URL_GITHUB_RAW)

# -----------------------------------------------
# VALIDACIÓN DE CARGA
# -----------------------------------------------
if items is None:
    st.stop()

if len(items) == 0:
    st.error("El archivo CSV está vacío. Agrega ítems antes de continuar.")
    st.stop()

# -----------------------------------------------
# INICIALIZAR VARIABLES DE SESIÓN
# -----------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "correctas" not in st.session_state:
    st.session_state.correctas = 0

total_preguntas = len(items)

# -----------------------------------------------
# TÍTULO
# -----------------------------------------------
st.title("📊 Cuestionario para elegir una prueba estadística")

# -----------------------------------------------
# PROGRESO (protect against zero division)
# -----------------------------------------------
progreso = st.session_state.indice / total_preguntas
st.progress(progreso)

# -----------------------------------------------
# FIN DEL CUESTIONARIO
# -----------------------------------------------
if st.session_state.indice >= total_preguntas:
    st.success("🎉 ¡Has terminado todas las preguntas!")
    st.write(f"**Respuestas correctas: {st.session_state.correctas} de {total_preguntas}**")
    st.stop()

# -----------------------------------------------
# MOSTRAR PREGUNTA ACTUAL
# -----------------------------------------------
fila = items.iloc[st.session_state.indice]

pregunta = fila["pregunta"]
opciones = [fila["opcion1"], fila["opcion2"], fila["opcion3"]]
correcta = fila["correcta"]

st.subheader(f"Pregunta {st.session_state.indice + 1}")
st.write(pregunta)

respuesta = st.radio("Selecciona tu respuesta:", opciones)

# -----------------------------------------------
# BOTÓN PARA ENVIAR RESPUESTA
# -----------------------------------------------
if st.button("Enviar respuesta"):
    if respuesta == correcta:
        st.success("✅ ¡Correcto!")
        st.session_state.correctas += 1
        st.session_state.indice += 1
    else:
        st.error("❌ Incorrecto. Intenta de nuevo.")

    st.rerun()
