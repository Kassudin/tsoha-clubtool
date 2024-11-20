# Joukkueen tapahtuma/ilmoittautumissovellus 

Suunnitelma:

Sovelluksessa näkyy joukkueen tulevia tapahtumia, joihin on mahdollista ilmoittautua. Jokainen käyttäjä on joko pelaaja tai valmentaja:  

- Pelaaja voi kirjautua sisään ja ulos sekä luoda uuden pelaajaprofiilin.
- Pelaajaprofiilin voi määrittää nimen, pelipaikan ja pelinumeron. 
- Pelaaja näkee sivulla tapahtumia aikajärjestyksessä. Pelaaja voi ilmoittautua niihin (In tai Out). Jos Out, pelaaja kirjoittaa syyn poissaololle. Pelaaja voi muuttaa ilmoittautumistaan ennen tapahtuman alkamista.
- Pelaaja voi painaa tapahtumasta, jolloin näytetään tapahtuman lisätiedot, sekä ketä tapahtumaan on ilmoittautunut.
- Valmentaja voi luoda uusia tapahtumia, muuttaa nykyisiä tapahtumia sekä poistaa tapahtumia. Valmentaja voi valita onko tapahtuma harjoitus/ottelu/muu.  
- Valmentaja valitsee tapahtumalle päivämäärän sekä kellonajan (esim. 17:00-19:00). Valmentaja voi kirjoittaa tapahtuman kuvaukseen lisätietoja tapahtumasta, kuten tapahtumapaikka, harjoitteet yms. Myös mahdollisuus lisätä kuvia harjoitteista.
- Valmentaja näkee, ketä on ilmoittautunut tapahtumaan. Valmentaja voi myös itse ilmoittautua tapahtumaan. Valmentaja näkyy erivärisenä pelaajille. 
- Valmentaja voi lisätä tapahtumaan joukkueen ulkopuolisia pelaajia sekä muuttaa pelaajien ilmoittautumisia. Ulkopuolinen pelaaja näkyy erivärisenä muille pelaajille.
- Valmentaja voi luoda tapahtumia, jotka näkyvät vain tietyille pelaajille (esim. Vain maalivahdeille).
- Valmenta voi lähettää ilmoituksia, jotka näkyvät erillisellä sivulla.

Sovelluksen nykytila:

- Pelaaja voi kirjautua sisään ja ulos sekä luoda uuden pelaajaprofiilin.
- Pelaajaprofiilin voi määrittää nimen, pelipaikan ja pelinumeron. 
- Pelaaja näkee sivulla tapahtumia aikajärjestyksessä. Pelaaja voi ilmoittautua niihin (In tai Out). Pelaaja voi kirjoittaa myös kommentin osaksi ilmoittautumistaan (esim. Jos OUT (kipeä))
- Pelaaja voi painaa tapahtumasta, jolloin näytetään tapahtuman lisätiedot, sekä ketä tapahtumaan on ilmoittautunut.
- Valmentaja voi luoda uusia tapahtumia, muuttaa nykyisiä tapahtumia sekä peruuttaa tapahtumia. Valmentaja voi valita onko tapahtuma harjoitus/ottelu/muu.  
- Valmentaja valitsee tapahtumalle päivämäärän sekä kellonajan (esim. 17:00-19:00). Valmentaja voi kirjoittaa tapahtuman kuvaukseen lisätietoja tapahtumasta, kuten tapahtumapaikka, harjoitteet yms.
- Valmentaja näkee, ketä on ilmoittautunut tapahtumaan. Valmentaja voi myös itse ilmoittautua tapahtumaan. Valmentaja näkyy erivärisenä pelaajille. 
- Valmentaja voi lisätä tapahtumaan joukkueen ulkopuolisia pelaajia. Ulkopuolinen pelaaja näkyy erivärisenä muille pelaajille.
- Valmentaja voi luoda tapahtumia, jotka näkyvät vain tietyille pelaajille (esim. Vain maalivahdeille).
- Valmenta voi lähettää ilmoituksia, jotka näkyvät erillisellä sivulla.

Sovelluksesta jätettiin pois:

Kuvien lisääminnen tapahtumiin, valmentajan mahdollisuus muuttaa muiden ilmoittautumisia sekä ilmoittautumisen sulkeutuminen. 
- Kuvien lisääminen tapahtumaan ei ollut mielekästä.
- Mielestäni valmentajan tehtävä ei ole muuttaa pelaajien ilmoittautumisia, vaan pelaajien täytyy tehdä se itse.
- Tässä toteutuksessa ei ollut järkevää luoda ilmoittautumisen sulkeutumista, koska sovellusta lähtökohtaisesti vain testataan, eikä tapahtumiin palata enää esim. seuraavana päivänä. Jos sovelluksen ottaisi käyttöön, voisi tämän toiminnallisuuden implementoida.

Ohjeet sovelluksen testaamiseen:

- Suorita komento:
  ```
  git clone git@github.com:Kassudin/tsoha-clubtool.git
  ```
  Tämä kloonaa sovelluksen etäreposition etäpalvelimelta paikalliseen koneeseen.
  
- Aktivoi virtuaaliypäristö komennoilla:
  ```
  $ python3 -m venv venv
  ```
  ```
  $ source venv/bin/activate
  ```
- Luo hakemistoon tiedosto .env, jonka sisältö on seuraava:
  - DATABASE_URL = "osoite tietokantaan" 
  - SECRET_KEY = "avainkoodi"
  - TEST_ENV = 'TRUE*
- Ps. Voit luoda salaisen avaimen kävetävästi python tulkilla:
   ``` 
  $ python3
  >>> import secrets
  >>> print (secrets.token_hex(16))
- Asenna sovelluksen riippuvuudet virtuaaliympäristöön:
  ```
  (venv) $ pip install -r requirements.txt
   ```
- Ohjaa tiedostossa schema.sql olevat komennot PostgreSQL-tulkille:
   ``` 
  (venv) $ psql > schema.sql
   ```
- Käynnistä sovellus komennolla:
   ```
  (venv) $ flask run
   ```


   


    
