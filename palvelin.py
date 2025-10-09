"""
=================================================================

Nimi:       palvelin.py
kuvaus:     Tässä tiedostossa luodaan Flask sovellus olio ja sitä
            käyttäen käynnistetään Flask palvelin, palvelin
            käynnistyy käynnistämällä tämän tiedoston.

Tekiä:      Viljam Vänskä
Päivämäärä: 25.9.2025
Versio:     1.1

=================================================================
"""

from flask import Flask
from sovellus import rekistoroi_blueprintit
from asetukset import Asetukset


def luo_sovellus() -> object:
    """
    Luo Flask sovellus olion ja rekisteröi siihen blueprint:it

    Palauttaa:
        - Flask sovellus olion
    """

    sovellus = Flask(__name__, template_folder='html-sivut', static_folder='ulkoasu')
    rekistoroi_blueprintit(sovellus)

    return sovellus



def kaynnista_palvelin(konfiguraatio:object):
    """
    Functio lataa Flask palvelimelle asetukset annetusta konfiguraatio oliosta luo Flask sovelluksen ja käynnistää Flask palvelimen
    
    Parametri:
        - konfiguraatio: Olio joka pitää sisällään asetukset Flask palvelimelle
    """

    sovellus = luo_sovellus()
    sovellus.config.from_object(konfiguraatio)
    
    sovellus.run(port=sovellus.config['PORT'], host=sovellus.config['HOST'])




if __name__ == '__main__':
    kaynnista_palvelin(Asetukset)


