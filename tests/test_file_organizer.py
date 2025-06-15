"""Tests für das FileOrganizer-Modul."""

from pathlib import Path
import pytest
from src.file_organizer import FileOrganizer


def test_file_organizer_init() -> None:
    """Test der Initialisierung."""
    organizer = FileOrganizer(".")
    assert isinstance(organizer.source_dir, Path)


def test_scan_files(tmp_path: Path) -> None:
    """Test der Datei-Scan-Funktion."""
    # Test-Dateien erstellen
    (tmp_path / "test.py").touch()
    (tmp_path / "doc.md").touch()
    (tmp_path / "data.json").touch()

    organizer = FileOrganizer(tmp_path)
    files = organizer.scan_files()

    assert ".py" in files
    assert ".md" in files
    assert ".json" in files
    assert len(files[".py"]) == 1


def test_main(capsys: pytest.CaptureFixture[str]) -> None:
    """Test der main Funktion."""
    from src.file_organizer import main

    main()

    captured = capsys.readouterr()
    assert "Gefundene Dateitypen:" in captured.out
    assert "Dateien" in captured.out
