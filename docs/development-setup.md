# Windows development setup

## Prerequisites

- Windows 10/11 x64
- Visual Studio 2022 with **Desktop development with C++**, MSVC v142, MSVC v143, and a Windows SDK
- CMake 3.23 or newer
- Git, Python 3.11 or newer, and [uv](https://docs.astral.sh/uv/)
- Archicad 27, 28, or 29 for runtime testing

Clone the repository with the official CMake tools submodule and create the locked Python environment:

```powershell
git clone --recurse-submodules https://github.com/vysmaty/archicad-dev.git
cd archicad-dev
uv sync --all-groups --locked
```

If the repository was cloned without submodules, run `git submodule update --init --recursive`.

## Download a pinned DevKit

The manifest pins one official Windows archive per supported major. The bootstrap verifies the expected archive structure and stores it under the ignored `third_party/devkits/` directory:

```powershell
.\tools\bootstrap.ps1 -Version 27
.\tools\bootstrap.ps1 -Version 28
.\tools\bootstrap.ps1 -Version 29
```

DevKits are licensed by Graphisoft and are never added to Git.

## Configure and build

Use the wrapper for normal work:

```powershell
.\tools\build.ps1 -Version 29 -Configuration Debug
.\tools\build.ps1 -Version 27 -Configuration Release
```

Or use a named preset after setting `AC_API_DEVKIT_DIR` to that DevKit's `Support` directory:

```powershell
$env:AC_API_DEVKIT_DIR = "C:\path\to\AC29\Support"
cmake --preset ac29-debug
cmake --build --preset ac29-debug
```

Load the resulting `.apx` only into the matching Archicad major through **Options → Add-On Manager**. An AC29 binary cannot be used by AC28.

## Python automation

Open a project in Archicad, then run:

```powershell
uv run --script tools/connection_test.py
uv run python/examples/project_info.py
uv run python/examples/selected_elements.py
```

See [Python scripting](python-scripting.md). Tapir installation is separate and optional; see [Tapir](tapir.md).

## Common setup failures

- **CMake cannot find Visual Studio 17 2022:** install the C++ workload and use a Windows 2022 GitHub runner. The repository intentionally does not use `windows-latest`.
- **Requested toolset is missing:** install v142 for AC27/28 or v143 for AC29 from Visual Studio Installer.
- **DevKit path rejected:** point `AC_API_DEVKIT_DIR` at the archive's `Support` directory, not its parent.
- **Python cannot connect:** start Archicad, open a project, and confirm no firewall or duplicate instance is occupying the selected port.
- **Tapir namespace unavailable:** install the matching verified Tapir `.apx` and restart/reload Archicad.

Do not distribute local output. Follow [Developer ID and distribution](developer-id.md) first.
