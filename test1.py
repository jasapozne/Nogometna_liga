import pandas as pd
import os

def uvozi_ekipa():
    data = pd.read_csv("podatki/csv/ekipa.csv")
    f = open("podatki/sql/ekipa.sql", "w")
    for i in range(len(data.index)):
        stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
        vrednosti = "('" + "', '".join(str(v) for v in data.iloc[[i]].values.tolist()[0]) + "')"
        f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti} \n".format(tabela="ekipa", stolpci=stolpci, vrednosti=vrednosti))
    f.close()



uvozi_ekipa()  