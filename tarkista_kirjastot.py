"""
=================================================================

Nimi:       tarkista_kirjastot.py
kuvaus:     Tiedosto pitää sisällään function joka tarkistaa onko
            käyttäjän koneella kaikki tarpeelliset kirjastot ja
            jos ei niin ne asennetaan.

Tekiä:      Viljam Vänskä
Päivämäärä: 24.9.2025
Versio:     1.0

=================================================================
"""

import importlib
from os import system


def tarkista_kirjastot():
    """
    Functio tarkistaa onko käyttäjä asentanut kaikki tarpeelliset kirjastot ja jos ei niin ne asennetaan

    Kirjastot:
        - hashlib
        - flask
        - python-dotenv
    """

    try:
        importlib.import_module('hashlib')
    except ImportError:
        system('pip install hashlib')

    try:
        importlib.import_module('flask')
    except ImportError:
        system('pip install flask')

    try:
        importlib.import_module('dotenv')
    except ImportError:
        system('pip install python-dotenv')



if __name__ == '__main__':
    tarkista_kirjastot()


