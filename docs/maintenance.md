# Maintenance Guide

This repository is the operational source of truth for WebVulnBench metadata.
Docker image layers live on Docker Hub; this repo tracks what those images
contain and how the benchmark should be counted.

## Release Checklist

1. Build and upload the Docker images to Docker Hub.
2. Confirm that each image tag follows the release tag policy.
3. Export or update request-level PoC metadata.
4. Verify application counts, vulnerability counts, PoC counts, and type counts.
5. Run the repository validator.
6. Commit the metadata update and tag the GitHub release.

Validation command:

```bash
python3 tools/validate_manifest.py
```

## Regenerating PHPBench Metadata

The current PHPBench export is generated from the native artifact layout:

```text
PHPBench_Artifact/Constructed_Benchmark/Verifiable_PoCs/Verifiable_PoCs.json
PHPBench_Artifact/Constructed_Benchmark/Target_Application_Dataset/Target_Application_Dataset.json
```

When `PHPBench_Artifact` is checked out next to this repository, regenerate with:

```bash
python3 tools/export_phpbench_pocs.py
python3 tools/validate_manifest.py
```

## Counting Rules

For PHPBench `v0.1.0`, each key in the native `Verifiable_PoCs.json` file is one
stable `vuln_id`. Each exported `vuln_id` has one verifiable request-level PoC.

That means:

```text
vulnerability_count == poc_count
```

If a future dataset version allows multiple PoCs for one vulnerability, keep both
fields and update the counting rule in `manifest.json`, `README.md`, and this
guide.

## Expanding the Benchmark

For each new application or vulnerability batch:

1. Preserve the original vulnerable sample, normal input, PoC input, and oracle.
2. Build a reproducible vulnerable Docker image.
3. Assign a stable application id for image tags and metadata paths.
4. Export request-level PoC metadata into `datasets/<dataset>/...`.
5. Add source references for target applications.
6. Recompute all aggregate counts from data, not by hand.
7. Run validation before release.

High-quality additions should include vulnerable code, a normal input that
reaches the sink, a PoC input, a vulnerability label, and a stable verification
oracle. A payload alone is not enough for benchmark maintenance.
