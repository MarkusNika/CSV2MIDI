"""
Tests für CSV Parser
"""
import pytest
from csv2midi.core.parser import CSVParser
from csv2midi.core.validator import ValidationError


def test_parse_simple_csv(tmp_path):
    """Test einfache CSV-Datei parsen"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,100,1,1.0,1.0
Piano,1,E,4,100,1,2.0,1.0
Piano,1,G,4,100,1,3.0,1.0"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    song = CSVParser.parse_csv_file(str(csv_file))

    # assert song.title == "test"
    assert len(song.tracks) == 1
    assert song.tracks[0].name == "Piano"
    assert len(song.tracks[0].notes) == 3


def test_parse_multi_track_csv(tmp_path):
    """Test Multi-Track CSV"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,C,4,100,1,1.0,1.0
Bass,2,C,2,110,1,1.0,2.0
Piano,1,E,4,100,1,2.0,1.0"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    song = CSVParser.parse_csv_file(str(csv_file))

    assert len(song.tracks) == 2
    track_names = [t.name for t in song.tracks]
    assert "Piano" in track_names
    assert "Bass" in track_names


def test_invalid_csv_missing_columns(tmp_path):
    """Test fehlende Spalten"""
    csv_content = """track_name,midi_channel,note
Piano,1,C"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    with pytest.raises(ValidationError):
        CSVParser.parse_csv_file(str(csv_file))


def test_invalid_note_value(tmp_path):
    """Test ungültige Note"""
    csv_content = """track_name,midi_channel,note,octave,velocity,bar,beat,duration
Piano,1,X,4,100,1,1.0,1.0"""

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    with pytest.raises(ValidationError):
        CSVParser.parse_csv_file(str(csv_file))
