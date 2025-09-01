"""
Tämä tiedosto sisältää sql functioita jotka palauttavat sql komentoja, sql komennot ovat siis täällä jotta niitä olisi helpompi ylläpitää, tarkistaa ja muokata

Kaikki functiot tiedostossa ovat pelkästään sql komentoja, ne ovat täällä apu functioina sql.py tiedostolle
# TODO kirjoita lisää kommenttia!!!
"""

# Taulukoiden luonti functiot

def luo_elokuva_taulukko() -> str:
    """Functio palauttaa sql komennon joka luo tietokantaan taulukon elokuville"""

    return '''CREATE TABLE IF NOT EXISTS "elokuvat" (
    "id"                INTEGER NOT NULL,
    "julkaisu_vuosi"    VARCHAR(4) NOT NULL,
    "nimi"              VARCHAR NOT NULL,
    "keskiarvo"         FLOAT,
    "juoni"             VARCHAR,
    "arvostelu_maara"   INT,
    PRIMARY KEY("id" AUTOINCREMENT)
    )'''


def luo_arvostelu_taulukko() -> str:
    """Functio palauttaa sql komennon joka luo tietokantaan taulukon elokuville"""

    return '''CREATE TABLE IF NOT EXISTS "arvostelut" (
    "id"                INTEGER NOT NULL,
    "elokuva_id"        INTEGER NOT NULL,
    "kayttaja_nimi"     VARCHAR NOT NULL,
    "arvosana"          FLOAT NOT NULL,
    "kommentti"         VARCHAR,
    PRIMARY KEY("id" AUTOINCREMENT)
    )'''


def luo_kayttajat_taulukko() -> str:
    """Functio palauttaa sql komennon joka luo tietokantaan taulukon käyttäjä tiedoille/käyttäjille"""

    return '''CREATE TABLE IF NOT EXISTS "kayttajat" (
    "id"                INTEGER NOT NULL,
    "kayttaja_nimi"     VARCHAR NOT NULL,
    "kayttaja_salasana" VARCHAR NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    )'''

# * ----------------------------------------------------------------- *
# Tietokantaan lisäämis functiot

def luo_kayttaja_tietokantaan() -> str:
    """
    Functio palauttaa sql komennon joka lisää käyttäjän sql tietokannan käyttäjät tauluun

    Sql Parametrit:
        - kayttaja_nimi: käyttäjän nimi str muodossa
        - kayttaja_salasana: Käyttäjän salasana "hash" (bytes) muodossa
    """

    return 'INSERT INTO kayttajat (kayttaja_nimi, kayttaja_salasana) VALUES (?, ?)'


def lisaa_arvostelu_tietokantaan() -> str:
    """
    Functio palauttaa sql komennon joka lisää arvostelun tietokantaan

    Sql Parametrit:
        - elokuva_id: Elokuvan id id muodossa johonka arvostelu linkitetään
        - kayttaja_nimi: Käyttäjän joka arvostelee id int muodossa
        - arvosana: annettu arvosana float muodossa
        - kommentti: mahdollinen kommentti str muodossa
    """

    return "INSERT INTO arvostelut (elokuva_id, kayttaja_nimi, arvosana, kommentti) VALUES (?, ?, ?, ?)"


def lisää_elokuva_tietokantaan() -> str:
    """
    Functio palauttaa sql komennon joka lisää elokuvan tietokantaan

    Sql Parametrit:
        - id: elokuvan id int muodossa
        - julkaisu_vuosi. Minä vuonna elokuva on julkaistu int muodossa
        - nimi: Elokuvan nimi str muodossa
        - keskiarvo: Elokuvan keskiarvo float muodossa
        - juoni: Kuvaus elokuvan juonesta str muodossa
    """

    return """INSERT OR IGNORE INTO elokuvat (id, julkaisu_vuosi, nimi, keskiarvo, juoni) 
                                                VALUES (?, ?, ?, ?, ?)"""


# * ----------------------------------------------------------------- *
# Tietokannasta valinta functiot

def valitse_kayttajanimi_tietokannasta() -> str:
    """Palauttaa sql komennon joka valitsee käyttäjänimen tietokannan käyttäjät taulukosta"""

    return 'SELECT kayttaja_nimi FROM kayttajat'


def valitse_kayttaja_kirjautumistiedoilla_tietokannasta() -> str:
    """
    Palauttaa sql komennon joka valitsee käyttäjätiedot kayttaja taulukosta käyttäjätietojen perusteella
    
    Sql Parametrit:
        - kayttaja_nimi: Halutun käyttäjän nimi str muodossa
        - kayttaja_salasana: Halutun käyttäjän salasana "hash" (bytes) muodossa
    """

    return "SELECT * FROM kayttajat WHERE kayttaja_nimi = (?) AND kayttaja_salasana = (?)"


def valitse_keskiarvo_ja_maara_tietokannasta() -> str:
    """
    Palauttaa sql komennon joka valitsee keskiarvon ja arvosteluiden määrän elokuvat taulukosta

    Sql Parametri:
        - id: ottaa elokuvan id:n int muodossa ja etsii sen perusteella elokuvalle keskiarvon ja arvosteluiden määrän
    """

    return "SELECT keskiarvo, arvostelu_maara FROM elokuvat WHERE id = ?"


def valitse_nimi_kommentti_arvosana_tietokannasta() -> str:
    """
    Palauttaa sql komennon joka valitsee käyttäjänimen, arvosanan, kommentit arvosteluista elokuvan id:n perusteella

    Sql Parametri:
        - elokuva_id: Valitun elokuvan id int muodossa
    """

    return "SELECT kayttaja_nimi, arvosana, kommentti FROM arvostelut WHERE elokuva_id = ?"


def valitse_kayttajatiedot_tietokannasta():
    """
    palauttaa sql komennon joka valitsee käyttäjänimen ja arvosteluiden määrän käyttäjätiedoista käyttäjänimen perusteella

    Sql Parametri:
        - kayttaja_nimi: Valittavan käyttäjän käyttäjänimi str muodossa
    """

    return "SELECT kayttaja_nimi, arvostelu_maara FROM kayttajat WHERE kayttaja_nimi = ?"


# * ----------------------------------------------------------------- *
# Tietokannan päivittämis functiot

def paivita_keskiarvo_maara_tietokantaan() -> str:
    """
    Palauttaa sql komennon joka päivittää elokuvan keskiarvon ja arvosteluiden määrän annetun id:n perusteella

    Sql Parametrit:
        - keskiarvo: Elokuvan keskiarvo float muodossa, tämä arvo laitetaan tietokantaan
        - arvostelu_maara: Montako arvostelua elokuvalla on (int muodossa), tämä arvo laitetaan tietokantaan
        - id: Valitun elokuvan id int muodossa, tämä on se elokuva jonka tietoja muokataan/päivitetään
    """

    return "UPDATE elokuvat SET keskiarvo = ?, arvostelu_maara = ? WHERE id = ?"


def paivita_kayttajan_arvostelumaara_tietokantaan() -> str:
    """
    Palauttaa sql komennon joka päivittää käyttäjän arvostelu määrää käyttäjänimen perusteella

    Sql Parametri:
        - kayttaja_nimi: Käyttäjän nimi jonka tietoja halutaan muokata str muodossa
    """

    return "UPDATE kayttajat SET arvostelu_maara = arvostelu_maara + 1 WHERE kayttaja_nimi = ?"
