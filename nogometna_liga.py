from bottleext import *
import hashlib
import psycopg2, psycopg2.extensions, psycopg2.extras
import os

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from auth_public import *

# PRIVZETO
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Odkomentiraj, če želiš sporočila o napakah
debug(True)



skrivnost = "xn1AD5jy*RM*%qM$To0C8YlZ2uriO4"

napakaSporocilo = None
def nastaviSporocilo(sporocilo = None):
    global napakaSporocilo
    staro = napakaSporocilo
    napakaSporocilo = sporocilo
    return staro

####UPORABNIKI
def hashGesla(geslo):
    f = hashlib.sha256()
    f.update(geslo.encode("utf-8"))
    return f.hexdigest()



@get('/registracija')
def registracija_get():
    napaka = nastaviSporocilo()
    return template('registracija.html', napaka=napaka)

@post('/registracija')
def registracija_post():
    emso = request.forms.emso
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    geslo2 = request.forms.geslo2
    cur.execute("""SELECT * FROM oseba WHERE emso = %s""", (emso, ))
    uporabnik = cur.fetchone()
    cur.execute("""SELECT * FROM OSEBA WHERE uporabnisko_ime = %s""", (uporabnisko_ime, ))
    unique_uporabnisko_ime = cur.fetchone()
    if uporabnik == None:
        nastaviSporocilo("Izbrani EMŠO ni v bazi.")
        redirect(url('registracija_get'))
    if unique_uporabnisko_ime != None:
        nastaviSporocilo("Izbrano uporabniško ime ni na voljo.")
        redirect(url('registracija_get'))
    if len(geslo) <= 6:
        nastaviSporocilo("Geslo mora biti dolgo vsaj 6 znakov.")
        redirect(url('registracija_get'))
    if geslo != geslo2:
        nastaviSporocilo("Gesli se ne ujemata.")
        redirect(url('registracija_get'))
    zgostitev = hashGesla(geslo)
    try:
        cur.execute("""UPDATE oseba SET uporabnisko_ime = %s, geslo = %s WHERE emso = %s""", (uporabnisko_ime, zgostitev, emso))
        conn.commit()
        response.set_cookie("uporabnisko_ime", uporabnisko_ime, secret=skrivnost)
        nastaviSporocilo('Registracija je bila uspešna.')
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Registracija in uspela.")
        redirect(url('registracija_get'))
    redirect(url('index'))

@get('/prijava')
def prijava_get():
    napaka = nastaviSporocilo()
    return template('prijava.html', napaka=napaka)

@post('/prijava')
def prijava_post():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    hash_gesla = None
    try:
        cur.execute("""SELECT geslo FROM oseba WHERE uporabnisko_ime = %s""", (uporabnisko_ime, ))
        hash_gesla = cur.fetchone()[0]
    except:
        hash_gesla = None
        conn.rollback()
    if hash_gesla == None:
        nastaviSporocilo('Podatki za prijavo niso ustrezni.')
        redirect(url('prijava_get')) 
    if hashGesla(geslo) != hash_gesla:
        nastaviSporocilo('Podatki za prijavo niso ustrezni.') 
        redirect(url('prijava_Get'))
    response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
    nastaviSporocilo('Prijava je bila uspešna.')
    redirect(url('index'))

@get('/odjava')
def odjava():
    response.delete_cookie('uporabnisko_ime')
    nastaviSporocilo('Odjava je bila uspešna.')
    redirect(url('index'))

def preveri_uporabnika():
    napaka = nastaviSporocilo()
    nastaviSporocilo('Potrebna je prijava.')
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret=skrivnost)
    if uporabnisko_ime:
        uporabnik = None
        try:
            cur.execute(""" SELECT * FROM oseba WHERE uporabnisko_ime = %s""", (uporabnisko_ime, ))
            uporabnik = cur.fetchone()[0]
        except:
            uporabnik = None
        if uporabnik:
            return uporabnik
    redirect(url('prijava_get', napaka=napaka))
    








@get('/')
def index():
    uspeh = nastaviSporocilo()
    return template('index.html', uspeh=uspeh) 

