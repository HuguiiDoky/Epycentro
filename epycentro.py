import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import fisica    
import graficas  

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Epycentro - Simulador Sísmico", layout="wide", page_icon="Epycentro.png")

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        logo = Image.open("Epycentro.png")
        st.image(logo, use_container_width=True)
    except:
        st.header("🌋 Epycentro")
        
    st.header("🎛️ Control de Simulación")
    st.caption("Configura los parámetros del evento:")
    
    # Parámetros ajustables
    magnitud = st.slider("Magnitud (Mw)", 1.0, 9.0, 5.0)
    suelo_select = st.selectbox("Material del Suelo", ["Roca", "Arena", "Arcilla"])
    distancia = st.number_input("Distancia (km)", value=50.0)
    tipo_onda = st.radio("Fase Sísmica", ["Onda P", "Onda S", "Superficial"])

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 12]) 

with col_logo:
    try:
        st.image("Epycentro.png", width=80)
    except:
        st.write("🌋") 

with col_titulo:
    st.title("Epycentro: Simulación Dinámica de Sismos")

st.markdown("**Herramienta didáctica para el análisis de fenómenos sísmicos.**")

# --- DEFINICIÓN DE PESTAÑAS ---
tab_inicio, tab_tutorial, tab_sim, tab_teoria, tab_equipo = st.tabs([
    "🏠 Inicio & Descripción", 
    "🎓 Tutorial de Uso", 
    "📊 Simulación & Panel", 
    "📘 Marco Teórico", 
    "👥 Equipo & Créditos"
])

# --- CÁLCULOS (BACKEND) ---
datos_suelo = fisica.obtener_propiedades(suelo_select)
t = np.linspace(0, 60, 1000)
senal, t_llegada, amp_max = fisica.simular_evento(t, distancia, magnitud, datos_suelo, tipo_onda)
imm_val, imm_desc = fisica.estimar_mercalli(magnitud, distancia)


# --- PESTAÑA 1: INICIO Y DESCRIPCIÓN (INTACTA) ---
with tab_inicio:
    st.header("Bienvenido a Epycentro")
    st.markdown("""
    Este proyecto tiene como objetivo **simular el comportamiento de ondas sísmicas** (P, S y superficiales) 
    para comprender mejor su dinámica y propagación en distintos medios.
    """)
    
    st.divider()
    
    col_desc1, col_desc2 = st.columns(2)
    with col_desc1:
        st.subheader("🔍 ¿Qué verás en la simulación?")
        st.markdown("""
        **1. Sismograma (1D):** Gráfica que muestra el desplazamiento del suelo (Amplitud) a lo largo del tiempo. 
        Permite visualizar el momento exacto en que llega la onda a la estación.
        
        **2. Mapa de Propagación (2D):**
        Una vista aérea que representa cómo la energía sísmica se expande desde el epicentro 
        hacia afuera, similar a las ondas en el agua.
        """)
    
    with col_desc2:
        st.subheader("📋 Datos Generados")
        st.markdown("""
        El sistema calcula en tiempo real:
        * **Velocidad de propagación:** Según si el suelo es Roca, Arena o Arcilla.
        * **Tiempo de llegada:** Cuánto tarda la onda en recorrer la distancia definida.
        * **Intensidad Mercalli:** Una estimación del nivel de destrucción o percepción.
        """)
    
    st.info("👆 Navega por las pestañas de arriba para comenzar.")


# --- PESTAÑA 2: TUTORIAL (INTACTA - Texto Completo) ---
with tab_tutorial:
    st.header("🎓 Guía de Uso")
    st.markdown("Sigue estos pasos para realizar una simulación correcta:")
    
    st.markdown("""
    ### 1. Configura el Evento (Barra Lateral)
    En el menú de la izquierda encontrarás los controles:
    * **Magnitud:** Define la energía liberada por el sismo (Escala Richter/Mw). A mayor magnitud, mayor amplitud en las gráficas.
    * **Material del Suelo:** Selecciona el medio por donde viaja la onda.
        * *Roca:* Ondas rápidas, poca atenuación (Suelo rígido).
        * *Arena:* Velocidad media, atenuación moderada (Suelo granular).
        * *Arcilla:* Ondas lentas, mayor amplificación (Suelo blando, más peligroso).
    * **Distancia:** Qué tan lejos está la estación de medición del epicentro.
    * **Fase Sísmica:** Elige ver ondas Primarias (P), Secundarias (S) o Superficiales:
        
        * **🔴Onda P (Primaria):**
            * *Definición:* Son las ondas más rápidas y las primeras en registrarse en un sismograma (de ahí su nombre "Primarias").
            * *Movimiento:* Funcionan como un acordeón: comprimen y estiran la roca en la misma dirección en la que viajan (movimiento logitudinal).
            * *Caractrísticas:* Pueden viajar a tráves de sólidos, líquidos y gases (por eso atraviesan el núcleo de la Tierra). Suelen sentirse
               como un "golpe" o "ruido" repentino al inicio del sismo.
        * **🔵Onda S (Secundaria):**
            * *Definición:* Son más lentas que las ondas P y llegan en segundo lugar.
            * *Movimiento:* Sacuden el suelo hacia arriba y hacia abajo, o de lado a lado, perpendicular a la dirección en la que viajan (movimiento transversal o de cizalla).
            * *Características:* Solo viajan a través de sólidos (no pueden atravesar el núcleo líquido externo de la Tierra). Son las que empiezan a causar daños 
                en las estructuras por su movimiento de sacudida.
        * **🔘Onda Superficial (R y L):**
            * *Definición:* Son ondas que viajan solo por la corteza terrestre (la superficie), no por el interior profundo. Son más lentas que las P y S, pero tienen mayor amplitud.
            * *Movimiento:* Tienen un movimiento complejo, similar a las olas del mar (rodante) o de serpiente (lateral).
            * *Características:* Son las responsables de la mayor parte de la destrucción y daños catastróficos durante un terremoto grande, ya que mueven el suelo violentamente y su energía tarda más en disiparse.
    ### 2. Analiza el Panel de Simulación
    Ve a la pestaña **📊 Simulación & Panel**. Observa cómo cambian las gráficas al mover los controles.
    * *Nota:* Si aumentas la distancia, la onda tardará más en aparecer en el sismograma.

    ### 3. Exporta tus Resultados
    Al final del panel de simulación, encontrarás una sección para descargar los datos en formato CSV para usarlos en Excel o Python.
    """)


