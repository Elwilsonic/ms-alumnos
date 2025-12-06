# ms-alumnos

## Requerimientos
- Python >= 3.12 (importante para las dependencias según el pyproject)
- Docker
- Traefik
- Postgres

## Formas de Compilar y Ejecutar en Docker

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/Elwilsonic/ms-alumnos.git
    cd ms-alumnos
    ```
2. Activar el entorno
    Como se hace un git clone, no es necesario ejecutar en la terminal `uv init`, solamente tiene que instalar el entorno Virtual venv, activar el entorno virtual y sincronizar dependencias:
    ```bash
    uv venv
    .venv\Scripts\activate
    uv sync
    ```

3. Levantar docker
    Primero hay que estar en la carpeta base del proyecto `ms-alumnos`, luego instalar la imagen y levantar los servicios:
    ```powershell
    docker build -t gestion-alumnos:v1.0.0 .
    cd docker
    $env:COMPOSE_PROJECT_NAME="gestion-alumnos"; docker-compose up -d
    ```

4. Ejecutar pruebas con spike_tests.js
    Para ejecutar este archivo en js, solamente hay que estar en la terminal del proyecto y ejecutar:
    ```bash
    k6 run --out web-dashboard spike_tests.js
    ```
    Para ver en tiempo real en el navegador: [http://127.0.0.1:5665](http://127.0.0.1:5665)


    El análisis detallado de las métricas de test de carga se encuentra en el archivo
    [ANALISIS_METRICAS.md](./ANALISIS_METRICAS.md)

5. Ejecutar con POSTMAN
    Podemos ir al método GET y ejecutar:
    ```
    https://alumnos.universidad.localhost/api/v1/alumno?limit=100&offset=0
    https://alumnos.universidad.localhost/api/v1/alumno/<id>
    ```
    para obtener un listado de alumnos en formato JSON o buscar por ID.


## Acceso al Microservicio y Endpoints

El microservicio está disponible vía Traefik en:
```
https://alumnos.universidad.localhost
```
Los endpoints principales son:
```
GET https://alumnos.universidad.localhost/api/v1/alumno?limit=100&offset=0
GET https://alumnos.universidad.localhost/api/v1/alumno/<id>
```
Puedes probarlos con Postman o desde el navegador.

## Patrones de Microservicio

- **Circuit Breaker:** Implementado a nivel de infraestructura con Traefik. Si el servicio presenta alta latencia, errores 5xx o problemas de red, Traefik corta el tráfico temporalmente para proteger el sistema.
- **Retry:** Traefik reintenta automáticamente las peticiones fallidas hacia el microservicio, mejorando la resiliencia ante fallos transitorios.

Estos patrones están configurados en el archivo `docker/docker-compose.yml`.

## Integrantes
- Batista Martina
- Cabeza Florencia
- Cardozo Leandro
- Carrieri Bruno
- Peñalbé Hernán