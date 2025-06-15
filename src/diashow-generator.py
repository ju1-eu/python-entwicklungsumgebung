#!/usr/bin/env python3
"""
Diashow-Generator
----------------
Erzeugt eine HTML-Diashow mit optimierter Darstellung für große Bildschirme.
"""

import glob
import os
import re


# Funktion zur natürlichen Sortierung von Listen (z. B. 1, 2, 10 statt 1, 10, 2)
def natürlich_sortieren(liste):
    """Sortiert eine Liste auf natürliche Weise (z.B. '1.2' vor '1.10')."""

    def extrahiere_nummern(text):
        # Teilt den Text in Zahlen und Nicht-Zahlen auf, Zahlen werden als Integer verglichen
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", text)]

    return sorted(liste, key=extrahiere_nummern)


# Funktion zur Bildersuche in angegebenen Ordnern
def sammle_bilder(ordner_liste):
    """Sammelt alle Bilder aus den angegebenen Ordnern."""
    bild_dateien = []
    for ordner in ordner_liste:
        if not os.path.exists(ordner):
            # Ausgabe einer Warnung, falls ein Ordner nicht existiert
            continue

        # Sucht nach Bilddateien mit den Endungen png, jpg, jpeg, gif - sowohl Groß- als auch Kleinschreibung
        datei_muster = []

        # Füge alle Varianten für Groß- und Kleinschreibung hinzu
        for endung in ["png", "jpg", "jpeg", "gif"]:
            # Kleinbuchstaben
            datei_muster.append(os.path.join(ordner, f"*.{endung}"))
            # Großbuchstaben
            datei_muster.append(os.path.join(ordner, f"*.{endung.upper()}"))
            # Gemischt (nur erste Buchstabe groß)
            datei_muster.append(os.path.join(ordner, f"*.{endung.capitalize()}"))

        # Sammle alle passenden Dateien
        for muster in datei_muster:
            bild_dateien.extend(glob.glob(muster))

    # Entferne Duplikate (falls ein Bild mehrmals gefunden wurde) und sortiere natürlich
    bild_dateien = list(set(bild_dateien))
    return natürlich_sortieren(bild_dateien)


# Funktion zur Erzeugung des HTML-Codes für die Diashow
def erzeuge_html(bild_liste, titel="Bildergalerie"):
    """Erzeugt HTML-Code für die Diashow mit optimierter Darstellung."""
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titel}</title>
    <link rel="stylesheet" href="diashow.css">
</head>
<body>
    <div class="diashow-container">
        <h1>{titel}</h1>
        
        <div class="diashow">
"""
    # Hinzufügen der einzelnen Slides mit Bild und Bildinformationen
    for index, bild in enumerate(bild_liste):
        bild_pfad = bild.replace("\\", "/")  # Anpassung des Pfads für HTML
        ordner_name = os.path.basename(os.path.dirname(bild))
        datei_name = os.path.basename(bild)

        html += f"""            <div class="slide">
                <img src="{bild_pfad}" alt="{datei_name}" loading="lazy">
                <div class="bildinfo">
                    <span class="ordner">{ordner_name} /</span>
                    <span class="datei">{datei_name}</span>
                </div>
            </div>
"""

    # Hinzufügen der Navigationselemente (vorheriger/nächster Slide und Anzeige der Slide-Nummer)
    html += """        </div>
        
        <div class="navigation">
            <button class="prev">Zurück</button>
            <span class="slide-nummer">1 / <span class="gesamt">0</span></span>
            <button class="next">Weiter</button>
        </div>
        
        <div class="miniatur-container">
"""
    # Einbindung der Miniaturansichten (Thumbnails) für jedes Bild
    for index, bild in enumerate(bild_liste):
        bild_pfad = bild.replace("\\", "/")
        html += f'            <img class="miniatur" src="{bild_pfad}" alt="Miniatur" data-index="{index}" loading="lazy">\n'

    # Einbindung der externen JavaScript-Datei für die Diashow-Funktionalität
    html += """        </div>
    </div>

    <script src="diashow.js"></script>
</body>
</html>
"""
    return html


# Funktion zur Erzeugung des CSS-Codes für die Diashow
def erzeuge_css():
    """Erzeugt CSS-Code für die Diashow mit responsivem Design für große Bildschirme."""
    return """/* Diashow Styling - Mit optimierter Bildgröße für größere Bildschirme */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Farbschema und Variablen */