# --- PESTAÑA 3: SIMULACIÓN (INTACTA) ---
with tab_sim:
    # 1. MÉTRICAS
    st.subheader("Parámetros Físicos del Entorno")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad Medio", f"{datos_suelo['vel']} km/s")
    col2.metric("Amortiguamiento", f"{datos_suelo['amort']}")
    col3.metric("Densidad", f"{datos_suelo['densidad']} g/cm³")
    col4.metric("Intensidad (Mercalli)", f"{imm_val:.1f}", delta=imm_desc, delta_color="off")
    
    st.info(f"Suelo: {datos_suelo['desc']} | Tiempo de llegada estimado: **{t_llegada:.2f} s**")
    st.markdown("---")

    # 2. VISUALIZACIÓN VERTICAL
    st.subheader("Monitor de Propagación de Ondas")
    
    # GRÁFICA 1: SISMOGRAMA
    st.subheader("1. Sismograma (1D)")
    st.caption(f"Registro de amplitud en estación a {distancia} km")
    grafico1 = graficas.renderizar_sismograma(t, senal, t_llegada, f"Sismograma Sintético - {tipo_onda}")
    st.altair_chart(grafico1, use_container_width=True)
    
    st.markdown("---") 
        
    # GRÁFICA 2: MAPA 2D
    st.subheader("2. Propagación de Ondas (2D)")
    st.caption("Vista aérea del campo de desplazamiento desde el epicentro")
    
    fig2 = graficas.generar_mapa_calor(magnitud, distancia)
    st.pyplot(fig2, use_container_width=True)
        
    # 3. REGISTRO DE DATOS
    st.markdown("---")
    st.subheader("📋 Registro de Resultados")
    
    with st.expander("Ver Datos Detallados y Descargar"):
        df_export = pd.DataFrame({
            "Tiempo (s)": t,
            "Amplitud": senal,
            "Velocidad": np.gradient(senal, t)
        })
        st.dataframe(df_export.head(10), use_container_width=True)
        
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Descargar CSV", csv, "datos_sismo.csv", "text/csv")


# --- PESTAÑA 4: MARCO TEÓRICO (INTACTA - Texto Completo) ---
with tab_teoria:
    st.subheader("Fundamentos de Sismología")

    st.markdown('### Tipos de Ondas Sísmicas')
    colum_t1, colum_t2, colum_t3 = st.columns(3)

    with colum_t1:
        st.info("**🔴Onda P (Primaria)**")
        st.markdown("""
                    * **Velocidad:** Alta (aprox. 6 km/s en roca )
                    * **Llegada:** 1ra en registrarse.
                    * **Efecto:** Comprime y expande el suelo (como un acordeón). Se siente como un golpe seco vertical.""")
    
    with colum_t2:
        st.info("**🔵Onda S (Secundaria)**")
        st.markdown("""
                    * **Velocidad:** Media (aprox. 3.5 km/s)
                    * **Llegada:** 2da en registrarse.
                    * **Efecto:** Mueve el suelo de lado a lado (corte). Es peligrosa para edificios rígidos.""")
    
    with colum_t3:
        st.info("**🔘Onda Superficial**")
        st.markdown("""
                    * **Velocidad:** Baja (< 3 km/s).
                    * **Llegada:** Última en registrarse.
                    * **Efecto:** Movimiento rodante u oscilatorio violento. Causa la mayor destrucción en superficie.""")
    
    st.divider()
    
    st.subheader("Modelo Matemático")
    st.markdown("El comportamiento simulado se rige por la ecuación de onda amortiguada:")
    st.latex(fisica.formula_teorica_onda())
    st.markdown("""
    **Donde:**
    * $A_0$: Amplitud inicial (función de la magnitud)
    * $\\alpha$: Coeficiente de amortiguamiento del suelo
    * $t$: Tiempo transcurrido desde el origen
    """)


# --- PESTAÑA 5: EQUIPO (LA ÚNICA MODIFICADA) ---
with tab_equipo:
    st.header("Créditos del Proyecto")
    
    # Creamos las columnas para el diseño "Opción A"
    col_escuela, col_datos = st.columns([1, 2])
    
    with col_escuela:
        try:
            # Logo de la escuela a la izquierda
            logo_escuela = Image.open("hipocrates.png")
            st.image(logo_escuela, use_container_width=True)
        except:
            st.warning("No se encontró 'hipocrates.png'")
            
    with col_datos:
        st.subheader("👨‍🎓 Integrantes")
        st.write("* **Hugo Yael Castrejón Salgado**")
        st.write("* **Miguel Angel Navarro Hernandez**")
        st.write("* **Angel Jose Rendon Nuñez**")
        
        st.divider()
        
        st.subheader("👨‍🏫 Docentes & Materias")

        st.markdown("**Ing. Geiner Alfonso Niño Salgado**")
        st.caption("Cálculo Univariable")
        
        st.markdown("**Ing. Samuel Alvarado Agama**")
        st.caption("Entorno Gráfico de Programación")