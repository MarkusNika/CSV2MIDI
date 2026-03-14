# 📝 CONTRIBUTING.md (Vollständig)

```markdown
# Contributing to CSV2MIDI

👍 Vielen Dank für dein Interesse, zu CSV2MIDI beizutragen!

Wir freuen uns über Contributions jeder Art: Bug-Reports, Feature-Requests, Dokumentation oder Code-Beiträge.

---

## 📋 Inhaltsverzeichnis

- [Code of Conduct](#code-of-conduct)
- [Wie kann ich beitragen?](#wie-kann-ich-beitragen)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Prozess](#pull-request-prozess)
- [Testing](#testing)
- [Commit Messages](#commit-messages)

---

## 🤝 Code of Conduct

### Unsere Verpflichtung

Wir verpflichten uns, die Teilnahme an unserem Projekt und unserer Community zu einer belästigungsfreien Erfahrung für alle zu machen.

### Unsere Standards

**Positives Verhalten:**
- Respektvolle und inklusive Sprache
- Konstruktives Feedback geben und annehmen
- Fokus auf das Beste für die Community
- Empathie gegenüber anderen Community-Mitgliedern

**Inakzeptables Verhalten:**
- Beleidigende oder diskriminierende Kommentare
- Persönliche Angriffe
- Trolling oder absichtlich störendes Verhalten
- Veröffentlichung privater Informationen ohne Erlaubnis

---

## 💡 Wie kann ich beitragen?

### 🐛 Bug Reports

Gefunden einen Bug? Erstelle ein [GitHub Issue](https://github.com/MarkusNika/CSV2MIDI/issues/new) mit:

**Template:**
```
**Beschreibung:**
[Klare Beschreibung des Problems]

**Schritte zur Reproduktion:**
1. [Erster Schritt]
2. [Zweiter Schritt]
3. [...]

**Erwartetes Verhalten:**
[Was sollte passieren?]

**Aktuelles Verhalten:**
[Was passiert stattdessen?]

**System-Info:**
- OS: [z.B. Windows 11, Ubuntu 22.04, macOS 13]
- Python Version: [z.B. 3.10.5]
- CSV2MIDI Version: [z.B. 1.0.0]

**Zusätzliche Informationen:**
- Beispiel-CSV (falls relevant)
- Error-Logs
- Screenshots
```

---

### 🚀 Feature Requests

Idee für ein neues Feature? Erstelle ein Issue mit:

**Template:**
```
**Feature-Beschreibung:**
[Was soll das Feature tun?]

**Use Case:**
[Wann würde das Feature verwendet werden?]

**Vorgeschlagene Implementierung:**
[Optional: Wie könnte es umgesetzt werden?]

**Alternativen:**
[Gibt es andere Lösungen für das Problem?]
```

---

### 📖 Dokumentation

Verbesserungen an README, Docstrings oder Tutorials sind immer willkommen!

---

### 🎵 Beispiel-Bibliothek

Teile deine CSV-Patterns:
1. Erstelle CSV-Datei in `examples/community/`
2. Benenne sie aussagekräftig: `<genre>_<instrument>_<style>.csv`
   - Beispiel: `jazz_piano_comping.csv`
3. Füge Beschreibung zu `examples/community/README.md` hinzu

---

## 🛠️ Development Setup

### Voraussetzungen

- Python 3.8 oder höher
- Git
- Virtualenv (empfohlen)

### Setup-Schritte

```bash
# 1. Repository forken (via GitHub UI)

# 2. Clone dein Fork
git clone https://github.com/DEIN-USERNAME/CSV2MIDI.git
cd CSV2MIDI

# 3. Upstream Remote hinzufügen
git remote add upstream https://github.com/MarkusNika/CSV2MIDI.git

# 4. Virtual Environment erstellen
python -m venv .venv

# 5. Aktivieren
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 6. Dependencies installieren
pip install -r requirements.txt

# 7. Development-Dependencies (optional)
pip install pytest pytest-cov black pylint

