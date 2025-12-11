import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def configurar_estilo_visual():
    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'
    return "Estilos configurados."

def renderizar_sismograma(t, senal, t_llegada, titulo):
    df = pd.DataFrame({'Tiempo (s)': t, 'Amplitud (mm)': senal})
    base = alt.Chart(df).encode(x='Tiempo (s)')
    linea = base.mark_line(color='#4ECDC4').encode(y='Amplitud (mm)', tooltip=['Tiempo (s)', 'Amplitud (mm)'])
    area = base.mark_area(opacity=0.3, color='#4ECDC4').encode(y='Amplitud (mm)')
    regla = alt.Chart(pd.DataFrame({'x': [t_llegada]})).mark_rule(color='#FF6B6B', strokeDash=[5,5]).encode(x='x')
    return (area + linea + regla).properties(title=titulo, height=350).interactive()

def generar_mapa_calor(magnitud, distancia_estacion):
    x = np.linspace(-100, 100, 150)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X*2 + Y*2)
    Z = np.sin(R/5 - magnitud) * np.exp(-R/40)
    
    fig, ax = plt.subplots(figsize=(8, 6)) 
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    c = ax.contourf(X, Y, Z, cmap='inferno', levels=25)
    ax.plot(0, 0, marker='*', color='yellow', markersize=15, label='Epicentro')
    ax.plot(distancia_estacion, 0, marker='^', color='white', markersize=10, label='Estación')
    
    ax.axis('off')
    ax.legend(facecolor='#262730', labelcolor='white', loc='upper right')
    ax.set_title("Campo de Ondas (Vista Aérea)", color='white')
    
    cbar = plt.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color='white')
    
    return fig