###EKIPE

@get('/ekipa')
def ekipa():
    napaka = nastaviSporocilo()
    cur.execute("""SELECT ime,stadion,mesto FROM ekipa""")
    return template('ekipa.html', ekipa=cur, napaka=napaka)

@get('/ekipa_dodaj')
def ekipa_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    return template('ekipa_dodaj.html', napaka=napaka)

@post('/ekipa_dodaj')
def ekipa_dodaj_post():
    ime = request.forms.ime
    mesto = request.forms.mesto
    stadion = request.forms.stadion
    cur.execute(""" SELECT * FROM ekipa WHERE ime = %s """, (ime, ))
    unique_ime = cur.fetchone()
    if unique_ime != None:
        nastaviSporocilo("Ekipe {} ni mogoče dodati, saj je izbrano ime že v uporabi.".format(ime))
        redirect(url('ekipa_dodaj'))
    try:
        cur.execute("""INSERT INTO ekipa (ime, mesto, stadion) VALUES (%s, %s, %s);""", (ime, mesto, stadion))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Dodajanje ekipe ni uspelo.")
        redirect(url('ekipa_dodaj'))
    redirect(url('ekipa'))

@get('/ekipa_uredi/<ime>')
def ekipa_uredi_get(ime):
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    else:
        cur.execute(""" SELECT * FROM ekipa WHERE ime= %s""", (ime, ))
        ekipa = cur.fetchone()
        nastaviSporocilo('')
    return template('ekipa_uredi.html', ekipa=ekipa, napaka=napaka)


@post('/ekipa_uredi/<ime>')
def ekipa_uredi_post(ime):
    cur.execute(""" SELECT * FROM ekipa WHERE ime= %s""", (ime, ))
    staro = cur.fetchone()
    novo_ime = request.forms.novo_ime
    mesto = request.forms.mesto
    stadion = request.forms.stadion
    try:
        cur.execute("""UPDATE ekipa SET ime = %s, mesto = %s, stadion = %s WHERE ime = %s;""", (novo_ime, mesto, stadion, staro[0]))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje ekipe ni uspelo.")
        redirect(url('ekipa'))
    redirect(url('ekipa'))


@post('/ekipa/odstrani/<ime>')
def ekipa_odstrani(ime): 
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect(url('ekipa'))
    else:
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
    napaka = nastaviSporocilo()
    cur.execute("""SELECT goli.id_gol, tekma.id_tekme, goli.strelec, goli.podajalec, tekma.domaca_ekipa, tekma.tuja_ekipa, oseba.ime, oseba.priimek, podaja.ime, podaja.priimek, oseba.ekipa FROM goli
                    JOIN oseba ON oseba.emso = goli.strelec
                    JOIN oseba AS podaja ON podaja.emso = goli.podajalec 
                    JOIN tekma ON tekma.id_tekme = goli.id_tekme
                    ORDER BY id_tekme DESC
                    """)
    return template('goli.html', goli=cur, napaka=napaka)

