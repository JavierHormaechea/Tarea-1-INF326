# Tarea-1-INF326


### Requisitos
- Docker y Docker Compose instalados.
- Estar en la carpeta: infraestructure/
- tener el archivo .env con las variables de entorno, el archivo .env.example tiene un ejemplo

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
- Subscriber Valparaiso
- Subscriber Arica
- Subscriber Coquimbo
- Subscriber Concepcion
- Subscriber Punta Arenas

- Para detener todo:
```bash
docker compose down
```

### Probar los contenedores
- verificar api con 
```bash
curl http://localhost:8000/sismos/1
```

- Ver logs de los subscribers (en vivo):
```bash
# Valparaíso
docker compose logs -f sub-valparaiso

#abrir otra terminal y ejecutar para ver logs de otro subscriber:
docker compose logs -f sub-arica
```

- Publicar un evento (formato posicional con pipes)
```bash
docker compose run --rm publisher python publish.py "1|-33.45|-70.66|6.2|2025-09-18T12:00:00Z"
```
