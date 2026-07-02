#!/usr/bin/env python3
"""Validate WebVulnBench dataset manifests and per-application PoC files."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "datasets" / "phpbench" / "manifest.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    manifest = load_json(MANIFEST)
    applications = manifest.get("applications", {})
    expect(isinstance(applications, dict), "manifest applications must be an object")

    all_pocs = []
    app_counts = {}
    app_type_counts = {}

    for app, metadata in sorted(applications.items()):
        pocs_file = ROOT / metadata["pocs_file"]
        metadata_file = pocs_file.with_name("metadata.json")

        expect(pocs_file.exists(), f"missing PoC file for {app}: {pocs_file}")
        expect(metadata_file.exists(), f"missing metadata file for {app}: {metadata_file}")

        app_metadata = load_json(metadata_file)
        pocs = load_json(pocs_file)
        expect(isinstance(pocs, list), f"{pocs_file} must contain a list")

        for poc in pocs:
            expect(poc.get("application") == app, f"{pocs_file} contains PoC for another application")
            expect(poc.get("docker_image") == metadata["docker_image"], f"{poc.get('vuln_id')} docker_image mismatch")
            expect(poc.get("vuln_id"), f"{pocs_file} contains PoC without vuln_id")
            expect(poc.get("vuln_type") in {"xss", "sqli", "cmdi"}, f"{poc.get('vuln_id')} has unknown vuln_type")
            expect(poc.get("method") in {"GET", "POST"}, f"{poc.get('vuln_id')} has unknown HTTP method")

        type_counts = Counter(poc["vuln_type"] for poc in pocs)
        app_counts[app] = len(pocs)
        app_type_counts[app] = dict(sorted(type_counts.items()))
        all_pocs.extend(pocs)

        for key in ("poc_count", "vulnerability_count"):
            expect(metadata.get(key) == len(pocs), f"manifest {app}.{key} does not match pocs.json")
            expect(app_metadata.get(key) == len(pocs), f"metadata {app}.{key} does not match pocs.json")

        expect(metadata.get("vuln_type_counts") == app_type_counts[app], f"manifest {app}.vuln_type_counts mismatch")
        expect(app_metadata.get("vuln_type_counts") == app_type_counts[app], f"metadata {app}.vuln_type_counts mismatch")

    vuln_ids = [poc["vuln_id"] for poc in all_pocs]
    duplicate_ids = sorted(vuln_id for vuln_id, count in Counter(vuln_ids).items() if count > 1)
    expect(not duplicate_ids, f"duplicate vuln_id values: {', '.join(duplicate_ids[:10])}")

    total_type_counts = dict(sorted(Counter(poc["vuln_type"] for poc in all_pocs).items()))
    expect(manifest.get("total_applications") == len(applications), "manifest total_applications mismatch")
    expect(manifest.get("total_pocs") == len(all_pocs), "manifest total_pocs mismatch")
    expect(manifest.get("total_vulnerabilities") == len(set(vuln_ids)), "manifest total_vulnerabilities mismatch")
    expect(manifest.get("vuln_type_counts") == total_type_counts, "manifest vuln_type_counts mismatch")

    print(
        "Validated "
        f"{manifest.get('dataset')} {manifest.get('dataset_release')}: "
        f"{len(applications)} applications, {len(set(vuln_ids))} vulnerabilities, {len(all_pocs)} PoCs"
    )


if __name__ == "__main__":
    main()
