#!/usr/bin/env python3
"""
Erweiterter Markdown zu HTML Konverter mit Pandoc, Tabellenstil,
Visualisierungsunterstützung und MathJax für mathematische Formeln.
Konvertiert alle *.md Dateien im aktuellen Verzeichnis sowie im docs/-Verzeichnis zu *.html Dateien,
unterstützt Mermaid-Diagramme und mathematische Formeln,
und erstellt eine start.html mit Links zu allen HTML-Dateien.
"""

import argparse
import datetime
import glob
import os
import re
import shutil
import subprocess
from pathlib import Path


def check_pandoc():
    """Prüft, ob Pandoc installiert ist."""
    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except:
        return False


def create_main_enhanced_filter():
    """
    Erstellt/überschreibt main_enhanced_filter.lua so, dass:
    - Tabellen die CSS-Klasse 'cr-table' erhalten
    - Ein Hauptcontainer den Inhalt umschließt
    - Mermaid-Diagramme umgewandelt werden
    - MathJax-Formeln korrekt verarbeitet werden
    """
    lua_content = r"""--[[
main_enhanced_filter.lua - Ein erweiterter Pandoc Lua-Filter
- Fügt allen Tabellen die CSS-Klasse 'cr-table' hinzu
- Umschließt den Inhalt mit einem Hauptcontainer
- Erkennt und formatiert Mermaid-Diagramme und andere Visualisierungen
- Behandelt TeX-Formeln korrekt für MathJax
]]--

-- Funktion, die auf jede Tabelle im Dokument angewendet wird
function Table(el)
  el.classes:insert('cr-table')
  return el
end

-- Funktion zur Erkennung und Formatierung von Mermaid-Diagrammen
function CodeBlock(block)
  if block.classes:includes("mermaid") then
    local html = string.format([[
<div class="mermaid">
%s
</div>
]], block.text)
    return pandoc.RawBlock('html', html)
  end
  return block
end

function Math(el)
  if el.mathtype == "InlineMath" then
    local html = '<span class="math math-inline">$' .. el.text .. '$</span>'
    return pandoc.RawInline('html', html)

  elseif el.mathtype == "DisplayMath" then
    local html = '<div class="math math-display">$$' .. el.text .. '$$</div>'
    return pandoc.RawBlock('html', html)
  end

  return el
end



function Pandoc(doc)
  local main_container_begin = '<div class="main-container">'
  local main_container_end   = '</div>'

  -- Mermaid
  local mermaid_script = [==[
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis',
        // Anpassen der Knotenformen und Farben
        nodeSpacing: 50,
        rankSpacing: 70,
        // Farb-Thema für Diagrammelemente
        defaultRenderer: 'dagre-d3'
      },
      // Farbpalette anpassen
      themeVariables: {
        primaryColor: '#326693',
        primaryTextColor: '#fff',
        primaryBorderColor: '#1f4060',
        lineColor: '#326693',
        secondaryColor: '#f0f0f0',
        tertiaryColor: '#e6f3ff',
        nodeBorder: '#326693',
        mainBkg: '#e6f3ff',
        clusterBkg: '#f0f7ff',
        clusterBorder: '#326693',
        fontSize: '16px'
      }
    });
  });
</script>
]==]

  -- MathJax (mit [==[...]==] und KEIN [['...']] in den Arrays)
  local mathjax_script = [==[
<script>
MathJax = {
  tex: {
    inlineMath: [["$","$"], ["\\(","\\)"]],
    displayMath: [["$$","$$"], ["\\[","\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"]
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
]==]

  -- Hauptcontainer
  local header_include = pandoc.RawBlock('html', main_container_begin)
  local footer_include = pandoc.RawBlock('html', main_container_end)
  table.insert(doc.blocks, 1, header_include)
  table.insert(doc.blocks, footer_include)

  -- Einbinden in den HTML-Header
  if doc.meta.header == nil then
    doc.meta.header = pandoc.MetaBlocks({})
  end
  if type(doc.meta.header) == 'table' and doc.meta.header.t == 'MetaBlocks' then
    table.insert(doc.meta.header.content, pandoc.RawBlock('html', mermaid_script))
    table.insert(doc.meta.header.content, pandoc.RawBlock('html', mathjax_script))
  else
    doc.meta.header = pandoc.MetaBlocks({
      pandoc.RawBlock('html', mermaid_script),
      pandoc.RawBlock('html', mathjax_script)
    })
  end

  -- Markierung, ob mermaid/math vorhanden
  local has_mermaid = false
  local has_math = false

  for _, block in ipairs(doc.blocks) do
    if block.t == "RawBlock" and block.format == "html" and block.text:match('<div class="mermaid">') then
      has_mermaid = true
    end
    if block.t == "CodeBlock" and block.classes:includes("mermaid") then
      has_mermaid = true
    end
    if block.t == "Math" then
      has_math = true
    end
  end
  if has_mermaid then
    doc.meta.has_mermaid = pandoc.MetaBool(true)
  end
  if has_math then
    doc.meta.has_math = pandoc.MetaBool(true)
  end

  return doc
end

return {
  Table = Table,
  CodeBlock = CodeBlock,
  Math = Math,
  Pandoc = Pandoc
}
"""
    with open("main_enhanced_filter.lua", "w", encoding="utf-8") as f:
        f.write(lua_content)


