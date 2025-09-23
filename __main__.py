#!/usr/bin/python
"""
=================================================================

Nimi:       __main__.py
kuvaus:     Tämä tiedosto käynnistää Flask palvelimen (debug off).
            Tiedosto kutsuu tarvittavat functiot "palvelin.py"
            tiedostosta.

Tekiä:      Viljam Vänskä
Päivämäärä: 23.9.2025
Versio:     1.3

=================================================================
"""

from palvelin import kaynnista_palvelin


if __name__ == '__main__':
    kaynnista_palvelin(debug=False)

