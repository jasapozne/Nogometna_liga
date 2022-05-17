import pandas as pd
import os



def uvozi_csv(zazeni=True): 
    if zazeni == True:    
        for file in os.listdir("podatki/csv"):
            data = pd.read_csv("podatki/csv/{0}".format(str(file)))
            f = open("podatki/sql/{0}.sql".format(os.path.splitext(file)[0]), "w")
            for i in range(len(data.index)):
                stolpci = "(" + ", ".join(str(v) for v in list(data.columns)) + ")"
                vrednosti = "(" + ", ".join(str(v) for v in data.iloc[[i]].values.tolist()[0]) + ")"
                f.write("INSERT INTO {tabela} {stolpci} VALUES {vrednosti} \n".format(tabela=os.path.splitext(file)[0], stolpci=stolpci, vrednosti=vrednosti))
        f.close()
    else:
        pass

uvozi_csv(True)

