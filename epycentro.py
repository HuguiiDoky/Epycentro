import streamlit as st
import numpy as np
from PIL import Image
import fisica
import graficas

st.set_page_config(page_title="Epycentro - Simulador Sísmico", layout="wide", page_icon="🌋")

# BARRA LATERAL
with st.sidebar:
    try:
        logo = Image.open("Epycentro.png")
        st.image(logo)
    except:
        st.write("🌋 Proyecto Epycentro")
    
    #Controles de magnitud, tipo de suelo y distacia
    st.header("🎛️ Control de Sismo")
    magnitud = st.slider("Magnitud (Mw)", 1.0, 9.0, 5.0)
    suelo_select = st.selectbox("Material del Suelo", ["Roca", "Arena", "Arcilla"])
    distancia = st.number_input("Distancia (km)", value=50.0)
    # Control del tipo de onda
    tipo_onda = st.radio("Fase Sísmica", ["Onda P", "Onda S", "Superficial"])

# Nombre de la página en grande y los objetivos
st.title("🌋 Epycentro: Simulación Dinámica de Sísmos")
st.markdown("""**Objetivos:**
* Simular el comportamiento de ondas sísmicas (P, S y superficiales) a partir de un evento inicial.""")

# Pestañas mostradas
tab1, tab2, tab3 = st.tabs(["📊 Simulación & Panel", "📘 Marco Teórico", "👥 Equipo"])

# Lógica del programa
datos_suelo = fisica.obtener_propiedades(suelo_select) # Día 1
t_teorico = fisica.calcular_tiempo_teorico(distancia, datos_suelo['vel']) # Día 1

# Simulación
t = np.linspace(0, 60, 1000)
senal, t_llegada, amp_max = fisica.simular_evento(t, distancia, magnitud, datos_suelo, tipo_onda)

with tab1:
    # 1. Sección de Métricas (recupera los dato)
    st.subheader("Parámetros Físicos del Entorno")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad Medio", f"{datos_suelo['vel']} km/s")
    col2.metric("Amortiguamiento", f"{datos_suelo['amort']}")
    col3.metric("Densidad", f"{datos_suelo['densidad']} g/cm³")
    # Métrica nueva del Día 2
    col4.metric("Tiempo Llegada Real", f"{t_llegada:.2f} s", delta=f"Teórico: {t_teorico:.2f} s")
    
    st.info(f"Suelo: {datos_suelo['desc']}")
    
    st.markdown("---")
    
    # 2. Sección de la Gráfica
    st.subheader(f"Sismograma en Tiempo Real ({tipo_onda})")
    grafico = graficas.renderizar_sismograma(t, senal, t_llegada, f"Registro en estación a {distancia} km")
    st.altair_chart(grafico, use_container_width=True)

with tab2:
    # Marco teoríco
    st.subheader("Modelo Matemático")
    st.markdown("El comportamiento de la onda se rige por la ecuación diferencial amortiguada:")
    st.latex(fisica.formula_teorica_onda())
    st.markdown("""
    **Donde:**
    * $A_0$: Amplitud inicial (función de la magnitud)
    * $\\alpha$: Coeficiente de amortiguamiento del suelo
    * $t$: Tiempo transcurrido desde el origen
    """)

with tab3:
    # Integrantes del Equipo
    st.subheader("Integrantes del Equipo")
    st.write("* Hugo Yael Castrejón Salgado")
    st.write("* Miguel Angel Navarro Hernandez")
    st.write("* Angel Jose Rendon Nuñez")