# 8. Verifizierung
pytest -v
```

---

## 📐 Coding Standards

### Python Style Guide

Wir folgen **PEP 8** mit kleinen Anpassungen:

```python
# ✅ Gut
def convert_csv_to_midi(input_file: str, output_file: str, tempo: int = 120) -> None:
    """
    Konvertiert CSV-Datei zu MIDI.

    Args:
        input_file: Pfad zur CSV-Datei
        output_file: Pfad für MIDI-Output
        tempo: BPM (default: 120)

    Raises:
        ValidationError: Bei ungültigen CSV-Daten
    """
    pass

# ❌ Schlecht
def conv(i,o,t=120):
    pass
```

### Docstrings

Alle **öffentlichen** Funktionen, Klassen und Module benötigen Docstrings:

```python
class MIDIConverter:
    """
    Konvertiert Song-Objekte zu MIDI-Dateien.

    Attributes:
        ticks_per_beat: MIDI-Ticks pro Beat (default: 480)

    Example:
        >>> converter = MIDIConverter()
        >>> midi = converter.song_to_midi(song)
        >>> midi.save('output.mid')
    """
    pass
```

### Type Hints

Nutze Type Hints wo sinnvoll:

```python
from typing import List, Optional, Tuple

def parse_notes(data: pd.DataFrame) -> List[Note]:
    """Parse DataFrame zu Note-Objekten."""
    pass

def get_tempo(song: Song) -> Optional[int]:
    """Gibt Tempo zurück oder None."""
    pass
```

### Code-Formatierung

**Line Length:** Max. 100 Zeichen (nicht 79)

**Imports:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import pandas as pd
from PyQt5.QtWidgets import QMainWindow

# Local
from ..core.parser import CSVParser
from ..core.models import Song, Note
```

### Linting

Vor dem Commit:

```bash
# Automatische Formatierung
black csv2midi/

# Lint-Check
pylint csv2midi/
```

---

## 🔄 Pull Request Prozess

### 1. Branch erstellen

```bash
# Synce mit upstream
git fetch upstream
git checkout develop
git merge upstream/develop

# Neuen Feature-Branch
git checkout -b feature/amazing-feature

# ODER Bug-Fix:
git checkout -b fix/bug-description
```

### Branch-Naming Convention:

- `feature/` - Neue Features
- `fix/` - Bug-Fixes
- `docs/` - Dokumentation
- `refactor/` - Code-Refactoring
- `test/` - Tests hinzufügen/verbessern

### 2. Änderungen implementieren

```bash
# Code schreiben
# Tests schreiben
# Dokumentation aktualisieren

# Alle Tests ausführen
pytest -v

# Code formatieren
black csv2midi/

# Commit
git add .
git commit -m "feat: Add amazing feature"
```

### 3. Pull Request erstellen

```bash
# Push zu deinem Fork
git push origin feature/amazing-feature

# Auf GitHub: Create Pull Request
```

**PR-Template:**
```markdown
## Beschreibung
[Was macht dieser PR?]

## Art der Änderung
- [ ] Bug-Fix
- [ ] Neues Feature
- [ ] Breaking Change
- [ ] Dokumentation

## Checklist
- [ ] Code folgt Projekt-Style
- [ ] Self-Review durchgeführt
- [ ] Kommentare hinzugefügt (wo nötig)
- [ ] Dokumentation aktualisiert
- [ ] Keine neuen Warnings
- [ ] Tests hinzugefügt
- [ ] Alle Tests bestehen
- [ ] CHANGELOG.md aktualisiert

## Testing
[Wie wurde getestet?]

## Screenshots (optional)
[Bei UI-Änderungen]
```

### 4. Code Review

- Mindestens ein Maintainer muss approven
- Alle Tests müssen grün sein
- Keine merge conflicts

### 5. Merge

Nach Approval wird dein PR gemerged! 🎉

---

## 🧪 Testing

### Tests ausführen

```bash
# Alle Tests
pytest

# Mit Verbose-Output
pytest -v

# Einzelne Test-Datei
pytest tests/test_parser.py

# Einzelner Test
pytest tests/test_parser.py::test_parse_simple_csv

# Mit Coverage
pytest --cov=csv2midi --cov-report=html
```

### Tests schreiben

**Beispiel:**

```python
# tests/test_new_feature.py
import pytest
from csv2midi.core.new_feature import amazing_function

def test_amazing_function():
    """Test amazing function."""
    result = amazing_function(input_data)
    assert result == expected_output

def test_amazing_function_with_invalid_input():
    """Test error handling."""
    with pytest.raises(ValueError):
        amazing_function(invalid_data)
```

