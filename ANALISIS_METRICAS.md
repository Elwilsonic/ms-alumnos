# Análisis de Métricas de Test de Carga

## Herramienta utilizada
- k6 (script: spike_tests.js)
- Dashboard: http://127.0.0.1:5665

## Escenario de prueba
- 200 usuarios virtuales (VUs)
- 2 minutos de duración
- Endpoint probado: GET /alumno

## Resultados principales

- **Total de peticiones:** 75,215
- **Respuestas exitosas (status 200):** 75,215 (100%)
- **Errores (status 400, 404, 409, 429, 500):** 0
- **Latencia promedio:** 179 ms
- **Latencia máxima:** 1.12 s
- **Latencia p95:** 457 ms
- **Peticiones fallidas:** 0%
- **Datos recibidos:** 1.7 GB
- **Datos enviados:** 7.5 MB

## Interpretación

- El microservicio soporta alta concurrencia sin errores ni caídas.
- Todas las respuestas fueron correctas (status 200).
- El tiempo de respuesta se mantuvo bajo carga intensa.
- No hubo saturación de red ni de recursos
- Además lo probe con 2 millones de alumnos

## Conclusión

El microservicio de alumnos cumple con los requisitos de rendimiento y estabilidad bajo carga, respondiendo correctamente a todas las solicitudes concurrentes.