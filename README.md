# Python-Entwicklungsumgebung

<div align="center">

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/ju1-eu/python-entwicklungsumgebung)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/ju1-eu/python-entwicklungsumgebung)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: Mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Eine moderne Python-Entwicklungsumgebung mit automatisierter Qualitätssicherung, umfassenden Tests und bewährten Industriestandards.**

[Features](#-features) • [Schnellstart](#-schnellstart) • [Dokumentation](#-dokumentation) • [Tools](#-enthaltene-tools) • [Mitwirken](#-mitwirken)

</div>

---

## ✨ Features

<table>
<tr>
<td width="33%" valign="top">

### 🚀 Moderne Werkzeuge
- **Python 3.13+** - Neueste Features
- **Ruff** - Blitzschneller Linter
- **Black** - Konsistente Formatierung
- **Mypy** - Statische Typprüfung

</td>
<td width="33%" valign="top">

### 🛡️ Qualitätssicherung
- **100% Testabdeckung** ✅
- **Pre-commit Hooks** ✅
- **Sicherheitsscans** ✅
- **Dependency-Auditing** ✅

</td>
<td width="33%" valign="top">

### 📦 Professionelles Setup
- **Nox** Automatisierung
- **Pytest** Framework
- **Type-sicherer Code**
- **CI/CD bereit**

</td>
</tr>
</table>

## 🚀 Schnellstart

```bash
# Repository klonen
git clone https://github.com/ju1-eu/python-entwicklungsumgebung.git
cd python-entwicklungsumgebung

# Umgebung einrichten (ein Befehl)
python3.13 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt && pip install -e . && pre-commit install

# Alle Checks ausführen
nox
```

> 📌 **Tipp:** Siehe [QUICKSTART.md](QUICKSTART.md) für eine kompakte Befehlsreferenz!

<details>
<summary>📋 Manuelle Einrichtung</summary>

```bash
# Virtuelle Umgebung erstellen
python3.13 -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Dependencies installieren
pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .

# Pre-commit einrichten
pre-commit install
pre-commit run --all-files
```
</details>

## 📚 Dokumentation

### Projektstruktur

```
.
├── src/                    # Quellcode
│   ├── __init__.py
│   ├── example.py
│   └── file_organizer.py   # Datei-Organisation Tool
├── tests/                  # Test-Suite (100% Coverage)
│   ├── test_example.py
│   └── test_file_organizer.py
├── noxfile.py              # Nox-Automatisierung
├── pyproject.toml          # Zentrale Projektkonfiguration
├── .pre-commit-config.yaml # Pre-commit Hooks
├── mypy.ini                # Mypy-Konfiguration
├── QUICKSTART.md           # Schnellreferenz
├── DEVELOPMENT.md          # Entwicklerdokumentation
├── CHANGELOG.md            # Versionshistorie
└── requirements-dev.txt    # Entwickler-Dependencies
```

### 🔧 Entwicklungsworkflow

#### Code-Qualität
```bash
# Code formatieren
black src tests

# Code linten
ruff check . --fix

# Typprüfung
mypy src

# Sicherheitsscan
bandit -r src
```

#### Testing
```bash
# Tests ausführen
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Coverage-Report öffnen
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

#### Automatisierung
```bash
# Alle Checks ausführen
nox

# Spezifische Sessions
nox -s tests       # Unit-Tests
nox -s lint        # Code-Qualität
nox -s format      # Code formatieren
nox -s security    # Sicherheitsscan
nox -s docs        # Dokumentation prüfen
```

### 🎯 Code-Standards

Dieses Projekt erzwingt:

- ✅ **Type Hints** für alle öffentlichen APIs
- ✅ **Docstrings** (Google-Stil) für alle Module, Klassen und Funktionen
- ✅ **100% Testabdeckung** für neuen Code
- ✅ **Black**-Formatierung (88 Zeichen Zeilenlänge)
- ✅ **Ruff**-Linting mit strikten Regelsets
- ✅ **Sicherheits**-Scans bei jedem Commit

## 🔨 Enthaltene Tools

### FileOrganizer
Ein Tool zur Organisation und Analyse von Dateien in Python-Projekten:

```python
from src.file_organizer import FileOrganizer

# Dateien nach Typ scannen
organizer = FileOrganizer(".")
files = organizer.scan_files()

# Ausgabe der Dateitypen
for ext, paths in files.items():
    print(f"{ext}: {len(paths)} Dateien")
```

**Features:**
- Rekursives Scannen von Verzeichnissen
- Gruppierung nach Dateierweiterungen
- Type-safe mit modernen Python 3.13 Features

## 🤝 Mitwirken

Wir freuen uns über Beiträge! Siehe unsere [Entwicklerdokumentation](DEVELOPMENT.md) für detaillierte Informationen.

<details>
<summary>Kurzer Beitragsleitfaden</summary>

1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/tolles-feature`)
3. Änderungen committen (`git commit -m 'feat: Tolles Feature hinzugefügt'`)
4. Branch pushen (`git push origin feature/tolles-feature`)
5. Pull Request öffnen

