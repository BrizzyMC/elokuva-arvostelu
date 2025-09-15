"""
=================================================================

Nimi:       sql.py
kuvaus:     Tänne tiedostoon tulee sql yhteys ja sitä vahvasti
            käyttävät komennot (sql komennot eri tiedostossa!).
            Tämä tiedosto pitää sisällään class olion joka luo,
            ylläpitää ja sulkee sql tietokanta yhteyden.

Tekiä:      Viljam Vänskä & Benjamin
Päivämäärä: 12.9.2025
Versio:     1.1

=================================================================
"""


# * ------------------------------------------------------------------------------ *
# Kutsuu käytettävät kirjastot

import sqlite3      # Kutsuu sqlite3 kirjaston (joka on projektin pää tietokanta)

import json         # Kutsuu json kirjaston tiedoston lukua varten (vain "lataa_elokuvat_tietokantaan" käyttää kirjastoa)

import sql_komennot # Kutsuu sql komennot, sql_komennot tiedostosta

from apu_functiot import hash_salasana, vertaa_salasana # Apu functiot salasanan piilottamiseen ja vertaamiseen

# * ------------------------------------------------------------------------------ *



# Määritetään tiedosto mitä tietokanta käyttää, muuttujan tulisi olla tietokannan nimi (EI SAA MUUTTUA OHJELMAN AIKANA) ja loppua ".db"
TIETOKANTA = 'database.db'