def enhance_css_file():
    """Erweitert 'main-design.css' um CSS-Regeln für Visualisierungen und Math."""
    css_file = "main-design.css"
    if not os.path.exists(css_file):
        return

    visualization_and_math_css = r"""
/* Spezifische Formatierung für Mermaid-Diagramme */
.mermaid {
  display: flex;
  justify-content: center;
  margin: 1.5rem auto;
  padding: 1rem;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  overflow-x: auto;
}

/* Formatierungen für Charts und Grafiken */
.chart-container {
  margin: 1.5rem auto;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  max-width: 100%;
}

/* Anpassungen für interaktive Visualisierungen */
.interactive-viz {
  width: 100%;
  height: auto;
  min-height: 400px;
  margin: 1.5rem auto;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
}

/* Diagramm-Beschriftungen */
.viz-caption {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

/* Legenden für Diagramme */
.viz-legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.85rem;
}
.viz-legend-item {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}
.viz-legend-color {
  width: 12px;
  height: 12px;
  margin-right: 5px;
  border-radius: 2px;
}

/* Formatierung für mathematische Formeln */
.math {
  font-size: 0.85em;
  overflow-x: auto;
  max-width: 100%;
  padding: 0.2rem 0;
}

/* Inline-Formeln */
.math-inline {
  display: inline-block;
  margin: 0 0.2rem;
}

/* Block-Formeln */
.math-display {
  display: block;
  margin: 1rem auto;
  text-align: center;
}

/* Responsives Verhalten */
@media (max-width: 768px) {
  .mermaid, .chart-container {
    padding: 0.5rem;
  }
  .interactive-viz {
    min-height: 300px;
  }
  .math-display {
    font-size: 0.95rem;
  }
}

/* Bei Ausdruck Seitenumbrüche an sinnvollen Stellen */
@media print {
  .mermaid, .chart-container, .interactive-viz, .math-display {
    page-break-inside: avoid;
    box-shadow: none;
    border: 1px solid #e0e0e0;
  }
}
"""
    with open(css_file, encoding="utf-8") as f:
        content = f.read()

    if ".mermaid {" not in content:
        with open(css_file, "a", encoding="utf-8") as f:
            f.write(
                "\n\n/* Formatierungen für Visualisierungen und mathematische Formeln */\n"
            )
            f.write(visualization_and_math_css)
    elif ".math {" not in content:
        with open(css_file, "a", encoding="utf-8") as f:
            f.write("\n\n/* Formatierungen für mathematische Formeln */\n")
            f.write(
                """
.math {
  font-size: 1.05rem;
  overflow-x: auto;
  max-width: 100%;
  padding: 0.2rem 0;
}
.math-inline {
  display: inline-block;
  margin: 0 0.2rem;
}
.math-display {
  display: block;
  margin: 1rem auto;
  text-align: center;
}
"""
            )
    else:
        pass


