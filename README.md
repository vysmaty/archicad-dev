# Archicad Dev Add-On

Windows-first, multi-version C++ Add-On foundation for **Archicad 27+**. It builds separate x64 binaries for Archicad 27, 28, and 29 using Graphisoft's official CMake tooling and exactly pinned API Development Kits.

## What is included

- Official [`archicad-addon-cmake-tools`](https://github.com/GRAPHISOFT/archicad-addon-cmake-tools) as a pinned Git submodule
- CMake presets for AC27, AC28, and AC29 in Debug and Release
- A minimal Add-On with a Tools-menu command, resource metadata, and API-version compatibility branch
- Pin metadata plus bootstrap and update-check tools; DevKits are always local and ignored by Git
- Python utilities run with [uv](https://docs.astral.sh/uv/) and PEP 723 inline dependencies, including an Archicad connection test
- GitHub Actions matrix builds for all six version/configuration combinations
- Agent-facing project rules in [`AGENTS.md`](AGENTS.md)

## Quick start

```powershell
git submodule update --init --recursive
.\tools\bootstrap.ps1 -Version 29
.\tools\build.ps1 -Version 29 -Configuration Debug
```

See [Windows development setup](docs/development-setup.md) for prerequisites and the [compatibility matrix](docs/compatibility.md) for version details.

## Repository layout

```text
src/                         Minimal C++ Add-On
RINT/                        INT resources and MDID placeholder
external/                    Pinned Graphisoft CMake tooling submodule
tools/                       uv/PEP 723 bootstrap, update, and connection utilities
third_party/devkits/         Local downloads only (ignored)
archicad-dev.yaml            DevKit pins and upstream metadata
CMakePresets.json            AC27–29 Debug/Release presets
```

## Upstream model

This is an independent repository, not a fork of the CMake template. `archicad-addon-cmake-tools` is versioned through a submodule; the template itself is an upstream reference and is not automatically merged. DevKits are pinned by release in `archicad-dev.yaml`, downloaded on demand, and never committed.

References: [Graphisoft CMake template](https://github.com/GRAPHISOFT/archicad-addon-cmake), [Graphisoft API DevKit](https://github.com/GRAPHISOFT/archicad-api-devkit), and [Tapir's multi-version automation project](https://github.com/ENZYME-APD/tapir-archicad-automation).

## Maintenance

```powershell
uv run tools/check_updates.py
```

Review the output, DevKit release notes, and all three builds before changing a pin. Distribution needs Graphisoft-issued MDIDs; the included placeholders are only for local development.