@get('/goli_dodaj')
def goli_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT id_tekme FROM tekma""")
    tekme = cur.fetchall()
    cur.execute("""SELECT igralec.emso, oseba.ime, oseba.priimek FROM igralec
                    JOIN oseba ON oseba.emso = igralec.emso""")
    igralci = cur.fetchall()
    return template('goli_dodaj.html', tekme=tekme, igralci=igralci, napaka=napaka)

@post('/goli_dodaj')
def goli_dodaj_post():
    id_tekme = request.forms.id_tekme
    strelec = request.forms.strelec
    podajalec = request.forms.podajalec
    if strelec == podajalec:
        nastaviSporocilo("Podajalec in strelec morata biti različna.")
        redirect(url('goli_dodaj'))
    try:
        cur.execute("""INSERT INTO goli (id_gol, id_tekme, strelec, podajalec) VALUES (%s, %s, %s);""", (id_tekme, strelec, podajalec))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Dodajanje zadetka ni uspelo.")
        redirect(url('goli'))
    redirect(url('goli'))

@get('/goli_uredi/<id_gol>')
def goli_uredi_get(id_gol):
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT goli.id_gol, tekma.id_tekme, goli.strelec, goli.podajalec, tekma.domaca_ekipa, tekma.tuja_ekipa, oseba.ime, oseba.priimek, podaja.ime, podaja.priimek, oseba.ekipa FROM goli
                    JOIN oseba ON oseba.emso = goli.strelec
                    JOIN oseba AS podaja ON podaja.emso = goli.podajalec 
                    JOIN tekma ON tekma.id_tekme = goli.id_tekme
                    WHERE id_gol = %s""", (id_gol, ))
    gol = cur.fetchone()
    cur.execute("""SELECT id_tekme FROM tekma""")
    tekme = cur.fetchall()
    cur.execute("""SELECT igralec.emso, oseba.ime, oseba.priimek, oseba.ekipa FROM igralec
                    JOIN oseba ON oseba.emso = igralec.emso
                    WHERE oseba.ekipa = %s""", (gol[10], ))
    igralci = cur.fetchall() 
    return template('goli_uredi.html', gol=gol, tekme=tekme, igralci=igralci, napaka=napaka)

@post('/goli_uredi/<id_gol>')
def goli_uredi_post(id_gol):
    id_tekme = request.forms.id_tekme
    strelec = request.forms.strelec
    podajalec = request.forms.podajalec
    try:
        cur.execute("""UPDATE goli SET id_tekme = %s, strelec = %s, podajalec = %s WHERE id_gol = %s;""", (id_tekme, strelec, podajalec, id_gol))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje zadetka ni uspelo.")
        redirect(url('goli'))
    redirect(url('goli'))


@post('/goli/odstrani/<id_gol>')
def goli_odstrani(id_gol):
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect(url('goli')) 
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
    napaka = nastaviSporocilo()
    cur.execute("""SELECT oseba.emso, oseba.ime, oseba.priimek, pozicija,visina,teza,zacetek_pogodbe,konec_pogodbe,vrednost, oseba.ekipa from igralec
                    LEFT JOIN oseba ON oseba.emso = igralec.emso""")
    return template('igralec.html', igralec=cur, napaka=napaka)

@get('/igralec_dodaj')
def igralec_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT emso FROM oseba""")
    osebe = cur.fetchall()
    cur.execute("""SELECT DISTINCT pozicija FROM igralec""")
    pozicije = cur.fetchall()
    return template('igralec_dodaj.html', osebe=osebe, pozicije=pozicije, napaka=napaka)

@post('/igralec_dodaj')
def igralec_dodaj_post():
    emso = request.forms.emso
    pozicija = request.forms.pozicija
    visina = request.forms.visina
    teza = request.forms.teza
    vrednost = request.forms.vrednost
    zacetek_pogodbe = request.forms.zacetek_pogodbe
    konec_pogodbe = request.forms.konec_pogodbe
    try:
        cur.execute("""INSERT INTO igralec (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, emso) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, emso))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Dodajanje igralca ni uspelo.")
        redirect(url('igralec'))
    redirect(url('igralec'))

@get('/igralec_uredi/<emso>')
def igralec_uredi_get(emso):
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute(""" SELECT * FROM igralec WHERE emso= %s""", (emso, ))
    igralec = cur.fetchone()
    cur.execute(""" SELECT * FROM igralec""")
    igralci= cur.fetchall()
    cur.execute("""SELECT DISTINCT pozicija FROM igralec""")
    pozicije = cur.fetchall()
    return template('igralec_uredi.html', igralec=igralec, igralci=igralci, pozicije=pozicije, napaka=napaka)

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
    try:
        cur.execute("""UPDATE igralec SET pozicija = %s, visina = %s, teza = %s, vrednost = %s, zacetek_pogodbe = %s, konec_pogodbe = %s, emso = %s WHERE emso = %s;""", (pozicija, visina, teza, vrednost, zacetek_pogodbe, konec_pogodbe, novi_emso, staro[6]))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje igralca ni uspelo.")
        redirect(url('goli'))
    redirect(url('igralec'))


