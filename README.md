# archicad-dev

Windows-first development foundation for Archicad 27, 28, and 29. It combines a minimal multi-version C++ Add-On, Graphisoft's official CMake tooling, an `uv`-managed Python package, and optional Tapir commands without committing any API Development Kit or downloaded Add-On binary.

## Included

- Six CMake presets: AC27/28/29 × Debug/Release, targeting Windows x64
- Official `GRAPHISOFT/archicad-addon-cmake-tools` as a pinned Git submodule
- Exact DevKit pins and download URLs in `archicad-dev.yaml`
- A small C++ compatibility boundary under `src/compat/`
- `archicad_tools`, a tested wrapper around Graphisoft's official Python package
- PEP 723 script template, connection test, read-only examples, and optional Tapir bootstrap
- CI for all six C++ builds plus Ruff, ty, pytest/coverage, and package build
- Weekly upstream update proposals that always require pull-request review
- AI-agent rules in `AGENTS.md` and a `CLAUDE.md` compatibility bridge

## Quick start

```powershell
git clone --recurse-submodules https://github.com/vysmaty/archicad-dev.git
cd archicad-dev
uv sync --all-groups
.\tools\bootstrap.ps1 -Version 29
.\tools\build.ps1 -Version 29 -Configuration Debug
```

Run a read-only Python connection check while Archicad and a project are open:

```powershell
uv run --script tools/connection_test.py
uv run python/examples/project_info.py
```

To use Tapir, download the exact verified binary and then add the printed `.apx` through **Options → Add-On Manager**:

```powershell
uv run --script tools/tapir.py install 29
uv run python/examples/tapir_version.py
```

## Repository map

```text
src/                         C++ Add-On and compatibility boundary
python/src/archicad_tools/   Reusable Python wrapper
python/examples/             Runnable official API and Tapir examples
python/templates/            Copyable PEP 723 script template
tools/                       Bootstrap, build, update, and connection tools
docs/                        Architecture and development guidance
external/                    Pinned Graphisoft CMake tools submodule
third_party/                 Local DevKits/Tapir downloads; ignored by Git
archicad-dev.yaml            Source of truth for support and upstream pins
```

## Choose the smallest API

1. Use Graphisoft's official Python commands when they expose the operation.
2. Use Tapir when its documented command fills the gap and installing Tapir is acceptable.
3. Extend the C++ Add-On only for native events, UI, performance, or capabilities unavailable through JSON commands.

There is no silent fallback between these layers. See [Python scripting](docs/python-scripting.md), [Tapir](docs/tapir.md), and [architecture](docs/architecture.md).

## Documentation

- [Windows development setup](docs/development-setup.md)
- [Compatibility and API capability matrix](docs/compatibility.md)
- [Architecture and API selection](docs/architecture.md)
- [Python scripting guide](docs/python-scripting.md)
- [Tapir setup and command authoring](docs/tapir.md)
- [Developer ID, Local ID, and distribution](docs/developer-id.md)
- [Testing and release checks](docs/testing.md)

## Upstreams

This repository is independent rather than a fork. The template is a reference, the CMake tools are a pinned submodule, DevKits and Tapir are pinned downloads, and all updates are reviewed.

- [Graphisoft Archicad Add-On CMake template](https://github.com/GRAPHISOFT/archicad-addon-cmake)
- [Graphisoft Archicad Add-On CMake tools](https://github.com/GRAPHISOFT/archicad-addon-cmake-tools)
- [Graphisoft Archicad API DevKit releases](https://github.com/GRAPHISOFT/archicad-api-devkit/releases)
- [Tapir Archicad automation](https://github.com/ENZYME-APD/tapir-archicad-automation)

Graphisoft DevKits remain subject to Graphisoft's licence. Tapir is optional and keeps its own licence.
