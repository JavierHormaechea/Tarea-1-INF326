# Infraestructura

Con Docker vamos a levantar cada uno de los componentes como un contenedor.
- 1 contenedor para RabbitMQ (nuestra cola de mensajes)
- 1 contenedor para la API (FastAPI)
- 1 contenedor para el publisher (se usa on-demand para mandar un sismo)
- 5 contenedores con subscriber.py cada uno con distintas variables de entorno (CITY_NAME, CITY_LAT, CITY_LON).

en el docker-compose.yml se definen las variables de entorno para cada contenedor, es decir, las variables para las ciudades.