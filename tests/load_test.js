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
        http_req_duration: ['avg < 200', 'p(90) < 400', 'p(95) < 600'], 
    },
};

export default function () {
    const url = `${__ENV.URL}`;
    const systolic = getRandomNum(70, 190);
    const diastolic = getRandomNum(40, systolic);
    let res = http.get(url);
    sleep(1);
    res = res.submitForm({
        fields: {
            bpsystolic: systolic.toString(),
            bpdiastolic: diastolic.toString()
        }
    });
};
