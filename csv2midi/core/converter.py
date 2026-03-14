"""
MIDI Converter
"""
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
from .models import Song, Track, Note


class MIDIConverter:
    """Konvertiert Song zu MIDI-Datei"""

    @staticmethod
    def song_to_midi(song: Song) -> MidiFile:
        """
        Konvertiert Song-Objekt zu MIDI-Datei

        Args:
            song: Song-Objekt

        Returns:
            MidiFile-Objekt
        """
        # MIDI File erstellen (Type 1 = multi-track)
        midi = MidiFile(type=1, ticks_per_beat=song.ticks_per_beat)

        # Tempo Track (Track 0)
        tempo_track = MidiTrack()
        midi.tracks.append(tempo_track)

        # Tempo setzen
        tempo_track.append(MetaMessage('set_tempo',
                                       tempo=mido.bpm2tempo(song.tempo),
                                       time=0))

        # Time Signature setzen
        tempo_track.append(MetaMessage('time_signature',
                                       numerator=song.time_signature[0],
                                       denominator=song.time_signature[1],
                                       time=0))

        # Tracks konvertieren
        for track in song.tracks:
            midi_track = MIDIConverter._track_to_midi_track(track, song)
            midi.tracks.append(midi_track)

        return midi

    @staticmethod
    def _track_to_midi_track(track: Track, song: Song) -> MidiTrack:
        """Konvertiert einzelnen Track"""
        midi_track = MidiTrack()

        # Track Name
        midi_track.append(MetaMessage('track_name', name=track.name, time=0))

        # Program Change (Instrument)
        midi_track.append(Message('program_change',
                                  program=track.program,
                                  channel=track.midi_channel - 1,  # MIDI channels are 0-15
                                  time=0))

        # Notes sortieren nach Start-Zeit
        sorted_notes = sorted(track.notes,
                             key=lambda n: n.get_tick_start(song.ticks_per_beat,
                                                            song.time_signature))

        # Events erstellen (Note On/Off pairs)
        events = []
        for note in sorted_notes:
            start_tick = note.get_tick_start(song.ticks_per_beat, song.time_signature)
            duration_ticks = note.get_tick_duration(song.ticks_per_beat)

            events.append({
                'tick': start_tick,
                'type': 'note_on',
                'note': note.to_midi_note(),
                'velocity': note.velocity,
                'channel': note.midi_channel - 1
            })

            events.append({
                'tick': start_tick + duration_ticks,
                'type': 'note_off',
                'note': note.to_midi_note(),
                'velocity': 0,
                'channel': note.midi_channel - 1
            })

        # Events nach Tick sortieren
        events.sort(key=lambda e: (e['tick'], e['type'] == 'note_off'))

        # Delta-Times berechnen und Messages erstellen
        current_tick = 0
        for event in events:
            delta = event['tick'] - current_tick

            if event['type'] == 'note_on':
                midi_track.append(Message('note_on',
                                         note=event['note'],
                                         velocity=event['velocity'],
                                         channel=event['channel'],
                                         time=delta))
            else:
                midi_track.append(Message('note_off',
                                         note=event['note'],
                                         velocity=0,
                                         channel=event['channel'],
                                         time=delta))

            current_tick = event['tick']

        # End of Track
        midi_track.append(MetaMessage('end_of_track', time=0))

        return midi_track

    @staticmethod
    def save_midi(midi: MidiFile, filepath: str):
        """
        Speichert MIDI-Datei

        Args:
            midi: MidiFile-Objekt
            filepath: Ziel-Pfad
        """
        midi.save(filepath)

    @staticmethod
    def convert_and_save(song: Song, filepath: str):
        """
        Konvertiert Song und speichert direkt

        Args:
            song: Song-Objekt
            filepath: Ziel-Pfad
        """
        midi = MIDIConverter.song_to_midi(song)
        MIDIConverter.save_midi(midi, filepath)