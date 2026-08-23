# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.2"]
# ///
"""Check pinned Graphisoft DevKits and CMake tooling against their upstreams.

This script reports only. Updating a pin remains an explicit review decision.
"""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def manifest() -> dict[str, Any]:
    with (ROOT / "archicad-dev.yaml").open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def github_release(tag: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/GRAPHISOFT/archicad-api-devkit/releases/tags/{tag}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "archicad-dev-addon",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def submodule_head(path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT / path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    config = manifest()
    result = 0
    for version, item in sorted(config["devkits"].items()):
        try:
            release = github_release(item["release"])
            assets = {asset["name"] for asset in release.get("assets", [])}
            expected_asset = item["asset"]
            available = expected_asset in assets
            status = "available" if available else "MISSING ASSET"
            print(f"AC{version}: {item['release']} — {status}")
            result |= int(not available)
        except (urllib.error.URLError, urllib.error.HTTPError) as error:
            print(f"AC{version}: upstream check failed: {error}", file=sys.stderr)
            result = 1

    tools = config["upstreams"]["graphisoft_cmake_tools"]
    try:
        actual = submodule_head(tools["path"])
        expected = tools["pinned_commit"]
        status = "pinned" if actual == expected else f"DIFFERS ({actual})"
        print(f"CMake tools: {status}")
        result |= int(actual != expected)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"CMake tools: submodule check failed: {error}", file=sys.stderr)
        result = 1
    return result


if __name__ == "__main__":
    raise SystemExit(main())
