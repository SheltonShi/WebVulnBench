# Piwigo

| Field | Value |
| --- | --- |
| Application ID | piwigo |
| Docker image | `sheltonshi/webvulnbench:phpbench-piwigo-v0.1.0` |
| Source | https://github.com/Piwigo/Piwigo |
| Vulnerability count | 20 |
| PoC count | 20 |
| Vulnerability types | cmdi: 3, sqli: 2, xss: 15 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
