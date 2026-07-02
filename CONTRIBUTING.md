# Contributing

Contributions should keep benchmark metadata reproducible and countable.

Before opening a pull request:

1. Update generated metadata from the source artifact when possible.
2. Do not edit aggregate counts by hand unless the source format itself changed.
3. Run:

```bash
python3 tools/validate_manifest.py
```

For new benchmark cases, include:

- vulnerable source or a precise source reference,
- vulnerability type,
- normal input,
- PoC input,
- verification oracle,
- Docker image tag,
- application-level metadata.

Do not commit Docker image layers, credentials, API keys, or DockerHub access
tokens.
