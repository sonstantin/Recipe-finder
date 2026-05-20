# 🍲 Recipe Finder

**Recipe Finder** ist eine moderne Desktop-Anwendung zum Verwalten, Suchen und Organisieren von Rezepten.
Die App wurde mit Python und Tkinter entwickelt und bietet eine benutzerfreundliche Oberfläche mit Kategorien, Favoriten, Zutatenlisten und Bildunterstützung.

---

## ✨ Funktionen

* 🔍 Rezeptsuche über Titel
* 📂 Kategorien für verschiedene Gerichte
* ❤️ Favoriten-System
* 🛒 Zutaten- & Einkaufsliste
* 🖼️ Rezeptbilder
* 📜 Scrollbare Rezeptansicht
* ➕ Eigene Rezepte erstellen
* 💾 Speicherung aller Daten als JSON
* 🌐 Optionaler Servermodus
* 🎨 Moderne Oberfläche mit SVG-Piktogrammen

---

## 📦 Verwendete Bibliotheken

Das Projekt verwendet folgende Python-Bibliotheken:

* `tkinter`
* `ttk`
* `json`
* `os`
* `Pillow`
* `cairosvg`

Installation der benötigten Pakete:

```bash
pip install pillow cairosvg
```

---

## 📁 Projektstruktur

```plaintext
RecipeFinder/
│
├── Recipes/
│   ├── Pictures/
│   └── *.json
│
├── Ingredients/
│   └── ingredients.json
│
├── Pictograms/
│   └── *.svg
│
├── settings.json
├── categories.json
└── main.py
```

---

## 🚀 Starten der Anwendung

```bash
python main.py
```

Beim ersten Start erstellt die Anwendung automatisch alle benötigten Ordner und Dateien.

---

## 📝 Rezeptformat

Rezepte werden als JSON-Dateien gespeichert.

Beispiel:

```json
{
    "Title": "Spaghetti Carbonara",
    "Description": "Ein klassisches italienisches Nudelgericht.",
    "Category": "Nudelgerichte",
    "Ingredients": {
        "Spaghetti": "500g",
        "Eier": "3",
        "Parmesan": "100g"
    },
    "Liked": false,
    "Done": false
}
```

---

## 🖥️ Features der Oberfläche

* Sidebar-Navigation
* Dynamische Größenanpassung
* Scrollbare Inhalte
* SVG-Icons
* Vollbildmodus
* Debug-Modus (`STRG + ALT + D`)

---

## 🔧 Geplante Funktionen

* Cloud-/Server-Synchronisierung
* Mehrsprachigkeit
* Rezeptbilder direkt importieren
* Erweiterte Filtersuche
* Automatische Einkaufslisten-Kategorien
* Benutzerkonten

---


## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

