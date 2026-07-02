# MyBB

| Field | Value |
| --- | --- |
| Application ID | mybb |
| Docker image | `sheltonshi/webvulnbench:phpbench-mybb-v0.1.0` |
| Source | https://github.com/mybb/mybb |
| Vulnerability count | 42 |
| PoC count | 42 |
| Vulnerability types | cmdi: 5, sqli: 7, xss: 30 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
