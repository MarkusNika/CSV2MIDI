"""
Tests für MIDI Converter
"""
import pytest
from csv2midi.core.models import Song, Track, Note
from csv2midi.core.converter import MIDIConverter
import mido


def test_song_to_midi():
    """Test Song zu MIDI Konvertierung"""
    # Create test song
    note1 = Note(
        track_name="Piano",
        midi_channel=1,
        note="C",
        octave=4,
        velocity=100,
        bar=1,
        beat=1.0,
        duration=1.0
    )
    
    note2 = Note(
        track_name="Piano",
        midi_channel=1,
        note="E",
        octave=4,
        velocity=100,
        bar=1,
        beat=2.0,
        duration=1.0
    )
    
    track = Track(name="Piano", midi_channel=1, notes=[note1, note2])
    song = Song(title="Test", tempo=120, tracks=[track])
    
    # Convert
    midi = MIDIConverter.song_to_midi(song)
    
    # Verify
    assert isinstance(midi, mido.MidiFile)
    assert midi.type == 1  # Multi-track
    assert len(midi.tracks) == 2  # Tempo track + 1 instrument track


def test_note_to_midi_number():
    """Test Note zu MIDI Number Konvertierung"""
    note_c4 = Note("Piano", 1, "C", 4, 100, 1, 1.0, 1.0)
    assert note_c4.to_midi_note() == 60  # Middle C
    
    note_a4 = Note("Piano", 1, "A", 4, 100, 1, 1.0, 1.0)
    assert note_a4.to_midi_note() == 69  # A440
    
    note_c5 = Note("Piano", 1, "C", 5, 100, 1, 1.0, 1.0)
    assert note_c5.to_midi_note() == 72


def test_save_midi(tmp_path):
    """Test MIDI speichern"""
    note = Note("Piano", 1, "C", 4, 100, 1, 1.0, 1.0)
    track = Track(name="Piano", midi_channel=1, notes=[note])
    song = Song(title="Test", tempo=120, tracks=[track])
    
    output_file = tmp_path / "test.mid"
    MIDIConverter.convert_and_save(song, str(output_file))
    
    assert output_file.exists()
    
    # Verify MIDI file can be loaded
    midi = mido.MidiFile(str(output_file))
    assert len(midi.tracks) > 0