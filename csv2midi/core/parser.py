"""
CSV Parser
"""
import pandas as pd
import io
from typing import List
from .models import Note, Track, Song
from .validator import CSVValidator, ValidationError


class CSVParser:
    """Parst CSV zu internem Datenmodell"""

    @staticmethod
    def _remove_comments(filepath: str) -> str:
        """
        Entfernt Kommentarzeilen (beginnend mit #) aus CSV-Datei.

        Args:
            filepath: Pfad zur CSV-Datei

        Returns:
            CSV-Content ohne Kommentarzeilen als String
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Filtere Zeilen, die mit # beginnen (nach Whitespace-Entfernung)
        filtered_lines = [line for line in lines if not line.strip().startswith('#')]

        return ''.join(filtered_lines)

    @staticmethod
    def parse_csv_file(filepath: str, tempo: int = 120,
                       time_signature: tuple = (4, 4)) -> Song:
        """
        Liest CSV-Datei und erstellt Song-Objekt.

        Kommentarzeilen (beginnend mit #) werden automatisch ignoriert.

        Args:
            filepath: Pfad zur CSV-Datei
            tempo: BPM (default: 120)
            time_signature: Taktart als Tuple (Zähler, Nenner)

        Returns:
            Song-Objekt

        Raises:
            ValidationError: Bei ungültigen CSV-Daten
        """
        # CSV einlesen ohne Kommentare
        csv_content = CSVParser._remove_comments(filepath)
        df = pd.read_csv(io.StringIO(csv_content))

        # Validieren
        is_valid, errors = CSVValidator.validate_dataframe(df)
        if not is_valid:
            raise ValidationError("\n".join(errors))

        # Song erstellen
        import os
        filename = os.path.basename(filepath).replace('.csv', '')
        song = Song(
            title=filename,
            tempo=tempo,
            time_signature=time_signature
        )

        # Notes erstellen
        notes = []
        for _, row in df.iterrows():
            note = Note(
                track_name=row['track_name'],
                midi_channel=int(row['midi_channel']),
                note=row['note'],
                octave=int(row['octave']),
                velocity=int(row['velocity']),
                bar=int(row['bar']),
                beat=float(row['beat']),
                duration=float(row['duration'])
            )
            notes.append(note)

        # Tracks gruppieren
        track_dict = {}
        for note in notes:
            if note.track_name not in track_dict:
                track_dict[note.track_name] = Track(
                    name=note.track_name,
                    midi_channel=note.midi_channel,
                    notes=[]
                )
            track_dict[note.track_name].notes.append(note)

        song.tracks = list(track_dict.values())

        return song

    @staticmethod
    def parse_csv_string(csv_string: str, tempo: int = 120,
                        time_signature: tuple = (4, 4)) -> Song:
        """
        Parst CSV aus String (z.B. Clipboard).

        Kommentarzeilen (beginnend mit #) werden automatisch ignoriert.
        """
        # Kommentare entfernen
        lines = csv_string.split('\n')
        filtered_lines = [line for line in lines if not line.strip().startswith('#')]
        clean_csv = '\n'.join(filtered_lines)

        df = pd.read_csv(io.StringIO(clean_csv))

        # Validieren
        is_valid, errors = CSVValidator.validate_dataframe(df)
        if not is_valid:
            raise ValidationError("\n".join(errors))

        # Song erstellen (gleiche Logik wie parse_csv_file)
        song = Song(
            title="from_string",
            tempo=tempo,
            time_signature=time_signature
        )

        notes = []
        for _, row in df.iterrows():
            note = Note(
                track_name=row['track_name'],
                midi_channel=int(row['midi_channel']),
                note=row['note'],
                octave=int(row['octave']),
                velocity=int(row['velocity']),
                bar=int(row['bar']),
                beat=float(row['beat']),
                duration=float(row['duration'])
            )
            notes.append(note)

        track_dict = {}
        for note in notes:
            if note.track_name not in track_dict:
                track_dict[note.track_name] = Track(
                    name=note.track_name,
                    midi_channel=note.midi_channel,
                    notes=[]
                )
            track_dict[note.track_name].notes.append(note)

        song.tracks = list(track_dict.values())

        return song
