"""
=================================================================

Nimi:       sivut.py
kuvaus:     Tiedosto pitää sisällään sovelluksen reittien
            hallinnan, eli functioita jotka määräävät reitit
            Flask html sivuihin ("julkiset sivut").

Tekiä:      Viljam Vänskä
Päivämäärä: 1.10.2025
Versio:     1.0

Sisältää reitit:
    - /kirjaudu           -> kirjaudu.html
    - /koti/<nimi>        -> koti.html (parametri: käyttäjän nimi)
    - /arvostele          -> arvostelu.html

=================================================================
"""

from flask import render_template, Blueprint, session, abort, redirect, url_for, request

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
        return redirect(url_for('Sivut.kirjaudu_sisaan'))
    
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


@sivut.route('/koti/<nimi>')
def koti(nimi:str):
    """Renderöi kotisivun

    Parametri:
        - nimi: käyttäjän nimi (str)
    """

    return tarkista_henkilo(nimi, render_template('koti.html', nimi=nimi))


@sivut.route('/arvostele')
def arvostele():
    """Renderöi arvostelu sivun"""
    return render_template('arvostelu.html')



@sivut.route('/koti/<kayttaja_nimi>/elokuvan_tiedot/<nimi>')
def elokuvan_tiedot(kayttaja_nimi, nimi):
    """Renderöi sivun jossa on elokuvan tiedot ja elokuvaa on mahdollisuus arvostella

    Parametrit:
        - elokuva: elokuvan nimi jotta se voidaan kirjoittaa selaimeen
    """

    # Poimii elokuvan tiedot url osoitteesta
    elokuvan_id=request.args.get('id')
    genret=request.args.get('genret')
    juoni=request.args.get('juoni')
    keskiarvo=request.args.get('keskiarvo')
    julkaisu_vuosi=request.args.get('julkaisu_vuosi')
    kuva=request.args.get('kuva')
    
    # Poimii arvostelut sessioista
    arvostelut = session['arvostelut']
    print(arvostelut)
    session.pop('arvostelut')

    return tarkista_henkilo(kayttaja_nimi, render_template('elokuvan_tiedot.html', nimi=nimi, julkaisu_vuosi=julkaisu_vuosi, keskiarvo=keskiarvo,
    juoni=juoni, genret=genret, elokuvan_id=elokuvan_id, arvostelut=arvostelut))
    
