"""
Tiedosto sisältää sekalaisia apu functioita
# TODO LISÄÄ KOMMENTTIA

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

