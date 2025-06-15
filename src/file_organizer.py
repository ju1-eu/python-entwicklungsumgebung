"""Dateiorganisations-Tool für Python-Projekte."""

from pathlib import Path


class FileOrganizer:
    """Organisiert Dateien nach Typ und Datum."""

    def __init__(self, source_dir: str | Path) -> None:
        """Initialisiert den FileOrganizer.

        Args:
            source_dir: Quellverzeichnis (String oder Path)
        """
        self.source_dir = Path(source_dir)

    def scan_files(self) -> dict[str, list[Path]]:
        """Scannt Dateien und gruppiert sie nach Typ.

        Returns:
            Dictionary mit Dateitypen und Pfaden
        """
        files_by_type: dict[str, list[Path]] = {}

        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext not in files_by_type:
                    files_by_type[ext] = []
                files_by_type[ext].append(file_path)

        return files_by_type


def main() -> None:
    """Hauptfunktion."""
    import sys
    
    organizer = FileOrganizer(".")
    files = organizer.scan_files()

    sys.stdout.write("Gefundene Dateitypen:\n")
    for ext, paths in sorted(files.items()):
        sys.stdout.write(f"  {ext or '(ohne Erweiterung)'}: {len(paths)} Dateien\n")


if __name__ == "__main__":
    main()
