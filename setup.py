"""
Setup für CSV2MIDI
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='csv2midi',
    version='1.0.1',
    author='Markus Nika',
    author_email='your.email@example.com',
    description='CSV to MIDI Converter für Musiker und Komponisten',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MarkusNika/CSV2MIDI',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'mido>=1.3.0',
        'pandas>=2.0.0',
        'click>=8.1.0',
        'PyQt5>=5.15.0',
    ],
    entry_points={
        'console_scripts': [
            'csv2midi=csv2midi.cli.commands:cli',
        ],
    },
)
