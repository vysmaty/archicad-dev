"""Domain-specific errors raised by :mod:`archicad_tools`."""


class ArchicadConnectionError(RuntimeError):
    """Raised when no compatible running Archicad instance can be reached."""


class TapirUnavailableError(RuntimeError):
    """Raised when a requested operation needs Tapir but Tapir is unavailable."""


class TapirCommandError(RuntimeError):
    """Raised when an installed Tapir command fails."""
