"""
=================================================================

Nimi:       terminaali.py
kuvaus:     Tiedosto sisältää terminaali käyttöjärjestelmälle
            olennaiset tulostus ja input functioit. Luotu
            jotta "__main__.py" ei olisi niin täynnä tulostuksia.

Tekiä:      Viljam Vänskä
Päivämäärä: 11.9.2025
Versio:     1.0

=================================================================
"""

from sys import platform # Kutsutaan platform jotta tiedetään käyttäjän järjestelmä
from os import system    # Kutsutaan os jotta voidaan puhdistaa terminaali

def __puhdista_naytto() -> None:
    """
    (apu functio) Functio puhdistaa terminaali näytön käyttäen os -> system ja sys -> platform functioita

    Tukee:
        - Windows
        - Linux

    Logiikka:
        - sys --> platform: Tarkistetaan mikä käyttöjärjestelmä käyttäjällä on, tämän tiedon pohjalta voidaan puhdistaa näyttö oikealla komennolla
        - os  --> system:   Tällä functiolla voimma suorittaa oikean terminaalin pyyhkimis komennon
    """

    if platform == 'linux':   # Jos linux
        return system('clear')

    elif platform == 'win32': # Jos windows
        return system('cls')



def kirjautuminen(sql_yhteys:object) -> int:
    """
    Functio käyttää sql yhteyttä, kirjaa käyttäjän sisään/luo uuden käyttäjän ja palauttaa kirjautuneen käyttäjän id:n int muodossa

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja

    Palauttaa:
        - Kirjautuneen käyttäjän id int muodossa
    """

    # Aloitetaan puhtaalta näytöltä
    __puhdista_naytto()

    # Luodaan tyhjä valinta jotta silmukka pysyy käynnissä
    valinta = 0

    # Käyttäjä valitsee kirjautuuko vai luoko uuden käyttäjän
    while valinta not in ['1', '2']:
        valinta = input('Haluatko [1] Luoda käyttäjän vai [2] Kirjautua sisään?\n>: ')

    # Nyt kirjaudutaan/luodaan käyttäjä, False tarkoittaa että tämä prosessi ei ole valmis vielä
    kirjautuminen_valmis = False

    while not kirjautuminen_valmis:
        # Pyydetään käyttäjänimi ja salasana
        nimi     = input('Anna käyttäjänimi: ')
        salasana = input('Anna salasana: ')

        # Luo käyttäjä
        if valinta == '1':
            try:
                kayttaja_id = sql_yhteys.lisaa_kayttaja(nimi, salasana)
                kirjautuminen_valmis = True

            except NameError:
                print('Käyttäjänimi varattu!!')
            
        # kirjaudu sisään
        elif valinta == '2':
            try:
                kayttaja_id = sql_yhteys.kirjaudu(nimi, salasana)
                kirjautuminen_valmis = True

            except TypeError:
                print('Käyttäjää ei löytynyt!!')

            except ValueError:
                print('Väärä salasana!!')
    
    return kayttaja_id
        


def paa_valikko() -> int:
    """
    Functiossa on ohjelman "Pää valikko", tämä pitää siis sisällään valinta kysymyksen että mihin toimintoon käyttäjä haluaa jatkaa seuraavana, palauttaa valinnan int muodossa

    Palauttaa:
        - ... TODO numero mikä on mitä?!
    """

    # Aloitetaan puhtaalta näytöltä
    __puhdista_naytto()

    valinta = 0

    while valinta not in ['1', '2', '2']:
        valinta = input('Valitse... ') #TODO

    return valinta
        



def tulosta_elokuvat(sql_yhteys:object) -> None:
    """
    Tulostaa elokuvat hakusanan perusteella, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
    """
    
    pass



def tulosta_kayttajatiedot(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Tulostaa käyttäjätiedot (käyttäjän joka käyttää ohjelmaa), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """
    
    pass



def muuta_salasanaa(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Functiolla voi muokata OMAA salasanaansa (käyttäjä katsotaan id:n perusteella), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """

    pass



def muuta_kayttajanimea(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Functiolla muokataan OMAA käyttäjänimeään (käyttäjä katsotaan id:n perusteella), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """

    pass



def lisaa_arvostelu(sql_yhteys:object, kayttajan_id:int, elokuvan_id:int) -> None:
    """
    Functiolla lisätään arvostelu arvostelu elokuvalle, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - elokuvan_id: Arvosteltavan elokuvan id int muodossa
    """

    pass



def poista_arvostelu(sql_yhteys:object, kayttajan_id:int, arvostelun_id:int) -> None:
    """
    Functio poistaa arvostelun tietokannasta, tarvitsee käyttäjän id:tä koska pitää varmistaa ettei poista toisen käyttäjän arvostelua, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - arvostelun_id: Poistettavan arvostelun id int muodossa
    """

    pass



def muokkaa_kommenttia(sql_yhteys:object, kayttajan_id:int, arvostelun_id:int) -> None:
    """
    Functio muokka käyttäjän omaa kommenttia, tarvisteee käyttäjä id:tä jotta voi varmistua ettei muokkaa kenenkään muun kommenttia, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - arvostelun_id: Arvostelun id jossa kommentti on, (arvostelun id int muodossa)
    """

    pass

