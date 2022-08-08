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
                LIMIT 20""")
    return template('strelci.html', strelci=cur)

@get('/podajalci')
def podajalci():
    cur.execute("""SELECT oseba.ime,oseba.priimek, count(podajalec),oseba.ekipa from goli
                LEFT JOIN oseba ON oseba.emso = goli.podajalec
                GROUP BY oseba.ime,oseba.priimek,oseba.ekipa
                ORDER BY count(podajalec) DESC
                LIMIT 20""")
    return template('podajalci.html', podajalci=cur)



psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

run(host='localhost', port=8080, reloader=True)




