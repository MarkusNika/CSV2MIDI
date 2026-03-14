# 📝 README.md - Finale Version (Komplett)

```markdown
# CSV2MIDI Converter

🎵 Einfacher und flexibler CSV to MIDI Converter für Musiker, Komponisten und Entwickler.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-12%20passed-success)](https://github.com/MarkusNika/CSV2MIDI)

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

## 📋 Voraussetzungen

- **Python**: 3.8 oder höher
- **Betriebssystem**: Windows, Linux, macOS
- **RAM**: Minimum 256 MB
- **Festplatte**: ~50 MB für Installation

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

```
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
├── CONTRIBUTING.md      # Contribution Guidelines
├── CHANGELOG.md         # Version History
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
| **Setup** | venv, Dependencies, Projekt-Struktur | 10 min | 30 min |
| **Core** | Models, Parser, Validator, Converter | 15 min | 120 min |
| **CLI** | Click Commands (convert, batch, validate) | 5 min | 60 min |
| **GUI** | PyQt5 Main Window (3 Tabs, Bug-Fix) | 20 min | 180 min |
| **Tests** | pytest Suite (12 Tests) | 2 min | 90 min |
| **DAW Test** | Reaper Import Verifizierung | 3 min | 15 min |
| **Dokumentation** | README, CONTRIBUTING, CHANGELOG | 5 min | 30 min |
| **GESAMT** | **Production-Ready Application** | **~60 min** | **~525 min (8.75h)** |

**Produktivitätsfaktor: ~8.75x** 🚀

*Zeitersparnis durch KI-Unterstützung: ~7.75 Stunden*

---

## 🔮 Roadmap

Siehe [CHANGELOG.md](CHANGELOG.md) für Version-History.

### Version 1.1 (Geplant)
- [ ] MIDI → CSV Import (Reverse Engineering)
- [ ] Groove-Templates (Swing, Shuffle)
- [ ] Velocity Curves (Humanizing)
- [ ] Chord Notation (`Cmaj7` Shortcuts)
- [ ] Live Preview mit pygame

### Version 1.2 (Geplant)
- [ ] Drag & Drop Support
- [ ] Undo/Redo im CSV Editor
- [ ] Song-Templates
- [ ] Export-Optionen

### Version 2.0 (Vision)
- [ ] Web-Version
- [ ] Cloud-Sync
- [ ] Collaboration Features
- [ ] Direct AI Integration

---

## 🤝 Community & Contribution

Wir freuen uns über jeden Beitrag! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Bug Reports

Nutze [GitHub Issues](https://github.com/MarkusNika/CSV2MIDI/issues) für Bug-Reports und Feature-Requests.

### Beispiel-Bibliothek

Teile deine CSV-Patterns in `examples/community/`!

---

## 📚 Technische Details

### MIDI-Spezifikation

- **MIDI Type**: 1 (Multi-Track)
- **Ticks per Beat**: 480
- **Tempo**: Meta Message in Track 0
- **Time Signature**: Meta Message in Track 0
- **Note On/Off**: Delta-Time basiert

### Dependencies

- **mido**: MIDI File I/O
- **pandas**: CSV Parsing
- **click**: CLI Framework
- **PyQt5**: GUI Framework
- **pytest**: Testing

---

## 🐛 Bekannte Probleme

### Pylint (PyQt5)
- `.pylintrc` bereits konfiguriert für saubere Entwicklung

### Windows
- `python-rtmidi` optional (nur für Live-Playback in v1.1)

### Linux
```bash
sudo apt-get install python3-pyqt5
```

### macOS
- Keine bekannten Probleme

---

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

Copyright (c) 2024 Markus Nika

---

## 👨‍💻 Autor

**Markus Nika**
- GitHub: [@MarkusNika](https://github.com/MarkusNika)
- Projekt: [CSV2MIDI](https://github.com/MarkusNika/CSV2MIDI)

Entwickelt mit KI-Unterstützung (Claude) für maximale Produktivität.

---

## 🙏 Danksagungen

- **mido** - Exzellente MIDI-Bibliothek
- **PyQt5** - Robustes GUI-Framework
- **pandas** - Flexible Datenverarbeitung
- **click** - Elegante CLI-Entwicklung
- **Claude AI** - Entwicklungs-Partner

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/MarkusNika/CSV2MIDI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MarkusNika/CSV2MIDI/discussions)
- **Dokumentation**: Diese README

---

**Happy MIDI Composing! 🎵**
