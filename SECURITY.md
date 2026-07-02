# Security Policy

WebVulnBench intentionally publishes vulnerable web application images and
request-level PoC metadata for authorized benchmark evaluation.

Use these images only in isolated local or lab environments. Do not expose them
to the public Internet or to shared production networks.

This repository is not the right place to report newly discovered vulnerabilities
in the upstream third-party applications. Report those issues to the relevant
upstream maintainers.

For issues in the WebVulnBench metadata, image tags, or benchmark packaging,
open a GitHub issue with:

- affected application id,
- affected Docker tag,
- affected `vuln_id` when relevant,
- expected behavior,
- observed behavior,
- enough reproduction detail to validate the issue.
