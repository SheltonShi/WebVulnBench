# WebVulnBench

WebVulnBench maintains Docker image tags and PoC metadata for vulnerable web
application benchmarks used to evaluate fuzzers, scanners, and LLM-based
security agents.

Docker images are hosted on Docker Hub:

```bash
docker pull sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0
```

## PHP

The current release contains the 10 original PHPBench target applications.
Image tags use the benchmark maintenance version:

```text
phpbench-<application>-v0.1.0
```

| Application | Docker image | Vulns | PoCs |
| --- | --- | ---: | ---: |
| Doctor Appointment Booking System | `sheltonshi/webvulnbench:phpbench-doctorappt-v0.1.0` | 14 | 14 |
| Drupal | `sheltonshi/webvulnbench:phpbench-drupal-v0.1.0` | 26 | 26 |
| Hospital Management System | `sheltonshi/webvulnbench:phpbench-hospmgmt-v0.1.0` | 36 | 36 |
| Joomla | `sheltonshi/webvulnbench:phpbench-joomla-v0.1.0` | 27 | 27 |
| User Registration Login Management | `sheltonshi/webvulnbench:phpbench-loginmgmt-v0.1.0` | 22 | 22 |
| MyBB | `sheltonshi/webvulnbench:phpbench-mybb-v0.1.0` | 42 | 42 |
| OpenEMR | `sheltonshi/webvulnbench:phpbench-openemr-v0.1.0` | 89 | 89 |
| Piwigo | `sheltonshi/webvulnbench:phpbench-piwigo-v0.1.0` | 20 | 20 |
| PrestaShop | `sheltonshi/webvulnbench:phpbench-prestashop-v0.1.0` | 19 | 19 |
| WordPress | `sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0` | 80 | 80 |

Total: 10 applications, 375 vulnerabilities, and 375 verifiable PoCs.
The type split is 278 XSS, 52 SQL injection, and 45 command injection cases.

## Roadmap

WebVulnBench will continue to expand beyond the current PHPBench-derived PHP
targets. Future releases are expected to increase coverage along three axes:

- target application languages and frameworks,
- vulnerability types and exploit patterns,
- the overall number of vulnerabilities, PoCs, and runnable benchmark targets.

The goal is to maintain a growing, Docker-backed benchmark suite with clear
ground truth, reproducible PoCs, and stable metadata for tool evaluation.

## Layout

```text
PHP/
  manifest.json
  <application>/
    metadata.json
    pocs.json
```

`PHP/manifest.json` is the top-level index. Each `metadata.json` stores the
application name, Docker image, source repository, and counts. Each `pocs.json`
stores request-level PoC metadata.

For this release, each PHPBench `vuln_id` has one verifiable PoC, so the
vulnerability count and PoC count are equal.

## Safety

These images intentionally contain known vulnerabilities. Run them only in
isolated benchmark environments.
