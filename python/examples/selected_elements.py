"""List selected element GUIDs through Graphisoft's official Python API."""

from archicad_tools import Archicad


def main() -> None:
    client = Archicad.connect()
    selected = client.commands.GetSelectedElements()
    print(f"Selected elements: {len(selected)}")
    for item in selected:
        print(item.elementId.guid)


if __name__ == "__main__":
    main()
