"""
=================================================================

Nimi:       rajapinta.py
kuvaus:     Tiedosto pitäää sisällään functiot jotka kommunikoivat
            verkko rajapinnan kanssa ja vastaavat sivulla
            tapahtuvasta tiedon käsittelystä.

Tekiä:      Viljam Vänskä
Päivämäärä: 7.10.2025
Versio:     1.1

=================================================================
"""

from flask import redirect, url_for, request, Blueprint, session, render_template
from .tietokanta.sql import sql_yhteys


__tietokanta = sql_yhteys()

rajapinta = Blueprint('rajapinta', __name__)


# > ------------ [ Toiminto Functiot ] ------------------------ <

@rajapinta.route('/')
def tarkista_kirjautuminen():
    """
    Tarkistaa onko käyttäjä kirjautunut sisään, tieto hankitaan sessiota käyttäen
    
    Vaihtoehdot:
        - Kyllä: Ohjataan kotisivulle
        - Ei: Ohjataan käyttäjän luontiin
    """
    try:
        if session.get('kayttaja_id'):
            kayttaja_nimi = __tietokanta.kayttajan_tiedot(session['kayttaja_id'])[0]['nimi']
            print(kayttaja_nimi)
            return redirect(url_for('Sivut.koti', nimi=kayttaja_nimi))
            
        else:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))
            
    except TypeError:
        return redirect(url_for('Sivut.kirjaudu_sisaan'))


@rajapinta.route('/koti')
def koti_sivu():
    """Ohjaa käyttäjän kotisivulle "tarkista_kirjautuminen" function kautta"""
    return tarkista_kirjautuminen()



@rajapinta.route('/kirjaudu/luodaan_kayttaja', methods=['POST'])
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
            session['kayttaja_id'] = __tietokanta.kirjaudu(kayttaja, salasana) # Käyttäjä kirjataan sisään ja id tallennetaan sessioon
            session['nimi'] = kayttaja

            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except NameError:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))



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
            session['kayttaja_id'] = __tietokanta.kirjaudu(kayttaja, salasana)
            session['nimi'] = kayttaja
            
            return redirect(url_for('Sivut.koti', nimi=kayttaja))

        except ValueError:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))

        except TypeError:
            return redirect(url_for('Sivut.kirjaudu_sisaan'))




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
def paivita_nimi_salasana():
    """
    POST /paivita_kayttajaa
    ---
    Päivittää nimen, salasanan ja ohjaa kotisivulle

    HUOM:
        - Jos kenttä on tyhjä niin se jätetään huomiotta

    Ohjaa:
        - Kirjautumis sivulle (muutetaan tulevaisuudessa?)
    """

    uusi_nimi     = None
    uusi_salasana = None

    if request.method == 'POST':
        # Laiskan miehen error handling
        # KeyError tulee jos käyttäjä ei anna arvoa (selaimessa)
        # Voidaan "pass" koska arvot määritetty tyhjäksi function alussa
        try:
            uusi_nimi = request.form['nimi']
        except KeyError:
            pass

        try:
            uusi_salasana = request.form['salasana']
        except KeyError:
            pass

        if uusi_nimi:
            try:
                __tietokanta.muuta_kayttajanimea(session['kayttaja_id'], uusi_nimi)
                session['nimi'] = uusi_nimi
            except NameError: # Käyttäjänimi viety!!
                pass

        if uusi_salasana:
            __tietokanta.muuta_salasanaa(session['kayttaja_id'], uusi_nimi)

        return redirect(url_for('Sivut.kirjaudu_sisaan'))



@rajapinta.route('/lisää_arvostelu', methods=['POST'])
def lisaa_arvostelu():
    """
    POST /lisää_arvostelu
    ---
    Lisää arvostelun tietokantaan
    
    Ohjaa:
        - Takaisin elokuva tietojen sivulle
    """

    if request.method == 'POST':
        arvosana  = request.form['arvosana']
        kommentti = request.form['kommentti']
        elokuvan_id = request.form['_elokuvan_id']

        __tietokanta.lisaa_arvostelu(elokuvan_id, int(arvosana), session['kayttaja_id'], kommentti)

        return laheta_elokuvan_tiedot(elokuvan_id)



@rajapinta.route('/muokkaa_kommentti', methods=['POST'])
def muokkaa_kommentti():
    """
    POST /muokkaa_kommentti
    ---
    Muokkaa kommenttia
    """

    if request.method == 'POST':
        kommentti = request.form['kommentti']
        elokuvan_id = request.form['_elokuvan_id']

        try:
            __tietokanta.muokkaa_kommenttia(elokuvan_id, kommentti)

        except ValueError:
            redirect(url_for('Sivut.muokkaa_kommenttia'))

    return laheta_arvostelut()