</details>

### Commit-Konvention

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Neue Features
- `fix:` Fehlerbehebungen
- `docs:` Dokumentationsänderungen
- `style:` Code-Stil-Änderungen
- `refactor:` Code-Refactoring
- `test:` Test-Updates
- `chore:` Wartungsaufgaben

## 📊 Projektstatus

<div align="center">

| Metrik         | Status                                                                             |
| -------------- | ---------------------------------------------------------------------------------- |
| Tests          | ![Tests](https://img.shields.io/badge/tests-5%20passing-brightgreen.svg)           |
| Code-Abdeckung | ![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)          |
| Abhängigkeiten | ![Dependencies](https://img.shields.io/badge/dependencies-aktuell-brightgreen.svg) |
| Sicherheit     | ![Security](https://img.shields.io/badge/vulnerabilities-0-brightgreen.svg)        |
| Code-Qualität  | ![Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)         |

</div>

## 🛠️ Technologie-Stack

<div align="center">

| Kategorie           | Werkzeuge                                          |
| ------------------- | -------------------------------------------------- |
| **Sprache**         | Python 3.13+                                       |
| **Formatierung**    | Black, isort (via Ruff)                            |
| **Linting**         | Ruff (ersetzt Flake8, pylint, pyupgrade, und mehr) |
| **Typprüfung**      | Mypy (strict mode)                                 |
| **Testing**         | Pytest, pytest-cov                                 |
| **Sicherheit**      | Bandit, pip-audit                                  |
| **Automatisierung** | Nox, pre-commit                                    |
| **Dokumentation**   | Markdown, Sphinx (geplant)                         |

</div>

## 📈 Roadmap

- [x] Kern-Entwicklungsumgebung
- [x] Umfassende Dokumentation
- [x] Pre-commit Hooks
- [x] 100% Test Coverage
- [x] Moderne Python 3.13 Syntax
- [ ] GitHub Actions CI/CD-Pipeline
- [ ] Docker-Containerisierung
- [ ] Sphinx-Dokumentationsseite
- [ ] PyPI-Paketveröffentlichung
- [ ] VS Code Devcontainer
- [ ] Automatisierte Dependency-Updates

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

<div align="center">

Besonderer Dank an diese großartigen Projekte:

[**Ruff**](https://github.com/astral-sh/ruff) • [**Black**](https://github.com/psf/black) • [**Mypy**](https://github.com/python/mypy) • [**Pytest**](https://github.com/pytest-dev/pytest) • [**Nox**](https://github.com/wntrblm/nox)

</div>

---

<div align="center">

**[⬆ zurück nach oben](#python-entwicklungsumgebung)**

📖 [Vollständige Dokumentation](DEVELOPMENT.md) • 🚀 [Quick Reference](QUICKSTART.md) • 🐛 [Issues](https://github.com/ju1-eu/python-entwicklungsumgebung/issues)

Mit ❤️ und ☕ von Entwicklern für Entwickler erstellt

</div>


# Änderungen committen
git add README.md
git commit -m "docs: Enhance README with comprehensive documentation

- Add complete feature overview with tables
- Include detailed project structure
- Add code examples for FileOrganizer
- Enhance badges and visual presentation
- Add technology stack and roadmap
- Include contribution guidelines"

# Push
git push origin main
```

## **Wichtige Verbesserungen:**

1. ✅ **Vollständige Badge-Sammlung** (9 Badges)
2. ✅ **Visuell ansprechende Tabellen** für Features
3. ✅ **Detaillierte Projektstruktur**
4. ✅ **Code-Beispiele** für FileOrganizer
5. ✅ **Projekt-Status Tabelle**
6. ✅ **Technologie-Stack Übersicht**
7. ✅ **Roadmap** mit erledigten Punkten
8. ✅ **Navigation** zu allen wichtigen Dokumenten
