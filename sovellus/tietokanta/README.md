# Tietokanta

Kansio pitää sisällään python tiedostot jotka kommunikoivat sql tietokannan kanssa. Kansiossa on myös "hash_salasana.py" jossa on salasanan piilottamis algorytmi.

_Kaikki **sqlite3** koodi sijaitsee "sql.py" tiedostossa!_

 ---

## Tietokanta Esimerkit
**Käyttäjät**
| Id                | Nimi     | Käyttäjän_Salasana | Arvostelu_Määrä |
| :---------------- | :------: | :----------------: | --------------: |
| 1                 |   Jaakko | *<hash...>*        | 2               |
| 2                 |   Pekka  | *<hash...>*        | 0               |
| 3                 |   Kalle  | *<hash...>*        | 1               |

**Elokuvat**
| Id                | Julkaisu_Vuosi  | Nimi            | Keskiarvo | Juoni           | Arvostelu_Määrä | Genret | Kuva |
| :---------------- | :-------------: | :-------------: | :-------: | :-------------: | :-------------: | :----: | ---: |
| 1                 |   1999          |   Matrix        | 4.4       | Tietokonehak... | 4               | scifi  | link |
| 2                 |   1977          |   Tähtien sota  | 4.6       | Luke Skywalk... | 8               | scifi  | link |
| 3                 |   1997          |   Titanic       | 4.2       | Aristokraatt... | 3               | Rom... | link |

**Arvostelut**
| Id                | Elokuva_Id | Käyttäjä_id | Arvosana | Kommentti |
| :---------------- | :------: | :-----------: | :------: |---------: |
| 1                 |   1      | 1             | 4.5      | Elokuv... |    
| 2                 |   2      | 2             | 3.2      | Olisin... |
| 3                 |   3      | 3             | 2.7      | Muuten... |

---

## Functiot

```md
Lisää arvostelu (elokuvan_id:int, arvosana:float, kommentti:str) -> None
  ⤷Valitse elokuva id:n perusteella
    ⤷Valitse arvosana
      ⤷Kirjoita kommentti
        ⤷Lisätään arvostelu tietokantaan
```

```md
Näytä käyttäjätiedot (id:int) -> list[dict]
  ⤷Hakee käyttäjätiedot tietokannasta (id, nimi, arvioiden määrä, mah: kaikki käyttäjän arvostelut)
    ⤷Palauttaa seuraavat tiedot dict muodossa listan sisällä -> list[dict]
```

```md
Muuta käyttäjänimeä (käyttäjä_id:int, nimi:str) -> mah: NameError
  ⤷Käyttäjä antaa uuden nimen
    ⤷Onko nimi jo käytössä? Jos niin palautetaan NameError
    ⤷Uusi nimi päivitetään tietokantaan
```

```md
Lisää käyttäjä (nimi:str, salasana:str) -> int(id), mah: NameError
  ⤷Piilottaa salasanan "hash"
    ⤷Tarkistaa onko nimi vapaa, jos ei niin palauttaa NameError
    ⤷Lisätään käyttäjä tietokantaan
```

```md
Kirjaudu (nimi:str, salasana:str) -> int(id), mah: TypeError
  ⤷Tarkista onko käyttäjätiedot oikein
    ⤷Jos väärin niin palauttaa TypeError
    ⤷Jos oikein niin palauttaa käyttäjän int(id)
```

```md
Listaa elokuvat (hakusana:str) -> list[dict]
  ⤷Tyhjä str: Palauttaa kaikki elokuvat
  ⤷Hakusana: Palauttaa kaikki hakusanalla löytyvät elokuvat, hakusana voi olla nimi tai vuosi
  TODO: lisätään genre
```

```md
Muuta salasanaa (käyttäjä_id:int, uusi_salasana:str) -> None
  ⤷Uusi salasana "hash" muotoon
    ⤷Päivitetään uusi salasana tietokantaan
```

```md
Poista arvostelu (arvostelun_id:int) -> mah: ValueError
  ⤷Valitsee poistettavan arvosanan id:n perusteella
    ⤷Jos ei ole olemassa niin palauttaa ValueError
    ⤷Poistaa arvostelun tietokannasta
```

```md
Muokkaa kommenttia (kommentin_id:int, uusi_kommentti:str) -> mah: ValueError
  ⤷Valitse kommentti id:n perusteella
    ⤷Jos ei löydy niin ValueError
    ⤷Päivitä kommentti tietokantaan
```
