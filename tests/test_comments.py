"""
Tests für Kommentar-Unterstützung
"""
import pytest
from csv2midi.core.parser import CSVParser
from csv2midi.core.validator import ValidationError


def test_parse_csv_with_comments(tmp_path):
    """Test CSV mit Kommentaren"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
# Intro - Leitmotiv
Piano,1,C,4,100,1,1.0,1.0
Piano,1,E,4,100,1,2.0,1.0
# Verse 1
Piano,1,G,4,100,2,1.0,1.0
"""

    csv_file = tmp_path / "test_comments.csv"
    csv_file.write_text(csv_content)

    song = CSVParser.parse_csv_file(str(csv_file))

    assert song.title == "test_comments"
    assert len(song.tracks) == 1
    assert song.tracks[0].name == "Piano"
    assert len(song.tracks[0].notes) == 3  # Nur 3 Noten, keine Kommentare


def test_parse_csv_with_only_hash_comments(tmp_path):
    """Test CSV wo alle Kommentare mit # beginnen"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
# Kompletter Kommentar
Piano,1,C,4,100,1,1.0,1.0
#Kommentar ohne Leerzeichen
Piano,1,D,4,100,1,2.0,1.0
  # Kommentar mit Leading Whitespace
Piano,1,E,4,100,1,3.0,1.0
"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    song = CSVParser.parse_csv_file(str(csv_file))
    assert len(song.tracks[0].notes) == 3


def test_parse_csv_without_comments_still_works(tmp_path):
    """Test dass CSV ohne Kommentare weiterhin funktioniert"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,100,1,1.0,1.0
Piano,1,E,4,100,1,2.0,1.0
"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    song = CSVParser.parse_csv_file(str(csv_file))
    assert len(song.tracks[0].notes) == 2
