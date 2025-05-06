## Usage

Add knowledge:

```bash
uv run main.py knowledge add -n "namespace" \
  "https://example.com" \
  "./path/to/file"
```

> Depending on type and size of sources, performance can vary

Run chat:

```bash
uv run main.py chat -n "namespace"
```

or with custom preset/instructions for the agent:

```bash
uv run main.py chat -n "namespace" -i "path_to_text_file"
```
