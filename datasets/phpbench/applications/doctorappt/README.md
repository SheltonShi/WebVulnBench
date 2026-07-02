# Doctor Appointment Booking System

| Field | Value |
| --- | --- |
| Application ID | doctorappt |
| Docker image | `sheltonshi/webvulnbench:phpbench-doctorappt-v0.1.0` |
| Source | https://projectworlds.in/free-projects/php-projects/online-doctor-appointment-booking-system-php-and-mysql |
| Vulnerability count | 14 |
| PoC count | 14 |
| Vulnerability types | cmdi: 1, sqli: 4, xss: 9 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
