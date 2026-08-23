from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tools.tapir import DownloadIntegrityError, verify_sha256


def test_verify_sha256_accepts_matching_file(tmp_path: Path) -> None:
    downloaded = tmp_path / "Tapir.apx"
    downloaded.write_bytes(b"known tapir payload")
    digest = hashlib.sha256(downloaded.read_bytes()).hexdigest()

    verify_sha256(downloaded, digest)


def test_verify_sha256_rejects_corrupt_file(tmp_path: Path) -> None:
    downloaded = tmp_path / "Tapir.apx"
    downloaded.write_bytes(b"corrupt")

    with pytest.raises(DownloadIntegrityError, match="SHA-256"):
        verify_sha256(downloaded, "0" * 64)
