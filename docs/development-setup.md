# Windows development setup

## Prerequisites

- Windows 10/11 x64
- Visual Studio 2022 with **Desktop development with C++** and both toolsets: MSVC v142 and v143
- CMake 3.23 or newer
- Python 3.11 or newer and [uv](https://docs.astral.sh/uv/)
- Git

The official Graphisoft CMake tooling is checked out as a submodule. Clone with submodules or initialize it once:

```powershell
git clone --recurse-submodules <your-repository-url>
cd <repository-folder>
```

## Install a DevKit

`archicad-dev.yaml` pins the exact released DevKit. The bootstrap script downloads it outside version control and prints the `Support` directory used by CMake:

```powershell
.\tools\bootstrap.ps1 -Version 29
```

Repeat for AC27 or AC28 when needed. The source download is Graphisoft's official API DevKit release and is subject to its licence.

## Configure and build

Use the wrapper to select both a DevKit and matching CMake preset:

```powershell
.\tools\build.ps1 -Version 29 -Configuration Debug
.\tools\build.ps1 -Version 27 -Configuration Release
```

The output is placed below `build/acXX-<configuration>/<configuration>/`. Load the resulting `.apx` using **Options → Add-On Manager** in the matching Archicad version.

For IDE work, set `AC_API_DEVKIT_DIR` to the printed `Support` directory and run `cmake --preset ac29-debug`. Visual Studio can then open the generated solution in `build/ac29-debug`.

## Python connection test

Start Archicad with its Python connection enabled, then run this read-only test:

```powershell
uv run tools/connection_test.py
```

The script has self-contained PEP 723 dependency metadata, so uv resolves its package without a manually managed environment.

## Upstream maintenance

Check every pinned release and the CMake tools checkout:

```powershell
uv run tools/check_updates.py
```

It reports discrepancies but does not rewrite pins. Review DevKit/API changes before changing `archicad-dev.yaml`. To review newer official CMake tooling, update the submodule deliberately, test AC27–29, and then update its commit in the manifest.
