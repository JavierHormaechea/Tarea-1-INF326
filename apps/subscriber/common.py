import math

def calular_distancia_km(lat1, lon1, lat2, lon2):
    #esto es solo disntancia entre 2 puntos en un plano, la norma euclidea
    distancia=math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    
    return distancia
