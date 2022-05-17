import psycopg2, psycopg2.extensions, psycopg2.extras
import csv
import pandas as pd
import os

from auth_public import *



#psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
#conn = psycopg2.connect(database=d, host=host, user=user, password=password)


def uvozi_ekipa():
    data = pd.read_csv("podatki/csv/ekipa.csv")
    f = open("podatki/sql/ekipa.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[[i]].values.tolist()[0]) + "')"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti} \n".format(tabela="ekipa", stolpci=stolpci, vrednosti=vrednosti))
    f.close()

uvozi_ekipa()
         
def uvozi_goli():
    data = pd.read_csv("podatki/csv/goli.csv")
    f = open("podatki/sql/goli.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "(" + ", ".join(str(v) for v in data.iloc[[i]].values.tolist()[0]) + ")"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti} \n".format(tabela="goli", stolpci=stolpci, vrednosti=vrednosti))
    f.close()



uvozi_goli()  