@rajapinta.route('/kirjaudu_ulos', methods=['POST'])
def kirjaudu_ulos():
    """
    POST /kirjaudu_ulos
    ---
    Kirjaa käyttäjän ulos ja ohjaa kirjautumis sivulle

    Ohjaa:
        - Kirjautumis sivu
    """

    if request.method == 'POST':
        session.pop('nimi')
        session.pop('kayttaja_id')

        return redirect(url_for('Sivut.kirjaudu_sisaan'))


@rajapinta.route('/haku', methods=['GET', 'POST'])
def haku():
    """
    GET /haku - Renderöi haku sivun
    POST /haku - Hakee elokuvia hakusanan perusteella
    """
    
    if request.method == 'GET':
        return render_template('haku.html')
    
    elif request.method == 'POST':
        hakusana = request.form['hakusana']
        elokuvat = __tietokanta.hae_elokuvia(hakusana)

        # Amazonin linkki eteen
        for elokuva in elokuvat:
            elokuva['kuva'] = f'https://m.media-amazon.com/images/M/{elokuva['kuva']}'

        return render_template('haku.html', elokuvat=elokuvat)

      
      
@rajapinta.route('/lähetä_elokuvan_tiedot', methods=['POST'])
def laheta_elokuvan_tiedot(elokuvan_id:int=None):
    """
    POST /lähetä_elokuvan_tiedot
    ---
    Lähettää elokuvan nimen (str) ja loput tiedot (dict) sivun lataus functiolle, arvostelut lähetetään temp sessiossa

    Ohjaa:
        - Elokuvan tiedot sivu
    """

    if request.method == 'POST':
        if not elokuvan_id:
            elokuvan_id = request.form['elokuvan_id']
            
        # Hankkii elokuvan tiedot dict muodossa
        elokuva = __tietokanta.elokuva_id_dict(elokuvan_id)
        
        # Laitetaan arvostelut listaan
        arvostelut = __tietokanta.elokuvan_arvostelut(elokuvan_id)
        arvostelut_lista = []
        for arvostelu in arvostelut:
            nimi = __tietokanta.kayttajan_tiedot(arvostelu[0])[0]['nimi']
            arvostelut_lista.append({'nimi':nimi, 'arvosana':arvostelu[1], 'kommentti':arvostelu[2]})
        
        # Luodaan arvosteluista temp sessio, tämä tehdään koska selaimen url olisi muuten liian pitä
        # ja pythonin kautta ohjelman haluttu logiikka pettäisi. (sessio tuhotaan kun tiedot ovat kerätty)
        session['arvostelut'] =  arvostelut_lista

        return redirect(url_for('Sivut.elokuvan_tiedot', kayttaja_nimi=session['nimi'], **elokuva))


            
@rajapinta.route('/vaihda_nimi', methods=['POST'])
def vaihda_nimi():
    """
    POST /vaihda_nimi
    ---
    Ohjaa käyttäjän nimen vaihto sivulle antaen url osoitteelle käyttäjänimen

    Ohjaa:
        - Nimen vaihto sivulle
    """

    return redirect(url_for('Sivut.vaihda_nimi', nimi=session['nimi']))



@rajapinta.route('/vaihda_salasana', methods=['POST'])
def vaihda_salasana():
    """
    POST /vaihda_salasana
    ---
    Ohjaa käyttäjän salasanan vaihto sivulle antaen url osoitteelle käyttäjänimen

    Ohjaa:
        - Salasanan vaihto sivulle
    """

    return redirect(url_for('Sivut.vaihda_salasana', nimi=session['nimi']))



@rajapinta.route('/lähetä_arvostelut', methods=['POST'])
def laheta_arvostelut():
    """
    POST /lähetä_arvostelut
    ---
    Etsii käyttäjän arvostelut tietokannasta ja ohjaa käyttäjän katsomaan omia arvosteluja antaen url osoitteelle käyttäjänimen

    Ohjaa:
        - Omat arvostelut sivulle
    """

    # Etsitään arvostelut tietokannasta ja lisätään dict:iin elokuvan nimi
    arvostelut =__tietokanta.kayttajan_tiedot(session['kayttaja_id'], True)[0]['arvostelut']
    arvostelut_lista = []
    for arvostelu in arvostelut:
        arvostelu['nimi'] = __tietokanta.elokuva_id_dict(arvostelu['elokuvan_id'])['nimi']

    # Luo temp session johon arvostelut tallennetaan
    session['arvostelut'] = arvostelut

    return redirect(url_for('Sivut.omat_arvostelut', nimi=session['nimi']))



