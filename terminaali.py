"""
=================================================================

Nimi:       terminaali.py
kuvaus:     Tiedosto sisältää terminaali käyttöjärjestelmälle
            olennaiset tulostus ja input functioit. Luotu
            jotta "__main__.py" ei olisi niin täynnä tulostuksia.

Tekiä:      Viljam Vänskä
Päivämäärä: 12.9.2025
Versio:     1.1

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
                kirjautuminen_valmis = True # sql komento menee läpi

            except NameError:
                print('Käyttäjänimi varattu!!')
            
        # kirjaudu sisään
        elif valinta == '2':
            try:
                kayttaja_id = sql_yhteys.kirjaudu(nimi, salasana)
                kirjautuminen_valmis = True # sql komento menee läpi

            except TypeError:
                print('Käyttäjää ei löytynyt!!')

            except ValueError:
                print('Väärä salasana!!')
    
    return kayttaja_id
        


def paa_valikko() -> int:
    """
    Functiossa on ohjelman "Pää valikko", tämä pitää siis sisällään valinta kysymyksen että mihin toimintoon käyttäjä haluaa jatkaa seuraavana, palauttaa valinnan int muodossa

    Palauttaa (int):
        - 1: Hae elokuvia
        - 2: Jätä arvostelu
        - 3: Käyttäjätiedot
        - 4: Poista arvostelu
        - 5: Muokkaa arvostelua
        - 6: Lopeta
    """

    __puhdista_naytto()

    # Tyhjä valinta jotta silmukka pysyy päällä (Älä koske!)
    valinta = 0

    # Silmukka rikotaan kun valinta on (1 - "numerot") välissä. (Tehty näin jotta helpomi muokata tulevaisuudessa!)
    numerot = 6

    silmukka_valinnat = [f'{luku}' for luku in range(1, numerot+1)]

    # Rikotaan silmukka kun valinta on listan sisällä
    while valinta not in silmukka_valinnat:
        # Tulostetaan vaihtoehdot
        print("\nVaihtoehdot:")
        print("1 - Hae elokuvia")
        print("2 - Jätä arvostelu")
        print("3 - Käyttäjätiedot")
        print("4 - Poista arvostelu")
        print("5 - Muokkaa arvostelua")
        print("6 - Lopeta")
        valinta = input('>: ')

    return int(valinta) # Muutetaan valinta int muotoon (str --> int)
        


def tulosta_elokuvat(sql_yhteys:object) -> None:
    """
    Tulostaa elokuvat hakusanan perusteella, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
    """

    __puhdista_naytto()

    hakusana = input('Anna hakusana (tyhjä etsii kaikki elokuvat tietokannasta)\n>: ')

    # Haetaan elokuvat tietokannasta
    elokuvat = sql_yhteys.hae_elokuvia(hakusana)

    # Tulostaa kaikki elokuvat
    for elokuva in elokuvat:
        print(elokuva)

    input('paina enter jatkaaksesi...')



def tulosta_kayttajatiedot(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Tulostaa käyttäjätiedot (käyttäjän joka käyttää ohjelmaa), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """
    
    __puhdista_naytto()

    # Etsitään käyttäjätiedot tietokannasta
    kayttaja = sql_yhteys.kayttajan_tiedot(kayttajan_id)

    # Tulostetaan käyttäjätiedot
    print(kayttaja)

    input('Paina enter jatkaaksesi...')



def muuta_salasanaa(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Functiolla voi muokata OMAA salasanaansa (käyttäjä katsotaan id:n perusteella), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """

    __puhdista_naytto()

    # Käyttäjä antaa uuden salasanan (ei vahvistuksia cuz feeling lazy today)
    uusi_salasana = input('Anna uusi salasana: ')

    # Päivittää salasanan tietokantaan
    sql_yhteys.muuta_salasanaa(kayttajan_id, uusi_salasana)



def muuta_kayttajanimea(sql_yhteys:object, kayttajan_id:int) -> None:
    """
    Functiolla muokataan OMAA käyttäjänimeään (käyttäjä katsotaan id:n perusteella), ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
    """

    __puhdista_naytto()

    nimea_annetaan = True

    # Pyydetään uusi käyttäjänimi
    while nimea_annetaan:
        try:
            uusi_kayttajanimi = input('Anna uusi käyttäjänimi: ')

            # Päivittää nimen tietokantaan
            sql_yhteys.muuta_kayttajanimea(kayttajan_id, uusi_kayttajanimi)

            # Käyttäjänimi annettu onnistuneesti
            nimea_annetaan = False
            
        # Nimi varattu, takaisin silmukan alkuun
        except NameError:
            print('Käyttäjänimi varattu!')



def lisaa_arvostelu(sql_yhteys:object, kayttajan_id:int, elokuvan_id:int) -> None:
    """
    Functiolla lisätään arvostelu arvostelu elokuvalle, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - elokuvan_id: Arvosteltavan elokuvan id int muodossa
    """

    __puhdista_naytto()

    # Käytttäjä antaa arvostelut
    arvosana  = input('Anna arvosana: ') # arvosana --> int
    kommentti = input('Anna kommentti: ')

    # Lisää kommentin tietokantaan
    sql_yhteys.lisaa_arvostelu(elokuvan_id, int(arvosana), kayttajan_id, kommentti)



def poista_arvostelu(sql_yhteys:object, kayttajan_id:int, arvostelun_id:int) -> None:
    """
    Functio poistaa arvostelun tietokannasta, tarvitsee käyttäjän id:tä koska pitää varmistaa ettei poista toisen käyttäjän arvostelua, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - arvostelun_id: Poistettavan arvostelun id int muodossa
    """

    __puhdista_naytto()

    # Haluaako käyttäjä poistaa kommentin?
    poistetaanko = input('Poistetaanko arvostelu? (Y/N): ')

    # Jos haluaa niin kommentti poistetaan tietokannasta, jos ei niin poistutaan functiosta
    if poistetaanko.lower() == 'y':
        sql_yhteys.poista_arvostelu(arvostelun_id)



def muokkaa_kommenttia(sql_yhteys:object, kayttajan_id:int, arvostelun_id:int) -> None:
    """
    Functio muokka käyttäjän omaa kommenttia, tarvisteee käyttäjä id:tä jotta voi varmistua ettei muokkaa kenenkään muun kommenttia, ei palauta mitään

    Parametrit:
        - sql_yhteys: "sql.py" Tiedostosta luotu "yhteys" olio, joka ylläpitää sql tietokanta yhteys komentoja
        - kayttajan_id: Käyttäjän joka käyttää ohjelmaa id int muodossa
        - arvostelun_id: Arvostelun id jossa kommentti on, (arvostelun id int muodossa)
    """

    __puhdista_naytto()

    # Käyttäjä antaa uuden kommentin
    uusi_kommentti = input('Kirjoita uusi kommentti: ')

    # Päivitetään kommentti tietokantaan
    sql_yhteys.muokkaa_kommenttia(arvostelun_id, uusi_kommentti)
