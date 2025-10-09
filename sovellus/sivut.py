"""
=================================================================

Nimi:       sivut.py
kuvaus:     Tiedosto pitää sisällään sovelluksen reittien
            hallinnan, eli functioita jotka määräävät reitit
            Flask html sivuihin ("julkiset sivut").

Tekiä:      Viljam Vänskä
Päivämäärä: 9.10.2025
Versio:     1.1

Sisältää reitit:
    - /kirjaudu     -> kirjaudu.html
    - /koti/<nimi>  -> koti.html (parametri: käyttäjän nimi)
    - /kirjaudu     -> kirjaudu.html
    - /koti/<nimi>/omat_arvostelut  -> omat_arvostelut.html (parametri: käyttäjän nimi)
    - /koti/<nimi>/vaihda_salasana  -> vaihda_salasana.html (parametri: käyttäjän nimi)
    - /koti/<nimi>/vaihda_nimi      -> vaihda_nimi.html (parametri: käyttäjän nimi)
    - /koti/<kayttaja_nimi>/elokuvan_tiedot/<nimi>  -> elokuvan_tiedot.html (parametri: käyttäjän nimi, elokuvan_nimi)

=================================================================
"""

from flask import render_template, Blueprint, session, abort, redirect, url_for, request

# Luodaan blueprint
sivut = Blueprint('sivut', __name__)



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
        return redirect(url_for('sivut.kirjaudu_sisaan'))
    
    # Käyttäjä yrittää päästä toisen käyttäjälle
    if session['nimi'] != nimi:
        abort(403)
    
    else:
        return palauta



# > ------------ [ Sivun Lataus Functiot ] ------------------------ <

@sivut.route('/kirjaudu')
def kirjaudu_sisaan():
    """Renderöi kirjautumis sivun, jos error niin poimii sen url osoitteesta ja tulostaa käyttäjälle"""
    
    # Käsittelee virheilmoitukset sivun url osoitteesta
    virheilmoitus_kirjautuminen=request.args.get('virheilmoitus_kirjautuminen')
    if not virheilmoitus_kirjautuminen:
        virheilmoitus_kirjautuminen = ''

    virheilmoitus_kayttajan_luominen=request.args.get('virheilmoitus_kayttajan_luominen')
    if not virheilmoitus_kayttajan_luominen:
        virheilmoitus_kayttajan_luominen = ''

    return render_template('kirjaudu.html', virheilmoitus_kirjautuminen=virheilmoitus_kirjautuminen, virheilmoitus_kayttajan_luominen=virheilmoitus_kayttajan_luominen)



@sivut.route('/koti/<nimi>')
def koti(nimi:str):
    """Renderöi kotisivun

    Parametri:
        - nimi: käyttäjän nimi (str)
    """
    try:
        elokuva = session['elokuva']
        session.pop('elokuva')

        return tarkista_henkilo(nimi, render_template('koti.html', nimi=nimi, elokuva=elokuva))

    except KeyError:
        return redirect(url_for('rajapinta.koti_sivu'))



@sivut.route('/koti/<kayttaja_nimi>/elokuvan_tiedot/<nimi>', methods=['GET', 'POST'])
def elokuvan_tiedot(kayttaja_nimi, nimi):
    """Renderöi sivun jossa on elokuvan tiedot ja elokuvaa on mahdollisuus arvostella

    Parametrit:
        - kayttaja_nimi: Käyttäjän nimi
        - elokuva: elokuvan nimi jotta se voidaan kirjoittaa selaimeen
    """

    # Poimii elokuvan tiedot url osoitteesta
    elokuvan_id=request.args.get('id')
    genret=request.args.get('genret')
    juoni=request.args.get('juoni')
    keskiarvo=round(float(request.args.get('keskiarvo')),1) # Float vain yksi desimaali
    julkaisu_vuosi=request.args.get('julkaisu_vuosi')
    kuva=f'https://m.media-amazon.com/images/M/{request.args.get("kuva")}'
    
    # Poimii arvostelut sessioista ja tuhoaa temp session
    try:
        arvostelut = session['arvostelut']
        session.pop('arvostelut')
    
    # Kun sivu ladataan uudelleen (error handling koska session tuhotaan)
    except KeyError:
        return redirect(url_for('rajapinta.laheta_elokuvan_tiedot', **{'elokuvan_id':elokuvan_id}))

    return tarkista_henkilo(kayttaja_nimi, render_template('elokuvan_tiedot.html', nimi=nimi, julkaisu_vuosi=julkaisu_vuosi, keskiarvo=keskiarvo,
    juoni=juoni, genret=genret, kuva=kuva, elokuvan_id=elokuvan_id, arvostelut=arvostelut))
    


@sivut.route('/koti/<nimi>/vaihda_nimi')
def vaihda_nimi(nimi):
    """Renderöi salasanan vaihto sivun
    
    Parametri:
        - nimi: Käyttäjän nimi (str)
    """
    
    return tarkista_henkilo(nimi, render_template('vaihda_nimi.html'))



@sivut.route('/koti/<nimi>/vaihda_salasana')
def vaihda_salasana(nimi):
    """Renderöi salasanan vaihto sivun

    Parametri:
        - nimi: Käyttäjän nimi (str)
    """

    return tarkista_henkilo(nimi, render_template('vaihda_salasana.html'))



@sivut.route('/koti/<nimi>/omat_arvostelut')
def omat_arvostelut(nimi):
    """Ottaa arvostelut vastaan sessiossa ja renderöi omat arvostelut sivun

    Parametri:
        - nimi: Käyttäjän nimi (str)
    """

    try:
        # Poimii arvostelut sessioista ja tuhoaa temp session
        arvostelut = session['arvostelut']
        session.pop('arvostelut')

        return tarkista_henkilo(nimi, render_template('omat_arvostelut.html', arvostelut=arvostelut))

    except KeyError:
        return redirect(url_for('rajapinta.laheta_arvostelut'))



@sivut.route('/muokkaa_kommenttia', methods=['POST'])
def muokkaa_kommenttia():
    """Renderöi kommentin muokkaus sivun, käyttää post jotta saa elokuvan id:n annettua eteenpäin

    Parametri:
        - nimi: Käyttäjän nimi (str)
    """

    if request.method == 'POST':
        elokuvan_id = request.form['_elokuvan_id']
        print('Elokuvan id: ', elokuvan_id)

        return tarkista_henkilo(session['nimi'], render_template('muokkaa_kommenttia.html', elokuvan_id=elokuvan_id))

