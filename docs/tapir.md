# Tapir Python commands

[Tapir](https://github.com/ENZYME-APD/tapir-archicad-automation) is an optional Archicad Add-On that registers extra JSON commands under the `TapirCommand` namespace. It is not part of the C++ build and is never silently required.

## Install the pinned binary

Download and verify the exact asset for the target major:

```powershell
uv run --script tools/tapir.py install 29
uv run --script tools/tapir.py validate 29
```

The tool verifies the pinned SHA-256 before placing the file under `third_party/tapir/ac29/`. In Archicad, open **Options → Add-On Manager → Edit List of Available Add-Ons → Add**, select the printed `.apx`, and confirm. Use the AC27 binary only with AC27, and so on.

## Call a command

```python
from archicad_tools import Archicad

client = Archicad.connect(require_tapir=True)
print(client.tapir_version())
```

For another documented command:

```python
result = client.execute_tapir("DocumentedCommandName", {"documentedParameter": "value"})
```

Confirm the exact command name, parameter object, and response in [Tapir's command documentation](https://enzyme-apd.github.io/tapir-archicad-automation/archicad-addon/) before writing code. `execute_tapir` uses Graphisoft's `AddOnCommandId("TapirCommand", name)` and `ExecuteAddOnCommand` without reshaping the response.

If Tapir is missing, `require_tapir=True` raises `TapirUnavailableError`. A command failure raises `TapirCommandError`; the code does not substitute an official or C++ implementation behind the caller's back.

## Updating Tapir

`archicad-dev.yaml` pins the release, three Windows asset URLs, and their GitHub SHA-256 digests. `tools/check_updates.py --apply` changes Tapir only if one release contains verified assets for every supported major. The scheduled workflow submits that change for review.
