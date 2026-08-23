"""Typed convenience wrapper around Graphisoft's official Python package."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from archicad import ACConnection

from .errors import ArchicadConnectionError, TapirCommandError, TapirUnavailableError

TAPIR_NAMESPACE = "TapirCommand"


class Archicad:
    """A connected Archicad client with explicit optional Tapir access."""

    def __init__(self, connection: Any) -> None:
        """Wrap an existing official ``ACConnection`` instance."""
        self._connection = connection

    @classmethod
    def connect(cls, port: int | None = None, *, require_tapir: bool = False) -> Archicad:
        """Connect to a running Archicad and optionally require Tapir to be installed."""
        connection = ACConnection.connect(port)
        if connection is None:
            raise ArchicadConnectionError(
                "No compatible running Archicad instance was found. "
                "Start Archicad, open a project, and try again."
            )

        client = cls(connection)
        if require_tapir:
            try:
                client.tapir_version()
            except TapirCommandError as error:
                raise TapirUnavailableError(
                    "Tapir is required but its Add-On command namespace is unavailable."
                ) from error
        return client

    @property
    def version(self) -> int:
        """Return the connected Archicad major version."""
        return cast(int, self._connection.version)

    @property
    def build(self) -> int:
        """Return the connected Archicad build number."""
        return cast(int, self._connection.build)

    @property
    def language(self) -> str:
        """Return the connected Archicad language code."""
        return cast(str, self._connection.lang)

    @property
    def commands(self) -> Any:
        """Expose official Graphisoft commands without hiding their generated types."""
        return self._connection.commands

    @property
    def types(self) -> Any:
        """Expose official Graphisoft generated types."""
        return self._connection.types

    @property
    def utilities(self) -> Any:
        """Expose official Graphisoft utility helpers."""
        return self._connection.utilities

    def execute_tapir(
        self,
        command: str,
        parameters: Mapping[str, object] | None = None,
    ) -> dict[str, Any]:
        """Execute one Tapir Add-On command using its documented namespace."""
        command_id = self.types.AddOnCommandId(TAPIR_NAMESPACE, command)
        try:
            if parameters is None:
                result = self.commands.ExecuteAddOnCommand(command_id)
            else:
                result = self.commands.ExecuteAddOnCommand(command_id, dict(parameters))
        except Exception as error:
            raise TapirCommandError(f"Tapir command {command!r} failed: {error}") from error
        return cast(dict[str, Any], result)

    def tapir_version(self) -> dict[str, Any]:
        """Return Tapir's version payload or raise when Tapir is unavailable."""
        return self.execute_tapir("GetAddOnVersion")
