## Usage

Add knowledge:

```bash
uv run main.py knowledge add -n "namespace" \
  "https://fastapi.tiangolo.com" \
  "https://fastapi.tiangolo.com/features" \
  "https://fastapi.tiangolo.com/release-notes"
```

Docling supported [formats](https://docling-project.github.io/docling/usage/supported_formats/).

> Depending on type and size of sources, performance can vary

Run chat:

```bash
uv run main.py chat -n "namespace"
```

or with custom preset/instructions for the agent:

```bash
uv run main.py chat -n "namespace" -i "path_to_text_file"
```
<img width="830" alt="Screenshot 2025-05-06 at 11 51 24" src="https://github.com/user-attachments/assets/c76b3933-31e7-4f67-89a8-0704164e4c56" />
