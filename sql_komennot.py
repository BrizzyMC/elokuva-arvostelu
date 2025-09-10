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
    "kayttaja_id"       INTEGER NOT NULL,
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
    "arvostelu_maara"   INTEGER DEFAULT 0,
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
        - kayttaja_id: Käyttäjän joka arvostelee id int muodossa
        - arvosana: annettu arvosana float muodossa
        - kommentti: mahdollinen kommentti str muodossa
    """

    return "INSERT INTO arvostelut (elokuva_id, kayttaja_id, arvosana, kommentti) VALUES (?, ?, ?, ?)"


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

def valitse_kayttajan_arvostelut_tietokannasta() -> str:
    """
    Palauttaa sql komennon joka valitsee arvosanat käyttäjä id:n perusteella

    Sql Parametri:
        - kayttaja_id: Käyttäjän id int muodossa jonka arvosanat halutaan palauttaa
    """

    return "SELECT * FROM arvostelut WHERE kayttaja_id = (?)"


def valitse_kayttajatiedot_tietokannasta() -> str:
    """
    palauttaa sql komennon joka valitsee käyttäjänimen ja arvosteluiden määrän käyttäjätiedoista käyttäjän id:n perusteella

    Sql Parametri:
        - id: Valittavan käyttäjän käyttäjä id int muodossa
    """

    return "SELECT kayttaja_nimi, arvostelu_maara FROM kayttajat WHERE id = (?)"


def etsi_elokuvia_tietokannasta() -> str:
    """
    Palauttaa sql komennon joka valitsee elokuvat tietokannasta hakusanan perusteella

    Sql Parametri:
        - hakusana 2x: Hakusana voi olla elokuvan nimi tai vuosi str muodossa

    HUOM:
        Hakusana tulee antaa kahteen kertaan!!
    """

    return "SELECT * FROM elokuvat WHERE nimi LIKE '%' || ? || '%' or julkaisu_vuosi LIKE '%' || ? || '%'"


def etsi_kayttaja_nimen_perusteella() -> str:
    """
    Palauttaa komennon jolla haetaan käyttäjänimeä tietokannasta

    Sql Parametri:
        - kayttaja_nimi: Kayttajanimi mitä haetaan tietokannasta
    """

    return "SELECT kayttaja_nimi FROM kayttajat WHERE kayttaja_nimi = (?)"


def valitse_arvostelu_id_perusteella() -> str:
    """
    Palauttaa sql komennon joka valitsee arvostelun id:n perusteella

    Sql Parametri:
        - id: Aalittavan arvostelun id (int muodossa)
    """

    return "SELECT * FROM arvostelut WHERE id = (?)"


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
        - kayttaja_id: Käyttäjän id jonka tietoja halutaan muokata int muodossa
    """

    return "UPDATE kayttajat SET arvostelu_maara = arvostelu_maara + 1 WHERE id = ?"


def paivita_kayttajanimi() -> str:
    """
    Palauttaa sql komennon joka päivittää käyttäjän salasanan käyttäjä id:n perusteella

    Sql Parametrit:
        - kayttaja_id: Kayttäjän id jonka nimeä halutaan muokata (int muodossa)
        - uusi_kayttajanimi: Uusi haluttu käyttäjänimi (str muodossa)
    """

    return "UPDATE kayttajat SET kayttaja_nimi = (?) WHERE id = (?)"


def paivita_kommentti() -> str:
    """
    Palauttaa sql komennon joka päivittää kommentin id:n perusteella

    Sql Parametrit:
        - arvostelun id: Muokattava kommentti valitaan arvostelu id:n perusteella (int muodossa)
        - uusi_kommentti: Uusi kommentti jolla vanha korvataan (str muodossa)
    """

    return "UPDATE arvostelut SET kommentti = (?) WHERE id = (?)"


def paivita_salasana() -> str:
    """
    Palauttaa sql komennon joka päivittää uuden salasanan tietokantaa id:n perusteella

    Sql Parametrit:
        - kayttaja_id: Käyttäjän id jonka salasanaa halutaan muokata (int muodossa)
        - uusi_salasana: Uusi salasana joka päivitetään tietokantaan (str muodossa)
    """

    return "UPDATE kayttaja SET salasana = (?) WHERE id = (?)"


# * ----------------------------------------------------------------- *
# Tietokannasta poistamis functiot

def poista_arvostelu() -> str:
    """
    Palauttaa sql komennon joka poistaa arvostelun tietokannasta id:n perusteella
    
    Sql Parametri:
        - id: Poistettavan arvostelun id (int muodossa)
    """

    return "DELETE FROM arvostelut WHERE id = (?)"

