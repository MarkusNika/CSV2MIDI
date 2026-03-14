# CSV2MIDI Converter

🎵 Einfacher und flexibler CSV to MIDI Converter für Musiker, Komponisten und Entwickler.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Features

- ✅ **CSV-Format**: Einfache, menschenlesbare Musiknotation
- ✅ **Multi-Track Support**: Mehrere Instrumente/Spuren pro Song
- ✅ **GUI & CLI**: Grafische Oberfläche und Kommandozeilen-Tool
- ✅ **Batch-Processing**: Mehrere CSV-Dateien auf einmal konvertieren
- ✅ **Validation**: Automatische Überprüfung der CSV-Daten
- ✅ **CSV-Editor**: Integrierter Editor zum Erstellen/Bearbeiten
- ✅ **DAW-kompatibel**: Import in Reaper, Ableton, Logic, etc.

---

## 🚀 Quick Start

### Installation

```bash
# Repository klonen
git clone https://github.com/MarkusNika/CSV2MIDI.git
cd CSV2MIDI

# Virtual Environment erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ODER
.venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### GUI starten

```bash
python gui_launcher.py
```

### CLI verwenden

```bash
# Einzelne Datei konvertieren
python main.py convert examples/simple_melody.csv output.mid

# Mit Optionen
python main.py convert input.csv --tempo 140 --time-sig 3/4

# Batch-Konvertierung
python main.py batch ./csv_files ./midi_files

# CSV validieren
python main.py validate input.csv
```

---

## 📋 CSV-Format

### Beispiel

```csv
track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,100,1,1.0,1.0
Piano,1,E,4,100,1,2.0,1.0
Piano,1,G,4,100,1,3.0,1.0
Bass,2,C,2,110,1,1.0,4.0
```

### Spalten-Beschreibung

| Spalte | Beschreibung | Wertebereich |
|--------|--------------|--------------|
| `track_name` | Name der Spur | Text |
| `midi_channel` | MIDI-Kanal | 1-16 |
| `note` | Notenname | C, Cs/Db, D, Ds/Eb, E, F, Fs/Gb, G, Gs/Ab, A, As/Bb, B |
| `octave` | Oktave | 0-10 |
| `velocity` | Anschlagstärke | 0-127 |
| `bar` | Takt | >= 1 |
| `beat` | Zählzeit im Takt | >= 1.0 |
| `duration` | Notenlänge in Beats | > 0.0 |

### Notenwerte

- `1.0` = Viertelnote
- `2.0` = Halbe Note
- `0.5` = Achtelnote
- `0.25` = Sechzehntelnote
- `1.5` = Punktierte Viertelnote

---

## 🎹 Verwendung mit KI

CSV2MIDI ist ideal für KI-gestützte Musikkomposition:

```
Prompt an KI:
"Komponiere eine einfache Klaviermelodie in C-Dur und gebe sie als CSV im CSV2MIDI-Format aus."
```

Die KI kann direkt das CSV-Format generieren, welches dann sofort konvertiert werden kann!

---

## 📂 Projekt-Struktur

```Structure
CSV2MIDI/
├── csv2midi/
│   ├── core/              # Kern-Logik
│   │   ├── models.py      # Datenmodelle
│   │   ├── parser.py      # CSV Parser
│   │   ├── converter.py   # MIDI Converter
│   │   └── validator.py   # CSV Validation
│   ├── gui/               # PyQt5 GUI
│   │   ├── main_window.py # Hauptfenster
│   │   └── widgets.py     # Custom Widgets
│   └── cli/               # Command Line Interface
│       └── commands.py    # Click Commands
├── examples/              # Beispiel CSV-Dateien
│   ├── simple_melody.csv
│   ├── drum_pattern.csv
│   └── full_song.csv
├── tests/                 # Unit Tests
│   ├── test_parser.py
│   ├── test_converter.py
│   └── test_validator.py
├── main.py               # CLI Entry Point
├── gui_launcher.py       # GUI Entry Point
├── requirements.txt      # Dependencies
├── setup.py             # Package Setup
└── README.md            # Diese Datei
```

---

## 🧪 Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=csv2midi

# Einzelner Test
pytest tests/test_parser.py
```

---

## 🎼 Beispiele

### Einfache Melodie

```csv
track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,100,1,1.0,1.0
Piano,1,D,4,100,1,2.0,1.0
Piano,1,E,4,100,1,3.0,1.0
Piano,1,F,4,100,1,4.0,1.0
Piano,1,G,4,100,2,1.0,4.0
```

### Akkorde

```csv
track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,90,1,1.0,2.0
Piano,1,E,4,90,1,1.0,2.0
Piano,1,G,4,90,1,1.0,2.0
Piano,1,F,4,90,1,3.0,2.0
Piano,1,A,4,90,1,3.0,2.0
Piano,1,C,5,90,1,3.0,2.0
```

### Drum Pattern

```csv
track_name,midi_channel,note,octave,velocity,bar,beat,duration
Drums,10,C,2,120,1,1.0,0.25
Drums,10,D,2,80,1,1.5,0.25
Drums,10,C,2,120,1,2.0,0.25
Drums,10,D,2,80,1,2.5,0.25
```