def check_and_fix_content(md_files):
    """Scannt Markdown-Dateien nach Mermaid und Mathe."""
    files_with_mermaid = []
    files_with_math = []
    files_updated = []

    mermaid_pattern = re.compile(
        r"```(?:mermaid|)\s?.*?```|~~~(?:mermaid|)\s?.*?~~~", re.DOTALL
    )
    raw_mermaid_pattern = re.compile(
        r"(\n\s*)(graph|flowchart)\s+TD\s+[A-Z]", re.MULTILINE
    )
    math_pattern = re.compile(
        r"(?:\$.*?\$)|(?:\\\(.*?\\\))|(?:\\\[.*?\\\])|(?:\$\$.*?\$\$)", re.DOTALL
    )

    for md_file in md_files:
        try:
            with open(md_file, encoding="utf-8") as f:
                content = f.read()

            has_mermaid = False
            has_math = False
            content_modified = False

            if (
                mermaid_pattern.search(content)
                or "flowchart" in content
                or "graph TD" in content
            ):
                has_mermaid = True

            if math_pattern.search(content) or "\\frac" in content or "_{" in content:
                has_math = True

            # Beispielhaftes Ersetzen unformatierter Mermaid-Diagramme
            if raw_mermaid_pattern.search(content) and not mermaid_pattern.search(
                content
            ):
                content_new = raw_mermaid_pattern.sub(
                    r"\1```mermaid\n\1flowchart TD ", content
                )
                lines = content_new.split("\n")
                in_mermaid = False
                for i, line in enumerate(lines):
                    if "```mermaid" in line and not in_mermaid:
                        in_mermaid = True
                    elif (
                        in_mermaid
                        and not line.strip()
                        and i < len(lines) - 1
                        and not lines[i + 1].startswith(" ")
                    ):
                        lines[i] = "```\n"
                        in_mermaid = False
                        content_modified = True
                if in_mermaid:
                    lines.append("```")
                    content_modified = True

                content_new = "\n".join(lines)
                if "graph TD" in content_new:
                    content_new = content_new.replace("graph TD", "flowchart TD")
                    content_modified = True

                if content_modified:
                    with open(md_file, "w", encoding="utf-8") as f:
                        f.write(content_new)
                    files_updated.append(md_file)

            if has_mermaid:
                files_with_mermaid.append(md_file)
            if has_math:
                files_with_math.append(md_file)

        except Exception:
            pass

    return files_with_mermaid, files_with_math, files_updated


def generate_start_page(html_files_by_dir=None):
    """Erstellt eine start.html, welche Links zu allen .html-Dateien enthält."""
    if html_files_by_dir is None:
        # Suche HTML-Dateien im aktuellen Verzeichnis
        root_html_files = [
            f for f in glob.glob("*.html") if f not in ["start.html", "info.html"]
        ]

        # Suche HTML-Dateien im docs-Verzeichnis
        docs_html_files = []
        if os.path.isdir("docs"):
            docs_html_files = [
                os.path.join("docs", f) for f in glob.glob("docs/*.html")
            ]

        html_files_by_dir = {"root": root_html_files, "docs": docs_html_files}

    all_files = []
    for files in html_files_by_dir.values():
        all_files.extend(files)

    if not all_files:
        return

    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dokumentation - Startseite</title>
    <link rel="stylesheet" href="main-design.css">
</head>
<body>
    <div class="main-container">
        <h1>Technische Dokumentation</h1>
        
        <h2>Dokumente</h2>
"""

    if html_files_by_dir["root"]:
        html_files_by_dir["root"].sort()
        html_content += """
        <h3>Hauptverzeichnis</h3>
        <ul class="documentation-list">
"""
        for html_file in html_files_by_dir["root"]:
            title = Path(html_file).stem.replace("-", " ")
            html_content += f'            <li><a href="{html_file}">{title}</a></li>\n'
        html_content += "        </ul>\n"

    if html_files_by_dir["docs"]:
        html_files_by_dir["docs"].sort()
        html_content += """
        <h3>Docs-Verzeichnis</h3>
        <ul class="documentation-list">
"""
        for html_file in html_files_by_dir["docs"]:
            title = Path(html_file).stem.replace("-", " ")
            # Relativer Pfad für den Link
            html_content += f'            <li><a href="{html_file}">{title}</a></li>\n'
        html_content += "        </ul>\n"

    html_content += f"""
        <footer>
            <p>Dokumentation generiert am {current_time}</p>
        </footer>
    </div>
</body>
</html>
"""
    with open("start.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def create_mathjax_header():
    """Erstellt und gibt den Dateinamen einer temporären MathJax-Headerdatei zurück."""
    mathjax_header = r"""
