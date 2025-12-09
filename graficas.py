import altair as alt
import pandas as pd
import matplotlib.pyplot as plt

# DÍA 1
def configurar_estilo_visual():
    """Configura estilos globales (útil para cuando usemos Matplotlib en el futuro)."""
    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'
    return "Estilos configurados."

# DÍA 2
def renderizar_sismograma(t, senal, t_llegada, titulo):
    """
    Genera el gráfico interactivo del sismograma.
    """
    df = pd.DataFrame({'Tiempo (s)': t, 'Amplitud (mm)': senal})
    
    # Grafica
    base = alt.Chart(df).encode(x='Tiempo (s)')
    
    # Linea de la onda
    linea = base.mark_line(color='#4ECDC4').encode(
        y='Amplitud (mm)',
        tooltip=['Tiempo (s)', 'Amplitud (mm)']
    )
    
    # Relleno bajo la curva
    area = base.mark_area(opacity=0.3, color='#4ECDC4').encode(
        y='Amplitud (mm)'
    )
    
    # Linea vertical que marca la llegada de la onda
    regla = alt.Chart(pd.DataFrame({'x': [t_llegada]})).mark_rule(
        color='#FF6B6B', strokeDash=[5,5]
    ).encode(x='x')
    
    return (area + linea + regla).properties(title=titulo, height=350).interactive()