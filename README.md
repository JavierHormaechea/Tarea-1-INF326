# Tarea-1-INF326
Grupo 7

Integrantes:
- Javier Hormaechea
- Benjamin Camus

### Requisitos
- Docker y Docker Compose instalados.
- Estar en la carpeta: infraestructure/
- Tener el archivo .env con las variables de entorno, el archivo .env.example tiene un ejemplo con todos los valores necesarios, en nuestro caso usamos los mismos valores que hay en el archivo .env.example.

### Instrucciones
- Levantar todo con:
```bash
cd infraestructure
docker compose up -d --build
```

Con esto los servicios que se levantan son:
- RabbitMQ en el puerto 5672
- API en http://localhost:8000
- Publisher
- Subscriber Valparaíso
- Subscriber Arica
- Subscriber Concepción
- Subscriber Coquimbo
- Subscriber Punta Arenas

- Para detener todo:
```bash
docker compose down
```

### Probar los contenedores
- Se puede verificar laapi con 
```bash
curl http://localhost:8000/sismos/1
```

- Ver logs de los subscribers (en vivo):
(Para ejecutar estos comandos hay que estar en la carpeta: infraestructure/)
```bash
# Valparaíso
docker compose logs -f sub-valparaiso

#abrir otra terminal y ejecutar para ver logs de Arica:
docker compose logs -f sub-arica

# Lo mismo para las otras ciudades:
# Concepción
docker compose logs -f sub-concepcion
# Coquimbo
docker compose logs -f sub-coquimbo
# Punta Arenas
docker compose logs -f sub-punta-arenas
```

- Publicar un evento (formato posicional con pipes)
```bash
docker compose run --rm publisher python publish.py "1|-33.45|-70.66|6.2|2025-09-18T12:00:00Z"
```
