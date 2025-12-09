import matplotlib.pyplot as plt

def configurar_estilo_visual():
    """Configura los estilos globales de las gráficas para el modo oscuro."""
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = '#0E1117'
    plt.rcParams['axes.facecolor'] = '#0E1117'
    plt.rcParams['text.color'] = 'white'
    return "Estilos visuales configurados correctamente."

def obtener_placeholder_mapa():
    """Genera una imagen vacía o texto para ocupar espacio en la UI."""
    return "Aquí se visualizará el mapa de calor en lal fase 3."