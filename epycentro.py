# main.py - VERSIÓN DÍA 1
import streamlit as st
import fisica
import graficas
from PIL import Image

st.set_page_config(page_title="Epycentro", layout="wide")

# Cabecera
st.title("Epycentro: Simulación de Ondas Sísmicas")
st.markdown("""
**Objetivos:**
* Simular el comportamiento de ondas sísmicas (P, S y superficiales) a partir de un evento inicial.
* Reproducir escenarios de terremotos o temblores para comprender mejor su dinámica.
* Generar una herramienta didáctica para el análisis de fenómenos sísmicos.""")

# Sidebar completa
with st.sidebar:
    try:
        logo = Image.open("Epycentro.png")
        st.image(logo)
    except:
        st.warning("No se encontró 'Epycentro.png'. Aegurese de guardarlo en la carpeta del proyecto.")

    st.header("🔧 Configuración Sísmica")
    st.info("Defina los parámetros iniciales del evento.")
    magnitud = st.slider("Magnitud (Mw)", 1.0, 9.0, 5.0)
    suelo_select = st.selectbox("Material del Suelo", ["Roca", "Arena", "Arcilla"])
    distancia = st.number_input("Distancia Epicentral (km)", value=50.0)

# Uso de Pestañas para dar volumen al proyecto
tab1, tab2, tab3 = st.tabs(["📊 Panel de Control", "📘 Marco Teórico", "👥 Equipo"])

with tab1:
    st.subheader("Parámetros Físicos del Entorno")
    
    # Llamamos a fisica.py para obtener datos
    datos = fisica.obtener_propiedades(suelo_select)
    t_teorico = fisica.calcular_tiempo_teorico(distancia, datos['vel'])
    
    # Mostramos métricas visuales
    col1, col2, col3 = st.columns(3)
    col1.metric("Velocidad de Onda", f"{datos['vel']} km/s", delta="Constante")
    col2.metric("Coef. Amortiguamiento", f"{datos['amort']}", delta_color="inverse")
    col3.metric("Densidad Aprox.", f"{datos['densidad']} g/cm³")
    
    st.info(f"Descripción del medio: *{datos['desc']}*")
    st.warning(f"⏳ Tiempo estimado de arribo (Onda P): **{t_teorico:.2f} s** (Cálculo preliminar)")

with tab2:
    st.subheader("Modelo Matemático Implementado")
    st.markdown("El proyecto utilizará la siguiente ecuación diferencial para modelar el desplazamiento:")
    # Mostramos la fórmula LaTeX que viene de fisica.py
    st.latex(fisica.formula_teorica_onda())

with tab3:
    st.write("Integrantes: Hugo Yael Castrejón Salgado, Miguel Angel Navarro Hernandez, Angel Jose Rendón Núñez.")