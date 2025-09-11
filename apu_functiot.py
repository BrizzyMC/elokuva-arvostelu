"""
=================================================================

Nimi:       apu_functiot.py
kuvaus:     Tiedosto sisältää sekalaisia apufunctioita functioille
            Jotka sijaitsevat joissain toisissa tiedostoissa.

Tekiä:      Benjamin
Päivämäärä: 11.9.2025
Versio:     1.0

=================================================================
"""

import os       # TODO kirjoita kommentti
import hashlib  # hashlib salasanan piilottamiseen (hash_salasana)

def hash_salasana(salasana: str) -> bytes:
    """
    Apu functio salasanan piilottamiseen käyttäen hashlib kirjastoa, palauttaa piilotetun salasanan bytes muodossa

    parametri:
        salasana: piilotettava salasana str muodossa
    """
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


def vertaa_salasana(salasana: str, hashed_salasana: bytes) -> bool:
    """
    Vertailee annettua salasanaa ja tallennettua hashattua salasanaa.

    parametri:
        salasana: käyttäjän syöttämä salasana
        hashed: tallennettu hashattu salasana

    palauttaa:
        True jos salasanat ovat samat, muuten False
    """
    salt = hashed_salasana[:16]
    tallennettu_avain = hashed_salasana[16:]
    avain = hashlib.scrypt(
        salasana.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=64
    )

    return avain == tallennettu_avain
