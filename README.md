# ms-alumno
# Microservicio de Gestión de Alumnos

## Integrantes
- Luanna Guajardo  

## Tecnologías
- Python 3.10
- PostgreSQL
- Docker 
- Traefik

#Formas de compilar y ejecutar
1. Clonar el repositorio:

2. Activar el entorno
    ´´bash
    uv venv
    .venv\Scripts\activate
    uv sync

3. Levantar docker
Hay que estar en la carpeta base del proyecto 'ms-alumno', luego instalar la imagen y por ultimo levantar los servicios
```powershell
    docker build -t gestion-alumnos:v1.0.0 .
    cd docker
    $env:COMPOSE_PROJECT_NAME="gestion-alumnos"; docker-compose up -d
    ```

4. Ejecutar pruebas con spike_test.js
    Para ejecutar este archivo en js, solamente hay que estar en la terminal del proyecto y ejecutar:
    ```bash
    k6 run --out web-dashboard spike_tests.js
    ```

5. Ejecutar con POSTMAN
    Podemos ir al método GET y ejecutar:
    ```
    https://alumnos.universidad.localhost/api/v1/alumno?limit=100&offset=0
    https://alumnos.universidad.localhost/api/v1/alumno/<id>
    ```
    para obtener un listado de alumnos en formato JSON o buscar por ID.

##Acceso al microservicio y endpoints
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

