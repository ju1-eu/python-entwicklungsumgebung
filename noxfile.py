"""Nox-Konfiguration für automatisierte Tests und Checks."""

import nox


@nox.session(python=["3.11", "3.12", "3.13"])
def tests(session):
    """Tests mit Coverage ausführen."""
    session.install("pytest", "pytest-cov", "coverage[toml]")
    session.install("-e", ".")
    session.run("pytest", "--cov", "--cov-report=term-missing")


@nox.session
def lint(session):
    """Code-Qualität prüfen."""
    session.install("ruff", "black", "mypy")
    session.run("ruff", "check", ".")
    session.run("black", "--check", ".")
    session.run("mypy", "src/")


@nox.session
def format(session):
    """Code formatieren und Fehler beheben."""
    session.install("black", "ruff")
    session.run("black", ".")
    session.run("ruff", "check", "--fix", ".")


@nox.session
def security(session):
    """Sicherheitsprüfungen durchführen."""
    session.install("bandit", "pip-audit")
    session.run("bandit", "-r", "src/")
    session.run("pip-audit")


@nox.session
def docs(session):
    """Dokumentationsstil prüfen."""
    session.install("pydocstyle")
    session.run("pydocstyle", "src/")
