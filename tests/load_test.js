import http from 'k6/http';
import { sleep } from 'k6';

function getRandomNum(min, max) {
    return Math.random() * (max - min) + min;
};

export const options = {
    stages: [
        { duration: '30s', target: 200 },
        { duration: '1m', target: 200 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate < 0.01'],
        http_req_duration: ['avg < 100', 'p(90) < 200', 'p(95) < 300'], 
    },
};

export default function () {
    const url = `${__ENV.URL}`;
    const systolic = getRandomNum(70, 190);
    const diastolic = getRandomNum(40, systolic);
    const payload = JSON.stringify({
        bpsystolic: systolic.toString(),
        bpdiastolic: diastolic.toString(),
    });
    const params = {
        headers: {
          'Content-Type': 'application/json',
        },
    };
    http.get(url);
    sleep(1);
    http.post(url, payload, params);
};
