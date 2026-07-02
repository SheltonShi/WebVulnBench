# WebVulnBench

WebVulnBench is a Docker-backed benchmark collection of intentionally vulnerable
web applications for black-box evaluation of fuzzers, scanners, and LLM-based
security agents.

This repository is the public maintenance and metadata home for the benchmark:
it tracks image names, application inventory, vulnerability counts, and
request-level PoC ground truth. Docker image layers are hosted separately on
Docker Hub:

```bash
docker pull sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0
```

## Current Release

The initial release exports the 10 original PHPBench target applications.
Image tags use the benchmark maintenance version, not the upstream application
version:

```text
phpbench-<application>-v0.1.0
```

| Application | Docker image | Vulns | PoCs | XSS | SQLi | CMDi |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Doctor Appointment Booking System | `sheltonshi/webvulnbench:phpbench-doctorappt-v0.1.0` | 14 | 14 | 9 | 4 | 1 |
| Drupal | `sheltonshi/webvulnbench:phpbench-drupal-v0.1.0` | 26 | 26 | 19 | 4 | 3 |
| Hospital Management System | `sheltonshi/webvulnbench:phpbench-hospmgmt-v0.1.0` | 36 | 36 | 29 | 4 | 3 |
| Joomla | `sheltonshi/webvulnbench:phpbench-joomla-v0.1.0` | 27 | 27 | 18 | 6 | 3 |
| User Registration Login Management | `sheltonshi/webvulnbench:phpbench-loginmgmt-v0.1.0` | 22 | 22 | 19 | 1 | 2 |
| MyBB | `sheltonshi/webvulnbench:phpbench-mybb-v0.1.0` | 42 | 42 | 30 | 7 | 5 |
| OpenEMR | `sheltonshi/webvulnbench:phpbench-openemr-v0.1.0` | 89 | 89 | 62 | 13 | 14 |
| Piwigo | `sheltonshi/webvulnbench:phpbench-piwigo-v0.1.0` | 20 | 20 | 15 | 2 | 3 |
| PrestaShop | `sheltonshi/webvulnbench:phpbench-prestashop-v0.1.0` | 19 | 19 | 16 | 1 | 2 |
| WordPress | `sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0` | 80 | 80 | 61 | 10 | 9 |

Total: 10 applications, 375 vulnerabilities, and 375 verifiable PoCs.
The type split is 278 XSS, 52 SQL injection, and 45 command injection cases.

For PHPBench `v0.1.0`, each native `Verifiable_PoCs.json` key is treated as one
stable vulnerability id. Each vulnerability id has one verifiable PoC in this
release, so the vulnerability count and PoC count are equal.

## Repository Layout

- `datasets/phpbench/manifest.json`: machine-readable dataset summary and
  per-application index.
- `datasets/phpbench/applications/<application>/metadata.json`: application
  inventory, Docker image, source repository, and counts.
- `datasets/phpbench/applications/<application>/pocs.json`: request-level PoC
  ground truth.
- `datasets/phpbench/applications/<application>/README.md`: human-readable
  application summary.
- `docs/docker-images.md`: DockerHub image policy and tag inventory.
- `docs/maintenance.md`: release and expansion checklist.
- `tools/export_phpbench_pocs.py`: regenerates exported metadata from the native
  PHPBench artifact.
- `tools/validate_manifest.py`: checks that manifest, metadata, and PoC files
  stay internally consistent.

## PoC Schema

Each PoC entry contains:

- `vuln_id`: stable PHPBench vulnerability identifier.
- `application`: short application id used in the Docker tag.
- `docker_image`: Docker Hub image containing the vulnerable application.
- `source_repository`: upstream target-application source reference from the
  PHPBench artifact.
- `vuln_type`: `xss`, `sqli`, or `cmdi`.
- `method`: HTTP method.
- `path`: target HTTP path.
- `query_params`: query parameter values for the PoC request.
- `post_data`: POST body parameter values for the PoC request.
- `request_id`: original PHPBench request id when available.

This repository intentionally stores request-level PoC metadata only. Code-level
insertion locations are not part of the initial public metadata release.

## Validation

Run the consistency check before committing metadata changes:

```bash
python3 tools/validate_manifest.py
```

To regenerate the PHPBench export from a local checkout that has
`PHPBench_Artifact` next to this repository:

```bash
python3 tools/export_phpbench_pocs.py
python3 tools/validate_manifest.py
```

## Safety

These images intentionally contain known vulnerabilities. Run them only in
isolated benchmark environments, never on a shared or production network.