**Hinweis**: MIDI-Kanal 10 ist standardmäßig für Drums reserviert.

---

## 🛠️ Development Log

Entwicklung im Team Mensch (Markus) + KI (Claude)

| Phase | Features | Team Zeit | Solo (geschätzt) |
|-------|----------|-----------|------------------|
| **Setup** | Dependencies, Projekt-Struktur | 10 min | 30 min |
| **Core Models** | Datenklassen, Note/Track/Song | 15 min | 60 min |
| **Validator** | CSV-Validierung mit pandas | 10 min | 45 min |
| **Parser** | CSV → Internal Model | 15 min | 60 min |
| **Converter** | Internal Model → MIDI | 20 min | 90 min |
| **CLI** | Click Commands (convert, batch, validate) | 15 min | 60 min |
| **GUI** | PyQt5 Main Window (3 Tabs) | 30 min | 180 min |
| **Tests** | pytest Suite (Parser, Converter, Validator) | 15 min | 90 min |
| **Examples** | 3 Beispiel-CSV-Dateien | 5 min | 15 min |
| **Dokumentation** | README, Docstrings | 10 min | 45 min |
| **GESAMT** | **Full-Featured Applikation** | **~145 min** | **~675 min** |

**Produktivitätsfaktor: ~4.7x** 🚀
*Zeitersparnis durch KI-Unterstützung: ~8.8 Stunden*

---

## 🔮 Roadmap / Feature Planung

### Version 1.1 (Geplant)

- [ ] **MIDI → CSV Import**: Reverse-Engineering für Analyse
- [ ] **Groove-Templates**: Swing, Shuffle als Parameter
- [ ] **Velocity Curves**: Humanizing durch Variationen
- [ ] **Chord Notation**: `Cmaj7` statt einzelner Noten
- [ ] **Live Preview**: Abspielen vor Export (mit pygame MIDI)

### Version 1.2 (Geplant)

- [ ] **Drag & Drop**: Dateien in GUI ziehen
- [ ] **Undo/Redo**: Im CSV Editor
- [ ] **Templates**: Vorgefertigte Song-Strukturen
- [ ] **Export Optionen**: Verschiedene MIDI-Formate

### Version 2.0 (Vision)

- [ ] **Web-Version**: Browser-basierte GUI
- [ ] **Cloud-Sync**: Projekte online speichern
- [ ] **Collaboration**: Mehrere User gleichzeitig
- [ ] **AI Integration**: Direkte KI-Kompositions-Unterstützung

---

## 🤝 Community

### Beitragen

Pull Requests sind willkommen! Für größere Änderungen bitte zuerst ein Issue öffnen.

```bash
# Fork das Projekt
git clone https://github.com/MarkusNika/CSV2MIDI.git
cd CSV2MIDI

# Neuen Branch erstellen
git checkout -b feature/mein-feature

# Änderungen committen
git commit -am 'Add: Mein neues Feature'

# Push
git push origin feature/mein-feature

# Pull Request erstellen
```

### Beispiel-Bibliothek

Teile deine CSV-Patterns! Erstelle einen Pull Request mit deinen Beispielen in `examples/community/`.

### Coding Standards

- **PEP 8** für Python Code
- **Docstrings** für alle öffentlichen Funktionen
- **Type Hints** wo möglich
- **Tests** für neue Features

---

## 📚 Technische Details

### MIDI-Spezifikation

- **MIDI File Type**: 1 (Multi-Track)
- **Ticks per Beat**: 480 (Standard)
- **Tempo**: Meta Message in Track 0
- **Time Signature**: Meta Message in Track 0
- **Note On/Off**: Delta-Time basiert

### Dependencies

- **mido**: MIDI File I/O
- **pandas**: CSV Parsing und Validation
- **click**: CLI Framework
- **PyQt5**: GUI Framework
- **pytest**: Testing Framework

---

## 🐛 Bekannte Probleme

### Windows

- `python-rtmidi` benötigt C++ Compiler (optional, nur für Live-Playback)
  - **Lösung**: Vorerst nicht benötigt, später pygame als Alternative

### Linux

- PyQt5 benötigt möglicherweise System-Pakete:

  ```bash
  sudo apt-get install python3-pyqt5
  ```

### macOS

- Keine bekannten Probleme

---

## 📄 Lizenz

MIT License

Copyright (c) 2024 Markus Nika

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👨‍💻 Autor

**Markus Nika**

- GitHub: [@MarkusNika](https://github.com/MarkusNika)
- Projekt: [CSV2MIDI](https://github.com/MarkusNika/CSV2MIDI)

Entwickelt mit Unterstützung von KI für effiziente Softwareentwicklung.

---

## 🙏 Danksagungen

- **mido** Library für exzellente MIDI-Unterstützung
- **PyQt5** für das robuste GUI-Framework
- **pandas** für flexible CSV-Verarbeitung
- **click** für elegante CLI-Entwicklung
- **Claude AI** für Entwicklungs-Unterstützung

---

## 📞 Support

Bei Fragen oder Problemen:

1. Schaue in die [Issues](https://github.com/MarkusNika/CSV2MIDI/issues)
2. Erstelle ein neues Issue
3. Kontaktiere mich via GitHub

---
**Happy MIDI Composing! 🎵**

