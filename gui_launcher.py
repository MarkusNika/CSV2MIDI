#!/usr/bin/env python
"""
GUI Launcher für CSV2MIDI
"""
import sys
from PyQt5.QtWidgets import QApplication
from csv2midi.gui.main_window import CSV2MIDIMainWindow


def main():
    """GUI starten"""
    app = QApplication(sys.argv)
    app.setApplicationName("CSV2MIDI Converter")
    app.setOrganizationName("MarkusNika")
    
    window = CSV2MIDIMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()