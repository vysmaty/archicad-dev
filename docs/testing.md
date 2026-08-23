# Testing and release checks

## Python and repository contracts

Run the same locked checks as CI:

```powershell
uv sync --all-groups --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check python/src tools tests python/examples python/templates
uv run pytest --cov=archicad_tools --cov-report=term-missing --cov-fail-under=80
uv build
```

Unit tests fake the Archicad connection; they do not need Archicad. Structural tests protect the C++ compatibility boundary, the Windows 2022 runner, all six matrix entries, and the non-merging update workflow.

## C++ matrix

A shared C++ or CMake change is complete only after Debug and Release builds for AC27, AC28, and AC29. GitHub Actions downloads each pinned DevKit into ignored runner storage and publishes the matching `.apx` as a build artifact.

Locally, at minimum build the affected major:

```powershell
.\tools\build.ps1 -Version 29 -Configuration Debug
```

## Runtime smoke test

For each release candidate:

1. load the `.apx` through Add-On Manager in the matching Archicad;
2. confirm the Add-On loads without compatibility warnings;
3. invoke its Tools-menu command;
4. run `uv run --script tools/connection_test.py`;
5. if Tapir is part of the workflow, run `uv run python/examples/tapir_version.py`;
6. perform mutation tests only on a disposable project.

## Upstream review

Run `uv run --script tools/check_updates.py` for a report. The weekly workflow uses `--apply`, but only opens a pull request. Review release notes, manifest diffs, checksum changes, submodule code, and the complete CI matrix before merging.
