# Python-Entwicklungsumgebung

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/ju1-eu/python-entwicklungsumgebung)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/ju1-eu/python-entwicklungsumgebung)

Eine moderne Python 3.13 Entwicklungsumgebung mit Best Practices, 100% Test Coverage und automatisierter Qualitätssicherung.

## ✨ Features

- **Python 3.13+** mit modernen Type Hints
- **100% Test Coverage** mit pytest
- **Code-Qualität** durch Black, Ruff, Mypy
- **Pre-commit Hooks** für automatische Checks
- **Nox** für Automatisierung
- **Umfassende Dokumentation**

## 🚀 Installation

```bash
# Repository klonen
git clone https://github.com/ju1-eu/python-entwicklungsumgebung.git
cd python-entwicklungsumgebung

# Virtuelle Umgebung erstellen
python3.13 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements-dev.txt
pip install -e .

# Pre-commit einrichten
pre-commit install
```

## 📖 Verwendung

```bash
# Tests ausführen
pytest

# Code formatieren
black .

# Linting
ruff check .

# Type-Checking
mypy src/

# Alle Checks
nox
```

Siehe [QUICKSTART.md](QUICKSTART.md) für eine Kurzreferenz.

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE)
