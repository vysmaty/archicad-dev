from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
from archicad_tools import Archicad, ArchicadConnectionError, TapirUnavailableError


@dataclass
class FakeCommandId:
    namespace: str
    command: str


class FakeTypes:
    AddOnCommandId = FakeCommandId


class FakeCommands:
    def __init__(self, *, fail_tapir: bool = False) -> None:
        self.fail_tapir = fail_tapir
        self.calls: list[tuple[FakeCommandId, dict[str, object] | None]] = []

    def ExecuteAddOnCommand(
        self,
        command_id: FakeCommandId,
        parameters: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        self.calls.append((command_id, parameters))
        if self.fail_tapir:
            raise RuntimeError("command namespace is not installed")
        return {"version": "1.5.8"}


@dataclass
class FakeConnection:
    commands: FakeCommands
    types: FakeTypes = field(default_factory=FakeTypes)
    utilities: object = field(default_factory=object)
    version: int = 29
    build: int = 3000
    lang: str = "INT"


def test_connect_raises_clear_error_when_archicad_is_not_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("archicad_tools.client.ACConnection.connect", lambda port=None: None)

    with pytest.raises(ArchicadConnectionError, match="running Archicad"):
        Archicad.connect()


def test_client_exposes_connection_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    raw = FakeConnection(FakeCommands())
    monkeypatch.setattr("archicad_tools.client.ACConnection.connect", lambda port=None: raw)

    client = Archicad.connect(port=19723)

    assert client.version == 29
    assert client.build == 3000
    assert client.language == "INT"
    assert client.commands is raw.commands


def test_execute_tapir_uses_the_documented_namespace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands = FakeCommands()
    raw = FakeConnection(commands)
    monkeypatch.setattr("archicad_tools.client.ACConnection.connect", lambda port=None: raw)

    result = Archicad.connect().execute_tapir("GetAddOnVersion")

    assert result == {"version": "1.5.8"}
    assert commands.calls == [(FakeCommandId("TapirCommand", "GetAddOnVersion"), None)]


def test_require_tapir_fails_explicitly_when_addon_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = FakeConnection(FakeCommands(fail_tapir=True))
    monkeypatch.setattr("archicad_tools.client.ACConnection.connect", lambda port=None: raw)

    with pytest.raises(TapirUnavailableError, match="Tapir"):
        Archicad.connect(require_tapir=True)
