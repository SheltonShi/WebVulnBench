# WebVulnBench

WebVulnBench maintains Docker image tags and PoC metadata for vulnerable web
application benchmarks used to evaluate fuzzers, scanners, and LLM-based
security agents.

Docker images are hosted on Docker Hub (https://hub.docker.com/r/sheltonshi/webvulnbench), for example:

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
| OpenEMR | `sheltonshi/webvulnbench:phpbench-openemr-v0.1.0` | 89 | 89 |
| WordPress | `sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0` | 80 | 80 |
| MyBB | `sheltonshi/webvulnbench:phpbench-mybb-v0.1.0` | 42 | 42 |
| Hospital Management System | `sheltonshi/webvulnbench:phpbench-hospmgmt-v0.1.0` | 36 | 36 |
| Joomla | `sheltonshi/webvulnbench:phpbench-joomla-v0.1.0` | 27 | 27 |
| Drupal | `sheltonshi/webvulnbench:phpbench-drupal-v0.1.0` | 26 | 26 |
| User Registration Login Management | `sheltonshi/webvulnbench:phpbench-loginmgmt-v0.1.0` | 22 | 22 |
| Piwigo | `sheltonshi/webvulnbench:phpbench-piwigo-v0.1.0` | 20 | 20 |
| PrestaShop | `sheltonshi/webvulnbench:phpbench-prestashop-v0.1.0` | 19 | 19 |
| Doctor Appointment Booking System | `sheltonshi/webvulnbench:phpbench-doctorappt-v0.1.0` | 14 | 14 |
| Total | - | 375 | 375 |

Total: 10 applications, 375 vulnerabilities, and 375 verifiable PoCs.
The type split is 278 XSS, 52 SQL injection, and 45 command injection cases.

## Roadmap

WebVulnBench will continue to expand beyond the current PHPBench-derived PHP
targets. Future releases are expected to increase coverage along three axes:

- Application language types (e.g., Java and Golang),
- Vulnerability types (e.g., Broken Access Control),
- Scale, including the number of vulnerabilities and benchmark targets.

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

## CAGE Evaluation

WebVulnBench can also be used with
[CAGE](https://github.com/AgentCyberRange/CAGE) to evaluate autonomous security
agents against live, vulnerable web applications.

CAGE is the evaluation harness. WebVulnBench supplies the benchmark targets:
Docker images, request-level PoC metadata, and vulnerability ground truth. The
CAGE adapter turns those targets into runnable CAGE samples, launches each web
application in an isolated Docker Compose environment, records the agent's
model and tool activity, and scores whether the agent actually finds and
exploits the known vulnerabilities.

The evaluation is black-box from the agent's perspective. The agent receives
the target URL and must explore the web application over HTTP. Vulnerability
IDs, official PoCs, and verifier logic are kept on the evaluator side.

### Prerequisites

- Docker Engine or Docker Desktop with Docker Compose v2
- Python 3.11+
- `uv`
- A CAGE-supported coding agent image, for example `codex`, `qwen_code`, or
  `claude_code`
- A model API key configured through environment variables

Install CAGE:

```bash
git clone https://github.com/AgentCyberRange/CAGE.git
cd CAGE
uv venv
source .venv/bin/activate
uv pip install -e .
```

Clone WebVulnBench next to CAGE:

```bash
cd ..
git clone https://github.com/SheltonShi/WebVulnBench.git
```

### Configure a Model

CAGE stores model endpoints in `CAGE/config/models.yml`. Keep API keys in
environment variables rather than committing literal secrets.

Example for an OpenAI-compatible endpoint:

```bash
cd CAGE
cp config/models.example.yml config/models.yml
export MODEL_API_KEY=...

cage model set my-openai-compatible-model \
  --provider openai \
  --model <provider-model-name> \
  --endpoint <openai-compatible-base-url> \
  --api-key '${MODEL_API_KEY}'
```

Check that CAGE can see the model:

```bash
cage model list
```

### Generate the CAGE Adapter from PoC JSON

The CAGE adapter and verifier can be generated directly from WebVulnBench's
request-level PoC metadata. The source of truth is:

```text
PHP/<application>/pocs.json
```

Each PoC entry provides the information needed to construct one hidden verifier
case:

- `vuln_id`: stable vulnerability identifier used for scoring
- `vuln_type`: vulnerability class, such as `xss`, `sqli`, or `cmdi`
- `method` and `path`: vulnerable HTTP endpoint
- `query_params` and `post_data`: request parameters and payload values
- `docker_image`: target image used to launch the application

The conversion is mechanical:

1. Read `PHP/manifest.json` and every `PHP/<application>/pocs.json`.
2. Create one CAGE sample per application, using sample ids like
   `phpbench-wordpress`.
3. Generate `challenge.json` for each sample. It should expose only the target
   URL and high-level task to the agent, while keeping `vuln_id` lists and PoC
   details as hidden scoring metadata.
4. Generate `docker-compose.cage.yml` for each sample. It should launch the
   published WebVulnBench Docker image as the `target` service and an
   `evaluator` service with read-only access to the PoC JSON.
5. Generate a shared evaluator that loads the target's PoC JSON, builds one
   verifier case per `vuln_id`, and returns one pass/fail result per
   vulnerability.
6. Generate a CAGE project file such as `cage/default_webvulnbench_php.yml`
   pointing to the generated samples and evaluator.

For each `vuln_id`, the evaluator keeps the expected method, endpoint,
exploit-bearing parameters, and replay payload. The agent only sees the target
URL; the PoC JSON, vulnerable parameters, and verifier logic remain hidden from
the prompt and are mounted only inside the evaluator service.

At evaluation time, the verifier should:

1. read the agent's final report,
2. match reported findings to `vuln_id` candidates by vulnerability type,
   endpoint, and parameter evidence,
3. replay or validate the corresponding PoC request against the live target,
4. return one pass/fail result per `vuln_id`.

For XSS cases, the verifier can additionally check that the injected marker is
reflected or executed in the response context. For SQL injection and command
injection cases, the replay oracle can be strengthened with error-pattern,
differential-response, canary, or side-effect checks when those signals are
available. The request-level PoC remains the canonical mapping from benchmark
metadata to CAGE scoring.

This is a one-time adapter generation step. Once the generated `cage/`
directory is committed to the repository, benchmark users can skip this step
and run CAGE directly. You can ask Codex or another coding agent to generate
the adapter from the repository metadata. 

### Build the Agent and Target Wrappers

Build the agent image you want to evaluate:

```bash
cd CAGE
source .venv/bin/activate
cage agent build --agent qwen_code --variant pentestenv
```

Prepare the WebVulnBench CAGE target wrappers:

```bash
cd ../WebVulnBench
cage/scripts/build-wrappers
```

The first run may pull the target images from Docker Hub, for example:

```bash
docker pull sheltonshi/webvulnbench:phpbench-wordpress-v0.1.0
```

### Smoke Test One Target

Start with a single target before launching the full benchmark.

From the CAGE repository:

```bash
cd ../CAGE
source .venv/bin/activate

cage benchmark check ../WebVulnBench/cage/default_webvulnbench_php.yml \
  --sample phpbench-wordpress \
  --show-prompt
```

Run one pass against WordPress:

```bash
cage run ../WebVulnBench/cage/default_webvulnbench_php.yml \
  --agent qwen_code \
  --model my-openai-compatible-model \
  --sample phpbench-wordpress \
  --passk 1 \
  --max-concurrent 1 \
  --max-rounds 30 \
  --run-id webvulnbench-wordpress-smoke-001
```

### Run the Full PHP Benchmark

The default PHP configuration evaluates all 10 targets. A conservative run uses
one attempt per target and one target at a time:

```bash
cd CAGE
source .venv/bin/activate

cage run ../WebVulnBench/cage/default_webvulnbench_php.yml \
  --agent qwen_code \
  --model my-openai-compatible-model \
  --passk 1 \
  --max-concurrent 1 \
  --max-rounds 30 \
  --run-id webvulnbench-php-10targets-r30-001
```

To evaluate a single target, add `--sample phpbench-<application>`. To evaluate
multiple independent attempts per target, increase `--passk`.

### Results and Scoring

CAGE writes run artifacts under the benchmark output directory, typically:

```text
WebVulnBench/cage/.cage_runs/<agent>:<model>:<mode>/<run-id>/
```

Useful artifacts include trial summaries, scores, full agent trajectories,
proxied LLM request logs, tool-call history, final agent reports, and evaluator
outputs for each vulnerability. CAGE also starts or reuses its local inspector
UI in interactive runs; the run log prints the inspector URL.

Each vulnerability is scored by a verifier derived from the corresponding
`PHP/<application>/pocs.json` entry. A successful hit requires the agent to
report the relevant vulnerability and produce behavior that the evaluator can
match against the known vulnerable endpoint, parameters, and payload semantics.

## Citation

```bibtex
@inproceedings{shi2026phpbench,
  title = {PHPBench: Automated Generation of Verifiable and Hierarchical Benchmarks for PHP Web Fuzzing},
  author = {Shi, Youkun and Zhang, Yuan and Zhang, Lei and Dai, Jiarun and Bai, Tianhao and Liu, Fengyu and Xiang, Bocheng and Luo, Xiapu and Yang, Min},
  booktitle = {Proceedings of the ACM Conference on Computer and Communications Security (ACM CCS 2026)},
  year = {2026}
}
```

## Safety

These images intentionally contain known vulnerabilities. Run them only in
isolated benchmark environments.
