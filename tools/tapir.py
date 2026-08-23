# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.2"]
# ///
"""Download and verify the pinned Tapir Add-On for Archicad 27, 28, or 29."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "archicad-dev.yaml"


class DownloadIntegrityError(RuntimeError):
    """Raised when a downloaded Tapir binary does not match its pinned digest."""


def load_manifest() -> dict[str, Any]:
    """Load Tapir metadata from the repository manifest."""
    with MANIFEST.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def verify_sha256(path: Path, expected: str) -> None:
    """Raise when a file's SHA-256 digest differs from the manifest."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest.lower() != expected.lower():
        raise DownloadIntegrityError(
            f"SHA-256 mismatch for {path.name}: expected {expected}, received {digest}"
        )


def install(version: int) -> Path:
    """Download the pinned Tapir APX into the ignored third-party directory."""
    config = load_manifest()
    supported = {int(item) for item in config["project"]["supported_archicad"]}
    if version not in supported:
        raise ValueError(f"Archicad {version} is not supported by this repository")
    item = config["apis"]["tapir"]["assets"][version]
    destination = ROOT / "third_party" / "tapir" / f"ac{version}" / item["name"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".download")
    request = urllib.request.Request(item["url"], headers={"User-Agent": "archicad-dev"})
    try:
        with (
            urllib.request.urlopen(request, timeout=60) as response,
            temporary.open("wb") as target,
        ):
            shutil.copyfileobj(response, target)
        verify_sha256(temporary, item["sha256"])
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "path", "validate"))
    parser.add_argument("version", type=int, choices=(27, 28, 29))
    args = parser.parse_args()
    config = load_manifest()
    item = config["apis"]["tapir"]["assets"][args.version]
    path = ROOT / "third_party" / "tapir" / f"ac{args.version}" / item["name"]
    if args.command == "install":
        path = install(args.version)
    elif args.command == "validate":
        verify_sha256(path, item["sha256"])
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
