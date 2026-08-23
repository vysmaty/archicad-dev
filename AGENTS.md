# Archicad Add-On development guide

## Scope

This repository builds a Windows x64 Archicad C++ Add-On for **Archicad 27, 28, and 29**. Do not lower the compatibility floor without an explicit decision.

## Non-negotiable constraints

- Keep `external/archicad-addon-cmake-tools` as the official Graphisoft CMake tooling submodule. Do not copy its files into this repository.
- Do not commit anything beneath `third_party/devkits/`, build directories, `.apx` files, or local CMake presets.
- A build targets exactly one Archicad major version. Do not link libraries or headers across versions.
- Use `AC_VERSION` and `AC_API_DEVKIT_DIR` supplied by the selected CMake preset/wrapper. The DevKit path must end in `Support`.
- Windows is the supported platform and all shipped artifacts are x64.
- Toolset mapping is intentional: AC27/AC28 use `v142`; AC29 uses `v143`.

## Working conventions

- C++ follows the API patterns in `src/`; keep callbacks small and return Graphisoft error codes.
- Resource identifiers live in `src/ResourceIds.hpp`; matching resource text lives in `RINT/AddOn.grc`.
- Use `uv run tools/<script>.py`, never a manually activated virtual environment. Standalone Python tools must retain PEP 723 metadata.
- Make version or upstream changes in `archicad-dev.yaml` first, then update documentation and CI if needed.
- Do not use real MDIDs for example or local builds. Distribution requires IDs issued by Graphisoft.

## Validation

Before declaring a change ready, run the applicable checks:

```powershell
uv run ruff check tools
uv run ruff format --check tools
uv run tools/devkit.py validate
cmake --list-presets
```

If a DevKit is installed, also build the requested version:

```powershell
.\tools\build.ps1 -Version 29 -Configuration Release
```

## Upstream references

- [Graphisoft CMake template](https://github.com/GRAPHISOFT/archicad-addon-cmake)
- [Graphisoft CMake tools](https://github.com/GRAPHISOFT/archicad-addon-cmake-tools)
- [Graphisoft API DevKit releases](https://github.com/GRAPHISOFT/archicad-api-devkit/releases)
- [Tapir automation](https://github.com/ENZYME-APD/tapir-archicad-automation)
