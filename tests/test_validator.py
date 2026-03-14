"""
Tests für CSV Validator
"""
import pandas as pd
from csv2midi.core.validator import CSVValidator


def test_valid_csv():
    """Test valide CSV"""
    df = pd.DataFrame({
        'track_name': ['Piano'],
        'midi_channel': [1],
        'note': ['C'],
        'octave': [4],
        'velocity': [100],
        'bar': [1],
        'beat': [1.0],
        'duration': [1.0]
    })

    is_valid, errors = CSVValidator.validate_dataframe(df)
    assert is_valid
    assert len(errors) == 0


def test_missing_columns():
    """Test fehlende Spalten"""
    df = pd.DataFrame({
        'track_name': ['Piano'],
        'note': ['C']
    })

    is_valid, errors = CSVValidator.validate_dataframe(df)
    assert not is_valid
    assert len(errors) > 0
    assert 'Fehlende Spalten' in errors[0]


def test_invalid_midi_channel():
    """Test ungültiger MIDI Kanal"""
    df = pd.DataFrame({
        'track_name': ['Piano'],
        'midi_channel': [17],  # Max ist 16
        'note': ['C'],
        'octave': [4],
        'velocity': [100],
        'bar': [1],
        'beat': [1.0],
        'duration': [1.0]
    })

    is_valid, errors = CSVValidator.validate_dataframe(df)
    assert not is_valid
    assert any('MIDI Channel' in e for e in errors)


def test_invalid_velocity():
    """Test ungültige Velocity"""
    df = pd.DataFrame({
        'track_name': ['Piano'],
        'midi_channel': [1],
        'note': ['C'],
        'octave': [4],
        'velocity': [200],  # Max ist 127
        'bar': [1],
        'beat': [1.0],
        'duration': [1.0]
    })

    is_valid, errors = CSVValidator.validate_dataframe(df)
    assert not is_valid
    assert any('Velocity' in e for e in errors)


def test_invalid_note():
    """Test ungültige Note"""
    df = pd.DataFrame({
        'track_name': ['Piano'],
        'midi_channel': [1],
        'note': ['X'],  # Ungültig
        'octave': [4],
        'velocity': [100],
        'bar': [1],
        'beat': [1.0],
        'duration': [1.0]
    })

    is_valid, errors = CSVValidator.validate_dataframe(df)
    assert not is_valid
    assert any('Ungültige Note' in e for e in errors)
