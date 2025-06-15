#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


class TableOfContentsGenerator:
    """Generiert automatisch HTML-Inhaltsverzeichnisse aus Dateien."""

    def __init__(
        self,
        source_dir: str = ".",
        output_file: str = "start.html",
        css_file: str = "start.css",
    ):
        self.source_dir = Path(source_dir)
        self.output_file = output_file
        self.css_file = css_file
        self.supported_extensions = {".html", ".htm"}
        self.excluded_files = {"info.html", "info.md"}

    def get_files(self) -> list[tuple[str, str]]:
        """
        Sammelt alle HTML-Dateien und extrahiert Titel.
        Rückgabe: Liste von (Dateiname, Titel) Tupeln
        """
        files = []
        try:
            for file_path in self.source_dir.iterdir():
                if (
                    file_path.is_file()
                    and file_path.suffix.lower() in self.supported_extensions
                    and file_path.name != self.output_file
                    and file_path.name.lower() not in self.excluded_files
                ):

                    title = self._extract_title(file_path)
                    files.append((file_path.name, title))

            # Sortierung nach Dateiname
            return sorted(files, key=lambda x: x[0])

        except OSError:
            return []

    def _extract_title(self, file_path: Path) -> str:
        """Extrahiert Titel aus HTML-Dateien."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read(1000)  # Nur ersten 1000 Zeichen lesen

                # HTML: <title>-Tag suchen
                title_match = re.search(
                    r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE
                )
                if title_match:
                    return title_match.group(1).strip()

        except (OSError, UnicodeDecodeError):
            pass

        # Fallback: Dateiname ohne Erweiterung verwenden
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    def create_html(self, files: list[tuple[str, str]]) -> bool:
        """Erstellt HTML-Inhaltsverzeichnis."""
        try:
            with open(self.output_file, "w", encoding="utf-8") as html:
                html.write("<!DOCTYPE html>\n")
                html.write('<html lang="de">\n')
                html.write("<head>\n")
                html.write('  <meta charset="utf-8">\n')
                html.write(
                    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                )
                html.write("  <title>Inhaltsverzeichnis</title>\n")
                html.write(f'  <link rel="stylesheet" href="{self.css_file}">\n')
                html.write("</head>\n")
                html.write("<body>\n")
                html.write("  <header>\n")
                html.write("    <h1>Inhaltsverzeichnis</h1>\n")
                html.write(
                    f'    <p class="subtitle">{len(files)} Dokumente gefunden</p>\n'
                )
                html.write("  </header>\n")
                html.write("  <main>\n")

                if files:
                    html.write('    <ol class="toc-list">\n')
                    for index, (filename, title) in enumerate(files, start=1):
                        html.write('      <li class="toc-item">\n')
                        html.write(f'        <a href="{filename}" class="toc-link">\n')
                        html.write(
                            f'          <span class="toc-number">{index:02d}.</span>\n'
                        )
                        html.write(
                            f'          <span class="toc-title">{title}</span>\n'
                        )
                        html.write(
                            f'          <span class="toc-filename">({filename})</span>\n'
                        )
                        html.write("        </a>\n")
                        html.write("      </li>\n")
                    html.write("    </ol>\n")
                else:
                    html.write('    <p class="no-files">Keine Dateien gefunden.</p>\n')

                html.write("  </main>\n")
                html.write("  <footer>\n")
                html.write("    <p>Automatisch generiert</p>\n")
                html.write("  </footer>\n")
                html.write("</body>\n")
                html.write("</html>\n")
            return True
        except OSError:
            return False

    def create_css(self) -> bool:
        """Erstellt erweiterte CSS-Datei."""
        css_content = """/* Reset und Basis-Styles */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Layout */
main {
  flex: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
  margin-bottom: 2rem;
}

/* Header */
header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

h1 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.subtitle {
  color: #6c757d;
  margin: 0;
  font-style: italic;
}

/* Inhaltsverzeichnis */
.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-item {
  margin: 0.75rem 0;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.toc-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.toc-link {
  display: flex;
  align-items: center;
  padding: 1rem 1.25rem;
  text-decoration: none;
  color: inherit;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.toc-link:hover {
  background: #e3f2fd;
  border-color: #2196f3;
  color: #1976d2;
}

.toc-number {
  font-weight: 700;
  color: #6c757d;
  margin-right: 1rem;
  min-width: 3rem;
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
}

.toc-title {
  flex: 1;
  font-weight: 600;
  font-size: 1.1rem;
}

.toc-filename {
  color: #6c757d;
  font-size: 0.9rem;
  font-family: 'Courier New', monospace;
  margin-left: 1rem;
}

/* Keine Dateien Nachricht */
.no-files {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
}

/* Footer */
footer {
  text-align: center;
  padding: 1rem;
  color: #6c757d;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  main {
    margin: 1rem;
    padding: 1rem;
    border-radius: 8px;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .toc-link {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.75rem 1rem;
  }
  
  .toc-number {
    margin-right: 0;
    margin-bottom: 0.25rem;
  }
  
  .toc-filename {
    margin-left: 0;
    margin-top: 0.25rem;
  }
}

@media (max-width: 480px) {
  .toc-filename {
    display: none;
  }
}

/* Fokus-Styles für Barrierefreiheit */
.toc-link:focus {
  outline: 3px solid #2196f3;
  outline-offset: 2px;
}

/* Print-Styles */
@media print {
  body {
    background: white;
  }
  
  main {
    box-shadow: none;
    margin: 0;
  }
  
  .toc-item:hover {
    transform: none;
    box-shadow: none;
  }
}"""

        try:
            with open(self.css_file, "w", encoding="utf-8") as css:
                css.write(css_content)
            return True
        except OSError:
            return False

    def generate(self) -> bool:
        """Hauptfunktion: Generiert komplettes Inhaltsverzeichnis."""
        files = self.get_files()

        if not files:
            return False

        for _filename, _title in files:
            pass

        if not self.create_html(files):
            return False

        return self.create_css()


def main():
    parser = argparse.ArgumentParser(
        description="Erstellt automatisch ein HTML-Inhaltsverzeichnis aus HTML-Dateien"
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=".",
        help="Quellverzeichnis (Standard: aktuelles Verzeichnis)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="start.html",
        help="Ausgabe-HTML-Datei (Standard: start.html)",
    )
    parser.add_argument(
        "-c", "--css", default="start.css", help="CSS-Datei (Standard: start.css)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ausführliche Ausgabe"
    )

    args = parser.parse_args()

    generator = TableOfContentsGenerator(
        source_dir=args.directory, output_file=args.output, css_file=args.css
    )

    success = generator.generate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
