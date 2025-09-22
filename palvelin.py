"""
=================================================================

Nimi:       palvelin.py
kuvaus:     Tässä tiedostossa on flask palvelin, palvelin pitää
            sisällään flask nettisivut jotka kommunikoivat
            ohjelman sql koodin kanssa.

Tekiä:      Viljam Vänskä
Päivämäärä: 16.9.2025
Versio:     1.0

=================================================================
"""

from flask import Flask, redirect, url_for, request, render_template
from sql import sql_yhteys
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio.init_app(app)


# Muodostaa yhteyden sql tietokantaan
tietokanta = sql_yhteys()


# > ------------ [ Sivun Lataus Functiot ] ------------------------ <

# Aloitus sivu
@app.route('/')
def aloitus():
    return render_template('luo_kayttaja.html')

# Kirjautumis sivu
@app.route('/kirjaudu')
def kirjaudu_sisaan():
    return render_template('kirjaudu.html')

# Käyttäjän luonti sivu
@app.route('/luo_käyttäjä')
def uusi_kayttaja():
    return render_template('luo_kayttaja.html')

# kotisivu
@app.route('/koti/<nimi>')
def koti(nimi):
    return render_template('koti.html')




# > ------------ [ Toiminto Functiot ] ------------------------ <

@app.route('/createaccount', methods=['POST'])
def luo_kayttaja():
    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']
        try:
            print(tietokanta.lisaa_kayttaja(kayttaja, salasana))
            return redirect(url_for('koti', nimi=kayttaja))

        except NameError:
            return uusi_kayttaja()
        


@app.route('/login', methods=['POST'])
def kirjaudu():
    if request.method == 'POST':
        kayttaja = request.form['kayttaja']
        salasana = request.form['salasana']
        try:
            print(tietokanta.kirjaudu(kayttaja, salasana))
            return redirect(url_for('koti', nimi=kayttaja))

        except ValueError:
            return kirjaudu_sisaan()

        except TypeError:
            return kirjaudu_sisaan()



@app.route('/haku', methods=['POST'])
def hae():
    if request.method == 'POST':
        hakusana = request.form['hakusana']
        elokuvat = tietokanta.hae_elokuvia(hakusana)
        return elokuvat



@app.route('/kayttaja_tiedot', methods=['POST'])
def kayttaja_tiedot():
    if request.method == 'POST':
        kayttaja_id = request.form['kayttajatiedot']
        tiedot = tietokanta.kayttajan_tiedot(int(kayttaja_id))
        return tiedot



@app.route('/paivita_kayttajaa', methods=['POST'])
def paivita_nimi_salasana(kayttaja_id:int=1):
    if request.method == 'POST':
        print('here')
        uusi_nimi     = request.form['nimi']
        uusi_salasana = request.form['salasana']

        print(uusi_nimi, uusi_salasana)
        if uusi_nimi:
            tietokanta.muuta_kayttajanimea(kayttaja_id, uusi_nimi)
        if uusi_salasana:
            tietokanta.muuta_salasanaa(kayttaja_id, uusi_nimi)
        return uusi_nimi, uusi_salasana
    


            
        



if __name__ == '__main__':
    socketio.run(app, debug=True)
