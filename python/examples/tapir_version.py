"""Verify that the optional Tapir Add-On is loaded and print its version payload."""

from archicad_tools import Archicad


def main() -> None:
    client = Archicad.connect(require_tapir=True)
    print(client.tapir_version())


if __name__ == "__main__":
    main()
