# apps/publisher/publish.py
import os, sys, pika

URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
EX  = os.getenv("EXCHANGE_NAME", "sismos")

def main():
    # si es menor a 2 argumentos, mostrar uso
    if len(sys.argv) < 2:
        print('Uso: python publish.py "id|lat|lon|mag|ts"')
        sys.exit(1)

    message = sys.argv[1]

    connection = pika.BlockingConnection(pika.URLParameters(URL)) # aquí se usa URLParameters en vez de ConnectionParameters para usar el URL de env directamente
    channel = connection.channel()

    channel.exchange_declare(exchange=EX, exchange_type="fanout", durable=True)
    channel.basic_publish(exchange=EX, routing_key="", body=message.encode())
    print("enviado:", message)
    connection.close()

if __name__ == "__main__":
    main()
