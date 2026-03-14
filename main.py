#!/usr/bin/env python
"""
CSV2MIDI Main Entry Point
"""
import sys
from csv2midi.cli.commands import cli

if __name__ == '__main__':
    sys.exit(cli())