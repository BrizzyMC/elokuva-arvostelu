/* Tiedostossa on functio salasanan näyttämiseen ja sen piilottamiseen */


/**
 * 
 * @param {*} id - id jonka kanssa nappi kommunikoi (string muodossa).
 */

function nayta_salasana(id) {

    nappi = document.getElementById(id);
    if (nappi.type == "password") {
        nappi.type = "text";
    }
    else {
        nappi.type = "password";
    }
}
