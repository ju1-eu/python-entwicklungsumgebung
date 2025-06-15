#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path


# Stellt sicher, dass pngquant installiert ist
def ensure_pngquant():
    try:
        subprocess.run(["pngquant", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["brew", "install", "pngquant"], check=True)
        except Exception:
            sys.exit(1)


# Stellt sicher, dass libheif installiert ist (für HEIC-Konvertierung)
def ensure_libheif():
    try:
        subprocess.run(["heif-convert", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["brew", "install", "libheif"], check=True)
        except Exception:
            sys.exit(1)


def optimize_images():
    """Optimiert PNG-, JPG- und HEIC-Bilder mit macOS-Bordmitteln"""
    # Verzeichnisse konfigurieren
    input_dir = Path("./bilder_original")
    output_dir = Path("./images")

    # Ausgabeverzeichnis erstellen
    output_dir.mkdir(exist_ok=True)

    # Prüfen, ob sips (macOS-Tool) verfügbar ist
    if not shutil.which("sips"):
        sys.exit(1)

    # Stellt sicher, dass benötigte Tools verfügbar sind
    ensure_pngquant()
    ensure_libheif()

    # Unterstützte Dateiformate (case-insensitive)
    image_extensions = [".png", ".heic", ".jpg", ".jpeg"]

    # Alle Dateien im Eingabeverzeichnis durchsuchen
    file_count = 0

    for file_path in input_dir.glob("*"):
        # Überprüft die Dateiendung unabhängig von der Groß-/Kleinschreibung
        if any(
            file_path.name.lower().endswith(ext.lower()) for ext in image_extensions
        ):
            file_count += 1
            filename = file_path.name
            file_extension = file_path.suffix.lower()
            base_name = file_path.stem

            # Originalgröße für Bericht
            original_size = os.path.getsize(file_path)

            # Bei HEIC-Dateien: Konvertierung nach PNG durchführen
            if file_extension.lower() == ".heic":
                temp_png_path = output_dir / f"temp_{base_name}.png"

                # HEIC zu PNG konvertieren
                subprocess.run(
                    ["heif-convert", str(file_path), str(temp_png_path)],
                    capture_output=True,
                    check=False,
                )

                # Für die weitere Verarbeitung verwenden wir den PNG-Pfad
                working_path = temp_png_path
                output_filename = f"{base_name}.png"
            # Bei JPG-Dateien: Behandlung entsprechend anpassen
            elif file_extension.lower() in [".jpg", ".jpeg"]:
                # JPG kopieren für die Bearbeitung
                temp_path = output_dir / f"temp_{filename}"
                shutil.copy2(file_path, temp_path)
                working_path = temp_path

                # JPG bleibt JPG, aber wir verwenden für die Ausgabe einheitlich .jpg
                if file_extension.lower() == ".jpeg":
                    output_filename = f"{base_name}.jpg"
                else:
                    output_filename = filename
            else:
                # Bei PNG-Dateien: Original kopieren für die Bearbeitung
                temp_path = output_dir / f"temp_{filename}"
                shutil.copy2(file_path, temp_path)
                working_path = temp_path
                output_filename = filename

            output_path = output_dir / output_filename

            # Größe mit sips anpassen (macOS-Bordmittel)
            subprocess.run(
                [
                    "sips",
                    "--resampleWidth",
                    "1200",
                    "--out",
                    str(working_path),
                    str(working_path),
                ],
                capture_output=True,
                check=False,
            )

            # Bei PNG-Dateien: pngquant für weitere Optimierung nutzen
            if file_extension.lower() == ".png" or (file_extension.lower() == ".heic"):
                subprocess.run(
                    [
                        "pngquant",
                        "--quality=65-80",
                        "--force",
                        "--output",
                        str(output_path),
                        str(working_path),
                    ],
                    check=False,
                )
            # Bei JPG-Dateien: sips für Kompression nutzen
            elif file_extension.lower() in [".jpg", ".jpeg"]:
                # JPG mit sips optimieren (Qualität anpassen)
                subprocess.run(
                    [
                        "sips",
                        "--setProperty",
                        "formatOptions",
                        "75",  # Qualität auf 75% setzen
                        "--out",
                        str(output_path),
                        str(working_path),
                    ],
                    capture_output=True,
                    check=False,
                )

            # Temporäre Datei löschen
            os.unlink(working_path)

            # Größenvergleich
            if output_path.exists():
                new_size = os.path.getsize(output_path)
                (1 - new_size / original_size) * 100
            else:
                pass

    if file_count == 0:
        pass
    else:
        pass


# Hauptfunktion
def main():
    optimize_images()


if __name__ == "__main__":
    main()
