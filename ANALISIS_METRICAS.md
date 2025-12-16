##Analisis Metrico del Microservicio de Alumnos
1. Objetivo del analisis 
El objetivo del analisis metrico es evaluel el comportamiento del microservicio ms-alumno ante escenarios de carga y estres , verificando su estabilidad, tiempos de respuesta y tasa de errores cuando es accedido a traves de Traefik, en un entorno de arquitectura de microservicios.

2. Tipo de prueba realizada
Se implemento un Spike Test, que consiste en:
    - Un aumento brusco de usuarios concurrentes
    - Un periodo de carga sostenida
    - Una reduccion rapida de la carga
Este tipo de prueba permite identificar:
    - Limites de escalabilidad del servicio
    - Comportamiento ante picos repentinos de trafico
    - Correcta actuacion del balanceador y del patron Circuit Breaker

3. Herramientas utilizadas
    - k6: herramienta de testing de carga y estres 
    - Traefik: reverse proxy y balanceador de carga
    - Docker: contenedorizacion del microservicio
    - Gunicorn: servidor WSGI para ejecicion en produccion
Las pruebas se realizaron accediendo al servicio a traves de Traefik utilizando HTTPS, con certificados autofirmados, motivo por el cual se deshabilito la validacion estricta del certificado durante el test.

4. Escenario de prueba
El El escenario definido en k6 contempla:
    - Incremento rápido hasta N usuarios virtuales concurrentes.
    - Mantenimiento de la carga durante un período determinado.
    - Descenso controlado hasta cero usuarios
Durante la prueba, todos los usuarios realizan peticiones HTTPS GET al endpoint: 
´´´ 
/alumno
´´´
5. Metricas evaluadas
Durante la ejecucion del test se evaluaron las siguientes metricas:
*Tiempo de respuesta* 
- Percentil 95 (p95) del tiempo de respuesta
- Permite verificar que la mayoria de las solicitudes se resuelven en un tiempo aceptable

*Tasa de errores*
- Porcentaje de solicitudes fallidas (codigos HTTPS 5xx)
- Indica la estabilidd del servicio bajo carga

*Disponibilidad*
- Verificacion de respuestas exitosas (HTTP 200)
- Confirmacion de que el servicio continua respondiendo correctamente durante el pico de carga

6. Relacion con la arquitectura
El microservicio cuenta con:
    - Multiples replicas configuradas en Docker
    - Balanceo de carga mediante Traefik
    - Circuit Breaker para mitigar fallos ante latencias elevadas o errores reiterados

7. Resultados esperados
Se espera que, durante el pico de carga:
- El servicio mantenga tiempos de respuesta dentro de los límites definidos.
-La tasa de errores se mantenga baja.
-El balanceo entre réplicas funcione de forma transparente para el usuario.
-El sistema degrade de forma controlada ante situaciones extremas.
-Los resultados obtenidos permitirán validar la correcta configuración del microservicio y su preparación para entornos productivos

8. Resultados esperados
Los siguientes valores son los objetivos de rendimiento establecidos para validar la estabilidad y la capacidad de escalabilidad de la arquitectura bajo una prueba de carga tipo Spike Test (con un pico de 200 Usuarios Virtuales).

- Usuarios concurrentes maximos:   200 VUs
- p95 tiempo de respuesta: < 500 ms
- Tasa de errores: < 1%
- Estado general: Aceptable  

Nota Importante
Debido a inconvenientes técnicos o de configuración con la herramienta de pruebas de carga k6 durante la fase de validación, no se pudieron obtener resultados empíricos (medidos) que validen el cumplimiento de estos umbrales.

Por lo tanto, los valores de la tabla representan los objetivos de diseño que el microservicio debe alcanzar para considerar que su despliegue en contenedores es exitoso y estable.

La arquitectura está configurada para cumplir estos objetivos, pero su validación final queda pendiente.