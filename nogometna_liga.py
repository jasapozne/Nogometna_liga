from bottle import *
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
    cur.execute("""SELECT id_tekme,strelec,podajalec from goli""")
    return template('goli.html', goli=cur)

@get('/igralec')
def igralec():
    cur.execute("""SELECT pozicija,visina,teza,zacetek_pogodbe,konec_pogodbe,vrednost,emso from igralec""")
    return template('igralec.html', igralec=cur)

@get('/oseba')
def oseba():
    cur.execute("""SELECT emso,ime,priimek,rojstni_dan,ekipa from oseba""")
    return template('oseba.html', oseba=cur)

@get('/tekma')
def tekma():
    cur.execute("""SELECT id_tekme,domaca_ekipa,tuja_ekipa,goli_domace,goli_tuje from tekma""")
    return template('tekma.html', tekma=cur)

@get('/zaposlen')
def zaposlen():
    cur.execute("""SELECT delovno_mesto,placa,emso from zaposlen""")
    return template('zaposlen.html', zaposlen=cur)


psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

run(host='localhost', port=8080, reloader=True)