@post('/igralec/odstrani/<emso>')
def igralec_odstrani(emso):
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect(url('igralec')) 
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
    napaka = nastaviSporocilo()
    cur.execute("""SELECT emso, ime,priimek,rojstni_dan,ekipa from oseba""")
    return template('oseba.html', oseba=cur, napaka=napaka)

@get('/oseba_dodaj')
def oseba_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT * from ekipa""")
    ekipe = cur.fetchall()
    return template('oseba_dodaj.html', ekipe=ekipe, napaka=napaka)

@post('/oseba_dodaj')
def oseba_dodaj_post():
    emso = request.forms.emso
    ime = request.forms.ime
    priimek = request.forms.priimek
    rojstni_dan = request.forms.rojstni_dan
    ekipa = request.forms.ekipa
    try:
        cur.execute("""INSERT INTO oseba (emso, ime, priimek, rojstni_dan, ekipa) VALUES (%s, %s, %s, %s, %s);""", (emso, ime, priimek, rojstni_dan, ekipa))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Oseba z EMŠO {} je že bazi.".format(emso))
    redirect(url('oseba'))

@get('/oseba_uredi/<emso>')
def oseba_uredi_get(emso):
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute(""" SELECT * FROM oseba WHERE emso= %s""", (emso, ))
    oseba = cur.fetchone()
    cur.execute(""" SELECT DISTINCT ime FROM ekipa""")
    ekipe = cur.fetchall()
    return template('oseba_uredi.html', oseba=oseba, ekipe=ekipe)

@post('/oseba_uredi/<emso>')
def oseba_uredi_post(emso):
    cur.execute(""" SELECT * FROM oseba WHERE emso= %s""", (emso, ))
    staro = cur.fetchone()
    ime = request.forms.ime
    priimek = request.forms.priimek
    rojstni_dan = request.forms.rojstni_dan
    ekipa = request.forms.ekipa
    try:
        cur.execute("""UPDATE oseba SET ime = %s, priimek = %s, rojstni_dan = %s, ekipa = %s WHERE emso = %s;""", (ime, priimek, rojstni_dan, ekipa, staro[0]))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje igralca ni uspelo.")
        redirect(url('oseba'))
    redirect(url('oseba'))


@post('/oseba/odstrani/<emso>')
def oseba_odstrani(emso):
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect(url('oseba')) 
    try:
        cur.execute("DELETE FROM oseba WHERE emso = %s", (emso, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Osebe {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na to osebo.".format(emso))
    redirect(url('oseba'))



###TEKMA
@get('/tekma')
def tekma():
    napaka = nastaviSporocilo()
    cur.execute("""SELECT id_tekme,domaca_ekipa,tuja_ekipa,goli_domace,goli_tuje FROM tekma""")
    return template('tekma.html', tekma=cur, napaka=napaka)

@get('/tekma_dodaj')
def tekma_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT ime FROM ekipa """)
    ekipe = cur.fetchall()
    return template('tekma_dodaj.html', ekipe=ekipe, napaka=napaka)

