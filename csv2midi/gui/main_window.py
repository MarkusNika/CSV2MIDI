"""
PyQt5 Main Window
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QFileDialog,
                             QSpinBox, QComboBox, QGroupBox, QMessageBox,
                             QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import pandas as pd
from pathlib import Path
import traceback

from ..core.parser import CSVParser
from ..core.converter import MIDIConverter
from ..core.validator import CSVValidator, ValidationError


class ConversionThread(QThread):
    """Thread für Konvertierung im Hintergrund"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, csv_files, output_dir, tempo, time_sig):
        super().__init__()
        self.csv_files = csv_files
        self.output_dir = output_dir
        self.tempo = tempo
        self.time_sig = time_sig
    
    def run(self):
        try:
            total = len(self.csv_files)
            success = 0
            
            for i, csv_file in enumerate(self.csv_files):
                self.progress.emit(int((i / total) * 100), f"Konvertiere {csv_file.name}...")
                
                try:
                    song = CSVParser.parse_csv_file(str(csv_file), 
                                                   tempo=self.tempo, 
                                                   time_signature=self.time_sig)
                    output_file = self.output_dir / csv_file.with_suffix('.mid').name
                    MIDIConverter.convert_and_save(song, str(output_file))
                    success += 1
                except Exception as e:
                    self.progress.emit(int((i / total) * 100), f"Fehler bei {csv_file.name}: {e}")
            
            self.progress.emit(100, "Fertig!")
            self.finished.emit(True, f"{success}/{total} Dateien erfolgreich konvertiert")
            
        except Exception as e:
            self.finished.emit(False, f"Fehler: {str(e)}")


