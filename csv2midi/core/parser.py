"""
CSV Parser
"""
import pandas as pd
from typing import List
from .models import Note, Track, Song
from .validator import CSVValidator, ValidationError


class CSVParser:
    """Parst CSV zu internem Datenmodell"""

    @staticmethod
    def parse_csv_file(filepath: str, tempo: int = 120,
                       time_signature: tuple = (4, 4)) -> Song:
        """
        Liest CSV-Datei und erstellt Song-Objekt

        Args:
            filepath: Pfad zur CSV-Datei
            tempo: BPM
            time_signature: Taktart als Tuple (Zähler, Nenner)

        Returns:
            Song-Objekt

        Raises:
            ValidationError: Bei ungültigen Daten
        """
        # CSV einlesen
        df = pd.read_csv(filepath)

        # Validieren
        is_valid, errors = CSVValidator.validate_dataframe(df)
        if not is_valid:
            raise ValidationError("\n".join(errors))

        # Song erstellen
        song = Song(
            title=filepath.split('/')[-1].replace('.csv', ''),
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
    def parse_csv_string(csv_string: str, **kwargs) -> Song:
        """Parst CSV aus String (z.B. Clipboard)"""
        import io
        df = pd.read_csv(io.StringIO(csv_string))

        # Validieren
        is_valid, errors = CSVValidator.validate_dataframe(df)
        if not is_valid:
            raise ValidationError("\n".join(errors))

        # Ähnlich wie parse_csv_file, aber ohne File-I/O
        # ... (Rest analog zu parse_csv_file)
        pass