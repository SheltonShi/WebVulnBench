# User Registration Login Management

| Field | Value |
| --- | --- |
| Application ID | loginmgmt |
| Docker image | `sheltonshi/webvulnbench:phpbench-loginmgmt-v0.1.0` |
| Source | https://phpgurukul.com/user-registration-login-and-user-management-system-with-admin-panel/ |
| Vulnerability count | 22 |
| PoC count | 22 |
| Vulnerability types | cmdi: 2, sqli: 1, xss: 19 |

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
