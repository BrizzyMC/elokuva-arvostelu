"""
Tänne tiedostoon tulee sql yhteys ja sitä vahvasti käyttävät komennot (sql komennot eri tiedostossa!).
Tämä tiedosto pitää sisällään class olion joka luo, ylläpitää ja sulkee sql tietokanta yhteyden.

ESIMERKKI:
    # TODO JATKA KOMMENTTEJA!!!
"""


# * ------------------------------------------------------------------------------ *
# Kutsuu käytettävät kirjastot

import sqlite3      # Kutsuu sqlite3 kirjaston (joka on projektin pää tietokanta)

import json         # Kutsuu json kirjaston tiedoston lukua varten (vain "lataa_elokuvat_tietokantaan" käyttää kirjastoa)

import sql_komennot # Kutsuu sql komennot, sql_komennot tiedostosta

from apu_functiot import hash_salasana # Apu functio salasanan piilottamiseen

# * ------------------------------------------------------------------------------ *



# Määritetään tiedosto mitä tietokanta käyttää, muuttujan tulisi olla tietokannan nimi (EI SAA MUUTTUA OHJELMAN AIKANA) ja loppua ".db"
TIETOKANTA = 'database.db'



# Luodaan sqlite luokka joka hallinnoi kaikkea sql yhteyttä ohjelmassa (tiedoston loppukoodi luokan sisällä)
class sql_yhteys:
    """
    Luokka luo yhteyden ".db" tietokantaan käyttäen sqlite3 kirjastoa, jos tietokantaa ei ole olemassa niin se luodaan olion luonti prosessissa automaattisesti.

    Luokka hallinnoi elokuvia ja käyttäjie koskevaa koodia.

    #TODO KOMMENTOI KUN TIEDÄT LISÄÄ!!!
    """


    def __init__(self):
        """Yhdistaa SQLite tietokantaan, Luo taulukot (jos tarve), Palauttaa cursorin ja conn"""

        # Luo cursorin ja conn ( luo tietokanta tiedoston jos ei olemassa )
        self.conn   = sqlite3.connect(TIETOKANTA)
        self.cursor = self.conn.cursor()


        self.cursor.execute( sql_komennot.luo_arvostelu_taulukko() ) # Luo arvostelu taulukon tietokantaan (mikäli ei ole olemassa)

        self.cursor.execute( sql_komennot.luo_elokuva_taulukko()   ) # Luo elokuva taulukon tietokantaan   (mikäli ei ole olemassa)

        self.cursor.execute( sql_komennot.luo_kayttajat_taulukko() ) # Luo käyttäjät taulukon tietokantaan (mikäli ei ole olemassa)


        self.conn.commit() # Tallentaa mahdolliset muutokset



    def lisaa_kayttaja(self, nimi:str, salasana:str) -> bytes:
        """
        Functio lisää käyttäjän tietokantaan, palauttaa piilotetun salasanan bytes muodossa

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
                return "Nimi on jo otettu"
        
        # Lisää käyttäjän tietokantaan
        self.cursor.execute( sql_komennot.luo_kayttaja_tietokantaan(), (nimi, hashed_salasana) )

        # Tallentaa mahdolliset muutokset
        self.conn.commit()

        #clear_terminal()
        print("Kayttaja lisätty")

        return hashed_salasana
    


    def kirjaudu(self, kayttaja_nimi:str, salasana:str) -> int:
        """
        Functio etsii kirjautumis tietoihin vastaavan käyttäjän, palauttaa käyttäjän id:n int muodossa

        Parametrit:
            - kayttaja_nimi: käyttäjän nimi str muodossa
            - salasana: käyttäjän salasana str muodossa
        """
        # Etsii
        nimet = self.cursor.execute( sql_komennot.valitse_kayttaja_kirjautumistiedoilla_tietokannasta(), (kayttaja_nimi, salasana) )
        nimet = nimet.fetchall()

        return int(nimet)
    
    

    def lisaa_arvostelu(self, elokuva_id:int, arvosana:float, kayttaja_nimi:str, kommentti:str="") -> bool:
        """
        Lisää elokuvalle arvostelu ja päivittää elokuvan keskiarvon sekä käyttäjän arvostelumäärän.

        Palauttaa True/False

        Parametrit:
            - elokuva_id: arvosteltavan elokuvan id int muodossa
            - arvosana: annettava arvosana float muodossa (0-5)
            - kayttajan_nimi: Käyttäjän joka kommentoi nimi str muodossa
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
        self.cursor.execute( sql_komennot.lisaa_arvostelu_tietokantaan(), (elokuva_id, kayttaja_nimi, arvosana, kommentti) )
        
        # Päivittää käyttäjän arvostelumäärän
        self.cursor.execute( sql_komennot.paivita_kayttajan_arvostelumaara_tietokantaan(), (kayttaja_nimi,) )
        
        self.conn.commit() # Tallentaa mahdolliset muutokset

        print(f"Arvostelu lisätty. Uusi keskiarvo: {uusi_keskiarvo:.1f}")
        return True



    def elokuvan_arvostelut(self, elokuva_id:int) -> list:
        """
        Etsii elokuvien arvostelut id:n perusteella, palauttaa arvostelut listassa

        parametrit:
            - elokuva_id: Elokuvan id int muodossa, jonka arvostelut halutaan tietää
        """

        # hakee arvostelut
        arvostelut = self.cursor.execute( sql_komennot.valitse_nimi_kommentti_arvosana_tietokannasta(), (elokuva_id,) ).fetchall()

        return arvostelut
        
        # Kommentoitu koska ei tulosteta
        '''
        if not arvostelut:
            print("Elokuvalla ei ole vielä arvosteluja.")
            return

        print("\nArvostelut:")
            for arvostelu in arvostelut:
                kayttaja, arvosana, kommentti = arvostelu
                print(f"Käyttäjä: {kayttaja}")
                print(f"Arvosana: {arvosana}")
                if kommentti:
                    print(f"Kommentti: {kommentti}")
                print("-" * 30)
        '''
        
    

    def sulje_yhteys(self) -> None:
        """
        Sulkee sql yhteyden tietokantaan, ei palauta mitään

        Käytetään ohjelman lopussa tai sen sulkemisen yhteydessä
        """

        self.conn.close() # Sulkee sql yhteyden

    

    def kayttajan_tiedot(self, kayttaja_nimi:str) -> list:
        """
        Näyttää käyttäjän tiedot ja arvostelumäärän.
        """

        kayttaja = self.cursor.execute( sql_komennot.valitse_kayttajatiedot_tietokannasta(), (kayttaja_nimi,) ).fetchone()

        return kayttaja
        
        '''
        if not kayttaja:
            print("Käyttäjää ei löytynyt")
            return
        
        
        arvostelut = self.cursor.execute("""
            SELECT e.nimi, a.arvosana, a.kommentti 
            FROM arvostelut a 
            JOIN elokuvat e ON a.elokuva_id = e.id 
            WHERE a.kayttaja_nimi = ?
        """, (kayttaja_nimi,)).fetchall()
        
        
        print(f"\nKäyttäjä: {kayttaja[0]}")
        print(f"Arvosteluja jätetty: {kayttaja[1]}")
        
        if arvostelut:
            print("\nJätetyt arvostelut:")
            for arvostelu in arvostelut:
                elokuva_nimi, arvosana, kommentti = arvostelu
                print(f"Elokuva: {elokuva_nimi}")
                print(f"Arvosana: {arvosana}")
                if kommentti:
                    print(f"Kommentti: {kommentti}")
                print("-" * 30)
        '''
    


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



    def hae_elokuvia(self, hakusana:str) -> list:
        """
        Hakee elokuvia tietokannasta hakusanan perusteella, palauttaa listan jonka sisällä leffat dict muodossa -> [ { elokuva }, { elokuva } ... ]

        Parametri:
            - hakusana: Hakusana voi olla elokuvan nimi tai vuosi str muodossa

        Elokuva Dict:
            - id
            - nimi
            - julkaisu_vuosi
            - keskiarvo
            - juoni
            - arvostelu_maara
        """

        # Etsii elokuvat tietokannasta hakusanan perusteella
        self.cursor.execute( sql_komennot.etsi_elokuvia_tietokannasta(), ([hakusana,] * 2) ) # "* 2" antaa hakusanan 2 kertaa koska sql lauseella on 2 parametria

        # Käy läpi elokuvat 1x1, laittaa elokuvan tiedot dict muotoo, 
        return [ {'id':elokuva[0], 'nimi':elokuva[1], 'julkaisu_vuosi':elokuva[2], 'keskiarvo':elokuva[3], 'juoni':elokuva[4], 'arvostelu_maara':elokuva[5]}
                    for elokuva in self.cursor.fetchall() ]
        


if __name__ == '__main__':
    #yhteys = sql_yhteys()

    #yhteys.lataa_elokuvat_tietokantaan('elokuvat.json')

    #yhteys.lisaa_kayttaja('pekka', 'pekka123')

    #print(hash_salasana('pekka123'))

    #print( yhteys.kirjaudu('pekka', 'pekka123' ) )

    #yhteys.lisaa_arvostelu(2, 5, 'pekka', 'ihan ok leffa, ite ihan fiilasin')

    #yhteys.sulje_yhteys()

    pass
