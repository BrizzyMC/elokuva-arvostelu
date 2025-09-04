# Elokuva Arvostelu Työkalu

### Ohjelmasta

Ohjlema käyttää kielenä _Python 3.13.7 64-bit_ versiota

Ohjelma pitää yllä elokuva ja käyttäjä tietokantaa sqlite yhteyttä käyttäen.
Ohjelmalla voi ylläpitää, muokata ja poistaa arvosteluja, kommentteja, käyttäjiä ja elokuvia.

...

---

### Ohjelmassa käytetyt kirjastot

Kaikki kirjastot pitäisi tulloa pythonin mukanan sitä asentaessa!

**OS**
```
pip install os-sys
```

**Sqlite3**
```
pip install sqlite3
```

**HashLib**
```
pip install hashlib
```

**Json**
```
pip install json
```

---

### TODO:

> - Luo main loop "main.py"
> - Kirjaudu sisään "sql.py"
> - Lisää arvostelu "sql.py"
> - Näytä käyttäjätiedot "sql.py"
> - Muuta käyttäjänimeä "sql.py"
> - Lisää käyttäjä "sql.py"
> - Listaa elokuvat "sql.py"
> - Muuta salasana "sql.py"
> - Poista arvostelu "sql.py"
> - Muokkaa kommenttia "sql.py"
> - Luo input valikko "terminaali.py"
> - Luo uusi tietokanta jossa elokuvilla kuvat ja genret
> - Luo tulostukset ja inputut (Kirjaudu sisään) "terminaali.py"
> - Luo tulostukset ja inputut (Lisää arvostelu) "terminaali.py"
> - Luo tulostukset ja inputut (Näytä käyttäjätiedot) "terminaali.py"
> - Luo tulostukset ja inputut (Muuta käyttäjänimeä) "terminaali.py"
> - Luo tulostukset ja inputut (Lisää käyttäjä) "terminaali.py"
> - Luo tulostukset ja inputut (Listaa/hae elokuvat) "terminaali.py"
> - Luo tulostukset ja inputut (Muuta salasana) "terminaali.py"
> - Luo tulostukset ja inputut (Muokkaa kommenttia) "terminaali.py"

### Työnalla:

> - TARKASTA VALMIIT FUNCTIOT # Vili
> - LUO MAIN LOOP # Benjamin
> - 

### Valmis:

> -
> -
> -


## Diagrammi

<img width="1155" height="651" alt="image" src="https://github.com/user-attachments/assets/095055e1-37ac-4975-a4c3-85af297bfeca" />

---
## Functiot

```md
Lisää arvostelu (elokuvan_id:int, arvosana:float, kommentti.str) -> None
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
Muuta käyttäjänimeä (käyttäjä_id, nimi:str) -> mah: NameError
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
Muuta salasanaa (käyttäjä:id, uusi_salasana:str) -> None
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

---

## Tietokanta Esimerkit
**Käyttäjät**
| Id                | Nimi     | Käyttäjän_Salasana | Arvostelu_Määrä |
| :---------------- | :------: | :----------------: | --------------: |
| 1                 |   Jaakko | *<hash...>*        | 2               |
| 2                 |   Pekka  | *<hash...>*        | 0               |
| 3                 |   Kalle  | *<hash...>*        | 1               |

**Elokuvat**
| Id                | Julkaisu_Vuosi  | Nimi            | Keskiarvo | Juoni           | Arvostelu_Määrä |
| :---------------- | :-------------: | :-------------: | :-------: | :-------------: | --------------: |
| 1                 |   1999          |   Matrix        | 4.4       | Tietokonehak... | 4               |
| 2                 |   1977          |   Tähtien sota  | 4.6       | Luke Skywalk... | 8               |
| 3                 |   1997          |   Titanic       | 4.2       | Aristokraatt... | 3               |

**Arvostelut**
| Id                | Elokuva_Id | Käyttäjä_id | Arvosana | Kommentti |
| :---------------- | :------: | :-----------: | :------: |---------: |
| 1                 |   1      | 1             | 4.5      | Elokuv... |          |
| 2                 |   2      | 2             | 3.2      | Olisin... |
| 3                 |   3      | 3             | 2.7      | Muuten... |

---
