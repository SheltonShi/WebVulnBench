# OpenEMR

| Field | Value |
| --- | --- |
| Application ID | openemr |
| Docker image | `sheltonshi/webvulnbench:phpbench-openemr-v0.1.0` |
| Source | https://github.com/openemr/openemr |
| Vulnerability count | 89 |
| PoC count | 89 |
| Vulnerability types | cmdi: 14, sqli: 13, xss: 62 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
