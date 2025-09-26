import json, os, time
import pika, requests
from common import calcular_distancia_km

# config general
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "sismos")
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
RADIUS_KM = float(os.getenv("RADIUS_KM", "500"))

# ciudad parametrizable por .env
CITY_NAME = os.getenv("CITY_NAME")
CITY_LAT  = float(os.getenv("CITY_LAT"))
CITY_LON  = float(os.getenv("CITY_LON"))

# funcion para manejar mensajes
def on_msg(ch, method, props, body):
    texto = body.decode("utf-8", errors="replace").strip()
    try:
        id_, lat, lon, mag, ts = texto.split("|") # separar mensaje por pipe

        lat = float(lat); lon = float(lon); mag = float(mag)

        #calular la distancia entre el sismo y la ciudad
        #creo que hay que usar una funcion llamada haversine que no se como funciona
        dist = calcular_distancia_km(CITY_LAT, CITY_LON, lat, lon)
        
        print(f"[{CITY_NAME}] msg={texto} -> dist={dist:.1f} km, mag={mag}")

        # si el sismo está dentro del radio, buscar detalle 
        if dist <= RADIUS_KM:
            r = requests.get(f"{API_BASE}/sismos/{id_}", timeout=5)
            r.raise_for_status()
            print(f"[{CITY_NAME}] DETALLE:", r.json())


def main():
    # conectar a RabbitMQ
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)

    # cola efímera exclusiva, una por instancia
    q = channel.queue_declare(queue="", exclusive=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=q.method.queue)

    print(f"[{CITY_NAME}] Escuchando en exchange '{EXCHANGE_NAME}' (radio {RADIUS_KM} km)…")
    channel.basic_consume(queue=q.method.queue, on_message_callback=on_msg, auto_ack=False)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

if __name__ == "__main__":
    # pequeña espera por API/Rabbit
    time.sleep(0.5)
    main()
