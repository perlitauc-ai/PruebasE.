import streamlit as st
import pandas as pd
import requests

# -------------------------------------------------------------------
# 🔗 URL DEL CSV EN GITHUB (DEBE SER UN ENLACE RAW)
# Ejemplo: https://raw.githubusercontent.com/usuario/repositorio/main/items.csv
# -------------------------------------------------------------------
CSV_URL = "PON_AQUI_TU_URL_RAW_DEL_CSV"

# -------------------------------------------------------------------
# 📌 Función para cargar el CSV desde GitHub con manejo de errores
# -------------------------------------------------------------------
@st.cache_data
def cargar_items(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la URL no funciona
        df = pd.read_csv(pd.compat.StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error cargando el archivo desde GitHub:\n{e}")
        return None


# -------------------------------------------------------------------
# 📌 Cargar preguntas
# -------------------------------------------------------------------
items = cargar_items(CSV_URL)

if items is None:
    st.stop()  # Detiene la app si no hay datos


# -------------------------------------------------------------------
# 🔧 Inicializar estados de la app
# -------------------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "correctas" not in st.session_state:
    st.session_state.correctas = 0

if "mostrar_feedback" not in st.session_state:
    st.session_state.mostrar_feedback = False

if "respuesta_usuario" not in st.session_state:
    st.session_state.respuesta_usuario = None


# -------------------------------------------------------------------
# 🧠 TÍTULO
# -------------------------------------------------------------------
st.title("🧠 Cuestionario interactivo sobre Pruebas Estadísticas")


# -------------------------------------------------------------------
# 🏁 Si ya terminó todas las preguntas
# -------------------------------------------------------------------
if st.session_state.indice >= len(items):
    st.success("🎉 ¡Has completado el cuestionario!")
    st.write(f"Respuestas correctas: **{st.session_state.correctas} / {len(items)}**")
    st.balloons()
    st.stop()


# -------------------------------------------------------------------
# 📌 Pregunta actual
# -------------------------------------------------------------------
pregunta = items.iloc[st.session_state.indice]

st.subheader(f"Pregunta {st.session_state.indice + 1}")
st.write(pregunta["pregunta"])


# -------------------------------------------------------------------
# 📌 Opciones
# -------------------------------------------------------------------
opciones = [
    pregunta["opcion_a"],
    pregunta["opcion_b"],
    pregunta["opcion_c"],
    pregunta["opcion_d"],
]

respuesta = st.radio(
    "Selecciona una respuesta:",
    opciones,
    index=None,
    key="respuesta_usuario"
)


# -------------------------------------------------------------------
# 🎯 Botón para validar la respuesta
# -------------------------------------------------------------------
if st.button("Responder"):

    if respuesta is None:
        st.warning("Debes seleccionar una respuesta.")
    else:
        st.session_state.mostrar_feedback = True

        if respuesta == pregunta["respuesta_correcta"]:
            st.success("✔️ ¡Correcto!")
            st.info(pregunta["retroalimentacion"])
            st.session_state.correctas += 1
        else:
            st.error("❌ Incorrecto.")
            st.info("Pista: " + pregunta["retroalimentacion"])


# -------------------------------------------------------------------
# ⏭ Botón para continuar
# -------------------------------------------------------------------
if st.session_state.mostrar_feedback:
    if st.button("Siguiente"):
        st.session_state.indice += 1
        st.session_state.mostrar_feedback = False
        st.session_state.respuesta_usuario = None
        st.rerun()
