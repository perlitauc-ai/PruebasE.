import streamlit as st
import pandas as pd

# -----------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------
st.set_page_config(page_title="Cuestionario Estadístico", layout="centered")

# URL RAW DEL ARCHIVO CSV EN GITHUB (CÁMBIALO POR EL TUYO)
CSV_URL = "https://raw.githubusercontent.com/usuario/repositorio/rama/items.csv"

# -----------------------------------------------------
# Cargar datos
# -----------------------------------------------------
@st.cache_data
def cargar_items():
    return pd.read_csv(CSV_URL)

items = cargar_items()

# -----------------------------------------------------
# Inicializar variables de sesión
# -----------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "correctos" not in st.session_state:
    st.session_state.correctos = 0

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "retro" not in st.session_state:
    st.session_state.retro = ""

# -----------------------------------------------------
# Función para procesar la respuesta
# -----------------------------------------------------
def verificar_respuesta(opcion_seleccionada, respuesta_correcta):
    st.session_state.respondido = True
    if opcion_seleccionada == respuesta_correcta:
        st.session_state.retro = "✅ ¡Correcto!"
        st.session_state.correctos += 1
    else:
        st.session_state.retro = f"❌ Incorrecto. La respuesta correcta es: **{respuesta_correcta}**"

# -----------------------------------------------------
# Mostrar cuestionario
# -----------------------------------------------------
st.title("📊 Cuestionario sobre Pruebas Estadísticas")

if st.session_state.indice < len(items):
    
    item = items.iloc[st.session_state.indice]

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {len(items)}")
    st.write(item["pregunta"])

    opciones = [item["opcion1"], item["opcion2"], item["opcion3"], item["opcion4"]]

    opcion = st.radio("Selecciona una opción:", opciones, index=None)

    if st.button("Responder"):
        if opcion is None:
            st.warning("Selecciona una opción antes de continuar.")
        else:
            verificar_respuesta(opcion, item["respuesta"])

    # Mostrar retroalimentación
    if st.session_state.respondido:
        st.info(st.session_state.retro)

        if st.button("Siguiente"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.retro = ""
            st.rerun()

else:
    # -------------------------------------------------
    # RESULTADOS FINALES
    # -------------------------------------------------
    st.success("🎉 ¡Has terminado el cuestionario!")

    total = len(items)
    correctos = st.session_state.correctos
    incorrectos = total - correctos

    st.write(f"✔ Respuestas correctas: **{correctos}**")
    st.write(f"✘ Respuestas incorrectas: **{incorrectos}**")

    porcentaje = round((correctos / total) * 100, 2)
    st.write(f"📊 Puntaje final: **{porcentaje}%**")

    if st.button("Reiniciar"):
        st.session_state.indice = 0
        st.session_state.correctos = 0
        st.session_state.respondido = False
        st.session_state.retro = ""
        st.rerun()
