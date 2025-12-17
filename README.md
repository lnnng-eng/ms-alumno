
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
```bash
    git clone https://github.com/lnnng-eng/ms-alumno.git
    cd ms-alumno
    ```

2. Activar el entorno
    ´´bash
    uv venv
    .venv\Scripts\activate
    uv sync

3. Contruir la imagen e iniciar servicios 
Hay que estar en la carpeta base del proyecto 'ms-alumno', luego instalar la imagen y por ultimo levantar los servicios
```powershell
    docker compose up -d --build --force-recreate
```
Este comando construye la imagen con el codigo mas recientem fuerza la recreacion de los contenedores y levanta los servicios en segundo plano 

4. Ejecutar pruebas con spike_test.js
    Para ejecutar este archivo en js, solamente hay que estar en la terminal del proyecto y ejecutar:
    ```bash
    k6 run --out web-dashboard spike_tests.js
    ```

5. Ejecutar con POSTMAN
    Podemos ir al método GET y ejecutar:
    ```
    https://alumnos.universidad.localhost/api/v1/alumno/
    https://alumnos.universidad.localhost/api/v1/alumno/1
    https://alumnos.universidad.localhost/api/v1/alumno/1/pdf
    ```
    para obtener un listado de alumnos en formato JSON, buscar por ID o generar el informe PDF.

#Acceso al microservicio y endpoints
    El microservicio está disponible vía Traefik en:
    ```
    http://localhost:8080/dashboard/
    ```
    Los endpoints principales son:
    ```
GET https://alumnos.universidad.localhost/api/v1/alumno
GET https://alumnos.universidad.localhost/api/v1/alumno/<id>
GET https://alumnos.universidad.localhost/api/v1/alumno/<id>/pdf
    ```
Puedes probarlos con Postman o desde el navegador.

#Patrones de Microservicio

- **Circuit Breaker:** Implementado a nivel de infraestructura con Traefik. Si el servicio presenta alta latencia, errores 5xx o problemas de red, Traefik corta el tráfico temporalmente para proteger el sistema.
- **Retry:** Traefik reintenta automáticamente las peticiones fallidas hacia el microservicio, mejorando la resiliencia ante fallos transitorios.

CORRECCIONES DADAS POR EL PROFESOR 
- Sin README.md, no se puede saber los integrantes. 
- Sin análisis de métricas. 
- Sin versionado en los requerimientos (Se debe usar uv). 
-Dependencias innecesarias en el proyecto. 
-Dockerfile:  curl htop iputils-ping no son necesarias pero build-essential, libpq-dev y psycopg2-binary estoy casi seguro que sí (por más que la iA se los haya dicho).
- AlumnoSchema no es la estructura recomendada que debe retornar el microservicio de alumnos.
- Tiene código de más no hace falta el CRUD completo solamente R (Lo hablamos también en reiteradas veces en clases)

