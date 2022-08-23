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
@get('/registracija')
def registracija_get():
    return template('registracija.html')

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

###EKIPE

@get('/ekipa')
def ekipa():
    cur.execute("""SELECT ime,stadion,mesto FROM ekipa""")
    return template('ekipa.html', ekipa=cur)

@get('/ekipa_dodaj')
def ekipa_dodaj():
    return template('ekipa_dodaj.html')

@post('/ekipa_dodaj')
def ekipa_dodaj_post():
    ime = request.forms.ime
    mesto = request.forms.mesto
    stadion = request.forms.stadion
    cur.execute("""INSERT INTO ekipa (ime, mesto, stadion) VALUES (%s, %s, %s);""", (ime, mesto, stadion))
    conn.commit()
    redirect(url('ekipa'))

@get('/ekipa_uredi/<ime>')
def ekipa_uredi_get(ime):
    cur.execute("""SELECT * FROM ekipa """)
    ekipe = cur.fetchall()
    cur.execute(""" SELECT * FROM ekipa WHERE ime= %s""", (ime, ))
    ekipa = cur.fetchone()
    return template('ekipa_uredi.html', ekipa=ekipa, ekipe=ekipe)

@post('/ekipa_uredi/<ime>')
def ekipa_uredi_post(ime):
    cur.execute(""" SELECT * FROM ekipa WHERE ime= %s""", (ime, ))
    staro = cur.fetchone()
    ime = request.forms.novo_ime
    mesto = request.forms.mesto
    stadion = request.forms.stadion
    cur.execute("""UPDATE ekipa SET ime = %s, mesto = %s, stadion = %s WHERE ime = %s;""", (ime, mesto, stadion, staro[0]))
    redirect(url('ekipa'))


