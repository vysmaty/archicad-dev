# Compatibility

The repository supports **Windows x64** builds for Archicad 27, 28, and 29. Each binary is compiled independently against the matching, pinned API Development Kit; an `.apx` is not portable between Archicad major versions.

| Archicad | Pinned DevKit | Visual Studio toolset | C++ standard | CMake presets |
| --- | --- | --- | --- | --- |
| 27 | 27.6003 | v142 | C++17 | `ac27-debug`, `ac27-release` |
| 28 | 28.4001 | v142 | C++17 | `ac28-debug`, `ac28-release` |
| 29 | 29.3100 | v143 | C++20 | `ac29-debug`, `ac29-release` |

The source of truth for these pins is [`archicad-dev.yaml`](../archicad-dev.yaml). The corresponding release archives are downloaded locally under `third_party/devkits/` and are intentionally ignored by Git.

## Version-specific coding

Use the Graphisoft API compatibility pattern when an API changes:

```cpp
#ifdef ServerMainVers_2700
    return ACAPI_MenuItem_RegisterMenu(menuId, 0, MenuCode_Tools, MenuFlag_Default);
#else
    return ACAPI_Register_Menu(menuId, 0, MenuCode_Tools, MenuFlag_Default);
#endif
```

Build all three versions after modifying shared Add-On code. Do not use AC29-only C++20 features in code intended for AC27 or AC28.

## Distribution

Local builds set `AC_ADDON_FOR_DISTRIBUTION=OFF`. They use placeholder MDIDs and must not be distributed. Before a release, obtain valid IDs through Graphisoft, update the resource metadata, and introduce an explicit reviewed distribution build path.
