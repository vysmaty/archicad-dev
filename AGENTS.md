# Agent guide for archicad-dev

## Mission and scope

Maintain a Windows x64 foundation for Archicad 27, 28, and 29. Treat `archicad-dev.yaml` as the source of truth. Never add another Archicad major, lower the compatibility floor, enable distribution, or change real MDIDs without an explicit reviewed decision.

## API selection rule

Choose the narrowest sufficient layer in this order:

1. Graphisoft official Python API for documented JSON commands.
2. Tapir for a documented `TapirCommand` absent from the official surface.
3. C++ Add-On code for native hooks, menus, performance-sensitive work, or missing JSON capabilities.

Do not silently fall back from one layer to another. If a task requires Tapir, call `Archicad.connect(require_tapir=True)` or raise a clear error. If a task changes the model, state the mutation and test on a disposable file first.

## Evidence before code

Resolve API details in this order:

1. Headers and documentation in the exact pinned DevKit.
2. Graphisoft's generated `archicad` Python modules for the connected version.
3. Official Graphisoft template/examples.
4. Tapir command documentation and examples when Tapir is selected.
5. Existing repository code and tests.

Never invent an API symbol, parameter, return shape, resource ID, or version guard. Cite the source in code comments only when the compatibility decision would otherwise be unclear.

## C++ rules

- A binary targets exactly one Archicad major and one matching DevKit.
- Put version-sensitive calls in `src/compat/`; do not scatter version checks through features.
- Keep entry points and callbacks small, return Graphisoft error codes, and keep resource IDs in `src/ResourceIds.hpp`.
- AC27/28 use toolset `v142`; AC29 uses `v143`. Shared C++ must compile under the lowest supported standard.
- Keep `AC_ADDON_FOR_DISTRIBUTION=OFF` for local and CI builds.

## Python and script rules

- Manage the project with `uv`; never edit dependency arrays or the lockfile by hand.
- Reusable code belongs in `python/src/archicad_tools/` with public type hints and docstrings.
- A standalone script must include PEP 723 metadata with exact dependency pins. Start from `python/templates/script_template.py`.
- Prefer read-only examples. Put runnable examples in `python/examples/` and tests in `tests/`.
- Keep official API and Tapir calls explicit. Avoid generic wrappers that hide generated Graphisoft types.

## Dependencies and generated content

- Do not commit DevKits, downloaded Tapir binaries, `.apx` files, build output, or local presets.
- Keep `external/archicad-addon-cmake-tools` as a pinned submodule; do not copy or edit its contents for a local workaround.
- Update only the supported majors through `tools/check_updates.py --apply`. A new major is a separate architectural decision.

## Required validation

After changes, run the relevant subset; before a push, run all of it:

```powershell
uv sync --all-groups --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check python/src tools tests python/examples python/templates
uv run pytest --cov=archicad_tools --cov-report=term-missing --cov-fail-under=80
uv build
cmake --list-presets
```

Build every affected Archicad major. A shared C++ change requires AC27, AC28, and AC29 Debug and Release validation in CI.

## Primary references

- https://github.com/GRAPHISOFT/archicad-addon-cmake
- https://github.com/GRAPHISOFT/archicad-addon-cmake-tools
- https://github.com/GRAPHISOFT/archicad-api-devkit
- https://github.com/ENZYME-APD/tapir-archicad-automation
