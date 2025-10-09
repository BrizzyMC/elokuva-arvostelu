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

---

### Käyttö ja Käynnistys


1. **Asenna kirjastot** - ```tarkista_kirjastot.py```
2. **Käynnistä flask palvelin** - ```palvelin.py```
3. **Yhdistä flask palvelimelle selaimessa** - ```127.0.0.1:8000``` _(oletus)_


---

### Ohjelmassa käytetyt kirjastot

_Jos sinulla ei ole python asennettu niin asenna se [täältä](https://www.python.org/downloads/)!_

**HashLib**
```
pip install hashlib
```

**Flask**
```
pip install flask
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
> - [X] **LUO MAIN LOOP** <mark>Benjamin</mark>
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
> - [X] **Luo uudet taulukot** _jossa elokuvilla kuvat ja genret_ <mark>Benjamin</mark>
> - [X] Luo input valikko _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Kirjaudu sisään) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Lisää arvostelu) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Näytä käyttäjätiedot) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Muuta käyttäjänimeä) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Lisää käyttäjä) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Listaa/hae elokuvat) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Muuta salasana) _"terminaali.py"_ <mark>Vili</mark>
> - [X] Luo tulostukset ja inputit (Muokkaa kommenttia) _"terminaali.py"_ <mark>Vili</mark>
> - [X] **Luo Flask yhteys** _"flask.py"_ <mark>Vili</mark>
> - [X] **Luo testi Flask sivut** _"flask.py"_ <mark>Vili</mark>

### Perjantai 26.9
> - [X] **Suunnittele nettisivut** _(figma:lla?)_ <mark>Benjamin</mark>
> - [X] TODO Flask kirjastolle ja nettisivulle <mark></mark>

### Maanatai 29.9
> - [X] kirjautumis/käyttäjänluonti sivu  <mark>Vili</mark>
> - [X] kotisivu <mark>Vili</mark>
> - [X] Haku sivu <mark>Benjamin</mark>

### Tiistai 30.9
Tehdään edelliset valmiiksi

### Keskiviikko 1.10
> - [X] Elokuva tiedot/arvostelut sivu <mark>Vili</mark>

### Torstai 2.10
> - [X] Käyttäjätietojen muokkaus sivu <mark>Vili</mark>

### Perjantai 3.10
Ohjelman katsaus

---

## Diagrammi

<img width="1155" height="651" alt="image" src="https://github.com/user-attachments/assets/095055e1-37ac-4975-a4c3-85af297bfeca" />

---

## Tiedostorakenne

```md
.
└── elokuva-arvostelu/
    ├── .gitignore
    ├── README.md
    ├── __main__.py
    ├── .env
    ├── palvelin.py
    ├── database.db
    ├── elokuvat.json
    ├── sovellus/
    │   ├── __init__.py
    │   ├── rajapinta.py
    │   ├── sivut.py
    │   └── tietokanta/
    │       ├── hash_salasana.py
    │       ├── sql_komennot.py
    │       └── sql.py
    ├── templates/
    │   ├── koti.html
    │   └── # html tiedostot
    └── static/
        └── # css & js
```

> **sql.py**

Tiedosto pitää sisällään sqlite3 luokan jossa luodaan sqlite3 yhteys tietokantaan, tiedosto pitää myös sisällään kaikki functiot jotka kommunikoivat tietokannan kanssa tai käyttävät sitä.

> **sql_komennot.py**

Tiedostossa on ohjelman kaikki sql komennot, tämä tarkoittaa sitä että "_sql.py_" kutsuu sql käskyt "_sql_komennot_" tiedostosta. Tiedosto siis ylläpitää kaikkia sql käskyjä ja niitä pystyy helposti muokasta sieltä.

> **palvelin.py**

Tiedosto pitää sisällään flask palvelimen, tiedostossa luodaan flask olio, annetaan sille asetukset ja käynistetään palvelin.

> **terminaali.py**

Tässä tiedostossa on kaikki tulostus ja input functioit jota ohjelman terminaali (beta) versio tarvitsee ennen kun saamme sen verkko muotoon (main.py saattaa pitää sisällään myös joitain tulostuksia ja input:teja.

> **hash_salasana.py**

Nimensä mukaan tämä tiedosto pitää sisällään vain salasanan piilottamiseen ja taas lukemiseen tarkoitettu functio.

> **database.db**

Tähän tietokanta tiedostoon tallennetaan kaikki ohjelman data, se tulee kommunikoimaan ohjelman kanssa sqlite3 yhteyden kautta. Tiedosto pitää sisällään kaikki kolme taulua ja niiden datan.

> **_ _init _ _.py**

Tiedosto rekistöröi rajapinta ja sivut blueprintit.

> **sivut.py**

Tiedosto pitää sisällään functiot ja reitit sivujen lataamiseen (html sivujen).

> **rajapinta.py**

Tiedosto pitää sisällään functiot jotka kommunikoivat tietokannan, nettisivujen ja palvelimen välissä.

> **asetukset.py**

Tiedosto pitää sisällään flask palvelimen asetukset helposti muokattavassa muodossa.

---


