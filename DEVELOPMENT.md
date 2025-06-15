# 🛠️ Entwicklerdokumentation

Umfassende technische Dokumentation für Entwickler.

## 🚀 Schnellstart

### Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/ju1-eu/python-entwicklungsumgebung.git
cd python-entwicklungsumgebung

# Virtuelle Umgebung
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac

# Dependencies installieren
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
```

## 🔧 Entwicklungswerkzeuge

### Ruff - Der moderne Linter

Ruff ist ein extrem schneller Python-Linter, geschrieben in Rust.

```bash
# Basis-Checks
ruff check .

# Mit automatischen Fixes
ruff check --fix .
```

### Black - Code-Formatierung

```bash
# Code formatieren
black .

# Nur prüfen
black --check .
```

### Mypy - Typprüfung

```bash
# Type-Checking
mypy src/

# Mit striktem Modus (bereits konfiguriert)
mypy --strict src/
```

### Pytest - Testing

```bash
# Tests ausführen
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Einzelnen Test
pytest tests/test_file_organizer.py::test_scan_files -v
```

### Nox - Automatisierung

```bash
# Alle Sessions
nox

# Spezifische Session
nox -s tests
nox -s lint
nox -s format
```

## 📁 Projektstruktur

```
python-entwicklungsumgebung/
├── src/                    # Hauptquellcode
│   ├── __init__.py
│   ├── example.py
│   └── file_organizer.py
├── tests/                  # Tests (100% Coverage!)
│   ├── test_example.py
│   └── test_file_organizer.py
├── noxfile.py             # Nox-Automatisierung
├── pyproject.toml         # Projektkonfiguration
├── .pre-commit-config.yaml # Pre-commit Hooks
├── mypy.ini               # Mypy-Konfiguration
└── requirements-dev.txt   # Development Dependencies
```

## 🧪 Testing Best Practices

### Coverage erreichen

```python
# Alle Branches testen
def divide(a: float, b: float) -> float:
    if b == 0:  # Branch 1
        raise ValueError("Division durch Null")
    return a / b  # Branch 2

def test_divide() -> None:
    assert divide(10, 2) == 5  # Normal case
    with pytest.raises(ValueError):
        divide(10, 0)  # Error case
```

## 📏 Code-Standards

### Type Hints (Python 3.13)

```python
# Modern - keine typing imports nötig!
def process_data(
    items: list[str],
    options: dict[str, Any] | None = None
) -> tuple[int, list[str]]:
    """Verarbeitet Daten."""
    options = options or {}
    processed = [item.strip() for item in items]
    return len(processed), processed
```

### Docstrings (Google Style)

```python
def complex_function(param: str) -> bool:
    """Kurze Beschreibung.
    
    Längere Erklärung der Funktion.
    
    Args:
        param: Parameter-Beschreibung
        
    Returns:
        True wenn erfolgreich
        
    Raises:
        ValueError: Bei ungültigen Parametern
    """
```

## 🐛 Debugging

### VS Code Konfiguration

```json
// .vscode/settings.json
{
    "python.testing.pytestEnabled": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

## 🆘 Troubleshooting

### PATH-Konflikte (Anaconda)

```bash
# Tools über Python-Module aufrufen
python -m pytest
python -m black .
python -m mypy src/
```

### Import-Fehler

```bash
# Projekt neu installieren
pip install -e .
```

## 📚 Ressourcen

- [Ruff Dokumentation](https://docs.astral.sh/ruff/)
- [Black](https://black.readthedocs.io/)
- [Mypy](https://mypy.readthedocs.io/)
- [Pytest](https://docs.pytest.org/)




### **5. Optional: py.typed Marker hinzufügen:**
```bash
# Für Type-Checking Support
touch src/py.typed
```

### **6. Alle Dateien committen und pushen:**
```bash
# Alle neuen Dateien hinzufügen
git add .pre-commit-config.yaml mypy.ini DEVELOPMENT.md CHANGELOG.md src/py.typed

# Status prüfen
git status

# Commit
git commit -m "Add development configuration and documentation

- Add .pre-commit-config.yaml for automated checks
- Add mypy.ini for type checking configuration
- Add comprehensive DEVELOPMENT.md documentation
- Add CHANGELOG.md following Keep a Changelog format
- Add py.typed marker for PEP 561 compliance"

# Push
git push origin main
```

### **7. Pre-commit hooks aktivieren:**
```bash
# Pre-commit neu installieren mit den Hooks
pre-commit install

# Hooks testen
pre-commit run --all-files
```
