"""Print information about a running Archicad without modifying the project."""

from archicad_tools import Archicad


def main() -> None:
    client = Archicad.connect()
    version, build, language = client.commands.GetProductInfo()
    print(f"Archicad {version}, build {build}, language {language}")


if __name__ == "__main__":
    main()
