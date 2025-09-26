from math import radians, sin, cos, sqrt, atan2

# funcion para calcular distancia geodesica
def calcular_distancia_km(lat1, lon1, lat2, lon2):
    R = 6371 # radio de la tierra en kms
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    
    # se calcula la distancia con la formula de haversine
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    distancia = 2 * R * atan2(sqrt(a), sqrt(1 - a))

    return distancia
