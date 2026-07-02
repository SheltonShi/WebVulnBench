#!/usr/bin/env python3
"""Export PHPBench native PoC metadata into GitHub-ready files."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT.parent / "PHPBench_Artifact"
POC_SOURCE = SOURCE_ROOT / "Constructed_Benchmark" / "Verifiable_PoCs" / "Verifiable_PoCs.json"
TARGET_SOURCE = (
    SOURCE_ROOT
    / "Constructed_Benchmark"
    / "Target_Application_Dataset"
    / "Target_Application_Dataset.json"
)
OUTPUT_ROOT = ROOT / "datasets" / "phpbench"
DOCKERHUB_REPOSITORY = "sheltonshi/webvulnbench"
DATASET_VERSION = "v0.1.0"
SOURCE_ARTIFACT = "PHPBench_Artifact/Constructed_Benchmark"


APP_SOURCE_KEYS = {
    "doctorappt": "doctor.appt",
    "hospmgmt": "hosp.mgmt",
    "loginmgmt": "login.mgmt",
}


APP_DISPLAY_NAMES = {
    "doctorappt": "Doctor Appointment Booking System",
    "drupal": "Drupal",
    "hospmgmt": "Hospital Management System",
    "joomla": "Joomla",
    "loginmgmt": "User Registration Login Management",
    "mybb": "MyBB",
    "openemr": "OpenEMR",
    "piwigo": "Piwigo",
    "prestashop": "PrestaShop",
    "wordpress": "WordPress",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def docker_image(app: str) -> str:
    return f"{DOCKERHUB_REPOSITORY}:phpbench-{app}-{DATASET_VERSION}"


def markdown_table(rows: list[tuple[str, str]]) -> str:
    lines = ["| Field | Value |", "| --- | --- |"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def write_app_readme(app_dir: Path, app: str, app_metadata: dict) -> None:
    type_counts = ", ".join(
        f"{name}: {count}" for name, count in sorted(app_metadata["vuln_type_counts"].items())
    )
    content = f"""# {app_metadata["name"]}

{markdown_table([
    ("Application ID", app),
    ("Docker image", f'`{app_metadata["docker_image"]}`'),
    ("Source", app_metadata.get("source_repository", "")),
    ("Vulnerability count", str(app_metadata["vulnerability_count"])),
    ("PoC count", str(app_metadata["poc_count"])),
    ("Vulnerability types", type_counts),
])}

## Files

- `metadata.json`: application-level metadata.
- `pocs.json`: PHPBench native PoC ground truth for this application.

Each PoC entry includes the stable `vuln_id`, vulnerability type, HTTP method, path, query parameters, and POST data.
For PHPBench `v0.1.0`, each exported `vuln_id` has one verifiable PoC, so the vulnerability count and PoC count are equal.
"""
    (app_dir / "README.md").write_text(content, encoding="utf-8")


def normalized_poc(vuln_id: str, raw: dict, source_repositories: dict[str, str]) -> dict:
    app = raw["project"]
    source_key = APP_SOURCE_KEYS.get(app, app)
    return {
        "vuln_id": vuln_id,
        "dataset": "phpbench",
        "application": app,
        "application_name": APP_DISPLAY_NAMES.get(app, app),
        "docker_image": docker_image(app),
        "source_repository": source_repositories.get(source_key, ""),
        "vuln_type": raw["vuln_type"],
        "method": raw["req_type"].upper(),
        "path": raw["path"],
        "query_params": raw.get("query_params", {}),
        "post_data": raw.get("post_data", {}),
        "request_id": raw.get("request_id", ""),
        "source_file": f"{SOURCE_ARTIFACT}/Verifiable_PoCs/Verifiable_PoCs.json",
    }


def main() -> None:
    raw_pocs = load_json(POC_SOURCE)
    source_repositories = load_json(TARGET_SOURCE)

    pocs = [
        normalized_poc(vuln_id, raw, source_repositories)
        for vuln_id, raw in sorted(raw_pocs.items())
    ]

    by_app: dict[str, list[dict]] = defaultdict(list)
    for poc in pocs:
        by_app[poc["application"]].append(poc)

    app_manifest = {}
    for app, app_pocs in sorted(by_app.items()):
        type_counts = Counter(poc["vuln_type"] for poc in app_pocs)
        app_dir = OUTPUT_ROOT / "applications" / app
        app_path = app_dir / "pocs.json"
        app_metadata = {
            "application": app,
            "name": APP_DISPLAY_NAMES.get(app, app),
            "docker_image": docker_image(app),
            "source_repository": app_pocs[0].get("source_repository", ""),
            "vulnerability_count": len(app_pocs),
            "poc_count": len(app_pocs),
            "vuln_type_counts": dict(sorted(type_counts.items())),
            "pocs_file": str(app_path.relative_to(ROOT)),
        }
        dump_json(app_path, app_pocs)
        dump_json(app_dir / "metadata.json", app_metadata)
        write_app_readme(app_dir, app, app_metadata)
        app_manifest[app] = app_metadata

    all_types = Counter(poc["vuln_type"] for poc in pocs)
    manifest = {
        "schema_version": "0.1.0",
        "dataset": "PHPBench",
        "dataset_release": DATASET_VERSION,
        "source_artifact": SOURCE_ARTIFACT,
        "source_files": {
            "pocs": f"{SOURCE_ARTIFACT}/Verifiable_PoCs/Verifiable_PoCs.json",
            "target_applications": f"{SOURCE_ARTIFACT}/Target_Application_Dataset/Target_Application_Dataset.json",
        },
        "dockerhub_repository": DOCKERHUB_REPOSITORY,
        "docker_tag_template": "phpbench-{application}-v0.1.0",
        "total_applications": len(app_manifest),
        "total_vulnerabilities": len({poc["vuln_id"] for poc in pocs}),
        "total_pocs": len(pocs),
        "counting_method": (
            "Each native PHPBench Verifiable_PoCs key is treated as one stable vulnerability id. "
            "For this release, each vulnerability id has one verifiable PoC, so total_vulnerabilities equals total_pocs."
        ),
        "ground_truth_scope": "HTTP request-level PoC metadata only; code-level insertion locations are not included in this repository.",
        "vuln_type_counts": dict(sorted(all_types.items())),
        "applications": app_manifest,
        "layout": "datasets/phpbench/applications/{application}/pocs.json",
    }

    dump_json(OUTPUT_ROOT / "manifest.json", manifest)

    print(f"Exported {len(pocs)} PHPBench PoCs into {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