### Test-Coverage

Ziel: **>80% Coverage**

```bash
pytest --cov=csv2midi --cov-report=term-missing
```

---

## 📝 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:

- `feat:` - Neues Feature
- `fix:` - Bug-Fix
- `docs:` - Dokumentation
- `style:` - Formatierung
- `refactor:` - Code-Refactoring
- `test:` - Tests
- `chore:` - Build/Config

### Beispiele:

```bash
# Gute Commit Messages:
git commit -m "feat(parser): Add support for triplet notation"
git commit -m "fix(gui): Resolve crash when loading empty CSV"
git commit -m "docs(readme): Update installation instructions"

# Schlechte Commit Messages:
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdf"
```

### Multi-Line Commits:

```bash
git commit -m "feat(converter): Add swing quantization

- Implement swing percentage parameter
- Add tests for different swing values
- Update documentation

Closes #42"
```

---

## 🎯 Entwicklungs-Workflow (Best Practices)

### 1. Kleiner Scope

- **Ein PR = Ein Feature/Fix**
- Einfacher zu reviewen
- Schnelleres Feedback

### 2. Tests zuerst (TDD)

```python
# 1. Test schreiben (fails)
def test_new_feature():
    assert new_feature() == expected

# 2. Feature implementieren (pass)
def new_feature():
    return expected
```

### 3. Regelmäßig committen

```bash
# Besser: Viele kleine Commits
git commit -m "feat: Add parser"
git commit -m "test: Add parser tests"
git commit -m "docs: Update parser docs"

# Schlechter: Ein riesiger Commit
git commit -m "Add complete feature with tests and docs"
```

### 4. Sync mit Upstream

```bash
# Täglich (bei aktiver Entwicklung)
git fetch upstream
git rebase upstream/develop
```

---

## 🏆 Recognition

Contributors werden in der README erwähnt:

```markdown
## Contributors

- [@username](https://github.com/username) - Feature XYZ
```

---

## 📞 Fragen?

- **GitHub Issues**: Für technische Fragen
- **Discussions**: Für generelle Diskussionen
- **Email**: [Deine Email] für private Fragen

---

## 📚 Ressourcen

- [Python PEP 8](https://pep8.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Danke für deinen Beitrag zu CSV2MIDI! 🎵**
```

---

## 🎯 Zusätzlich erstellen: CHANGELOG.md

**CHANGELOG.md:**

```markdown
# Changelog

All notable changes to CSV2MIDI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- MIDI to CSV import (reverse engineering)
- Groove templates (swing, shuffle)
- Chord notation shortcuts
- Live MIDI preview

## [1.0.0] - 2024-XX-XX

### Added
- ✅ Core CSV to MIDI conversion engine
- ✅ Multi-track support
- ✅ PyQt5 GUI with 3 tabs
  - Single file converter
  - Batch processor
  - CSV editor
- ✅ CLI tool with click framework
- ✅ Batch processing capabilities
- ✅ CSV validation with detailed error messages
- ✅ 12 comprehensive unit tests
- ✅ 3 example CSV files
- ✅ Complete documentation (README, CONTRIBUTING)
- ✅ Pylint configuration for PyQt5

### Technical
- Python 3.8+ support
- Dependencies: mido, pandas, click, PyQt5, pytest
- Cross-platform compatibility (Windows, Linux, macOS)
- MIDI Type 1 (multi-track) export
- 480 ticks per beat
- Custom tempo and time signature support

### Development
- Team development: Human + AI
- Development time: ~55 minutes
- Productivity factor: ~9x

---

[Unreleased]: https://github.com/MarkusNika/CSV2MIDI/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MarkusNika/CSV2MIDI/releases/tag/v1.0.0
```

---

## ✅ Finale Checkliste vor Commit:

- [ ] **CONTRIBUTING.md** erstellt
- [ ] **CHANGELOG.md** erstellt
- [ ] **README.md** aktualisiert (Development Log mit echten Zeiten)
- [ ] **.pylintrc** vorhanden
- [ ] **.gitignore** aktuell
- [ ] Alle Tests laufen durch
- [ ] GUI funktioniert
- [ ] CLI funktioniert

---