@post('/ekipa/odstrani/<ime>')
def ekipa_odstrani(ime): 
    try:
        cur.execute("DELETE FROM ekipa WHERE ime = %s", (ime, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Ekipe {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na to ekipo".format(ime))
    redirect(url('ekipa'))




###GOLI
@get('/goli')
def goli():
    cur.execute("""SELECT goli.id_gol, tekma.id_tekme, goli.strelec, goli.podajalec, tekma.domaca_ekipa, tekma.tuja_ekipa, oseba.ime, oseba.priimek, podaja.ime, podaja.priimek, oseba.ekipa FROM goli
                    JOIN oseba ON oseba.emso = goli.strelec
                    JOIN oseba AS podaja ON podaja.emso = goli.podajalec 
                    JOIN tekma ON tekma.id_tekme = goli.id_tekme
                    ORDER BY id_tekme DESC
                    """)
    return template('goli.html', goli=cur)

@get('/goli_dodaj')
def goli_dodaj():
    cur.execute("""SELECT id_tekme FROM tekma""")
    tekme = cur.fetchall()
    cur.execute("""SELECT igralec.emso, oseba.ime, oseba.priimek FROM igralec
                    JOIN oseba ON oseba.emso = igralec.emso""")
    igralci = cur.fetchall()
    return template('goli_dodaj.html', tekme=tekme, igralci=igralci)

@post('/goli_dodaj')
def goli_dodaj_post():
    id_gol = request.forms.id_gol
    id_tekme = request.forms.id_tekme
    strelec = request.forms.strelec
    podajalec = request.forms.podajalec
    cur.execute("""INSERT INTO goli (id_gol, id_tekme, strelec, podajalec) VALUES (%s, %s, %s, %s);""", (id_gol, id_tekme, strelec, podajalec))
    conn.commit()
    redirect(url('goli'))

@get('/goli_uredi/<id_gol>')
def goli_uredi_get(id_gol):
    cur.execute("""SELECT goli.id_gol, tekma.id_tekme, goli.strelec, goli.podajalec, tekma.domaca_ekipa, tekma.tuja_ekipa, oseba.ime, oseba.priimek, podaja.ime, podaja.priimek, oseba.ekipa FROM goli
                    JOIN oseba ON oseba.emso = goli.strelec
                    JOIN oseba AS podaja ON podaja.emso = goli.podajalec 
                    JOIN tekma ON tekma.id_tekme = goli.id_tekme
                    WHERE id_gol = %s""", (id_gol))
    gol = cur.fetchone()
    cur.execute("""SELECT id_tekme FROM tekma""")
    tekme = cur.fetchall()
    cur.execute("""SELECT igralec.emso, oseba.ime, oseba.priimek FROM igralec
                    JOIN oseba ON oseba.emso = igralec.emso""")
    igralci = cur.fetchall()   
    return template('goli_uredi.html', gol=gol, tekme=tekme, igralci=igralci)

@post('/goli_uredi/<id_gol>')
def goli_uredi_post(id_gol):
    id_tekme = request.forms.id_tekme
    strelec = request.forms.strelec
    podajalec = request.forms.podajalec
    cur.execute("""UPDATE goli SET id_tekme = %s, strelec = %s, podajalec = %s WHERE id_gol = %s;""", (id_tekme, strelec, podajalec, id_gol))
    redirect(url('goli'))


@post('/goli/odstrani/<id_gol>')
def goli_odstrani(id_gol): 
    try:
        cur.execute("DELETE FROM goli WHERE id_gol = %s", (id_gol))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Gola {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na ta gol".format(id_gol))
    redirect(url('goli'))



###IGRALEC
@get('/igralec')
def igralec():
    cur.execute("""SELECT oseba.emso, oseba.ime, oseba.priimek, pozicija,visina,teza,zacetek_pogodbe,konec_pogodbe,vrednost, oseba.ekipa from igralec
                    LEFT JOIN oseba ON oseba.emso = igralec.emso""")
    return template('igralec.html', igralec=cur)

@get('/igralec_dodaj')
def igralec_dodaj():
    cur.execute("""SELECT emso FROM oseba""")
    osebe = cur.fetchall()
    cur.execute("""SELECT DISTINCT pozicija FROM igralec""")
    pozicije = cur.fetchall()
    return template('igralec_dodaj.html', osebe=osebe, pozicije=pozicije)

@post('/igralec_dodaj')
def igralec_dodaj_post():
    emso = request.forms.emso
    pozicija = request.forms.pozicija
    visina = request.forms.visina
    teza = request.forms.teza
    vrednost = request.forms.vrednost
    zacetek_pogodbe = request.forms.zacetek_pogodbe
    konec_pogodbe = request.forms.konec_pogodbe
    cur.execute("""INSERT INTO igralec (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, emso) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, emso))
    conn.commit()
    redirect(url('igralec'))

@get('/igralec_uredi/<emso>')
def igralec_uredi_get(emso):
    cur.execute(""" SELECT * FROM igralec WHERE emso= %s""", (emso, ))
    igralec = cur.fetchone()
    cur.execute(""" SELECT * FROM igralec""")
    igralci= cur.fetchall()
    cur.execute("""SELECT DISTINCT pozicija FROM igralec""")
    pozicije = cur.fetchall()
    return template('igralec_uredi.html', igralec=igralec, igralci=igralci, pozicije=pozicije)

@post('/igralec_uredi/<emso>')
def igralec_uredi_post(emso):
    cur.execute(""" SELECT * FROM igralec WHERE emso= %s""", (emso, ))
    staro = cur.fetchone()
    pozicija = request.forms.pozicija
    visina = request.forms.visina
    teza = request.forms.teza
    vrednost = request.forms.vrednost
    zacetek_pogodbe = request.forms.zacetek_pogodbe
    konec_pogodbe = request.forms.konec_pogodbe
    novi_emso = request.forms.novi_emso
    cur.execute("""UPDATE igralec SET pozicija = %s, visina = %s, teza = %s, vrednost = %s, zacetek_pogodbe = %s, konec_pogodbe = %s, emso = %s WHERE emso = %s;""", (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, novi_emso, staro[6]))
    redirect(url('igralec'))


@post('/igralec/odstrani/<emso>')
def igralec_odstrani(emso): 
    try:
        cur.execute("DELETE FROM igralec WHERE emso = %s", (emso, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Igralca {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na tega igralca".format(emso))
    redirect(url('igralec'))



###OSEBA
@get('/oseba')
def oseba():
    cur.execute("""SELECT emso, ime,priimek,rojstni_dan,ekipa from oseba""")
    return template('oseba.html', oseba=cur)

@get('/oseba_dodaj')
def oseba_dodaj():
    cur.execute("""SELECT * from ekipa""")
    ekipe = cur.fetchall()
    return template('oseba_dodaj.html', ekipe=ekipe)

@post('/oseba_dodaj')
def oseba_dodaj_post():
    emso = request.forms.emso
    ime = request.forms.ime
    priimek = request.forms.priimek
    rojstni_dan = request.forms.rojstni_dan
    ekipa = request.forms.ekipa
    cur.execute("""INSERT INTO oseba (emso, ime, priimek, rojstni_dan, ekipa) VALUES (%s, %s, %s, %s, %s);""", (emso, ime, priimek, rojstni_dan, ekipa))
    conn.commit()
    redirect(url('oseba'))

@get('/oseba_uredi/<emso>')
def oseba_uredi_get(emso):
    cur.execute(""" SELECT * FROM oseba WHERE emso= %s""", (emso, ))
    oseba = cur.fetchone()
    cur.execute(""" SELECT DISTINCT ime FROM ekipa""")
    ekipe = cur.fetchall()
    cur.execute(""" SELECT emso FROM oseba """)
    emsoji = cur.fetchall()
    return template('oseba_uredi.html', oseba=oseba, ekipe=ekipe, emsoji=emsoji)

@post('/oseba_uredi/<emso>')
def oseba_uredi_post(emso):
    cur.execute(""" SELECT * FROM oseba WHERE emso= %s""", (emso, ))
    staro = cur.fetchone()
    emso = request.forms.nov_emso
    ime = request.forms.ime
    priimek = request.forms.priimek
    rojstni_dan = request.forms.rojstni_dan
    ekipa = request.forms.ekipa
    cur.execute("""UPDATE oseba SET emso = %s, ime = %s, priimek = %s, rojstni_dan = %s, ekipa = %s WHERE emso = %s;""", (emso, ime, priimek, rojstni_dan, ekipa, staro[0]))
    redirect(url('oseba'))


@post('/oseba/odstrani/<emso>')
def oseba_odstrani(emso): 
    try:
        cur.execute("DELETE FROM oseba WHERE emso = %s", (emso, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Osebe {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na to osebo".format(emso))
    redirect(url('oseba'))



###TEKMA
@get('/tekma')
def tekma():
    cur.execute("""SELECT id_tekme,domaca_ekipa,tuja_ekipa,goli_domace,goli_tuje FROM tekma""")
    return template('tekma.html', tekma=cur)

@get('/tekma_dodaj')
def tekma_dodaj():
    cur.execute("""SELECT ime FROM ekipa """)
    ekipe = cur.fetchall()
    return template('tekma_dodaj.html', ekipe=ekipe)

@post('/tekma_dodaj')
def tekma_dodaj_post():
    id_tekme = request.forms.id_tekme
    domaca_ekipa = request.forms.domaca_ekipa
    tuja_ekipa = request.forms.tuja_ekipa
    goli_domace = request.forms.goli_domace
    goli_tuje = request.forms.goli_tuje
    cur.execute("""INSERT INTO tekma (id_tekme, domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje) VALUES (%s, %s, %s, %s, %s);""", (id_tekme, domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje))
    conn.commit()
    redirect(url('tekma'))

@get('/tekma_uredi/<id_tekme>')
def tekma_uredi_get(id_tekme):
    cur.execute(""" SELECT * FROM tekma WHERE id_tekme= %s""", (id_tekme, ))
    tekma = cur.fetchone()
    cur.execute("""SELECT id_tekme FROM tekma""")
    id_tekm = cur.fetchall()
    cur.execute("""SELECT ime FROM ekipa """)
    ekipe = cur.fetchall()
    return template('tekma_uredi.html', tekma=tekma, id_tekm=id_tekm, ekipe=ekipe)

@post('/tekma_uredi/<id_tekme>')
def tekma_uredi_post(id_tekme):
    cur.execute(""" SELECT * FROM tekma WHERE id_tekme= %s""", (id_tekme, ))
    staro = cur.fetchone()
    id_tekme = request.forms.nov_id_tekme
    domaca_ekipa = request.forms.domaca_ekipa
    tuja_ekipa = request.forms.tuja_ekipa
    goli_domace = request.forms.goli_domace
    goli_tuje = request.forms.goli_tuje
    cur.execute("""UPDATE tekma SET id_tekme = %s, domaca_ekipa = %s, tuja_ekipa = %s, goli_domace = %s, goli_tuje = %s WHERE id_tekme = %s;""", (id_tekme, domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje, staro[0]))
    redirect(url('tekma'))


@post('/tekma/odstrani/<id_tekme>')
def tekma_odstrani(id_tekme): 
    try:
        cur.execute("DELETE FROM tekma WHERE id_tekme = %s", (id_tekme, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Tekme {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na to tekmo".format(id_tekme))
    redirect(url('tekma'))




###ZAPOSLEN
@get('/zaposlen')
def zaposlen():
    cur.execute("""SELECT oseba.emso, oseba.ime, oseba.priimek,delovno_mesto,placa,oseba.ekipa from zaposlen
                    LEFT JOIN oseba ON oseba.emso = zaposlen.emso""")
    return template('zaposlen.html', zaposlen=cur)

@get('/zaposlen_dodaj')
def zaposlen_dodaj():
    cur.execute("""SELECT emso FROM oseba """)
    emsoji = cur.fetchall()
    return template('zaposlen_dodaj.html', emsoji=emsoji)

@post('/zaposlen_dodaj')
def zaposlen_dodaj_post():
    emso = request.forms.emso
    delovno_mesto = request.forms.delovno_mesto
    placa = request.forms.placa
    cur.execute("""INSERT INTO zaposlen (emso, delovno_mesto, placa) VALUES (%s, %s, %s);""", (emso, delovno_mesto, placa))
    conn.commit()
    redirect(url('zaposlen'))

@get('/zaposlen_uredi/<emso>')
def zaposlen_uredi_get(emso):
    cur.execute(""" SELECT * FROM zaposlen WHERE emso= %s""", (emso, ))
    zaposlen = cur.fetchone()
    cur.execute("""SELECT emso FROM oseba """)
    emsoji = cur.fetchall()
    return template('zaposlen_uredi.html', zaposlen=zaposlen, emsoji=emsoji)

@post('/zaposlen_uredi/<emso>')
def zaposlen_uredi_post(emso):
    cur.execute(""" SELECT * FROM zaposlen WHERE emso= %s""", (emso, ))
    staro = cur.fetchone()
    emso = request.forms.nov_emso
    delovno_mesto = request.forms.delovno_mesto
    placa = request.forms.placa
    cur.execute("""UPDATE zaposlen SET emso = %s, delovno_mesto = %s, placa = %s WHERE emso = %s;""", (emso, delovno_mesto, placa, staro[0]))
    redirect(url('zaposlen'))


@post('/zaposlen/odstrani/<emso>')
def zaposlen_odstrani(emso): 
    try:
        cur.execute("DELETE FROM zaposlen WHERE emso = %s", (emso, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Zaposlenega {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na tega zaposlenega".format(emso))
    redirect(url('zaposlen'))



####=======================

@get('/strelci')
def strelci():
    cur.execute("""SELECT oseba.ime,oseba.priimek, count(strelec), oseba.ekipa FROM goli
                LEFT JOIN oseba ON oseba.emso = goli.strelec
                GROUP BY oseba.ime,oseba.priimek,oseba.ekipa
                ORDER BY count(strelec) DESC
                """)
    return template('strelci.html', strelci=cur)

@get('/podajalci')
def podajalci():
    cur.execute("""SELECT oseba.ime,oseba.priimek, count(podajalec),oseba.ekipa FROM goli
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




