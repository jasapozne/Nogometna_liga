import psycopg2, psycopg2.extensions, psycopg2.extras
import csv
import pandas as pd
import os

from auth import *



psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def uvozi_ekipa():
    data = pd.read_csv("podatki/csv/ekipa.csv")
    f = open("podatki/sql/ekipa.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[[i]].values.tolist()[0]) + "')"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="ekipa", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_ekipa()

def uvozi_oseba():
    data = pd.read_csv("podatki/csv/oseba.csv")
    f = open("podatki/sql/oseba.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "(" + str(data.iloc[i, 0]) + ", '" + "', '".join(str(v) for v in data.iloc[i, 1:].values.tolist()) + "')"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="oseba", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_oseba()

def uvozi_igralec():
    data = pd.read_csv("podatki/csv/igralec.csv")
    f = open("podatki/sql/igralec.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[i, 0:5].values.tolist()) + "', " + "{0}".format(data.iloc[i, 5]) + ", " +  "{0}".format(data.iloc[i, 6]) + ")"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="igralec", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_igralec()

def uvozi_zaposlen():
    data = pd.read_csv("podatki/csv/zaposlen.csv")
    f = open("podatki/sql/zaposlen.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[i, 0:1].values.tolist()) + "', " + "{0}".format(data.iloc[i, 1]) + ", " + "{0}".format(data.iloc[i, 2]) + ")"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="zaposlen", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_zaposlen()

def uvozi_tekma():
    data = pd.read_csv("podatki/csv/tekma.csv")
    f = open("podatki/sql/tekma.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)[1:]) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[i, 1:3].values.tolist()) + "', " + ", ".join(str(v) for v in data.iloc[i, 3:].values.tolist()) + ")"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="tekma", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_tekma()
         
def uvozi_goli():
    data = pd.read_csv("podatki/csv/goli.csv", delimiter=";")
    f = open("podatki/sql/goli.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)[1:]) + ")"
        vrednosti = "(" + ", ".join(str(v) for v in data.iloc[[i], 1:].values.tolist()[0]) + ")"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti}; \n".format(tabela="goli", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_goli()



 





def ustvari_tabele():
    with open("klub.sql") as f:
        koda = f.read()
        cur.execute(koda)
    conn.commit()

def uvoziSQL(datoteka):
    with open("podatki/sql/{0}".format(datoteka)) as f:
        koda = f.read()
        cur.execute(koda)
    conn.commit()

ustvari_tabele()
uvoziSQL("ekipa.sql")
uvoziSQL("oseba.sql")
uvoziSQL("igralec.sql")
uvoziSQL("zaposlen.sql")
uvoziSQL("tekma.sql")
uvoziSQL("goli.sql")


