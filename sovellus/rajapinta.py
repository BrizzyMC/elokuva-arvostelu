"""
=================================================================

Nimi:       rajapinta.py
kuvaus:     Tiedosto pitäää sisällään functiot jotka kommunikoivat
            verkko rajapinnan kanssa ja vastaavat sivulla
            tapahtuvasta tiedon käsittelystä.

Tekiä:      Viljam Vänskä
Päivämäärä: 24.9.2025
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
    Luo käyttäjän ja ohjaa kotisivulle
    """

    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']

        try:
            __tietokanta.lisaa_kayttaja(kayttaja, salasana)
            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except NameError:
            return redirect(url_for('Sivut.luo_käyttäjä'))
        


@rajapinta.route('/kirjaudu/kirjataan_sisaan', methods=['POST'])
def kirjaudu():
    """
    POST /kirjaudu/kirjataan_sisaan
    ---
    Kirjaa käyttäjän sisään ja ohjaa kotisivulle
    """

    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']

        try:
            __tietokanta.kirjaudu(kayttaja, salasana)
            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except ValueError:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))

        except TypeError:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))



@rajapinta.route('/haku', methods=['POST'])
def hae():
    """
    POST /haku
    ---
    Hakee elokuvia hakusanan perusteella

    Palauttaa:
        - Löytyneet elokuvat
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
    Hakee käyttäjätietoja käyttäjä id:n perusteella

    Palauttaa:
        - Käyttäjän tiedot
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
    Päivittää nimen, salasanan ja ohjaa kotisivulle

    HUOM:
        - Jos kenttä on tyhjä niin se jätetään huomiotta
    """

    if request.method == 'POST':
        uusi_nimi     = request.form['nimi']
        uusi_salasana = request.form['salasana']

        if uusi_nimi:
            __tietokanta.muuta_kayttajanimea(kayttaja_id, uusi_nimi)

        if uusi_salasana:
            __tietokanta.muuta_salasanaa(kayttaja_id, uusi_nimi)

        return redirect(url_for('Sivut.kirjaudu_sisaan'))



@rajapinta.route('/lisää_arvostelu', methods=['POST'])
def lisaa_arvostelu():
    """
    POST /lisää_arvostelu
    ---
    Lisää arvostelun tietokantaan
    """

    if request.method == 'POST':
        arvosana  = request.form['arvosana']
        kommentti = request.form['kommentti']

        __tietokanta.lisaa_arvostelu(1, int(arvosana), 1, kommentti)

    return [arvosana, kommentti]



def muokkaa_kommentti():
    """
    POST /muokkaa_kommenttia
    ---
    Muokkaa kommenttia
    """

    if request.method == 'POST':
        kommentti = request.form['kommentti']

        try:
            __tietokanta.muokkaa_kommenttia(1, kommentti)

        except ValueError:
            redirect(url_for('Sivut.muokkaa_kommenttia'))

    return [kommentti]




            
