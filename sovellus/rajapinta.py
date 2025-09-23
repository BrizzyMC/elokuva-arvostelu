"""
=================================================================

Nimi:       rajapinta.py
kuvaus:     Tiedosto pitäää sisällään functiot jotka kommunikoivat
            verkko rajapinnan kanssa ja vastaavat sivulla
            tapahtuvasta tiedon käsittelystä.

Tekiä:      Viljam Vänskä
Päivämäärä: 23.9.2025
Versio:     1.0

=================================================================
"""

from flask import redirect, url_for, request, Blueprint
from .tietokanta.sql import sql_yhteys


__tietokanta = sql_yhteys()

rajapinta = Blueprint('rajapinta', __name__)


# > ------------ [ Toiminto Functiot ] ------------------------ <

@rajapinta.route('/luo_käyttäjä/luodaan', methods=['POST'])
def luo_kayttaja():
    """
    POST /luo_käyttäjä/luodaan
    ---
    
    """

    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']
        try:
            print(__tietokanta.lisaa_kayttaja(kayttaja, salasana))
            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except NameError:
            return redirect(url_for('Sivut.luo_käyttäjä'))
        


@rajapinta.route('/kirjaudu/kirjataan_sisaan', methods=['POST'])
def kirjaudu():
    """
    POST /kirjaudu/kirjataan_sisaan
    ---

    """

    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']
        try:
            print(__tietokanta.kirjaudu(kayttaja, salasana))
            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except ValueError:
            return redirect(url_for('Sivut.kirjaudu'))

        except TypeError:
            return redirect(url_for('Sivut.kirjaudu'))



@rajapinta.route('/haku', methods=['POST'])
def hae():
    """
    POST /haku
    ---

    """

    if request.method == 'POST':
        hakusana = request.form['hakusana']
        elokuvat = __tietokanta.hae_elokuvia(hakusana)
        return elokuvat



@rajapinta.route('/kayttaja_tiedot', methods=['POST'])
def kayttaja_tiedot():
    """
    POST /kayttaja_tiedot
    ---

    """

    if request.method == 'POST':
        kayttaja_id = request.form['kayttajatiedot']
        tiedot = __tietokanta.kayttajan_tiedot(int(kayttaja_id))
        return tiedot



@rajapinta.route('/paivita_kayttajaa', methods=['POST'])
def paivita_nimi_salasana(kayttaja_id:int=1):
    """
    POST /paivita_kayttajaa
    ---

    """

    if request.method == 'POST':
        uusi_nimi     = request.form['nimi']
        uusi_salasana = request.form['salasana']

        if uusi_nimi:
            __tietokanta.muuta_kayttajanimea(kayttaja_id, uusi_nimi)

        if uusi_salasana:
            __tietokanta.muuta_salasanaa(kayttaja_id, uusi_nimi)

        return redirect(url_for('Sivut.kirjaudu'))



def lisaa_arvostelu():
    # coming soon, tulossa pian, odota vain, se tulee, hetki vielä
    pass
    


            
