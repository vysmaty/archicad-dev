# Python scripting

## Two supported styles

Use the project package for maintained automation:

```python
from archicad_tools import Archicad

client = Archicad.connect()
selected = client.commands.GetSelectedElements()
```

Run it with `uv run python/examples/selected_elements.py`.

For a portable one-file utility, copy `python/templates/script_template.py`. Keep its PEP 723 header and use an exact official package pin:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["archicad==29.3000"]
# ///
```

Run it with `uv run --script path/to/script.py`. Do not manually activate a virtual environment or add ad-hoc installation instructions.

## Authoring workflow

1. Search the generated commands for the connected Archicad version and confirm the signature/return type.
2. Start with a read-only call on a disposable project.
3. Handle `ACConnection.connect()` returning `None`; there is no `.connected` property.
4. Keep selection, lookup, and mutation phases separate.
5. For a model mutation, validate inputs first, report partial failures, and make reruns safe where possible.
6. Add a unit test with a fake connection for reusable logic.

`Archicad.connect()` turns a missing instance into `ArchicadConnectionError`. Its `commands`, `types`, and `utilities` properties remain the official generated objects. `version`, `build`, and `language` expose connection metadata.

## Examples

- `tools/connection_test.py`: self-contained PEP 723 health check
- `python/examples/project_info.py`: official read-only product information
- `python/examples/selected_elements.py`: official selection query
- `python/examples/tapir_version.py`: explicit optional Tapir check

Prefer the official command surface. Move to Tapir only after confirming the operation is absent; see [Tapir](tapir.md).