class CSV2MIDIMainWindow(QMainWindow):
    """Haupt-GUI-Fenster"""
    
    def __init__(self):
        super().__init__()
        self.current_input_file = None
        self.current_output_file = None
        self.current_input_dir = None
        self.current_output_dir = None
        self.init_ui()
        
    def init_ui(self):
        """UI initialisieren"""
        self.setWindowTitle('CSV2MIDI Converter v1.0')
        self.setGeometry(100, 100, 1000, 700)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        layout = QVBoxLayout(central_widget)
        
        # Tab Widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab 1: Single File
        tabs.addTab(self.create_single_tab(), "Einzelne Datei")
        
        # Tab 2: Batch Processing
        tabs.addTab(self.create_batch_tab(), "Batch-Verarbeitung")
        
        # Tab 3: CSV Editor
        tabs.addTab(self.create_editor_tab(), "CSV Editor")
        
        # Status Bar
        self.statusBar().showMessage('Bereit')
        
    def create_single_tab(self):
        """Tab für einzelne Datei-Konvertierung"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Settings Group
        settings_group = QGroupBox("Einstellungen")
        settings_layout = QVBoxLayout()
        
        # Tempo
        tempo_layout = QHBoxLayout()
        tempo_layout.addWidget(QLabel("Tempo (BPM):"))
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setRange(20, 300)
        self.tempo_spin.setValue(120)
        tempo_layout.addWidget(self.tempo_spin)
        tempo_layout.addStretch()
        settings_layout.addLayout(tempo_layout)
        
        # Time Signature
        time_sig_layout = QHBoxLayout()
        time_sig_layout.addWidget(QLabel("Taktart:"))
        self.time_sig_combo = QComboBox()
        self.time_sig_combo.addItems(['4/4', '3/4', '6/8', '2/4', '5/4', '7/8'])
        time_sig_layout.addWidget(self.time_sig_combo)
        time_sig_layout.addStretch()
        settings_layout.addLayout(time_sig_layout)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # File Selection
        file_group = QGroupBox("Datei")
        file_layout = QVBoxLayout()
        
        # Input File
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("CSV Input:"))
        self.input_label = QLabel("Keine Datei ausgewählt")
        self.input_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; }")
        input_layout.addWidget(self.input_label, 1)
        self.browse_btn = QPushButton("Durchsuchen...")
        self.browse_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(self.browse_btn)
        file_layout.addLayout(input_layout)
        
        # Output File
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("MIDI Output:"))
        self.output_label = QLabel("Automatisch generiert")
        self.output_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; }")
        output_layout.addWidget(self.output_label, 1)
        self.browse_output_btn = QPushButton("Speichern als...")
        self.browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(self.browse_output_btn)
        file_layout.addLayout(output_layout)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Preview
        preview_group = QGroupBox("CSV Vorschau")
        preview_layout = QVBoxLayout()
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Courier", 9))
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.validate_btn = QPushButton("✓ Validieren")
        self.validate_btn.clicked.connect(self.validate_csv)
        self.validate_btn.setEnabled(False)
        button_layout.addWidget(self.validate_btn)
        
        self.convert_btn = QPushButton("▶ Konvertieren")
        self.convert_btn.clicked.connect(self.convert_single)
        self.convert_btn.setEnabled(False)
        self.convert_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.convert_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def create_batch_tab(self):
        """Tab für Batch-Verarbeitung"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Settings
        settings_group = QGroupBox("Einstellungen")
        settings_layout = QVBoxLayout()
        
        # Tempo
        tempo_layout = QHBoxLayout()
        tempo_layout.addWidget(QLabel("Tempo (BPM):"))
        self.batch_tempo_spin = QSpinBox()
        self.batch_tempo_spin.setRange(20, 300)
        self.batch_tempo_spin.setValue(120)
        tempo_layout.addWidget(self.batch_tempo_spin)
        tempo_layout.addStretch()
        settings_layout.addLayout(tempo_layout)
        
        # Time Signature
        time_sig_layout = QHBoxLayout()
        time_sig_layout.addWidget(QLabel("Taktart:"))
        self.batch_time_sig_combo = QComboBox()
        self.batch_time_sig_combo.addItems(['4/4', '3/4', '6/8', '2/4', '5/4', '7/8'])
        time_sig_layout.addWidget(self.batch_time_sig_combo)
        time_sig_layout.addStretch()
        settings_layout.addLayout(time_sig_layout)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Directories
        dir_group = QGroupBox("Verzeichnisse")
        dir_layout = QVBoxLayout()
        
        # Input Directory
        input_dir_layout = QHBoxLayout()
        input_dir_layout.addWidget(QLabel("CSV Ordner:"))
        self.input_dir_label = QLabel("Kein Ordner ausgewählt")
        self.input_dir_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; }")
        input_dir_layout.addWidget(self.input_dir_label, 1)
        self.browse_input_dir_btn = QPushButton("Durchsuchen...")
        self.browse_input_dir_btn.clicked.connect(self.browse_input_directory)
        input_dir_layout.addWidget(self.browse_input_dir_btn)
        dir_layout.addLayout(input_dir_layout)
        
        # Output Directory
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(QLabel("MIDI Ordner:"))
        self.output_dir_label = QLabel("Gleicher Ordner wie Input")
        self.output_dir_label.setStyleSheet("QLabel { background-color: #f0f0f0; padding: 5px; }")
        output_dir_layout.addWidget(self.output_dir_label, 1)
        self.browse_output_dir_btn = QPushButton("Durchsuchen...")
        self.browse_output_dir_btn.clicked.connect(self.browse_output_directory)
        output_dir_layout.addWidget(self.browse_output_dir_btn)
        dir_layout.addLayout(output_dir_layout)
        
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)
        
        # File List
        files_group = QGroupBox("Gefundene CSV-Dateien")
        files_layout = QVBoxLayout()
        self.file_list = QTextEdit()
        self.file_list.setReadOnly(True)
        self.file_list.setMaximumHeight(150)
        files_layout.addWidget(self.file_list)
        files_group.setLayout(files_layout)
        layout.addWidget(files_group)
        
        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Log
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 9))
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.batch_convert_btn = QPushButton("▶ Batch Konvertieren")
        self.batch_convert_btn.clicked.connect(self.convert_batch)
        self.batch_convert_btn.setEnabled(False)
        self.batch_convert_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.batch_convert_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def create_editor_tab(self):
        """Tab für CSV Editor"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Info
        info_label = QLabel("CSV Editor - Erstelle oder bearbeite CSV-Notendaten")
        info_label.setStyleSheet("QLabel { background-color: #e3f2fd; padding: 10px; font-weight: bold; }")
        layout.addWidget(info_label)
        
        # Table
        self.csv_table = QTableWidget()
        self.csv_table.setColumnCount(8)
        self.csv_table.setHorizontalHeaderLabels([
            'track_name', 'midi_channel', 'note', 'octave', 
            'velocity', 'bar', 'beat', 'duration'
        ])
        self.csv_table.setRowCount(10)
        layout.addWidget(self.csv_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_row_btn = QPushButton("+ Zeile hinzufügen")
        add_row_btn.clicked.connect(self.add_table_row)
        button_layout.addWidget(add_row_btn)
        
        delete_row_btn = QPushButton("- Zeile löschen")
        delete_row_btn.clicked.connect(self.delete_table_row)
        button_layout.addWidget(delete_row_btn)
        
        button_layout.addStretch()
        
        load_csv_btn = QPushButton("CSV laden")
        load_csv_btn.clicked.connect(self.load_csv_to_table)
        button_layout.addWidget(load_csv_btn)
        
        save_csv_btn = QPushButton("Als CSV speichern")
        save_csv_btn.clicked.connect(self.save_table_to_csv)
        button_layout.addWidget(save_csv_btn)
        
        convert_from_editor_btn = QPushButton("▶ Direkt zu MIDI")
        convert_from_editor_btn.clicked.connect(self.convert_from_editor)
        convert_from_editor_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(convert_from_editor_btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    # ==================== Event Handlers ====================
    
    def browse_input_file(self):
        """CSV-Datei auswählen"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "CSV-Datei öffnen", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            self.current_input_file = Path(file_name)
            self.input_label.setText(str(self.current_input_file))
            
            # Auto-generate output file
            self.current_output_file = self.current_input_file.with_suffix('.mid')
            self.output_label.setText(str(self.current_output_file))
            
            # Load preview
            self.load_csv_preview()
            
            # Enable buttons
            self.validate_btn.setEnabled(True)
            self.convert_btn.setEnabled(True)
    
    def browse_output_file(self):
        """MIDI-Ausgabedatei auswählen"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "MIDI speichern als", "", "MIDI Files (*.mid);;All Files (*)"
        )
        if file_name:
            self.current_output_file = Path(file_name)
            self.output_label.setText(str(self.current_output_file))
    
    def load_csv_preview(self):
        """CSV-Datei Vorschau laden"""
        try:
            with open(self.current_input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Limit preview to 1000 chars
                preview = content[:1000]
                if len(content) > 1000:
                    preview += "\n\n... (gekürzt)"
                self.preview_text.setText(preview)
        except Exception as e:
            self.preview_text.setText(f"Fehler beim Laden: {e}")
    
    def validate_csv(self):
        """CSV validieren"""
        try:
            df = pd.read_csv(self.current_input_file)
            is_valid, errors = CSVValidator.validate_dataframe(df)
            
            if is_valid:
                QMessageBox.information(
                    self, "Validierung erfolgreich",
                    f"✅ CSV ist valide!\n\n"
                    f"• {len(df)} Zeilen\n"
                    f"• Tracks: {', '.join(df['track_name'].unique())}"
                )
                self.statusBar().showMessage('✅ Validierung erfolgreich', 3000)
            else:
                error_msg = "\n".join(errors)
                QMessageBox.warning(
                    self, "Validierungsfehler",
                    f"❌ Folgende Fehler wurden gefunden:\n\n{error_msg}"
                )
                self.statusBar().showMessage('❌ Validierung fehlgeschlagen', 3000)
                
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Validieren:\n{str(e)}")
            self.statusBar().showMessage('❌ Fehler beim Validieren', 3000)
    
    def convert_single(self):
        """Einzelne Datei konvertieren"""
        try:
            # Tempo und Time Signature
            tempo = self.tempo_spin.value()
            time_sig_str = self.time_sig_combo.currentText()
            num, den = map(int, time_sig_str.split('/'))
            time_sig = (num, den)
            
            self.statusBar().showMessage('🔄 Konvertiere...')
            
            # Parse
            song = CSVParser.parse_csv_file(
                str(self.current_input_file),
                tempo=tempo,
                time_signature=time_sig
            )
            
            # Convert & Save
            MIDIConverter.convert_and_save(song, str(self.current_output_file))
            
            # Success
            track_info = "\n".join([f"• {t.name}: {len(t.notes)} Noten" for t in song.tracks])
            QMessageBox.information(
                self, "Konvertierung erfolgreich",
                f"✅ MIDI-Datei erfolgreich erstellt!\n\n"
                f"Datei: {self.current_output_file}\n\n"
                f"Tracks:\n{track_info}"
            )
            self.statusBar().showMessage('✅ Konvertierung erfolgreich', 5000)
            
        except ValidationError as e:
            QMessageBox.warning(self, "Validierungsfehler", f"❌ {str(e)}")
            self.statusBar().showMessage('❌ Validierungsfehler', 3000)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler bei Konvertierung:\n{str(e)}\n\n{traceback.format_exc()}")
            self.statusBar().showMessage('❌ Konvertierung fehlgeschlagen', 3000)
    
    # ==================== Batch Processing ====================
    
    def browse_input_directory(self):
        """Input-Verzeichnis auswählen"""
        dir_name = QFileDialog.getExistingDirectory(self, "CSV-Ordner auswählen")
        if dir_name:
            self.current_input_dir = Path(dir_name)
            self.input_dir_label.setText(str(self.current_input_dir))
            
            # Auto-set output dir
            if not self.current_output_dir:
                self.current_output_dir = self.current_input_dir
                self.output_dir_label.setText(str(self.current_output_dir))
            
            # Scan for CSV files
            self.scan_csv_files()
    
    def browse_output_directory(self):
        """Output-Verzeichnis auswählen"""
        dir_name = QFileDialog.getExistingDirectory(self, "MIDI-Ausgabe-Ordner auswählen")
        if dir_name:
            self.current_output_dir = Path(dir_name)
            self.output_dir_label.setText(str(self.current_output_dir))
    
    def scan_csv_files(self):
        """CSV-Dateien im Verzeichnis scannen"""
        if not self.current_input_dir:
            return
        
        csv_files = list(self.current_input_dir.glob('*.csv'))
        
        if csv_files:
            file_list_text = f"Gefunden: {len(csv_files)} CSV-Datei(en)\n\n"
            file_list_text += "\n".join([f"• {f.name}" for f in csv_files])
            self.file_list.setText(file_list_text)
            self.batch_convert_btn.setEnabled(True)
        else:
            self.file_list.setText("Keine CSV-Dateien gefunden")
            self.batch_convert_btn.setEnabled(False)
    
    def convert_batch(self):
        """Batch-Konvertierung starten"""
        if not self.current_input_dir or not self.current_output_dir:
            QMessageBox.warning(self, "Fehler", "Bitte wähle Input- und Output-Verzeichnis")
            return
        
        csv_files = list(self.current_input_dir.glob('*.csv'))
        if not csv_files:
            QMessageBox.warning(self, "Fehler", "Keine CSV-Dateien gefunden")
            return
        
        # Tempo und Time Signature
        tempo = self.batch_tempo_spin.value()
        time_sig_str = self.batch_time_sig_combo.currentText()
        num, den = map(int, time_sig_str.split('/'))
        time_sig = (num, den)
        
        # Create output directory if not exists
        self.current_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Start conversion thread
        self.log_text.clear()
        self.log_text.append(f"Starte Batch-Konvertierung von {len(csv_files)} Datei(en)...\n")
        
        self.conversion_thread = ConversionThread(
            csv_files, self.current_output_dir, tempo, time_sig
        )
        self.conversion_thread.progress.connect(self.on_batch_progress)
        self.conversion_thread.finished.connect(self.on_batch_finished)
        self.conversion_thread.start()
        
        self.batch_convert_btn.setEnabled(False)
    
    def on_batch_progress(self, percent, message):
        """Batch-Progress Update"""
        self.progress_bar.setValue(percent)
        self.log_text.append(message)
        self.statusBar().showMessage(message)
    
    def on_batch_finished(self, success, message):
        """Batch-Konvertierung abgeschlossen"""
        self.batch_convert_btn.setEnabled(True)
        self.log_text.append(f"\n{message}")
        
        if success:
            QMessageBox.information(self, "Fertig", message)
            self.statusBar().showMessage('✅ Batch-Konvertierung abgeschlossen', 5000)
        else:
            QMessageBox.warning(self, "Fehler", message)
            self.statusBar().showMessage('❌ Batch-Konvertierung mit Fehlern', 5000)
    
    # ==================== CSV Editor ====================
    
    def add_table_row(self):
        """Zeile zur Tabelle hinzufügen"""
        row_count = self.csv_table.rowCount()
        self.csv_table.insertRow(row_count)
    
    def delete_table_row(self):
        """Aktuelle Zeile löschen"""
        current_row = self.csv_table.currentRow()
        if current_row >= 0:
            self.csv_table.removeRow(current_row)
    
    def load_csv_to_table(self):
        """CSV in Tabelle laden"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "CSV laden", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            try:
                df = pd.read_csv(file_name)
                
                # Set table size
                self.csv_table.setRowCount(len(df))
                
                # Fill table
                for row_idx, row in df.iterrows():
                    for col_idx, col_name in enumerate(df.columns):
                        item = QTableWidgetItem(str(row[col_name]))
                        self.csv_table.setItem(row_idx, col_idx, item)
                
                self.statusBar().showMessage(f'✅ CSV geladen: {len(df)} Zeilen', 3000)
                
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Laden:\n{str(e)}")
    
    def save_table_to_csv(self):
        """Tabelle als CSV speichern"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "CSV speichern", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            try:
                # Extract data from table
                headers = [self.csv_table.horizontalHeaderItem(i).text() 
                          for i in range(self.csv_table.columnCount())]
                
                data = []
                for row in range(self.csv_table.rowCount()):
                    row_data = []
                    for col in range(self.csv_table.columnCount()):
                        item = self.csv_table.item(row, col)
                        row_data.append(item.text() if item else '')
                    # Skip empty rows
                    if any(row_data):
                        data.append(row_data)
                
                # Create DataFrame and save
                df = pd.DataFrame(data, columns=headers)
                df.to_csv(file_name, index=False)
                
                self.statusBar().showMessage(f'✅ CSV gespeichert: {len(df)} Zeilen', 3000)
                QMessageBox.information(self, "Erfolg", f"CSV gespeichert:\n{file_name}")
                
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern:\n{str(e)}")
    
    def convert_from_editor(self):
        """Direkt aus Editor zu MIDI konvertieren"""
        try:
            # Extract data from table
            headers = [self.csv_table.horizontalHeaderItem(i).text() 
                      for i in range(self.csv_table.columnCount())]
            
            data = []
            for row in range(self.csv_table.rowCount()):
                row_data = []
                for col in range(self.csv_table.columnCount()):
                    item = self.csv_table.item(row, col)
                    row_data.append(item.text() if item else '')
                # Skip empty rows
                if any(row_data):
                    data.append(row_data)
            
            if not data:
                QMessageBox.warning(self, "Fehler", "Tabelle ist leer!")
                return
            
            # Create temporary CSV
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
                df = pd.DataFrame(data, columns=headers)
                df.to_csv(tmp.name, index=False)
                tmp_csv = tmp.name
            
            # Validate
            is_valid, errors = CSVValidator.validate_dataframe(df)
            if not is_valid:
                error_msg = "\n".join(errors)
                QMessageBox.warning(self, "Validierungsfehler", 
                                   f"❌ Fehler in den Daten:\n\n{error_msg}")
                return
            
            # Ask for output file
            file_name, _ = QFileDialog.getSaveFileName(
                self, "MIDI speichern als", "", "MIDI Files (*.mid);;All Files (*)"
            )
            
            if file_name:
                # Convert
                song = CSVParser.parse_csv_file(tmp_csv, tempo=120, time_signature=(4, 4))
                MIDIConverter.convert_and_save(song, file_name)
                
                QMessageBox.information(self, "Erfolg", 
                                       f"✅ MIDI erstellt!\n\n{file_name}")
                self.statusBar().showMessage('✅ MIDI aus Editor erstellt', 3000)
            
            # Clean up temp file
            import os
            os.unlink(tmp_csv)
            
        except Exception as e:
            QMessageBox.critical(self, "Fehler", 
                               f"Fehler bei Konvertierung:\n{str(e)}\n\n{traceback.format_exc()}")