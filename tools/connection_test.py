# /// script
# requires-python = ">=3.11"
# dependencies = ["archicad>=27"]
# ///
"""Perform a read-only connection test against a running Archicad instance."""

from __future__ import annotations

import sys

from archicad import ACConnection


def main() -> int:
    connection = ACConnection.connect()
    if not connection.connected:
        print("No compatible running Archicad instance was found.", file=sys.stderr)
        return 1

    product_info = connection.commands.GetProductInfo()
    print(f"Connected to {product_info.productName} {product_info.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
