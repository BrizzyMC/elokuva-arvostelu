import os
import scrypt
import sqlite3
import hashlib
import json

# Lisää käyttäjän nimi ja salasanan tietokantaan turvallisesti
def lisaa_kayttaja(nimi, salasana):
    hashed_salasana = hash_salasana(salasana)
    pointer = sqlite3.connect("database.db")
    nimet = pointer.execute("SELECT kayttaja_nimi FROM kayttajat")
    for i in nimet.fetchall():
        if i[0] == nimi:
            return f"Nimi on jo otettu"
    pointer.execute("INSERT INTO kayttajat (kayttaja_nimi, kayttaja_salasana) VALUES (?,?)",(nimi,hashed_salasana))
    pointer.commit()
    pointer.close()
    clear_terminal()
    print("Kayttaja lisätty")
    return hashed_salasana

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def kirjaudu(kayttaja_nimi, salasana):
    connect = sqlite3.connect("database.db")

    nimet = connect.execute(f"SELECT * FROM kayttajat WHERE kayttaja_nimi = '{kayttaja_nimi}'")
    nimet = nimet.fetchall()

def hash_salasana(salasana: str) -> bytes:
    salt = os.urandom(16)
    
    key = hashlib.scrypt(
        salasana.encode(), 
        salt=salt, 
        n=16384,  
        r=8,                
        p=1,                
        maxmem=0,          
        dklen=64            
    )
    return salt + key


def vahvista_salasana(kayttaja_nimi,salis):
    '''Katsoo onko kayttajan nimi ja salasan oikein
    Palauttaa False/str
    '''
    connect = sqlite3.connect("database.db")
    nimet = connect.execute(f"SELECT kayttaja_salasana FROM kayttajat WHERE kayttaja_nimi = '{kayttaja_nimi}'")
    connect.commit()
    nimet = nimet.fetchall()
    connect.close()

    if len(nimet) == 0:
        return False

    hashed_salis = nimet[0][0]
    salt = hashed_salis[:16]
    tallennettu_avain = hashed_salis[16:]
    avain = hashlib.scrypt(
        salis.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=64
    )

    return avain == tallennettu_avain

def lisaa_arvostelu(elokuva_id, arvosana, kayttaja_nimi, kommentti=""):
    '''
    Lisää elokuvalle arvostelu ja päivittää elokuvan keskiarvon sekä käyttäjän arvostelumäärän.
    Palauttaa True/False
    '''
    connect = sqlite3.connect("database.db")
    # Hakee keskiarvon ja arvostelujen määrän
    elokuva = connect.execute("SELECT keskiarvo, arvostelu_maara FROM elokuvat WHERE id = ?", (elokuva_id,)).fetchone()
    
    if not elokuva:
        print("Elokuvaa ei löytynyt")
        connect.close()
        return False
    
    vanha_keskiarvo = elokuva[0] if elokuva[0] else 0
    arvostelu_maara = elokuva[1] if elokuva[1] else 0
    
    uusi_arvostelu_maara = arvostelu_maara + 1
    uusi_keskiarvo = ((vanha_keskiarvo * arvostelu_maara) + arvosana) / uusi_arvostelu_maara
    
    # Päivittää elokuvan keskiarvon ja arvostelujen määrän
    connect.execute("UPDATE elokuvat SET keskiarvo = ?, arvostelu_maara = ? WHERE id = ?", (uusi_keskiarvo, uusi_arvostelu_maara, elokuva_id))
    
    # Lisää arvostelun
    connect.execute("INSERT INTO arvostelut (elokuva_id, kayttaja_nimi, arvosana, kommentti) VALUES (?, ?, ?, ?)", (elokuva_id, kayttaja_nimi, arvosana, kommentti))
    
    # Päivittää käyttäjän arvostelumäärän
    connect.execute("UPDATE kayttajat SET arvostelu_maara = arvostelu_maara + 1 WHERE kayttaja_nimi = ?", (kayttaja_nimi,))
    
    connect.commit()
    connect.close()
    print(f"Arvostelu lisätty. Uusi keskiarvo: {uusi_keskiarvo:.1f}")
    return True

def nayta_elokuvan_arvostelut(elokuva_id):
    '''
    Näyttää elokuvan kaikki arvostelut käyttäjien kanssa.
    Ei palauta mitään
    '''
    connect = sqlite3.connect("database.db")
    arvostelut = connect.execute("SELECT kayttaja_nimi, arvosana, kommentti FROM arvostelut WHERE elokuva_id = ?", (elokuva_id,)).fetchall()
    connect.close()
    
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

def nayta_kayttajan_tiedot(kayttaja_nimi):
    '''
    Näyttää käyttäjän tiedot ja arvostelumäärän.
    '''
    connect = sqlite3.connect("database.db")
    kayttaja = connect.execute("SELECT kayttaja_nimi, arvostelu_maara FROM kayttajat WHERE kayttaja_nimi = ?", (kayttaja_nimi,)).fetchone()
    
    if not kayttaja:
        print("Käyttäjää ei löytynyt")
        connect.close()
        return
    
    arvostelut = connect.execute("""
        SELECT e.nimi, a.arvosana, a.kommentti 
        FROM arvostelut a 
        JOIN elokuvat e ON a.elokuva_id = e.id 
        WHERE a.kayttaja_nimi = ?
    """, (kayttaja_nimi,)).fetchall()
    
    connect.close()
    
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

