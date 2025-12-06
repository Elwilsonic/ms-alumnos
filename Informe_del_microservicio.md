# Informe Técnico: Microservicio, Pruebas de Carga y Patrones

## 1. Análisis y Resultado de K6

## Prueba de carga GET paginada (limit/offset)

**Configuración:**
- Script: `spike_tests.js` (GET paginado)
- Carga: 200 VUs, 2 minutos
- Endpoint: `GET /api/v1/alumno/alumno?limit=100&offset=0`
- Tenía 2 millones de alumnos creados

**Resultados:**
- Peticiones totales: 71,359
- Respuestas 200: 100%
- Errores: 0%
- Latencia promedio: 189 ms
- Throughput: ~595 req/s

**Conclusión:**
El microservicio responde correctamente y eficientemente bajo carga alta, cumpliendo con el requerimiento de solo exponer el endpoint GET de alumnos en JSON. No se detectaron errores ni caídas durante la prueba.

## 2. Proyecto funcionando (Dockerfile)

- Imagen Docker creada y ejecutada correctamente:
  ```dockerfile
  CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]
  ```
- Proceso de build y despliegue exitoso.

## 3. Patrones de Microservicios

### Balanceo de Carga
- Usando Traefik como proxy reverso y balanceador entre réplicas del microservicio.
- Configuración en `docker-compose.yml`:
  ```yaml
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.alumnos-service.rule=Host(`alumnos.universidad.localhost`)"
    - "traefik.http.services.alumnos-service.loadbalancer.server.port=5000"
  ```

### Retry
- Middleware de Traefik para reintentos automáticos:
  ```yaml
  labels:
    - "traefik.http.middlewares.alumnos-service.retry.attempts=4"
    - "traefik.http.middlewares.alumnos-service.retry.initialinterval=100ms"
  ```

### Rate Limit (alternativo)
- Limitar peticiones por IP/usuario:
  ```yaml
  labels:
    - "traefik.http.middlewares.alumnos-ratelimit.ratelimit.average=100"
    - "traefik.http.middlewares.alumnos-ratelimit.ratelimit.period=1s"
  ```

### Corte circuito (Circuit Breaker)
- Middleware para evitar saturar servicios caídos:
  ```yaml
  labels:
    - "traefik.http.middlewares.alumnos-service.circuitbreaker.expression=LatencyAtQuantileMS(50.0) > 100"
  ```

### Cache de Objetos
- Redis configurado en Docker y disponible para cachear consultas frecuentes (no esta aplicado en el codigo del proyecto, si lo estuviera, tendria que estar actualizar de alumno_service)
- Ejemplo en Python:
  ```python
  import redis
  redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
  def buscar_todos():
      cache_key = "alumnos_todos"
      alumnos = redis_client.get(cache_key)
      if alumnos:
          return json.loads(alumnos)
      alumnos = Alumno.query.all()
      redis_client.setex(cache_key, 60, json.dumps([a.to_dict() for a in alumnos]))
      return alumnos
  ```