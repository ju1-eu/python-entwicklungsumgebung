"""Tests für das Beispielmodul."""

from src.example import add, greet


def test_greet():
    """Test der greet-Funktion."""
    assert greet("Welt") == "Hallo, Welt!"
    assert greet("Python") == "Hallo, Python!"


def test_add():
    """Test der add-Funktion."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
