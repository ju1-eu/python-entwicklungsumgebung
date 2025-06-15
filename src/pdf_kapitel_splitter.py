#!/usr/bin/env python3
"""
PDF Kapitel Splitter

Dieses Skript ermöglicht das Aufteilen einer PDF-Datei in mehrere Kapitel-Dateien
basierend auf definierten Seitenbereichen.

Version: 2.0
Autor: Basierend auf Code von Jan Unger
Datum: 27.02.2025
"""

import logging
import os

from PyPDF2 import PdfReader, PdfWriter

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def extrahiere_kapitel(
    eingangs_pdf_pfad: str,
    ausgangs_pdf_pfad: str,
    startseite: int,
    endseite: int,
) -> None:
    """
    Extrahiert einen Seitenbereich aus einer PDF-Datei und speichert diesen in einer neuen PDF.

    Args:
        eingangs_pdf_pfad: Pfad zur ursprünglichen PDF-Datei
        ausgangs_pdf_pfad: Pfad, unter dem die neue PDF gespeichert werden soll
        startseite: Erste zu extrahierende Seite (beginnend bei 1)
        endseite: Letzte zu extrahierende Seite (beginnend bei 1)
    """
    try:
        # Initialisiere PDF Reader und Writer
        reader = PdfReader(eingangs_pdf_pfad)
        writer = PdfWriter()

        # Übertrage Metadaten wenn vorhanden
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        # Konvertiere von menschlicher Seitenzählung (1-basiert)
        # zu Python-Indexierung (0-basiert)
        startseite_index = startseite - 1
        endseite_index = endseite - 1

        # Validiere die Seitenzahlen
        gesamt_seiten = len(reader.pages)
        if startseite_index < 0 or endseite_index >= gesamt_seiten:
            msg = (
                f"Ungültige Seitenzahlen. Die PDF hat {gesamt_seiten} Seiten. "
                f"Bitte Zahlen zwischen 1 und {gesamt_seiten} eingeben."
            )
            raise ValueError(msg)

        # Extrahiere die gewählten Seiten
        total_seiten = endseite - startseite + 1
        logging.info(
            "Extrahiere Kapitel von Seite %s bis %s (%s Seiten)",
            startseite,
            endseite,
            total_seiten,
        )

        for seitennummer in range(startseite_index, endseite_index + 1):
            writer.add_page(reader.pages[seitennummer])

        # Stelle sicher, dass das Ausgabeverzeichnis existiert
        output_dir = os.path.dirname(ausgangs_pdf_pfad)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Speichere die neue PDF
        with open(ausgangs_pdf_pfad, "wb") as ausgabe_pdf:
            writer.write(ausgabe_pdf)

        logging.info("✓ Kapitel erfolgreich gespeichert unter: %s", ausgangs_pdf_pfad)

    except (OSError, ValueError) as e:
        logging.exception("❌ Fehler beim Extrahieren des Kapitels: %s", e)
        raise


def pdf_in_kapitel_aufteilen(
    eingangs_pdf_pfad: str,
    kapitel_definitionen: list[dict[str, int]],
    output_dir: str = "Kapitel",
    dateiname_prefix: str = "Kapitel",
) -> None:
    """
    Teilt eine PDF-Datei in mehrere Kapitel basierend auf definierten Seitenbereichen.

    Args:
        eingangs_pdf_pfad: Pfad zur ursprünglichen PDF-Datei
        kapitel_definitionen: Liste mit Kapitelinformationen (Nr, Start- und Endseite)
        output_dir: Verzeichnis für die Ausgabedateien
        dateiname_prefix: Prefix für die Ausgabedateien
    """
    # Prüfe ob PDF existiert
    if not os.path.exists(eingangs_pdf_pfad):
        msg = f"Die Datei '{eingangs_pdf_pfad}' existiert nicht."
        raise ValueError(msg)

    # Erstelle Ausgabeverzeichnis falls nicht vorhanden
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info("Verzeichnis '%s' erstellt", output_dir)

    # Extrahiere jedes Kapitel
    for kapitel in kapitel_definitionen:
        kapitel_nr = kapitel["nr"]
        startseite = kapitel["start"]
        endseite = kapitel["ende"]

        # Generiere Dateinamen für das Kapitel
        ausgangs_pdf_pfad = os.path.join(
            output_dir, f"{dateiname_prefix}_{kapitel_nr}.pdf"
        )

        # Extrahiere das Kapitel
        extrahiere_kapitel(eingangs_pdf_pfad, ausgangs_pdf_pfad, startseite, endseite)

    logging.info(
        "✓ Alle %s Kapitel wurden erfolgreich extrahiert.", len(kapitel_definitionen)
    )


if __name__ == "__main__":
    try:
        # Banner ausgeben

        # Standard-Konfiguration
        eingangs_pdf = input("Pfad zur PDF-Datei [ebook.pdf]: ") or "ebook.pdf"
        ziel_verzeichnis = input("Ausgabeverzeichnis [Kapitel]: ") or "Kapitel"

        # Definiere die Kapitel für die gegebenen Seitenbereiche
        kapitel_bereiche = [
            {"nr": 1, "start": 14, "ende": 25},
            {"nr": 2, "start": 26, "ende": 31},
            {"nr": 3, "start": 32, "ende": 33},
            {"nr": 4, "start": 34, "ende": 41},
            {"nr": 5, "start": 42, "ende": 47},
        ]

        # Teile PDF in Kapitel
        pdf_in_kapitel_aufteilen(eingangs_pdf, kapitel_bereiche, ziel_verzeichnis)

    except ValueError as e:
        logging.exception("❌ Fehler: %s", e)
    except KeyboardInterrupt:
        logging.warning("Programm durch Benutzer abgebrochen")
    except OSError as e:
        logging.error("❌ Dateisystemfehler: %s", e, exc_info=True)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("❌ Unerwarteter Fehler: %s", e, exc_info=True)
