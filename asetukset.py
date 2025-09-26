"""
=================================================================

Nimi:       asetukset.py
kuvaus:     Tämä tiedosto pitää sisällää luokan Flask asetuksista,
            nämä asetukset Flask sovellus olio lataa käyttöönsä
            ennen kuin avaa julkisen palvelin yhteyden.

Tekiä:      Viljam Vänskä
Päivämäärä: 25.9.2025
Versio:     1.0

=================================================================
"""

class Asetukset:
    """Luokka pitää sisällään Flask palvelimen asetukset"""
    
    # Yleiset asetukset
    DEBUG      = True
    PORT       = 8000
    TESTING    = True
    HOST       = '127.0.0.1'
    SECRET_KEY = 'testi'
    
    # Keksit
    SESSION_COOKIE_NAME        = 'testi_keksi'
    SESSION_COOKIE_HTTPONLY    = True
    SESSION_COOKIE_SECURE      = False
    PERMANENT_SESSION_LIFETIME = 3600

