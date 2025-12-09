import numpy as np

# Datos de propiedades del suelo
DATOS_SUELO = {
    "Roca": {"vel": 6.0, "amort": 0.05, "densidad": 2.7, "desc": "Suelo rígido, alta velocidad."},
    "Arena": {"vel": 3.5, "amort": 0.10, "densidad": 1.9, "desc": "Suelo granular, disipación media."},
    "Arcilla": {"vel": 2.0, "amort": 0.20, "densidad": 1.6, "desc": "Suelo blando, alta amplificación."}
}

def obtener_propiedades(tipo_suelo):
    return DATOS_SUELO.get(tipo_suelo, DATOS_SUELO["Arena"])

def calcular_tiempo_teorico(distancia, velocidad):
    return distancia / velocidad

def formula_teorica_onda():
    return r"A(t) = A_0 \cdot e^{-\alpha t} \cdot \sin(2\pi f t - kx)"

# simulación de un evento sísmico
def simular_evento(t, distancia, magnitud, suelo_data, tipo_onda):
    vel = suelo_data['vel']
    amort = suelo_data['amort']
    
    if tipo_onda == "Onda P":
        freq = 5.0; factor = 0.5; v_real = vel
    elif tipo_onda == "Onda S":
        freq = 3.0; factor = 1.0; v_real = vel / 1.7
    else: 
        freq = 1.0; factor = 2.0; v_real = vel / 2.5

    t_llegada = distancia / v_real
    amp_max = np.exp(magnitud / 2) * factor
    
    senal = np.zeros_like(t)
    mask = t >= t_llegada
    t_fase = t[mask] - t_llegada
    
    senal[mask] = amp_max * np.exp(-amort * t_fase) * np.sin(2 * np.pi * freq * t_fase)
    
    # Retornar la señal simulada, tiempo de llegada y amplitud máxima
    return senal, t_llegada, amp_max