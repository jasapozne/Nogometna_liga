from bottleext import *
import sqlite3
#import auth_public as auth
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from auth import *

# KONFIGURACIJA 
baza_datoteka = "sem2022_jasap"

# Odkomentiraj, če želiš sporočila o napakah
debug(True)









napakaSporocilo = None 
def nastaviSporocilo(sporocilo = None):
    global napakaSporocilo
    staro = napakaSporocilo
    napakaSporocilo = sporocilo
    return staro


####UPORABNIKI
@get('/prijava')
def prijava_get():
    return template('prijava.html')
 
#@post("/prijava")
#def prijava_post():
#    emso = request.forms.get("emso")
#    uporabnisko_ime = request.forms.get("uporabnisko_ime")
#    geslo = request.forms.get("geslo")
#    ponovno_geslo = request.froms.get("geslo2") 
#    uporabnik = cur.execute("""SELECT * FROM oseba WHERE emso = ? """)

     
     


@get('/')
def index():
    return template('index.html') #index=cur

@get('/ekipa')
def ekipa():
    cur.execute("""SELECT ime,stadion,mesto from ekipa""")
    return template('ekipa.html', ekipa=cur)

@get('/goli')
def goli():
    cur.execute("""SELECT tekma.domaca_ekipa, tekma.tuja_ekipa,oseba.ime,oseba.priimek, podaja.ime,podaja.priimek,oseba.ekipa from goli
                    JOIN oseba ON oseba.emso = goli.strelec
                    JOIN oseba AS podaja ON podaja.emso = goli.podajalec 
                    JOIN tekma ON tekma.id_tekme = goli.id_tekme
                    """)
    return template('goli.html', goli=cur)

@get('/igralec')
def igralec():
    cur.execute("""SELECT oseba.ime, oseba.priimek, pozicija,visina,teza,zacetek_pogodbe,konec_pogodbe,vrednost, oseba.ekipa from igralec
                    LEFT JOIN oseba ON oseba.emso = igralec.emso""")
    return template('igralec.html', igralec=cur)

@get('/oseba')
def oseba():
    cur.execute("""SELECT ime,priimek,rojstni_dan,ekipa from oseba""")
    return template('oseba.html', oseba=cur)

@get('/tekma')
def tekma():
    cur.execute("""SELECT id_tekme,domaca_ekipa,tuja_ekipa,goli_domace,goli_tuje from tekma""")
    return template('tekma.html', tekma=cur)

@get('/zaposlen')
def zaposlen():
    cur.execute("""SELECT oseba.ime, oseba.priimek,delovno_mesto,placa,oseba.ekipa from zaposlen
                    LEFT JOIN oseba ON oseba.emso = zaposlen.emso""")
    return template('zaposlen.html', zaposlen=cur)


@get('/strelci')
def strelci():
    cur.execute("""SELECT oseba.ime,oseba.priimek, count(strelec),oseba.ekipa from goli
                LEFT JOIN oseba ON oseba.emso = goli.strelec
                GROUP BY oseba.ime,oseba.priimek,oseba.ekipa
                ORDER BY count(strelec) DESC
                """)
    return template('strelci.html', strelci=cur)

@get('/podajalci')
def podajalci():
    cur.execute("""SELECT oseba.ime,oseba.priimek, count(podajalec),oseba.ekipa from goli
                LEFT JOIN oseba ON oseba.emso = goli.podajalec
                GROUP BY oseba.ime,oseba.priimek,oseba.ekipa
                ORDER BY count(podajalec) DESC
                """)
    return template('podajalci.html', podajalci=cur)

@get('/lestvica')
def lestvica():
    
    cur.execute(""" 
    DROP VIEW IF EXISTS domaca_lestvica;
    DROP VIEW IF EXISTS gostujoca_lestvica;

    CREATE VIEW domaca_lestvica AS
    SELECT domaca_ekipa AS ekipa, sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END)+ sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) + sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END)
    AS tekme,sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END) AS zmage, sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS remi,
    sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS porazi, sum(CASE WHEN goli_domace > goli_tuje THEN 3 ELSE 0 END)+sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS tocke 
    FROM tekma
    GROUP BY domaca_ekipa;
                
    CREATE VIEW gostujoca_lestvica AS
    SELECT tuja_ekipa AS ekipa, sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END)+ sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) + sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS tekme,
    sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS zmage, sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS remi,
    sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END) AS porazi,
    sum(CASE WHEN goli_domace < goli_tuje THEN 3 ELSE 0 END)+sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS tocke FROM tekma
    GROUP BY tuja_ekipa;
    
   SELECT domaca_lestvica.ekipa,sum(domaca_lestvica.tekme)+sum(gostujoca_lestvica.tekme),
   sum(domaca_lestvica.zmage)+sum(gostujoca_lestvica.zmage),sum(domaca_lestvica.remi)+sum(gostujoca_lestvica.remi),
   sum(domaca_lestvica.porazi)+sum(gostujoca_lestvica.porazi),sum(domaca_lestvica.tocke) +sum(gostujoca_lestvica.tocke)
   FROM domaca_lestvica
   JOIN gostujoca_lestvica ON domaca_lestvica.ekipa = gostujoca_lestvica.ekipa
   GROUP BY domaca_lestvica.ekipa,domaca_lestvica.tocke,gostujoca_lestvica.tocke
   ORDER BY domaca_lestvica.tocke+gostujoca_lestvica.tocke  DESC;

    """)
    return template('lestvica.html', lestvica=cur)





psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

run(host='localhost', port=8080, reloader=True)




