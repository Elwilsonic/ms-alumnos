# Informe Técnico: Microservicio, Pruebas de Carga y Patrones

## 1. Análisis y Resultado de K6

**Configuración:**
- Script: `spike_tests.js`
- Carga: 200 VUs, 2 minutos
- Endpoint: `POST /api/v1/alumno/alumno`
- Datos: Únicos por iteración

**Resultados:**
- Peticiones totales: ~91,800
- Respuestas 200: 100%
- Errores: 0%
- Latencia promedio: 146 ms
- Latencia p95: 394 ms
- Throughput: ~765 req/s

**Conclusión:**
El microservicio soporta alta concurrencia sin errores ni saturación, con latencia estable.

## 1.2 Prueba de carga GET ficha JSON

**Configuración:**
- Script: `spike_tests.js` (GET ficha JSON)
- Carga: 200 VUs, 2 minutos
- Endpoint: `GET /api/v1/alumno/alumnos/<id>/ficha?formato=json`
- IDs simulados: 1 a 10

**Resultados:**
- Peticiones totales: 180,027
- Respuestas 200: 20%
- Respuestas 404: 9%
- Errores 400/429/500: 0%
- Latencia promedio: 74 ms
- Latencia p95: 200 ms
- Throughput: ~1,500 req/s

**Conclusión:**
El endpoint de ficha soporta alta concurrencia, responde rápido y sin errores graves. La mayoría de los 404 corresponden a IDs inexistentes en la base de datos.

## 1.3 Prueba de carga GET ficha PDF

**Configuración:**
- Script: `spike_tests.js` (GET ficha PDF)
- Carga: 200 VUs, 2 minutos
- Endpoint: `GET /api/v1/alumno/alumnos/<id>/ficha?formato=pdf`
- IDs simulados: 1 a 10

**Resultados:**
- Peticiones totales: 76,411
- Respuestas 200: 85%
- Respuestas 404: 14%
- Errores 400/429/500: 0%
- Latencia promedio: 176 ms
- Latencia p95: 520 ms
- Throughput: ~637 req/s

**Conclusión:**
El endpoint de ficha en PDF soporta alta concurrencia y responde correctamente para IDs válidos. La generación de PDF es más costosa que JSON, pero el rendimiento sigue siendo bueno y no hubo errores graves.

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