# Compatibility

The compatibility floor is Archicad 27 on Windows x64. Each `.apx` is built independently with the matching DevKit.

| Archicad | Pinned DevKit | MSVC toolset | C++ standard | Presets | Tapir asset |
| --- | --- | --- | --- | --- | --- |
| 27 | 27.6003 | v142 | C++17 | `ac27-debug`, `ac27-release` | `TapirAddOn_AC27_Win.apx` |
| 28 | 28.4001 | v142 | C++17 | `ac28-debug`, `ac28-release` | `TapirAddOn_AC28_Win.apx` |
| 29 | 29.3100 | v143 | C++20 | `ac29-debug`, `ac29-release` | `TapirAddOn_AC29_Win.apx` |

`archicad-dev.yaml` is authoritative. Tapir 1.5.8 and the Graphisoft Python package 29.3000 are pinned independently from the C++ DevKits.

## Capability matrix

| Need | Official Python | Tapir | C++ Add-On |
| --- | --- | --- | --- |
| Product info, selected elements, properties, classifications | Preferred when generated command exists | Usually unnecessary | Avoid |
| Extra documented automation command absent from official JSON API | Not available | Preferred | Only if Tapir cannot meet constraints |
| Native menu, notification, event handler, custom palette/dialog | No | No | Required |
| High-volume native processing or new Add-On command provider | Limited by JSON transport | Limited by JSON transport | Required |
| Script that must run without an installed custom Add-On | Preferred | Not suitable | Not suitable |

The Python package selects its generated command/type module based on the connected Archicad release. A method still must exist in that version; verify it before use.

## Version-sensitive C++

All compatibility decisions belong under `src/compat/`. Feature entry points call stable `ACCompat` functions. If an API differs between versions:

1. confirm the symbol and guard in each pinned DevKit header;
2. add the smallest wrapper or overload in `src/compat/`;
3. add a structure/unit test where practical;
4. build all three majors in Debug and Release.

Do not copy guessed `ServerMainVers_*` branches from unrelated examples. Shared code must remain valid under the AC27 compiler baseline.

## Adding a future major

The update workflow has `allow_automatic_new_major: false` and cannot add AC30. A future major requires a reviewed change to the manifest, presets, toolset/standard mapping, DevKit pin, CI matrix, Tapir asset, compatibility documentation, and a successful build of every supported major.
