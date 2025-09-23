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
from dotenv import load_dotenv
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



def kaynnista_palvelin(debug:bool=False):
    """
    Functio lataa ".env" tiedoston configuroinnin, luo Flask sovelluksen ja käynnistää Flask palvelimen

    Parametri:
        - debug: True/False (bool)
    """

    load_dotenv()
    sovellus = luo_sovellus()
    sovellus.run(debug=debug)




if __name__ == '__main__':
    kaynnista_palvelin(debug=True)


