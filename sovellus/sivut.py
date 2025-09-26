"""
=================================================================

Nimi:       sivut.py
kuvaus:     Tiedosto pitää sisällään sovelluksen reittien
            hallinnan, eli functioita jotka määräävät reitit
            Flask html sivuihin ("julkiset sivut").

Tekiä:      Viljam Vänskä
Päivämäärä: 25.9.2025
Versio:     1.0

Sisältää reitit:
    - /kirjaudu           -> kirjaudu.html
    - /luo_käyttäjä       -> luo_kayttaja.html
    - /koti/<nimi>        -> koti.html (parametri: käyttäjän nimi)
    - /arvostele          -> arvostelu.html
    - /muokkaa_kommenttia -> muokkaa_kommenttia.html

=================================================================
"""

from flask import render_template, Blueprint, session, abort, redirect, url_for

# Luodaan blueprint
sivut = Blueprint('Sivut', __name__)



def tarkista_henkilo(nimi:str, palauta):
    """
    Tarkistaa onko henkilö se keneksi koittaa kirjautua
    
    Parametrit:
        - nimi: Nimi jolla koitetaan kirjautua sisään
        - palauta: Palauttaa annetun komennon
    
    Ohjaa (jos henkilö on):
        - Aito: Ohjaa haetulle sivulle
        - Väärä: Antaa abort 403
    """
    
    # Käyttäjä ei ole kirjautunut sisään
    if 'nimi' not in session:
        return redirect(url_for('Sivut.uusi_kayttaja'))
    
    # Käyttäjä yrittää päästä toisen käyttäjälle
    if session['nimi'] != nimi:
        abort(403)
    
    else:
        return palauta



# > ------------ [ Sivun Lataus Functiot ] ------------------------ <

@sivut.route('/kirjaudu')
def kirjaudu_sisaan():
    """Renderöi kirjautumis sivun"""
    return render_template('kirjaudu.html')


@sivut.route('/luo_käyttäjä')
def uusi_kayttaja():
    """Renderöi käyttäjän luonti sivun"""
    return render_template('luo_kayttaja.html')


@sivut.route('/koti/<nimi>')
def koti(nimi:str):
    """Renderöi kotisivun

    Parametri:
        - nimi: käyttäjän nimi (str)
    """

    return tarkista_henkilo(nimi, render_template('koti.html'))


@sivut.route('/arvostele')
def arvostele():
    """Renderöi arvostelu sivun"""
    return render_template('arvostelu.html')


@sivut.route('/muokkaa_kommenttia')
def muokkaa_kommenttia():
    """Renderöi kommentin muokkaus sivun"""
    return render_template('muokkaa_kommenttia.html')

    