:root {
    --bg-color: #f5f5f5;
    --container-bg: white;
    --container-shadow: rgba(0, 0, 0, 0.1);
    --dark-grey-bg: #2B3E51;
    --text-color: #333;
    --title-color: #222222; 
    --info-bg: var(--dark-grey-bg);
    --info-folder-color: hsl(199, 100%, 61%);
    --info-file-color: hsl(199, 100%, 61%);
    --button-bg: hsl(0, 85%, 35%);
    --button-hover: #d02222;
    --nav-bg: var(--dark-grey-bg);
    --slide-number-color: #e0e0e0;
    --miniatur-border: #ddd;
    --miniatur-active: hsl(199, 100%, 61%);
    --miniatur-hover: hsl(0, 85%, 35%);
    --navigation-bg: var(--nav-bg);
    --navigation-border: #444;
    --miniatur-container-bg: rgba(0, 0, 0, 0.05);
    --miniatur-container-border: rgba(0, 0, 0, 0.1);
}

body {
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
    padding: 20px;
}

.diashow-container {
    max-width: 1200px;
    width: 95%;
    margin: 0 auto;
    background: var(--container-bg);
    border-radius: 8px;
    box-shadow: 0 0 10px var(--container-shadow);
    padding: 20px;
    border: 1px solid #ddd;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    color: var(--title-color);
    font-size: 28px;
    font-weight: 500;
    letter-spacing: 1px;
}

.diashow {
    position: relative;
    margin-bottom: 0;
    border: 1px solid #444;
    background: var(--dark-grey-bg);
    overflow: hidden;
    border-radius: 4px 4px 0 0;
    height: auto;
}

.slide {
    display: none;
    text-align: center;
}

.slide img {
    max-width: 100%;
    max-height: 800px;
    width: auto;
    height: auto;
    display: block;
    margin: 0 auto;
    padding: 10px;
    object-fit: contain;
}

.bildinfo {
    background: var(--info-bg);
    color: var(--info-folder-color);
    padding: 10px 15px;
    position: relative;
    bottom: 0;
    width: 100%;
    text-align: left;
    font-size: 16px;
    border-top: 1px solid #444;
}

.ordner {
    font-weight: bold;
    margin-right: 1px;
    color: var(--info-folder-color);
}

.datei {
    font-style: italic;
    color: var(--info-file-color);
}

.navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 0 15px 0;
    background: var(--navigation-bg);
    padding: 12px 15px;
    border-radius: 0 0 4px 4px;
    border: 1px solid #444;
    border-top: none;
}

button {
    background: var(--button-bg);
    color: white;
    border: none;
    padding: 12px 25px;
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.2s, transform 0.1s;
    font-weight: bold;
    font-size: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

button:hover {
    background: var(--button-hover);
    transform: translateY(-1px);
}

button:active {
    transform: translateY(1px);
}

.slide-nummer {
    font-size: 20px;
    color: var(--slide-number-color);
    font-weight: bold;
}

.miniatur-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    margin-top: 20px;
    background: var(--miniatur-container-bg);
    padding: 18px;
    border-radius: 4px;
    border: 1px solid var(--miniatur-container-border);
}

.miniatur {
    width: 100px;
    height: 75px;
    object-fit: cover;
    cursor: pointer;
    border: 2px solid var(--miniatur-border);
    border-radius: 4px;
    transition: all 0.3s;
}

.miniatur:hover {
    border-color: var(--miniatur-hover);
    transform: scale(1.05);
}

.miniatur.aktiv {
    border-color: var(--miniatur-active);
    box-shadow: 0 0 8px rgba(57, 194, 255, 0.6);
}

/* Responsives Design für verschiedene Bildschirmgrößen */
@media (min-width: 1600px) {
    .diashow-container {
        max-width: 1500px;
    }
    
    .slide img {
        max-height: 900px;
    }
    
    h1 {
        font-size: 32px;
    }
    
    .miniatur {
        width: 120px;
        height: 90px;
    }
    
    button {
        padding: 14px 30px;
        font-size: 18px;
    }
    
    .slide-nummer {
        font-size: 22px;
    }
}

@media (max-width: 1200px) {
    .diashow-container {
        width: 95%;
    }
    
    .slide img {
        max-height: 700px;
    }
}

@media (max-width: 768px) {
    .diashow-container {
        padding: 10px;
        width: 98%;
    }
    
    h1 {
        font-size: 20px;
    }
    
    .slide img {
        max-height: 500px;
    }
    
    button {
        padding: 8px 15px;
        font-size: 14px;
    }
    
    .miniatur {
        width: 70px;
        height: 52px;
    }
}

