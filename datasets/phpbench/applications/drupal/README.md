# Drupal

| Field | Value |
| --- | --- |
| Application ID | drupal |
| Docker image | `sheltonshi/webvulnbench:phpbench-drupal-v0.1.0` |
| Source | https://github.com/drupal/drupal |
| Vulnerability count | 26 |
| PoC count | 26 |
| Vulnerability types | cmdi: 3, sqli: 4, xss: 19 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
