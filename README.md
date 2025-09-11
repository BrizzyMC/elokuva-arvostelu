# Elokuva Arvostelu Työkalu

> IMDb harjoitus ohjelma, README pitää sisällään lyhyen kuvauksen ohjelmasta, ohjelman logiikasta, ohjelmassa käytetyistä kirjastoista, yhteensopivuudesta, functioista ja tietorakenteesta.

### Ohjelmasta

Ohjelma käyttää **Pythonia** ja on kirjoitettu _Python 3.13.7 64-bit_ versiolla.

kaikki projectin koodi tulisi toimia uusimmilla **Windows** ja **Linux** versioilla, mikäli virheiä löytyy tai jokin ei toimi niin avaathan ihmeessä uuden "Issue":n ja kerro mikä meni vikaan, tulemme korjaamaan sen niin pian kun vain suinkin kykenemme.

Ohjelma pitää yllä elokuva ja käyttäjä tietokantaa sqlite yhteyttä käyttäen.
Ohjelmalla voi ylläpitää, muokata ja poistaa arvosteluja, kommentteja, käyttäjiä ja elokuvia.

Tulevaisuudessa ohjelman tulisi toimia webbi pohjaisena käyttäen pythonin _Flask_ kirjastoa, tästä lisää myöhemmin.

