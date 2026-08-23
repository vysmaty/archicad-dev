from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_addon_entrypoint_delegates_version_sensitive_api_calls() -> None:
    entrypoint = (ROOT / "src" / "AddOnMain.cpp").read_text(encoding="utf-8")

    assert '#include "compat/ArchicadCompatibility.hpp"' in entrypoint
    assert "ACCompat::RegisterMenu" in entrypoint
    assert "ACCompat::InstallMenuHandler" in entrypoint
    assert "ServerMainVers_" not in entrypoint
