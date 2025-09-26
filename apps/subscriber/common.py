from math import radians, sin, cos, sqrt, atan2

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    #Se calcula la distancia con la formula de haversine
    R = 6371
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    distancia = 2 * R * atan2(sqrt(a), sqrt(1 - a))

    return distancia
