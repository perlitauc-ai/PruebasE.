import streamlit as st
import pandas as pd
import requests

# URL del archivo CSV en GitHub (en formato RAW)
CSV_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/items.csv"

@st.cache_data
def cargar_items():
    return pd.read_csv(CSV_URL)

# Cargar preguntas
items = cargar_items()

# Estado inicial
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "correctas" not in st.session_state:
    st.session_state.correctas = 0

if "mostrar_feedback" not in st.session_state:
    st.session_state.mostrar_feedback = False

if "respuesta_usuario" not in st.session_state:
    st.session_state.respuesta_usuario = None


st.title("🧠 Cuestionario sobre Pruebas Estadísticas")

# Si ya terminó todas las preguntas
if st.session_state.indice >= len(items):
    st.success(f"¡Has terminado el cuestionario! 🎉\n\n"
               f"Respuestas correctas: **{st.session_state.correctas} / {len(items)}**")
    st.stop()

# Obtener pregunta actual
pregunta_actual = items.iloc[st.session_state.indice]

st.subheader(f"Pregunta {st.session_state.indice + 1}")
st.write(pregunta_actual["pregunta"])

# Opciones de respuesta
opciones = [
    pregunta_actual["opcion_a"],
    pregunta_actual["opcion_b"],
    pregunta_actual["opcion_c"],
    pregunta_actual["opcion_d"],
]

respuesta = st.radio("Selecciona una respuesta:", opciones, index=None, key="respuesta_usuario")

# Botón para validar respuesta
if st.button("Responder"):
    if respuesta is None:
        st.warning("Selecciona una respuesta antes de continuar.")
    else:
        st.session_state.mostrar_feedback = True

        if respuesta == pregunta_actual["respuesta_correcta"]:
            st.success("✔️ ¡Correcto!")
            st.info(pregunta_actual["retroalimentacion"])
            st.session_state.correctas += 1
        else:
            st.error("❌ Incorrecto.")
            st.info("Pista: " + pregunta_actual["retroalimentacion"])

# Botón para continuar si ya se respondió
if st.session_state.mostrar_feedback:
    if st.button("Siguiente pregunta"):
        st.session_state.indice += 1
        st.session_state.mostrar_feedback = False
        st.session_state.respuesta_usuario = None
        st.rerun()
