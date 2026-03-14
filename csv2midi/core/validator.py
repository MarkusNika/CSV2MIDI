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
        
        # Datentypen und Wertebereiche prüfen
        for idx, row in df.iterrows():
            row_num = idx + 2  # +2 wegen Header und 0-based index
            
            # MIDI Channel (1-16)
            if not 1 <= row['midi_channel'] <= 16:
                errors.append(f"Zeile {row_num}: MIDI Channel muss 1-16 sein")
            
            # Note
            if row['note'] not in CSVValidator.VALID_NOTES:
                errors.append(f"Zeile {row_num}: Ungültige Note '{row['note']}'")
            
            # Octave (0-10 für MIDI)
            if not 0 <= row['octave'] <= 10:
                errors.append(f"Zeile {row_num}: Octave muss 0-10 sein")
            
            # Velocity (0-127)
            if not 0 <= row['velocity'] <= 127:
                errors.append(f"Zeile {row_num}: Velocity muss 0-127 sein")
            
            # Bar (positive)
            if row['bar'] < 1:
                errors.append(f"Zeile {row_num}: Bar muss >= 1 sein")
            
            # Beat (positive)
            if row['beat'] < 1:
                errors.append(f"Zeile {row_num}: Beat muss >= 1 sein")
            
            # Duration (positive)
            if row['duration'] <= 0:
                errors.append(f"Zeile {row_num}: Duration muss > 0 sein")
        
        return len(errors) == 0, errors