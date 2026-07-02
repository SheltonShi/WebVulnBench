# Hospital Management System

| Field | Value |
| --- | --- |
| Application ID | hospmgmt |
| Docker image | `sheltonshi/webvulnbench:phpbench-hospmgmt-v0.1.0` |
| Source | https://phpgurukul.com/hospital-management-system-in-php |
| Vulnerability count | 36 |
| PoC count | 36 |
| Vulnerability types | cmdi: 3, sqli: 4, xss: 29 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
