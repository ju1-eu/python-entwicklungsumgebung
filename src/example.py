"""Beispielmodul zur Demonstration der Entwicklungsumgebung."""


def greet(name: str) -> str:
    """Erstellt eine Begrüßungsnachricht.

    Args:
        name: Name der zu begrüßenden Person

    Returns:
        Formatierte Begrüßungsnachricht
    """
    return f"Hallo, {name}!"


def add(a: int, b: int) -> int:
    """Addiert zwei Zahlen.

    Args:
        a: Erste Zahl
        b: Zweite Zahl

    Returns:
        Summe der beiden Zahlen
    """
    return a + b
