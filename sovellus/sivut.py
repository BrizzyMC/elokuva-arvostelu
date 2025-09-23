"""
=================================================================

Nimi:       sivut.py
kuvaus:     Tiedosto pitää sisällään sovelluksen reittien
            hallinnan, eli functioita jotka määräävät reitit
            Flask html sivuihin.

Tekiä:      Viljam Vänskä
Päivämäärä: 23.9.2025
Versio:     1.0

=================================================================
"""

from flask import render_template, Blueprint


# Luodaan blueprint
sivut = Blueprint('Sivut', __name__)


# > ------------ [ Sivun Lataus Functiot ] ------------------------ <

# Aloitus sivu
@sivut.route('/')
def aloitus():
    return render_template('muuta_tietoja.html')

# Kirjautumis sivu
@sivut.route('/kirjaudu')
def kirjaudu_sisaan():
    return render_template('kirjaudu.html')

# Käyttäjän luonti sivu
@sivut.route('/luo_käyttäjä')
def uusi_kayttaja():
    return render_template('luo_kayttaja.html')

# kotisivu
@sivut.route('/koti/<nimi>')
def koti(nimi):
    return render_template('koti.html')

    
