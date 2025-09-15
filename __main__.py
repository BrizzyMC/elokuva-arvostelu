"""
=================================================================

Nimi:       __main__.py
kuvaus:     Tämä tiedosto pitää sisällään ohjelman "main loopin",
            tähän silmukkaan on kasattu ohjelman koodi toimivaksi
            kokonaisuudeksi. Tämän tiedoston suorittaminen
            käynnistää ohjelman.

Tekiä:      Viljam Vänskä
Päivämäärä: 15.9.2025
Versio:     1.1

=================================================================
"""

import terminaali   
from sql import sql_yhteys

if __name__ == '__main__':
    ohjelma_kaynnissa = True

    # Luodaan tietokanta yhteys
    tietokanta = sql_yhteys()
    tietokanta.lataa_elokuvat_tietokantaan("elokuvat.json")

    # Käyttäjä kirjautuu sisään, varastoidaan käyttäjän id int muodossa
    kayttajan_id = terminaali.kirjautuminen(tietokanta)

    while ohjelma_kaynnissa:

        # Käyttäjä valitsee toiminnon minkä haluaa suorittaa
        toiminto = terminaali.paa_valikko()
        
        if toiminto == 1:   # Hae elokuvia
            terminaali.tulosta_elokuvat(tietokanta)

        elif toiminto == 2: # Jätä arvostelu
            e_id = int(input('Elokuvan id: '))
            terminaali.lisaa_arvostelu(tietokanta, kayttajan_id, e_id)

        elif toiminto == 3: # Käyttäjätiedot
            terminaali.tulosta_kayttajatiedot(tietokanta, kayttajan_id)

        elif toiminto == 4: # Poista arvostelu
            a_id = int(input('Arvostelun id: '))
            terminaali.poista_arvostelu(tietokanta, kayttajan_id, a_id)

        elif toiminto == 5: # Muokkaa arvostelua
            a_id = int(input('Arvostelun id: '))
            terminaali.muokkaa_kommenttia(tietokanta, kayttajan_id, a_id)

        elif toiminto == 6: # Lopeta
            ohjelma_kaynnissa = False


    # Suljetaan tietokanta yhteys kun ohjelma lopetetaan
    tietokanta.sulje_yhteys()
