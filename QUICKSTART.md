# 🚀 Quick Reference

## 🔧 Ersteinrichtung
```bash
# Repository klonen
git clone https://github.com/ju1-eu/python-entwicklungsumgebung
cd python-entwicklungsumgebung

# Schnell-Setup (alles in einem Befehl)
make setup              # Oder: ./scripts/setup.sh

# Manuelles Setup
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
```

## 📝 Tägliche Befehle
```bash
# Umgebung aktivieren
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

# Tests
pytest                      # Alle Tests mit Coverage
pytest -v                   # Verbose output
pytest tests/test_file.py   # Einzelne Datei
pytest -k "test_name"       # Spezifischer Test

# Code-Qualität
black .                     # Code formatieren
ruff check . --fix          # Linting mit Auto-Fixes
mypy src/                   # Type checking

# Alles auf einmal
nox                         # Führt alle Checks aus
```

## 🎯 Vor dem Commit
```bash
# Option 1: Pre-commit Hooks (automatisch beim commit)
git add .
git commit -m "feat: Neue Funktion"

# Option 2: Manuell alle Checks
pre-commit run --all-files  # Alle Pre-commit Hooks
nox                         # Alle Tests und Checks

# Option 3: Einzelne Checks
black --check .             # Nur Formatierung prüfen
ruff check .                # Nur Linting
mypy src/                   # Nur Types
pytest                      # Nur Tests
```

## 🛠️ Entwicklungs-Workflows

### Neues Feature entwickeln
```bash
# 1. Feature-Branch erstellen
git checkout -b feature/mein-feature

# 2. Code schreiben und testen
# ... entwickeln ...
pytest tests/test_mein_feature.py

# 3. Code aufräumen
black .
ruff check . --fix

# 4. Alle Checks
nox

# 5. Committen und pushen
git add .
git commit -m "feat: Beschreibung"
git push origin feature/mein-feature
```

### Debugging
```bash
# Tests mit Output
pytest -v -s

# Einzelnen Test debuggen
pytest tests/test_file.py::test_function -v

# Coverage-Report generieren
pytest --cov=src --cov-report=html
open htmlcov/index.html     # macOS
xdg-open htmlcov/index.html # Linux
```

## 🔍 Nützliche Aliases

Füge zu ~/.bashrc oder ~/.zshrc hinzu:

```bash
# Python Development
alias act='source venv/bin/activate'
alias pytest='python -m pytest'
alias nox='python -m nox'
alias black='python -m black'
alias mypy='python -m mypy'
alias ruff='python -m ruff'

# Git Shortcuts
alias gs='git status'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -10'

# Projekt-spezifisch
alias dev='cd ~/projekts/python_umgebung && source venv/bin/activate'
alias test='pytest -v'
alias check='nox'
```

## 🚨 Troubleshooting

### PATH-Probleme (Anaconda-Konflikt)
```bash
# Temporär venv priorisieren
export PATH="$PWD/venv/bin:$PATH"

# Oder Python-Module direkt nutzen
python -m pytest
python -m black .
python -m mypy src/
```

### Import-Fehler
```bash
# Projekt neu installieren
pip install -e .

# PYTHONPATH setzen
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Pre-commit Fehler
```bash
# Cache löschen und neu installieren
pre-commit clean
pre-commit install --install-hooks
```

## 📊 Status-Checks
```bash
# Coverage anzeigen
pytest --cov=src

# Installierte Pakete
pip list

# Python-Version
python --version

# Tool-Versionen
black --version
ruff --version
mypy --version
```

## 🔗 Wichtige Befehle
```bash
# Hilfe anzeigen
pytest --help
ruff --help
nox --list

# Verfügbare Nox-Sessions
nox --list-sessions

# Nur bestimmte Nox-Session
nox -s tests
nox -s lint
nox -s format
```

## 📚 Weitere Dokumentation
- Vollständige Entwicklerdoku: [DEVELOPMENT.md](DEVELOPMENT.md)
- Projekt-README: [README.md](README.md)
- Python Style Guide: [PEP 8](https://pep8.org/)

