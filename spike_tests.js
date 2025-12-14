import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    // Tu configuración de Traefik redirige a HTTPS y usa un certificado auto-firmado.
    insecureSkipTLSVerify: true,
    // Spike test: subida rapida, sostenimiento y caida
    stages: [
        { duration: "10s", target: 200 }, // subida brusca
        { duration: "2m", target: 200 }, // carga sostenida
        { duration: "5s", target: 0 }, // bajada
    ],

    thresholds: {
        http_req_failed: ['rate<0.01'], //1% de errores
        http_req_duration: ['p(95)<500'], //p95< 500ms
    },
};

export default function () {
    // Apuntamos al entrypoint HTTPS de Traefik.
    const BASE_URL = 'https://localhost';
    const params = {
        headers: {
            'Host': 'alumnos.universidad.localhost',
        },
    };

    // 2. Cambia la petición a un GET hacia un endpoint válido, como '/alumno'.
    //    No necesitamos 'payload' ni 'params' para una petición GET simple.
    const res = http.get(`${BASE_URL}/alumno`, params);
   
    check(res, {
        'status is 200': (r) => r.status === 200, // El endpoint /alumno debería devolver 200 OK
        'status is not 500': (r) => r.status !== 500, // Verificamos que no haya errores internos del servidor
    });

    // Agregamos una pausa de 1 segundo al final de cada iteración.
    // Esto simula un comportamiento de usuario más realista y evita agotar los puertos de red del sistema operativo.
    sleep(1);
}


//elimine metricas innecesarias (Trend)
//baje la carga de 1000 VUs a 200 VUs
//agregue thresholds (lo cual es clave para justificar replicas)