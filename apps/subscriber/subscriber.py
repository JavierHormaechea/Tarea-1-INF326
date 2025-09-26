import json, os, time
import pika, requests
from common import calcular_distancia_km

# config general
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")  # en Docker usar 'rabbitmq'
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "sismos")
API_BASE = os.getenv("API_BASE_URL", "http://api:8000")  # en Docker usar el nombre del servicio
RADIUS_KM = float(os.getenv("RADIUS_KM", "500"))

# ciudad parametrizable por .env
CITY_NAME = os.getenv("CITY_NAME")
CITY_LAT  = float(os.getenv("CITY_LAT"))
CITY_LON  = float(os.getenv("CITY_LON"))

# funcion para manejar mensajes
def on_msg(ch, method, props, body):
    texto = body.decode("utf-8", errors="replace").strip()
    try:
        id_, lat, lon, mag, ts = texto.split("|")  # separar mensaje por pipe

        lat = float(lat); lon = float(lon); mag = float(mag)

        dist = calcular_distancia_km(CITY_LAT, CITY_LON, lat, lon)
        
        print(f"[{CITY_NAME}] msg={texto} -> dist={dist:.1f} km, mag={mag}")

        # si el sismo está dentro del radio, buscar detalle 
        if dist <= RADIUS_KM:
            r = requests.get(f"{API_BASE}/sismos/{id_}", timeout=5)
            r.raise_for_status()
            print(f"[{CITY_NAME}] DETALLE:", r.json())
    except Exception as e:
        # manejar errores de parseo o request
        print(f"[{CITY_NAME}] Error procesando '{texto}': {e}")
    finally:
        # confirmar recepción del mensaje (ya que auto_ack=False)
        ch.basic_ack(delivery_tag=method.delivery_tag)


# conectar a RabbitMQ con reintentos (esto es por si aun no está listo el contenedor de RabbitMQ)
def connect_with_retries(url, retries=15, delay=2.0):
    params = pika.URLParameters(url)
    for i in range(1, retries+1):
        try:
            return pika.BlockingConnection(params)
        except Exception as e:
            # activar linea para ver logs
            #print(f"[{CITY_NAME}] Conexión RabbitMQ falló ({i}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("No se pudo conectar a RabbitMQ")


def main():
    # pequeña espera por API/Rabbit
    time.sleep(0.5)
    
    # conectar a RabbitMQ
    connection = connect_with_retries(RABBITMQ_URL)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)

    channel.basic_qos(prefetch_count=1)

    # cola efímera exclusiva, una por instancia
    q = channel.queue_declare(queue="", exclusive=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=q.method.queue)

    print(f"[{CITY_NAME}] Escuchando en exchange '{EXCHANGE_NAME}' (radio {RADIUS_KM} km)…")
    channel.basic_consume(queue=q.method.queue, on_message_callback=on_msg, auto_ack=False)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
