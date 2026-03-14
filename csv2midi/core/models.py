"""
Data Models für CSV2MIDI
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class NoteValue(Enum):
    """MIDI Note Values"""
    C = 0
    Cs = 1
    Db = 1
    D = 2
    Ds = 3
    Eb = 3
    E = 4
    F = 5
    Fs = 6
    Gb = 6
    G = 7
    Gs = 8
    Ab = 8
    A = 9
    As = 10
    Bb = 10
    B = 11


@dataclass
class Note:
    """Einzelne Note"""
    track_name: str
    midi_channel: int
    note: str  # z.B. "C", "D#", "Eb"
    octave: int
    velocity: int
    bar: int  # Takt
    beat: float  # Zählzeit (1.0, 1.5, 2.0, etc.)
    duration: float  # in Beats

    def to_midi_note(self) -> int:
        """Konvertiert Note + Octave zu MIDI Note Number (0-127)"""
        note_val = NoteValue[self.note.replace('#', 's')].value
        return (self.octave + 1) * 12 + note_val

    def get_tick_start(self, ticks_per_beat: int, time_signature: tuple = (4, 4)) -> int:
        """Berechnet Start-Tick basierend auf Takt und Beat"""
        beats_per_bar = time_signature[0]
        total_beats = (self.bar - 1) * beats_per_bar + (self.beat - 1)
        return int(total_beats * ticks_per_beat)

    def get_tick_duration(self, ticks_per_beat: int) -> int:
        """Berechnet Dauer in Ticks"""
        return int(self.duration * ticks_per_beat)


@dataclass
class Track:
    """MIDI Track mit allen Noten"""
    name: str
    midi_channel: int
    notes: List[Note]
    program: int = 0  # MIDI Program Change (Instrument)


@dataclass
class Song:
    """Kompletter Song mit allen Tracks"""
    title: str
    tempo: int = 120  # BPM
    time_signature: tuple = (4, 4)
    ticks_per_beat: int = 480
    tracks: List[Track] = None

    def __post_init__(self):
        if self.tracks is None:
            self.tracks = []