<script>
MathJax = {
  tex: {
    inlineMath: [["$","$"], ["\\(","\\)"]],
    displayMath: [["$$","$$"], ["\\[","\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"]
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
"""
    with open("mathjax-header.html", "w", encoding="utf-8") as f:
        f.write(mathjax_header)
    return "mathjax-header.html"


def ensure_css_for_docs_dir():
    """Stellt sicher, dass die CSS-Datei auch im docs-Verzeichnis verfügbar ist."""
    css_file = "main-design.css"
    docs_css_path = os.path.join("docs", css_file)

    if not os.path.exists("docs"):
        os.makedirs("docs", exist_ok=True)

    if os.path.exists(css_file) and not os.path.exists(docs_css_path):
        shutil.copy2(css_file, docs_css_path)


def convert_all_markdown_files(args):
    """Konvertiert alle *.md-Dateien mithilfe von Pandoc und dem Lua-Filter."""
    if not check_pandoc():
        return

    create_main_enhanced_filter()  # hier wird die korrigierte Lua-Datei erzeugt
    enhance_css_file()  # CSS ergänzen

    css_file = "main-design.css"
    if not os.path.exists(css_file):
        pass

    # Verzeichnisse mit Markdown-Dateien
    md_dirs = [".", "docs"]

    # Sammle alle Markdown-Dateien
    if args.files:
        markdown_files = [f for f in args.files if f.endswith(".md")]
    else:
        markdown_files = []
        for md_dir in md_dirs:
            if os.path.isdir(md_dir):
                for md_file in glob.glob(os.path.join(md_dir, "*.md")):
                    markdown_files.append(md_file)

    if not markdown_files:
        return

    files_with_mermaid, files_with_math, files_updated = check_and_fix_content(
        markdown_files
    )
    if files_with_mermaid:
        pass
    if files_with_math:
        pass
    if files_updated:
        pass

    # Sorge dafür, dass CSS auch im docs-Verzeichnis vorhanden ist
    ensure_css_for_docs_dir()

    mermaid_header_file = "mermaid-header.html"
    mathjax_header_file = create_mathjax_header()

    # Kurzes Mermaid-Headerfile
    with open(mermaid_header_file, "w", encoding="utf-8") as f:
        f.write(
            r"""
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      flowchart: { 
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis',
        nodeSpacing: 50,
        rankSpacing: 70,
        defaultRenderer: 'dagre-d3'
      },
      themeVariables: {
        primaryColor: '#326693',
        primaryTextColor: '#fff',
        primaryBorderColor: '#1f4060',
        lineColor: '#326693',
        secondaryColor: '#f0f0f0',
        tertiaryColor: '#e6f3ff',
        nodeBorder: '#326693',
        mainBkg: '#e6f3ff',
        clusterBkg: '#f0f7ff',
        clusterBorder: '#326693',
        fontSize: '16px'
      }
    });
  });
</script>
"""
        )

    # Erfolgreich konvertierte HTML-Dateien nach Verzeichnis ordnen
    html_files_by_dir = {"root": [], "docs": []}

    for md_file in markdown_files:
        html_file = Path(md_file).with_suffix(".html")

        # Bestimme das Zielverzeichnis
        target_dir = os.path.dirname(md_file)
        html_category = "root" if target_dir == "." else "docs"

        cmd = [
            "pandoc",
            md_file,
            "-o",
            str(html_file),
            "--standalone",
            "--css",
            css_file,
            "--lua-filter=main_enhanced_filter.lua",
            "--mathjax",
        ]
        if md_file in files_with_mermaid:
            cmd.append(f"--include-in-header={mermaid_header_file}")
        if md_file in files_with_math:
            cmd.append(f"--include-in-header={mathjax_header_file}")

        try:
            subprocess.run(cmd, check=True)
            html_files_by_dir[html_category].append(str(html_file))
        except subprocess.CalledProcessError:
            pass

    for temp_file in [mermaid_header_file, mathjax_header_file]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    if not args.no_start_page:
        generate_start_page(html_files_by_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Konvertiert Markdown-Dateien zu HTML mit Visualisierungs- und MathJax-Unterstützung."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Spezifische Markdown-Dateien, die konvertiert werden sollen (optional)",
    )
    parser.add_argument(
        "--no-start-page", action="store_true", help="Keine Startseite generieren"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Ausführliche Ausgabe"
    )

    args = parser.parse_args()
    convert_all_markdown_files(args)


if __name__ == "__main__":
    main()
