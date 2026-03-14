"""
CLI Commands mit Click
"""
import click
from pathlib import Path
from ..core.parser import CSVParser
from ..core.converter import MIDIConverter
from ..core.validator import ValidationError


@click.group()
@click.version_option(version='1.0.0', prog_name='CSV2MIDI')
def cli():
    """CSV2MIDI - Konvertiert CSV-Notendaten zu MIDI-Dateien"""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(), required=False)
@click.option('--tempo', '-t', default=120, help='Tempo in BPM (default: 120)')
@click.option('--time-sig', '-ts', default='4/4', help='Taktart (default: 4/4)')
def convert(input_file, output_file, tempo, time_sig):
    """
    Konvertiert einzelne CSV-Datei zu MIDI

    Beispiel:
        csv2midi convert input.csv output.mid
        csv2midi convert input.csv --tempo 140 --time-sig 3/4
    """
    try:
        # Output-Datei generieren falls nicht angegeben
        if not output_file:
            output_file = Path(input_file).with_suffix('.mid')

        # Taktart parsen
        num, den = map(int, time_sig.split('/'))
        time_signature = (num, den)

        click.echo(f"📄 Lese CSV: {input_file}")

        # Parsen
        song = CSVParser.parse_csv_file(input_file, tempo=tempo, time_signature=time_signature)

        click.echo(f"✅ {len(song.tracks)} Track(s) gefunden:")
        for track in song.tracks:
            click.echo(f"   • {track.name}: {len(track.notes)} Noten")

        # Konvertieren
        click.echo(f"🎵 Konvertiere zu MIDI...")
        MIDIConverter.convert_and_save(song, str(output_file))

        click.echo(f"✅ MIDI gespeichert: {output_file}")

    except ValidationError as e:
        click.echo(f"❌ Validierungsfehler:\n{e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Fehler: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_dir', type=click.Path(), required=False)
@click.option('--tempo', '-t', default=120, help='Tempo in BPM (default: 120)')
@click.option('--time-sig', '-ts', default='4/4', help='Taktart (default: 4/4)')
@click.option('--recursive', '-r', is_flag=True, help='Rekursiv in Unterordner')
def batch(input_dir, output_dir, tempo, time_sig, recursive):
    """
    Batch-Konvertierung aller CSV-Dateien in einem Ordner

    Beispiel:
        csv2midi batch ./csv_files ./midi_files
        csv2midi batch ./csv_files --recursive
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir else input_path
    output_path.mkdir(parents=True, exist_ok=True)

    # Taktart parsen
    num, den = map(int, time_sig.split('/'))
    time_signature = (num, den)

    # CSV-Dateien finden
    pattern = '**/*.csv' if recursive else '*.csv'
    csv_files = list(input_path.glob(pattern))

    if not csv_files:
        click.echo(f"❌ Keine CSV-Dateien in {input_dir} gefunden")
        return

    click.echo(f"📁 {len(csv_files)} CSV-Datei(en) gefunden\n")

    success_count = 0
    error_count = 0

    for csv_file in csv_files:
        try:
            # Relative Struktur beibehalten
            rel_path = csv_file.relative_to(input_path)
            output_file = output_path / rel_path.with_suffix('.mid')
            output_file.parent.mkdir(parents=True, exist_ok=True)

            click.echo(f"🔄 {csv_file.name} → {output_file.name}")

            # Parsen und konvertieren
            song = CSVParser.parse_csv_file(str(csv_file), tempo=tempo, time_signature=time_signature)
            MIDIConverter.convert_and_save(song, str(output_file))

            click.echo(f"   ✅ {len(song.tracks)} Track(s), {sum(len(t.notes) for t in song.tracks)} Noten\n")
            success_count += 1

        except Exception as e:
            click.echo(f"   ❌ Fehler: {e}\n", err=True)
            error_count += 1

    click.echo(f"\n📊 Fertig: {success_count} erfolgreich, {error_count} Fehler")


@cli.command()
@click.argument('csv_file', type=click.Path(exists=True))
def validate(csv_file):
    """
    Validiert CSV-Datei ohne Konvertierung

    Beispiel:
        csv2midi validate input.csv
    """
    import pandas as pd
    from ..core.validator import CSVValidator

    try:
        click.echo(f"🔍 Validiere: {csv_file}")

        df = pd.read_csv(csv_file)
        is_valid, errors = CSVValidator.validate_dataframe(df)

        if is_valid:
            click.echo(f"✅ CSV ist valide!")
            click.echo(f"   • {len(df)} Zeilen")
            click.echo(f"   • Tracks: {df['track_name'].unique().tolist()}")
        else:
            click.echo(f"❌ Validierungsfehler gefunden:\n")
            for error in errors:
                click.echo(f"   • {error}")
            raise click.Abort()

    except Exception as e:
        click.echo(f"❌ Fehler: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()