# Sovellus

Kansio sisältää Flask rajapinnan ja nettisivujen reitit.

---

### Logiikka

Rakenteen toiminta logiikka on seuraava, **rajapinta.py** pitää sisällään Flask functiot jotka jotka kommunikoivat nettisivujen kanssa. **sivut.py** pitää sisällään html sivujen url ohjauksen.
**init** rekistöröi rajapinnan ja sivujen blueprintit jotta ne on helppo kutsua palvelimen käyttöön.
