# WordPress

| Field | Value |
| --- | --- |
| Application ID | wordpress |
| Docker image | `sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0` |
| Source | https://github.com/WordPress/WordPress |
| Vulnerability count | 80 |
| PoC count | 80 |
| Vulnerability types | cmdi: 9, sqli: 10, xss: 61 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
