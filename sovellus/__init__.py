"""
=================================================================

Nimi:       __init__.py
kuvaus:     Tiedosto sisältää function jolla rekistöröidään flask
            blueprint:it, api ja sivut.

Tekiä:      Viljam Vänskä
Päivämäärä: 23.9.2025
Versio:     1.0

=================================================================
"""

from .rajapinta import rajapinta
from .sivut import sivut


def rekistoroi_blueprintit(sovellus):
    """
    Ottaa vastaan Flask sovellus olion ja rekisteröi blueprint:it, api ja sivut

    Parametri:
        - sovellus: Flask sovellus olio
    """

    sovellus.register_blueprint(rajapinta)
    sovellus.register_blueprint(sivut)

