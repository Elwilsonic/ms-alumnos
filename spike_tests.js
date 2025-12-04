import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    //Para los alumnos que siguen prefiriendo Windows 11 es posible que tengan que descomentar insecureSkipTLSVerify (https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/)
    //insecureSkipTLSVerify: true,
    stages: [
        { duration: "30s", target: 100 },   // rampa inicial
        { duration: "60s", target: 200 },   // carga sostenida
        { duration: "30s", target: 0 },     // rampa de salida
    ],
};

export default function () {
    // URL del microservicio de alumnos
    const BASE_URL = 'https://alumnos.universidad.localhost:8843/api/v1/alumno/alumno';

    // JSON válido para crear un alumno
    const uniqueSuffix = `${__VU}-${__ITER}-${Date.now()}`;
    const payload = JSON.stringify({
        "nombre": "Carga",
        "apellido": "K6",
        "nrodocumento": `ND-${uniqueSuffix}`,
        "tipo_documento_id": 2,
        "fecha_nacimiento": "1995-05-05",
        "sexo": "M",
        "nro_legajo": Number(String(Date.now()).slice(-6)),
        "fecha_ingreso": "2022-08-15"
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // POST al endpoint de alumnos
    const res = http.post(BASE_URL, payload, params);

    statusTrend.add(res.status);

    check(res, {
        'status is 200': (r) => r.status === 200,
        'status is 409': (r) => r.status === 409,
        'status is 404': (r) => r.status === 404,
        'status is 400': (r) => r.status === 400,
        'status is 429': (r) => r.status === 429,
        'status is 500': (r) => r.status === 500,
    });

}
