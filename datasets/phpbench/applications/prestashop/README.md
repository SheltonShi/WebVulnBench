# PrestaShop

| Field | Value |
| --- | --- |
| Application ID | prestashop |
| Docker image | `sheltonshi/webvulnbench:phpbench-prestashop-v0.1.0` |
| Source | https://github.com/PrestaShop/PrestaShop |
| Vulnerability count | 19 |
| PoC count | 19 |
| Vulnerability types | cmdi: 2, sqli: 1, xss: 16 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
