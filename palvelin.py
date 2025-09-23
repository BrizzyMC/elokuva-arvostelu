"""
=================================================================

Nimi:       palvelin.py
kuvaus:     Tässä tiedostossa luodaan Flask sovellus olio ja sitä
            käyttäen käynnistetään Flask palvelin, palvelin
            käynnistyy käynnistämällä tämän tiedoston.

Tekiä:      Viljam Vänskä
Päivämäärä: 23.9.2025
Versio:     1.0

=================================================================
"""

from flask import Flask
from sovellus import rekistoroi_blueprintit


def luo_sovellus() -> object:
    """
    Luo Flask sovellus olion ja rekisteröi siihen blueprint:it

    Palauttaa:
        - Flask sovellus olion
    """

    sovellus = Flask(__name__)
    rekistoroi_blueprintit(sovellus)

    return sovellus



if __name__ == '__main__':
    sovellus = luo_sovellus()
    sovellus.run(debug=True)