def lataa_elokuvat_tietokantaan():
    connect = sqlite3.connect("database.db")
    try:
        with open("elokuvat.json", "r", encoding="utf-8") as tiedosto:
            elokuvat = json.load(tiedosto)
            for elokuva in elokuvat:
                connect.execute("""
                INSERT OR IGNORE INTO elokuvat (id, julkaisu_vuosi, nimi, keskiarvo, juoni) 
                VALUES (?, ?, ?, ?, ?)
                """, (elokuva["id"], elokuva["julkaisu_vuosi"], elokuva["nimi"], 
                      elokuva["keskiarvo"], elokuva["juoni"]))
        connect.commit()
        print("Elokuvat ladattu tietokantaan!")
    except Exception as e:
        print(f"Virhe elokuvien lataamisessa: {e}")
    finally:
        connect.close()

def main():
    
    connect = sqlite3.connect("database.db")
    
    connect.execute('''CREATE TABLE IF NOT EXISTS elokuvat
                (id INTEGER PRIMARY KEY, 
                julkaisu_vuosi INTEGER,
                nimi VARCHAR, 
                keskiarvo FLOAT DEFAULT 0, 
                juoni TEXT,
                arvostelu_maara INTEGER DEFAULT 0)''')
    
    connect.execute('''CREATE TABLE IF NOT EXISTS arvostelut
                (id INTEGER PRIMARY KEY,
                elokuva_id INTEGER,
                kayttaja_nimi TEXT,
                arvosana FLOAT,
                kommentti TEXT,
                FOREIGN KEY(elokuva_id) REFERENCES elokuvat(id))''')
                
    connect.execute('''CREATE TABLE IF NOT EXISTS kayttajat
                (id INTEGER PRIMARY KEY,
                kayttaja_nimi NOT NULL,
                kayttaja_salasana NOT NULL,
                arvostelu_maara INTEGER DEFAULT 0)''')
    connect.commit()
    connect.close()
    
    # Lataa elokuvat JSON-tiedostosta jos niitä ei ole tietokannassa
    connect = sqlite3.connect("database.db")
    elokuva_count = connect.execute("SELECT COUNT(*) FROM elokuvat").fetchone()[0]
    connect.close()
    
    if elokuva_count == 0:
        lataa_elokuvat_tietokantaan()

    kirjautunut_kayttaja = None

    while True:
        print("\nVaihtoehdot:")
        print("1 - Lisää käyttäjä")
        print("2 - Kirjaudu")
        print("3 - Selaa elokuvia")
        print("4 - Jätä arvostelu")
        print("5 - Käyttäjätiedot")
        print("6 - Lopeta")
        
        try:
            valinta = int(input("Valinta: "))
        except ValueError:
            print("Syötä numero 1-6")
            continue
            
        if valinta == 1:
            kayttaja_nimi = str(input("Anna nimi: "))
            kayttaja_salasana = str(input("Anna salasana: "))
            tulos = lisaa_kayttaja(kayttaja_nimi, kayttaja_salasana)
            
            # Tarkistaa onko käyttjä onnistuneesti lisätty

            if isinstance(tulos, str):  # Jos palautus on string, se on virheviesti
                print(tulos)  # Näytetään virheviesti käyttäjälle
                print("Kokeile toista käyttäjänimeä.")
        
        elif valinta == 2:
            kayttaja_nimi = str(input("Nimi: "))
            salasana = str(input("Salasana: "))
            if vahvista_salasana(kayttaja_nimi, salasana):
                print("Kirjautunut")
                kirjautunut_kayttaja = kayttaja_nimi
            else:
                print("Käyttäjänimi tai salasana on väärin")
        
        elif valinta == 3:
            connect = sqlite3.connect("database.db")
            elokuvat = connect.execute("SELECT * FROM elokuvat")
            elokuva_lista = elokuvat.fetchall()
            connect.close()
            
            for elokuva in elokuva_lista:
                print(f"\nID: {elokuva[0]}")
                print(f"Nimi: {elokuva[2]}")
                print(f"Julkaisuvuosi: {elokuva[1]}")
                print(f"Keskiarvo: {elokuva[3] if elokuva[3] else 'Ei arvosteluja'}")
                print(f"Juoni: {elokuva[4]}")
            
            while True:
                nayta_arvostelut = input("\nHaluatko nähdä elokuvan arvostelut? (k/e): ")
                if nayta_arvostelut.lower() == 'k':
                    try:
                        elokuva_id = int(input("Anna elokuvan ID: "))
                        nayta_elokuvan_arvostelut(elokuva_id)
                    except ValueError:
                        print("Virheellinen elokuvan ID")
                elif nayta_arvostelut.lower() == "e":
                    clear_terminal()
                    break
        
        elif valinta == 4:
            if not kirjautunut_kayttaja:
                print("Sinun täytyy kirjautua sisään ennen arvostelun jättämistä")
                continue
                
            try:
                elokuva_id = int(input("Anna elokuvan ID: "))
                arvosana = float(input("Anna arvosana (1-5): "))
                if arvosana < 1 or arvosana > 5:
                    print("Arvosanan tulee olla välillä 1-5")
                    continue
                kommentti = input("Kommentti (valinnainen): ")
                lisaa_arvostelu(elokuva_id, arvosana, kirjautunut_kayttaja, kommentti)
            except ValueError:
                print("Virheellinen syöte")
        
        elif valinta == 5:
            if not kirjautunut_kayttaja:
                print("Sinun täytyy kirjautua sisään nähdäksesi käyttäjätiedot")
                continue
            
            nayta_kayttajan_tiedot(kirjautunut_kayttaja)
        
        elif valinta == 6:
            print("Suljetaan ohjelma...")
            break

        elif valinta not in [1,2,3,4,5,6]:
            clear_terminal()
            print("Valitse 1-6")


if __name__ == "__main__":
    main()



