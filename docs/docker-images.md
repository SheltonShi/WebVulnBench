# Docker Images

WebVulnBench Docker images are published under:

```text
sheltonshi/webvulnbench
```

The first PHPBench batch uses benchmark maintenance tags:

```text
phpbench-<application>-v0.1.0
```

The `v0.1.0` suffix is the WebVulnBench/PHPBench image maintenance version. It
does not encode the upstream application version.

## PHPBench v0.1.0 Inventory

| Application ID | Image tag |
| --- | --- |
| `doctorappt` | `sheltonshi/webvulnbench:phpbench-doctorappt-v0.1.0` |
| `drupal` | `sheltonshi/webvulnbench:phpbench-drupal-v0.1.0` |
| `hospmgmt` | `sheltonshi/webvulnbench:phpbench-hospmgmt-v0.1.0` |
| `joomla` | `sheltonshi/webvulnbench:phpbench-joomla-v0.1.0` |
| `loginmgmt` | `sheltonshi/webvulnbench:phpbench-loginmgmt-v0.1.0` |
| `mybb` | `sheltonshi/webvulnbench:phpbench-mybb-v0.1.0` |
| `openemr` | `sheltonshi/webvulnbench:phpbench-openemr-v0.1.0` |
| `piwigo` | `sheltonshi/webvulnbench:phpbench-piwigo-v0.1.0` |
| `prestashop` | `sheltonshi/webvulnbench:phpbench-prestashop-v0.1.0` |
| `wordpress` | `sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0` |

## Maintenance Rules

- Keep Docker layers out of this repository.
- Keep Docker image names in `datasets/phpbench/manifest.json` and
  `README.md` aligned.
- Use a new benchmark maintenance version when an image is rebuilt in a way that
  can change benchmark behavior.
- Do not add upstream application versions to tags unless the project adopts a
  new tag policy for a future release.
- After a DockerHub upload is finalized, optionally record immutable manifest
  digests in release notes or a dedicated image index.