@media (max-width: 480px) {
    .slide img {
        max-height: 350px;
    }
    
    .miniatur {
        width: 60px;
        height: 45px;
    }
    
    .miniatur-container {
        gap: 8px;
        padding: 10px;
    }
    
    button {
        padding: 8px 12px;
    }
}"""


# Funktion zur Erzeugung des JavaScript-Codes, der die Diashow interaktiv macht
def erzeuge_js():
    """Erzeugt JavaScript-Code für die Diashow-Funktionalität."""
    return """document.addEventListener('DOMContentLoaded', function() {
    // Auswahl der HTML-Elemente für Slides, Miniaturen, Navigation und Anzeige der Slide-Nummer
    const slides = document.querySelectorAll('.slide');
    const miniaturen = document.querySelectorAll('.miniatur');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const slideNummerElement = document.querySelector('.slide-nummer');
    const gesamtElement = document.querySelector('.gesamt');
    
    let aktuellerSlide = 0;
    const slidesAnzahl = slides.length;
    
    // Initialisierung: Gesamtzahl der Slides wird angezeigt und der erste Slide aktiviert
    gesamtElement.textContent = slidesAnzahl;
    aktualisiereAnzeige();
    
    // Event-Listener für die Navigationstasten
    prevButton.addEventListener('click', zeigeVorherigenSlide);
    nextButton.addEventListener('click', zeigeNächstenSlide);
    
    // Klick-Events für die Miniaturansichten: Auswahl eines spezifischen Slides
    miniaturen.forEach(miniatur => {
        miniatur.addEventListener('click', function() {
            aktuellerSlide = parseInt(this.dataset.index);
            aktualisiereAnzeige();
        });
    });
    
    // Tastatur-Navigation mittels Pfeiltasten
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            zeigeVorherigenSlide();
        } else if (e.key === 'ArrowRight') {
            zeigeNächstenSlide();
        }
    });
    
    // Funktion zur Anzeige des vorherigen Slides
    function zeigeVorherigenSlide() {
        aktuellerSlide = (aktuellerSlide - 1 + slidesAnzahl) % slidesAnzahl;
        aktualisiereAnzeige();
    }
    
    // Funktion zur Anzeige des nächsten Slides
    function zeigeNächstenSlide() {
        aktuellerSlide = (aktuellerSlide + 1) % slidesAnzahl;
        aktualisiereAnzeige();
    }
    
    // Aktualisiert die Anzeige: aktueller Slide, Slide-Nummer und aktive Miniaturansicht
    function aktualisiereAnzeige() {
        // Alle Slides zunächst ausblenden
        slides.forEach(slide => {
            slide.style.display = 'none';
        });
        
        // Den aktuellen Slide einblenden
        slides[aktuellerSlide].style.display = 'block';
        
        // Aktualisierung der angezeigten Slide-Nummer
        slideNummerElement.textContent = `${aktuellerSlide + 1} / ${slidesAnzahl}`;
        
        // Hervorhebung der aktiven Miniaturansicht
        miniaturen.forEach((miniatur, index) => {
            if (index === aktuellerSlide) {
                miniatur.classList.add('aktiv');
            } else {
                miniatur.classList.remove('aktiv');
            }
        });
        
        // Optionale Funktion: Automatisches Scrollen zur aktiven Miniatur (besonders auf mobilen Geräten)
        const activeMiniatur = document.querySelector('.miniatur.aktiv');
        if (activeMiniatur) {
            activeMiniatur.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
            });
        }
    }
});"""


# Hauptfunktion des Skripts
def main():
    # Festlegung der Ordner, in denen nach Bildern gesucht wird
    # ordner = ["Hochdruckerzeugung", "Hochdruckregelung", "Rail"]
    ordner = ["images"]

    # Filterung der existierenden Ordner
    vorhandene_ordner = [o for o in ordner if os.path.exists(o)]
    if not vorhandene_ordner:
        return

    # Sammlung der Bilder aus den vorhandenen Ordnern
    bilder = sammle_bilder(vorhandene_ordner)

    if not bilder:
        return

    # Erzeugung eines Titels für die Diashow
    titel = "Diashow"

    # Erstellung der Inhalte für HTML, CSS und JavaScript
    html_inhalt = erzeuge_html(bilder, titel)
    css_inhalt = erzeuge_css()
    js_inhalt = erzeuge_js()

    # Speichern der erzeugten Dateien
    with open("diashow.html", "w", encoding="utf-8") as html_datei:
        html_datei.write(html_inhalt)

    with open("diashow.css", "w", encoding="utf-8") as css_datei:
        css_datei.write(css_inhalt)

    with open("diashow.js", "w", encoding="utf-8") as js_datei:
        js_datei.write(js_inhalt)

    # Konsolenausgaben zur Bestätigung und weiteren Anweisungen


# Ausführung der Hauptfunktion, falls das Skript direkt gestartet wird
if __name__ == "__main__":
    main()