Projecti jäljittelee ja käyttää inspiraationa [Imdb](https://www.imdb.com/) sivua, emme toki kopioi sieltä mitään suoraan ja tämän projectin tarkoitus ei ole loukata tekiänoikeuksia, ohjelma on tehty vain harjoitusmielessä kahden opiskelian kesken.

Ohjlema suoritetaan käynnistämällä "_main.py_" tiedosto, tämä aloittaa pääloopin (main loop) jossa ohjlema pyörii. HUOM: "_main.py_" tulee avata pythonilla, avatessa muista tarkistaa että sinulla on [uusin Python versio](https://www.python.org/downloads/) käytössä! Mikäli avatessa tai ohjelman kulussa koituu ongelmia niin tarkista että **Python** versiosi on ajan tasalla!

Tietokannassa käytetty elokuvalista on luotu käyttäen [ChatGPT](https://fi.wikipedia.org/wiki/ChatGPT):tä!

...

---

### Ohjelmassa käytetyt kirjastot

Kaikki kirjastot pitäisi tulla pythonin mukanan sitä asentaessa!

_Jos sinulla ei ole python asennettu niin asenna se [täältä](https://www.python.org/downloads/)!_


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

## TODO:

**HUOM:** _Tummemmalla tekstillä on korkeampi prioriteetti!_

Todo:n aikataulutus [täällä](https://docs.google.com/spreadsheets/d/1DR5zW9wFk8KuKETYkIi0l3o9yxAkqSImYfiwekOqQYw/edit?usp=sharing)! ⏰

> - [X] **Lisää Projecti GitHubiin** <mark>Benjamin</mark>
> - [X] **Luo Tiedostorakenne** <mark>Vili</mark>
> - [X] **Kirjoita TODO GitHubiin** <mark>Vili</mark>
> - [X] **TODO:N aikataulutus** <mark>Vili & Benjamin</mark>
> - [X] **TARKASTA VALMIIT FUNCTIOT** <mark>Vili</mark>
> - [ ] **LUO MAIN LOOP** <mark>Benjamin</mark>
> - [X] **Kirjaudu sisään** _"sql.py"_ <mark>Benjamin</mark>
> - [X] **Lisää arvostelu** _"sql.py"_ <mark></mark>
> - [X] **Näytä käyttäjätiedot** _"sql.py"_ <mark></mark>
> - [X] **Muuta käyttäjänimeä** _"sql.py"_ <mark>Vili</mark>
> - [X] **Lisää käyttäjä** _"sql.py"_ <mark></mark>
> - [X] **Listaa/hae elokuvat** _"sql.py"_ <mark>Vili</mark>
> - [X] **Lataa elokuvat tietokantaan** _"sql.py"_ <mark></mark>
> - [X] **Muuta salasana** _"sql.py"_ <mark></mark>
> - [X] **Poista arvostelu** _"sql.py"_ <mark>Vili</mark>
> - [X] **Muokkaa kommenttia** _"sql.py"_ <mark>Vili</mark>
> - [ ] **Luo uudet taulukot** _jossa elokuvilla kuvat ja genret_ <mark></mark>
> - [X] Luo input valikko _"terminaali.py"_ <mark></mark>
> - [X] Luo tulostukset ja inputit (Kirjaudu sisään) _"terminaali.py"_ <mark></mark>
> - [ ] Luo tulostukset ja inputit (Lisää arvostelu) _"terminaali.py"_ <mark></mark>
> - [X] Luo tulostukset ja inputit (Näytä käyttäjätiedot) _"terminaali.py"_ <mark></mark>
> - [ ] Luo tulostukset ja inputit (Muuta käyttäjänimeä) _"terminaali.py"_ <mark></mark>
> - [X] Luo tulostukset ja inputit (Lisää käyttäjä) _"terminaali.py"_ <mark></mark>
> - [X] Luo tulostukset ja inputit (Listaa/hae elokuvat) _"terminaali.py"_ <mark></mark>
> - [ ] Luo tulostukset ja inputit (Muuta salasana) _"terminaali.py"_ <mark></mark>
> - [ ] Luo tulostukset ja inputit (Muokkaa kommenttia) _"terminaali.py"_ <mark></mark>
> - [ ] ~~Luo Flask yhteys _"Flask.py"_ <mark></mark>~~
> - [ ] ~~Luo Verkkosivut (avaa enemmän tulevaisuudessa) <mark></mark>~~
> - [ ] ~~Laajenna TODO Flask kirjastolle ja nettisivulle <mark></mark>~~

---

## Diagrammi

<img width="1155" height="651" alt="image" src="https://github.com/user-attachments/assets/095055e1-37ac-4975-a4c3-85af297bfeca" />

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
| 1                 |   1      | 1             | 4.5      | Elokuv... |    
| 2                 |   2      | 2             | 3.2      | Olisin... |
| 3                 |   3      | 3             | 2.7      | Muuten... |

---

## Tiedostorakenne

> **sql.py**

Tiedosto pitää sisällään sqlite3 luokan jossa luodaan sqlite3 yhteys tietokantaan, tiedosto pitää myös sisällään kaikki functiot jotka kommunikoivat tietokannan kanssa tai käyttävät sitä.

> **sql_komennot.py**

Tiedostossa on ohjelman kaikki sql komennot, tämä tarkoittaa sitä että "_sql.py_" kutsuu sql käskyt "_sql_komennot_" tiedostosta. Tiedosto siis ylläpitää kaikkia sql käskyjä ja niitä pystyy helposti muokasta sieltä.

> **main.py**

Tiedosto pitää sisällään ohjelman pääsilmukan (main loop), tässä silmukassa on kutsuttu kaikki ohjelman toiminnan kannalta tärkeät komponentit kasaan ja luotu niinsanotusti ohjelman sydän.

> **terminaali.py**

Tässä tiedostossa on kaikki tulostus ja input functioit jota ohjelman terminaali (beta) versio tarvitsee ennen kun saamme sen verkko muotoon (main.py saattaa pitää sisällään myös joitain tulostuksia ja input:teja.

> **apu_functiot.py**

Nimensä mukaan tämä tiedosto pitää sisällään vain functioita jotka on tarkoitettu avustamaan joitain toisia olennaisia functioita. Esimerkiski tiedostossa on functioit salasanan piilottaniseen yms.

> **database.db**

Tähän tietokanta tiedostoon tallennetaan kaikki ohjelman data, se tulee kommunikoimaan ohjelman kanssa sqlite3 yhteyden kautta. Tiedosto pitää sisällään kaikki kolme taulua ja niiden datan.

---

_Ohjelmaan on tulossa Flask webbipohjainen käyttöjärjestelmä, emme ole vielä suunnitelleet sitä liikkaa ja tämän takia sille ei löydy vielä functioita ja tiedostoja yms tästä README:estä. Flask käyttöjärjestelmä tulee silti käyttämään samaa logiikkaa kun tämänhetkinen versio ja noudattaa samaa diagrammi suunitelmaa. Tämä versio on tosin odotettavissa jo lähitulevaisuudessa!_