@post('/tekma_dodaj')
def tekma_dodaj_post():
    domaca_ekipa = request.forms.domaca_ekipa
    tuja_ekipa = request.forms.tuja_ekipa
    goli_domace = request.forms.goli_domace
    goli_tuje = request.forms.goli_tuje
    if domaca_ekipa == tuja_ekipa:
        nastaviSporocilo("Izberite dve različni ekipi.")
        redirect(url('tekma_dodaj'))
    try:
        cur.execute("""INSERT INTO tekma (domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje) VALUES (%s, %s, %s, %s);""", (domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Dodajanje tekme ni uspelo.")
        redirect(url('tekma_dodaj'))
    redirect(url('tekma'))

@get('/tekma_uredi/<id_tekme>')
def tekma_uredi_get(id_tekme):
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
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
    domaca_ekipa = request.forms.domaca_ekipa
    tuja_ekipa = request.forms.tuja_ekipa
    goli_domace = request.forms.goli_domace
    goli_tuje = request.forms.goli_tuje
    if domaca_ekipa == tuja_ekipa:
        nastaviSporocilo("Izberite dve različni ekipi.")
        redirect(url('tekma'))
    try:
        cur.execute("""UPDATE tekma SET domaca_ekipa = %s, tuja_ekipa = %s, goli_domace = %s, goli_tuje = %s WHERE id_tekme = %s;""", (domaca_ekipa, tuja_ekipa, goli_domace, goli_tuje, staro[0]))
        conn.commit()
        nastaviSporocilo('')
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje tekme ni uspelo.")
    redirect(url('tekma'))


@post('/tekma/odstrani/<id_tekme>')
def tekma_odstrani(id_tekme):
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect (url('tekma'))
    try:
        cur.execute("DELETE FROM tekma WHERE id_tekme = %s", (id_tekme, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Tekme {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na to tekmo.".format(id_tekme))
    redirect(url('tekma'))




###ZAPOSLEN
@get('/zaposlen')
def zaposlen():
    napaka = nastaviSporocilo()
    cur.execute("""SELECT oseba.emso, oseba.ime, oseba.priimek,delovno_mesto,placa,oseba.ekipa from zaposlen
                    LEFT JOIN oseba ON oseba.emso = zaposlen.emso""")
    return template('zaposlen.html', zaposlen=cur, napaka=napaka)

@get('/zaposlen_dodaj')
def zaposlen_dodaj():
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return
    nastaviSporocilo('')
    cur.execute("""SELECT emso FROM oseba """)
    emsoji = cur.fetchall()
    return template('zaposlen_dodaj.html', emsoji=emsoji, napaka=napaka)

@post('/zaposlen_dodaj')
def zaposlen_dodaj_post():
    emso = request.forms.emso
    delovno_mesto = request.forms.delovno_mesto
    placa = request.forms.placa
    try:
        cur.execute("""INSERT INTO zaposlen (emso, delovno_mesto, placa) VALUES (%s, %s, %s);""", (emso, delovno_mesto, placa))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Dodajanje zaposlenega ni uspelo.")
        redirect(url('zaposen_dodaj'))
    redirect(url('zaposlen'))

@get('/zaposlen_uredi/<emso>')
def zaposlen_uredi_get(emso):
    napaka = nastaviSporocilo()
    uporabnik = preveri_uporabnika()
    if uporabnik == None:
        return    
    cur.execute(""" SELECT * FROM zaposlen WHERE emso= %s""", (emso, ))
    zaposlen = cur.fetchone()
    cur.execute("""SELECT emso FROM oseba """)
    emsoji = cur.fetchall()
    nastaviSporocilo('')
    return template('zaposlen_uredi.html', zaposlen=zaposlen, emsoji=emsoji, napaka=napaka)

@post('/zaposlen_uredi/<emso>')
def zaposlen_uredi_post(emso):
    cur.execute(""" SELECT * FROM zaposlen WHERE emso= %s""", (emso, ))
    staro = cur.fetchone()
    delovno_mesto = request.forms.delovno_mesto
    placa = request.forms.placa
    try:
        cur.execute("""UPDATE zaposlen SET delovno_mesto = %s, placa = %s WHERE emso = %s;""", (delovno_mesto, placa, staro[0]))
        conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
        nastaviSporocilo("Urejanje zaposlenega ni uspelo.")
    redirect(url('zaposlen'))


@post('/zaposlen/odstrani/<emso>')
def zaposlen_odstrani(emso):
    uporabnik = preveri_uporabnika()
    nastaviSporocilo('')
    if uporabnik == None:
        redirect (url('zaposlen')) 
    try:
        cur.execute("DELETE FROM zaposlen WHERE emso = %s", (emso, ))
        conn.commit()
    except:
        conn.rollback()
        nastaviSporocilo("Zaposlenega {} ni mogoče odstraniti, saj druge tabele vsebujejo sklice na tega zaposlenega.".format(emso))
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
conn = psycopg2.connect(database=db, host=host, user=user, password=password, port=DB_PORT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

run(host='localhost', port=SERVER_PORT, reloader=RELOADER)




