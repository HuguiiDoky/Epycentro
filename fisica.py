import numpy as np

# Datos de cada tipo de suelo
DATOS_SUELO = {
    "Roca": {"vel": 6.0, "amort": 0.05, "densidad": 2.7, "desc": "Suelo rígido, alta velocidad."},
    "Arena": {"vel": 3.5, "amort": 0.10, "densidad": 1.9, "desc": "Suelo granular, disipación media."},
    "Arcilla": {"vel": 2.0, "amort": 0.20, "densidad": 1.6, "desc": "Suelo blando, alta amplificación."}
}
# Funcion para obtener las propiedades del suelo
def obtener_propiedades(tipo_suelo):
    """Devuelve el diccionario completo de propiedades del suelo."""
    return DATOS_SUELO.get(tipo_suelo, DATOS_SUELO["Arena"])

# Calcular el tiempo teorico de viaje de onda
def calcular_tiempo_teorico(distancia, velocidad):
    """Calcula el tiempo de viaje ideal (t = d/v)."""
    if velocidad <= 0: return 0
    return distancia / velocidad

# Fórmula teórica de la onda sísmica
def formula_teorica_onda():
    """Retorna la fórmula en formato LaTeX para mostrar en la web."""
    return r"""
    A(t) = A_0 \cdot e^{-\alpha t} \cdot \sin(2\pi f t - kx)
    """