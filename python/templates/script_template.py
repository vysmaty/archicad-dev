# /// script
# requires-python = ">=3.11"
# dependencies = ["archicad==29.3000"]
# ///
"""Copy this PEP 723 template for a self-contained Archicad automation script."""

from __future__ import annotations

from archicad import ACConnection


def main() -> int:
    connection = ACConnection.connect()
    if connection is None:
        raise RuntimeError("Start Archicad and open a project before running this script")
    version, build, language = connection.commands.GetProductInfo()
    print(f"Connected to Archicad {version}, build {build}, language {language}")
    # Add one small, explicit operation here. Prefer read-only commands first.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
