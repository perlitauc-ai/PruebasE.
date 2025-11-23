import streamlit as st
import pandas as pd
import urllib.error

# -----------------------------------------------------
# CONFIG GENERAL
# -----------------------------------------------------
st.set_page_config(page_title="Cuestionario Estadístico", layout="centered")

# ⭐ REEMPLAZA ESTA URL POR TU RAW DEL CSV ⭐
CSV_URL = "https://raw.githubusercontent.com/streamlit/example-data/master/hello.csv"

# -----------------------------------------------------
# FUNCIÓN PARA CARGAR CSV CON MANEJO DE ERRORES
# -----------------------------------------------------
@st.cache_data
def cargar_items(url):
    try:
        df = pd.read_csv(url)
        return df
    except urllib.error.HTTPError:
        st.error("❌ Error: No se pudo acceder al archivo CSV en GitHub.\n"
                 "Revisa que la URL RAW sea correcta.")
        return None
    except Exception as e:
        st.error(f"❌ Error inesperado al cargar el CSV: {e}")
        return None

items = cargar_items(CSV_URL)

# Si no cargó el CSV, detenemos la app
if items is None:
    st.stop()

# -----------------------------------------------------
# INICIALIZAR VARIABLES DE SESIÓN
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
# FUNCIÓN PARA EVALUAR RESPUESTA
# -----------------------------------------------------
def verificar_respuesta(opcion_seleccionada, respuesta_correcta):
    st.session_state.respondido = True
    if opcion_seleccionada == respuesta_correcta:
        st.session_state.retro = "✅ ¡Correcto!"
        st.session_state.correctos += 1
    else:
        st.session_state.retro = f"❌ Incorrecto. La respuesta correcta era: **{respuesta_correcta}**"

# -----------------------------------------------------
# INTERFAZ DEL CUESTIONARIO
# -----------------------------------------------------
st.title("📊 Cuestionario sobre Pruebas Estadísticas")

# Validar formato del CSV
columnas_requeridas = {"pregunta", "opcion1", "opcion2", "opcion3", "opcion4", "respuesta"}
if not columnas_requeridas.issubset(items.columns):
    st.error("❌ El CSV no contiene las columnas necesarias.")
    st.stop()

if st.session_state.indice < len(items):

    item = items.iloc[st.session_state.indice]

    st.subheader(f"Pregunta {st.session_state.indice + 1} de {len(items)}")
    st.write(item["pregunta"])

    opciones = [item["opcion1"], item["opcion2"], item["opcion3"], item["opcion4"]]
    opcion = st.radio("Selecciona una opción:", opciones, index=None)

    if st.button("Responder"):
        if opcion is None:
            st.warning("Debes seleccionar una opción.")
        else:
            verificar_respuesta(opcion, item["respuesta"])

    # Retroalimentación
    if st.session_state.respondido:
        st.info(st.session_state.retro)

        if st.button("Siguiente"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.retro = ""
            st.rerun()

else:
    # -------------------------------------------------
    # RESULTADOS
    # -------------------------------------------------
    st.success("🎉 ¡Has terminado el cuestionario!")
    
    total = len(items)
    correctos = st.session_state.correctos
    
    st.write(f"✔ Respuestas correctas: **{correctos}**")
    st.write(f"✘ Incorrectas: **{total - correctos}**")
    
    porcentaje = round((correctos / total) * 100, 2)
    st.write(f"📊 Puntaje final: **{porcentaje}%**")

    if st.button("Reiniciar"):
        st.session_state.indice = 0
        st.session_state.correctos = 0
        st.session_state.respondido = False
        st.session_state.retro = ""
        st.rerun()