# Luodaan sqlite luokka joka hallinnoi kaikkea sql yhteyttä ohjelmassa (tiedoston loppukoodi luokan sisällä)
class sql_yhteys:
    """
    Luokka luo yhteyden ".db" tietokantaan käyttäen sqlite3 kirjastoa, jos tietokantaa ei ole olemassa niin se luodaan olion luonti prosessissa automaattisesti.

    Luokalla hallinnoidaan käyttäjien, elokuvien ja arvosteluiden dataa sqlite3 kirjastoa käyttäen. 

    Pitää sisällään:
        - lisaa_kayttaja
            -> Lisätään uusi käyttäjä tietokantaan, palautetaan käyttäjän id.

        - kirjaudu
            -> Kirjataan olemassa oleva käyttäjä tietokantaan ja palautetaan käyttäjän id.

        - lisaa_arvostelu
            -> Lisätään arvostelu tietokantaan ja linkitetään se elokuvaan käyttäen elokuvan id:tä.

        - elokuvan_arvostelut
            -> Palauttaa listan elokuvat arvosteluista.

        - sulje_yhteys
            -> Sulkee sqlite3 yhteyden tietokantaan (ohjelman lopussa).

        - kayttajan_tiedot
            -> Palauttaa käyttäjän tiedot dict muodossa.

        - lataa_elokuvat_tietokantaan
            -> Lataa elokuvat tietokantaan json tiedostosta.

        - hae_elokuvia
            -> Hakee elokuvia tietokannasta niiden nimen ja vuosiluvun perusteella, palauttaa listan elokuvista.

        - muuta_kayttajanimea
            -> Muokkaa käyttäjän nimeä tietokannassa.

        - poista_arvostelu
            -> Poistaa arvostelun tietokannasta.

        - muokkaa_kommenttia
            -> Muokkaa olemassa olevan arvostelun kommenttia (vain kommenttia) tietokannasta.

        - muuta_salasanaa
            -> Antaa käyttäjän vaihtaa salasanaa tietokannasta.
    """


    def __init__(self):
        """Yhdistaa SQLite tietokantaan, Luo taulukot (jos tarve), Palauttaa cursorin ja conn."""

        # Luo cursorin ja conn ( luo tietokanta tiedoston jos ei olemassa )
        self.conn   = sqlite3.connect(TIETOKANTA)
        self.cursor = self.conn.cursor()


        self.cursor.execute( sql_komennot.luo_arvostelu_taulukko() ) # Luo arvostelu taulukon tietokantaan (mikäli ei ole olemassa)

        self.cursor.execute( sql_komennot.luo_elokuva_taulukko()   ) # Luo elokuva taulukon tietokantaan   (mikäli ei ole olemassa)

        self.cursor.execute( sql_komennot.luo_kayttajat_taulukko() ) # Luo käyttäjät taulukon tietokantaan (mikäli ei ole olemassa)


        self.conn.commit() # Tallentaa mahdolliset muutokset



    def lisaa_kayttaja(self, nimi:str, salasana:str) -> bytes or NameError:
        """
        Functio lisää käyttäjän tietokantaan, palauttaa piilotetun salasanan bytes muodossa. Jos käyttäjänimi varattu niin palauttaa NameError.

        Parametrit:
            - nimi: käyttäjän nimi str muodossa
            - salasana: Käyttäjän salasana str muodossa
        """

        # Piilottaa salasanan
        hashed_salasana = hash_salasana(salasana)

        # Valitsee nimet tietokannasta
        nimet = self.cursor.execute( sql_komennot.valitse_kayttajanimi_tietokannasta() )

        # Tarkastaa onko nimi varattu
        for i in nimet.fetchall():
            if i[0] == nimi:
                raise NameError('Käyttäjänimi on varattu!')
        
        # Lisää käyttäjän tietokantaan
        self.cursor.execute( sql_komennot.luo_kayttaja_tietokantaan(), (nimi, hashed_salasana) )

        # Tallentaa mahdolliset muutokset
        self.conn.commit()

        return hashed_salasana
    


    def kirjaudu(self, kayttaja_nimi: str, salasana: str) -> int or TypeError or ValueError:
        """
        Tarkistaa käyttäjän kirjautumistiedot ja palauttaa käyttäjän ID:n.

        Parametrit:
            kayttaja_nimi: Käyttäjän nimi
            salasana: Käyttäjän salasana

        Palauttaa:
            Käyttäjän ID jos kirjautuminen onnistuu
            
        Raises:
            ValueError: Jos kirjautuminen epäonnistuu
        """
        # Hakee käyttäjän tiedot nimen perusteella
        kayttaja = self.cursor.execute("SELECT id, kayttaja_salasana FROM kayttajat WHERE kayttaja_nimi = ?", (kayttaja_nimi,)).fetchone()
        
        # jos käyttäjää ei löytynyt
        if not kayttaja:
            raise TypeError("Käyttäjää ei löytynyt")
        
        kayttaja_id, tallennettu_salasana = kayttaja
        
        # Tarkistaa salasanan ja palauttaa ID:n jos onnistui
        if vertaa_salasana(salasana, tallennettu_salasana):
            return int(kayttaja_id)
        else:
            raise ValueError("Väärä salasana")

    
    

    def lisaa_arvostelu(self, elokuva_id:int, arvosana:int, kayttaja_id:int, kommentti:str="") -> bool:
        """
        Lisää elokuvalle arvostelu ja päivittää elokuvan keskiarvon sekä käyttäjän arvostelumäärän.

        Palauttaa True/False

        Parametrit:
            - elokuva_id: arvosteltavan elokuvan id int muodossa
            - arvosana: annettava arvosana int muodossa (0-5)
            - kayttajan_id: Käyttäjän joka kommentoi id int muodossa
            - kommentti: mahdollinen kommentti elokuvalle str muodossa (voi jättää tyhjäksi)
        """

        # Hakee keskiarvon ja arvostelujen määrän id:n perusteella
        elokuva = self.cursor.execute( sql_komennot.valitse_keskiarvo_ja_maara_tietokannasta(), (elokuva_id,) ).fetchone()
        
        # Tarkistaa löytyykö elokuvaa
        if not elokuva:
            print("Elokuvaa ei löytynyt")
            return False
        
        # Tarkistaa vanhan keskiarvon ja arvosteluiden määrän
        vanha_keskiarvo = elokuva[0] if elokuva[0] else 0
        arvostelu_maara = elokuva[1] if elokuva[1] else 0
        
        # Laskee keskiarvon
        uusi_arvostelu_maara = arvostelu_maara + 1
        uusi_keskiarvo = ((vanha_keskiarvo * arvostelu_maara) + arvosana) / uusi_arvostelu_maara
        
        # Päivittää elokuvan keskiarvon ja arvostelujen määrän
        self.cursor.execute( sql_komennot.paivita_keskiarvo_maara_tietokantaan(), (uusi_keskiarvo, uusi_arvostelu_maara, elokuva_id) )
        
        # Lisää arvostelun
        self.cursor.execute( sql_komennot.lisaa_arvostelu_tietokantaan(), (elokuva_id, kayttaja_id, arvosana, kommentti) )
        
        # Päivittää käyttäjän arvostelumäärän
        self.cursor.execute( sql_komennot.paivita_kayttajan_arvostelumaara_tietokantaan(), (kayttaja_id,) )
        
        self.conn.commit() # Tallentaa mahdolliset muutokset

        print(f"Arvostelu lisätty. Uusi keskiarvo: {uusi_keskiarvo:.1f}")
        return True



    def elokuvan_arvostelut(self, elokuva_id:int) -> list:
        """
        Etsii elokuvien arvostelut id:n perusteella, palauttaa arvostelut listassa.

        parametrit:
            - elokuva_id: Elokuvan id int muodossa, jonka arvostelut halutaan tietää
        """

        # hakee arvostelut
        arvostelut = self.cursor.execute( sql_komennot.valitse_nimi_kommentti_arvosana_tietokannasta(), (elokuva_id,) ).fetchall()

        return arvostelut
        
        
    
    def sulje_yhteys(self) -> None:
        """
        Sulkee sql yhteyden tietokantaan, ei palauta mitään

        Käytetään ohjelman lopussa tai sen sulkemisen yhteydessä
        """

        self.conn.close() # Sulkee sql yhteyden

    

    def kayttajan_tiedot(self, kayttaja_id:int, arvostelut:bool=False) -> list[dict]:
        """
        Palauttaa dict:in listan sisällä käyttäjän tiedoista, jos arvostelut = True niin palauttaa myös käyttäjän arvostelut listassa

        Parametrit:
            - kayttaja_id: Käyttäjän id int muodossa jonka tiedot halutaan tulostaa
            - arvostelut: Jos True (bool) niin palauttaa myös käyttäjän arvostelut dict muodossa

        Dict Arvot:
            - nimi (str)
            - arvostelu_maara (int)
            - arvostelut (list)
                - id (int)
                - elokuvan_id (int)
                - kayttaja_id (int)
                - arvosana (float)
                - kommentti (str)
        
        Esimerkki Palautus:
            > arvostelu = False:
            --> [{'nimi': 'jarppi', 'arvostelu_maara': 1, 'arvostelut': False}]
            > arvostelu = True
            --> [{'nimi': 'jarppi', 'arvostelu_maara': 1, 'arvostelut': [{'id': 1, 'elokuvan_id': 2, 'kayttaja_id': 1, 'arvosana': 5.0, 'kommentti': 'ihan ok leffa, ite ihan fiilasin'}]}]
        """

        # haetaan kayttäjätiedot tietokannasta
        kayttaja = self.cursor.execute( sql_komennot.valitse_kayttajatiedot_tietokannasta(), (kayttaja_id,) ).fetchone()

        if arvostelut:
            kayttajan_arvostelut = self.cursor.execute( sql_komennot.valitse_kayttajan_arvostelut_tietokannasta(), (kayttaja_id,) ).fetchall()

            arvostelut = []

            print(kayttajan_arvostelut)
            for arvostelu in kayttajan_arvostelut:
                arvostelut.append({'id':arvostelu[0], 'elokuvan_id':arvostelu[1], 'kayttaja_id':arvostelu[2], 'arvosana':arvostelu[3], 'kommentti':arvostelu[4]})
                

        kayttaja = {'nimi':kayttaja[0], 'arvostelu_maara':kayttaja[1], 'arvostelut':arvostelut}

        return [kayttaja]
    


    def lataa_elokuvat_tietokantaan(self, json_tiedoston_nimi:str) -> None:
        """
        Ottaa json tiedoston jossa on elokuvia, lataa elokuvat tietokantaan, ei palauta mitään

        Parametri:
            - json_tiedoston_nimi: json tiedoston nimi jossa elokuvat, tiedoston nimi tulee antaa str muodossa (muista ".json" loppu nimessä!)

        Esimerkki nimi:
            --> 'elokuvat.json'
        """

        try:
            # Luetaan tiedosto
            with open(json_tiedoston_nimi, "r", encoding="utf-8") as tiedosto:
                elokuvat = json.load(tiedosto)

                # Käydään elokuvat läpi yksi kerrallaan
                for elokuva in elokuvat:
                    
                    # Lisätään elokuva tietokantaan
                    self.cursor.execute( sql_komennot.lisää_elokuva_tietokantaan(), (elokuva["id"], elokuva["julkaisu_vuosi"], elokuva["nimi"], 
                        elokuva["keskiarvo"], elokuva["juoni"]) )

            self.conn.commit() # Tallentaa mahdolliset muutokset
            print("Elokuvat ladattu tietokantaan!")

        # Mahdollisen virheen korjaus
        except Exception as e:
            print(f"Virhe elokuvien lataamisessa: {e}")



    def hae_elokuvia(self, hakusana:str='') -> list[dict]:
        """
        Hakee elokuvia tietokannasta hakusanan perusteella, palauttaa listan jonka sisällä leffat dict muodossa -> [ { elokuva }, { elokuva } ... ]

        Parametri:
            - hakusana: Hakusana voi olla elokuvan nimi tai vuosi str muodossa

        Elokuva Dict:
            - id (int)
            - nimi (str)
            - julkaisu_vuosi (int)
            - keskiarvo (float)
            - juoni (str)
            - arvostelu_maara (int)
        """

        # Etsii elokuvat tietokannasta hakusanan perusteella
        self.cursor.execute( sql_komennot.etsi_elokuvia_tietokannasta(), ([hakusana,] * 2) ) # "* 2" antaa hakusanan 2 kertaa koska sql lauseella on 2 parametria

        # Käy läpi elokuvat 1x1, laittaa elokuvan tiedot dict muotoo, palauttaa list dict:ejä
        return [ {'id':elokuva[0], 'nimi':elokuva[1], 'julkaisu_vuosi':elokuva[2], 'keskiarvo':elokuva[3], 'juoni':elokuva[4], 'arvostelu_maara':elokuva[5]}
                    for elokuva in self.cursor.fetchall() ]


    
    def muuta_kayttajanimea(self, kayttaja_id:int, uusi_kayttajanimi:str) -> None or NameError:
        """
        Ottaa kaäyytäjän id:n ja uuden käyttäjänimen, jos käyttäjänimi on varattu niin palauttaa NameError, jos kaikki menee oikein niin päivittää uuden käyttäjänimen tietokantaan

        Parametrit:
            - kayttaja_id: Kayttäjän id jonka nimeä halutaan muokata (int muodossa)
            - uusi_kayttajanimi: Uusi haluttu käyttäjänimi (str muodossa)
        """
        
        # Etsitään löytyykö nimi jo tietokannasta
        self.cursor.execute( sql_komennot.etsi_kayttaja_nimen_perusteella, (uusi_kayttajanimi,) )

        # Jos nimi löytyy niin palautetaan NameError
        if self.cursor.fetchall():
            raise NameError('Käyttäjänimi on varattu!')

        # Jos nimi ei löydy niin päivitetään uusi nimi tietokantaan
        self.cursor.execute( sql_komennot.paivita_kayttajanimi(), (uusi_kayttajanimi, kayttaja_id,) )

        self.conn.commit() # Tallentaa muutokset



    def poista_arvostelu(self, arvostelu_id:int) -> None or ValueError:
        """
        Poistaa arvostelun tietokannasta id:n perusteella, jos poistettavaa arvostelua ei löydy niin palauttaa ValueError

        Parametri:
            - arvostelu_id: Poistettavan arvostelun id (int muodossa)
        """

        # Tarkistaa onko arvostelua tietokannassa
        self.cursor.execute( sql_komennot.valitse_arvostelu_id_perusteella(), (arvostelu_id,) )
        
        # Jos arvostelua ei ole tietokannassa niin palautta ValueError
        if not self.cursor.fetchall():
            raise ValueError('Arvostelua ei löytynyt!')

        # Poistaa arvostelun tietokannasta
        self.cursor.execute( sql_komennot.poista_arvostelu(), (arvostelu_id,) )

        self.conn.commit() # Tallentaa muutokset



    def muokkaa_kommenttia(self, arvostelun_id:int, uusi_kommentti:str) -> None or ValueError:
        """
        Päivittää arvostelun kommentin id:n perusteella tietokantaan, jos id:tä ei löydy nii palauttaa ValueError
        
        Parametrit:
            - arvostelun_id: Arvostelun id jonka kommenttia halutaan muokata (int muodossa)
            - uusi_kommentti: Uusi kommentti joka päivitetään tietokantaan (str muodossa)
        """

        # Tarkistaa onko arvostelua tietokannassa
        self.cursor.execute( sql_komennot.valitse_arvostelu_id_perusteella(), (arvostelu_id,) )

        # Jos arvostelua ei ole tietokannassa niin palautta ValueError
        if not self.cursor.fetchall():
            raise ValueError('Arvostelua ei löytynyt!')

        # Päivittää uuden kommentin tietokantaan
        self.cursor.execute( sql_komennot.paivita_kommentti(), (uusi_kommentti, arvostelun_id,) )

        self.conn.commit() # Tallentaa muutokset



    def muuta_salasanaa(self, kayttaja_id:int, uusi_salasana:str) -> None or ValueError:
        """
        Päivittää salasanan tietokantaan käyttäjä id:n perusteella, jos id:tä ei löydy niin palauttaa ValueError
        
        Parametrit:
            - kayttaja_id: Käyttäjän id jonka salasanaa halutaan muokata (int muodossa)
            - uusi_salasana: Uusi salasana joka päivitetään tietokantaan (str muodossa)
        """

        # Tarkistaa onko kayttäjää olemassa
        self.cursor.execute( sql_komennot.valitse_kayttajatiedot_tietokannasta(), (kayttaja_id,) )

        # Jos käyttäjää ei ole niin palautetaan ValueError
        if not self.cursor.fetchall():
            raise ValueError('Käyttäjää ei löytynyt!')

        # Piilottaa salasanan "hash" muotoon
        uusi_salasana = hash_salasana(uusi_salasana)

        # Päivittää salasanan tietokantaan
        self.cursor.execute( sql_komennot.paivita_salasana(), (uusi_salasana, kayttaja_id,) )

        self.conn.commit() # Tallentaa muutokset




if __name__ == '__main__':
    yhteys = sql_yhteys()


    #print(yhteys.hae_elokuvia('täH'))

    #yhteys.lataa_elokuvat_tietokantaan('elokuvat.json')

    #yhteys.lisaa_kayttaja('heikki', 'pekka123')

    #print(hash_salasana('pekka123'))

    #print( yhteys.kirjaudu('pekka', 'pekka123' ) )

    #yhteys.lisaa_arvostelu(2, 5, 3, 'i love it')

    #yhteys.sulje_yhteys()

    #print( yhteys.kayttajan_tiedot(1, True) )

    yhteys.poista_arvostelu(200)

    pass
