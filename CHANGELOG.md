# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-03-15

### Added in [1.0.1]

- ✅ **Comment Support**: CSV-Dateien können jetzt Kommentarzeilen enthalten (beginnend mit `#`)
  - Kommentare werden beim Parsen automatisch ignoriert
  - Verbessert Lesbarkeit von großen CSV-Dateien
  - Nützlich für Strukturierung und Dokumentation in CSV-Notationen

### Fixed [1.0.1]

- Parser ignoriert jetzt Zeilen, die mit `#` beginnen
- Auch Kommentare mit führenden Leerzeichen (`# comment`) werden erkannt

### Technical [1.0.1]

- Neue Methode `CSVParser._remove_comments()` für Kommentar-Filterung
- Erweiterte Tests in `tests/test_comments.py`

---

## [1.0.0] - 2026-03-14

### Added

- ✅ CSV to MIDI conversion engine
- ✅ Multi-track support
- ✅ PyQt5 GUI with 3 tabs
- ✅ CLI tool with click
- ✅ Batch processing
- ✅ CSV validation
- ✅ CSV editor with direct MIDI export
- ✅ 12 unit tests
- ✅ Example CSV files (3)
- ✅ Complete documentation

### Technical

- Core: mido, pandas, click, PyQt5
- Python 3.8+ support
- Cross-platform (Windows, Linux, macOS)

---
