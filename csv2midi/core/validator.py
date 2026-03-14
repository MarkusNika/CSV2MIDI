"""
CSV Validation
"""
import pandas as pd
from typing import List, Tuple


class ValidationError(Exception):
    """Custom Exception für Validierungsfehler"""
    pass


class CSVValidator:
    """Validiert CSV-Daten"""

    REQUIRED_COLUMNS = [
        'track_name',
        'midi_channel',
        'note',
        'octave',
        'velocity',
        'bar',
        'beat',
        'duration'
    ]

    VALID_NOTES = ['C', 'Cs', 'Db', 'D', 'Ds', 'Eb', 'E', 'F',
                   'Fs', 'Gb', 'G', 'Gs', 'Ab', 'A', 'As', 'Bb', 'B']

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validiert DataFrame

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # Pflichtfelder prüfen
        missing_cols = set(CSVValidator.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            errors.append(f"Fehlende Spalten: {', '.join(missing_cols)}")
            return False, errors

        # DATENTYPEN KONVERTIEREN (FIX!)
        try:
            df['midi_channel'] = pd.to_numeric(df['midi_channel'], errors='coerce')
            df['octave'] = pd.to_numeric(df['octave'], errors='coerce')
            df['velocity'] = pd.to_numeric(df['velocity'], errors='coerce')
            df['bar'] = pd.to_numeric(df['bar'], errors='coerce')
            df['beat'] = pd.to_numeric(df['beat'], errors='coerce')
            df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
        except Exception as e:
            errors.append(f"Fehler bei Datentyp-Konvertierung: {e}")
            return False, errors

        # Datentypen und Wertebereiche prüfen
        for idx, row in df.iterrows():
            row_num = idx + 2  # +2 wegen Header und 0-based index

            # MIDI Channel (1-16)
            if pd.isna(row['midi_channel']) or not 1 <= row['midi_channel'] <= 16:
                errors.append(f"Zeile {row_num}: MIDI Channel muss 1-16 sein (ist: {row['midi_channel']})")

            # Note
            if row['note'] not in CSVValidator.VALID_NOTES:
                errors.append(f"Zeile {row_num}: Ungültige Note '{row['note']}'")

            # Octave (0-10 für MIDI)
            if pd.isna(row['octave']) or not 0 <= row['octave'] <= 10:
                errors.append(f"Zeile {row_num}: Octave muss 0-10 sein (ist: {row['octave']})")

            # Velocity (0-127)
            if pd.isna(row['velocity']) or not 0 <= row['velocity'] <= 127:
                errors.append(f"Zeile {row_num}: Velocity muss 0-127 sein (ist: {row['velocity']})")

            # Bar (positive)
            if pd.isna(row['bar']) or row['bar'] < 1:
                errors.append(f"Zeile {row_num}: Bar muss >= 1 sein (ist: {row['bar']})")

            # Beat (positive)
            if pd.isna(row['beat']) or row['beat'] < 1:
                errors.append(f"Zeile {row_num}: Beat muss >= 1 sein (ist: {row['beat']})")

            # Duration (positive)
            if pd.isna(row['duration']) or row['duration'] <= 0:
                errors.append(f"Zeile {row_num}: Duration muss > 0 sein (ist: {row['duration']})")

        return len(errors) == 0, errors