"""
Tämä tiedosto sisältää sql functioita jotka palauttavat sql komentoja, sql komennot ovat siis täällä jotta niitä olisi helpompi ylläpitää, tarkistaa ja muokata

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


# * ----------------------------------------------------------------- *
# Tietokannasta haku functiot

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