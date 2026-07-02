# Joomla

| Field | Value |
| --- | --- |
| Application ID | joomla |
| Docker image | `sheltonshi/webvulnbench:phpbench-joomla-v0.1.0` |
| Source | https://github.com/joomla/joomla-cms |
| Vulnerability count | 27 |
| PoC count | 27 |
| Vulnerability types | cmdi: 3, sqli: 6, xss: 18 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
