DROP TABLE IF EXISTS ekipa ;
DROP TABLE IF EXISTS goli;
DROP TABLE IF EXISTS igralec;
DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS tekma;
DROP TABLE IF EXISTS zaposlen;

CREATE TABLE ekipa (
    ime TEXT PRIMARY KEY,
    mesto TEXT NOT NULL,
    stadion TEXT NOT NULL
);

CREATE TABLE oseba (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    rojstni_dan DATE NOT NULL DEFAULT now(),
    ekipa TEXT NOT NULL REFERENCES ekipa(ime)
);

CREATE TABLE igralec (
    pozicija TEXT NOT NULL,
    visina INTEGER NOT NULL,
    teza INTEGER NOT NULL,
    vrednost INTEGER NOT NULL,
    datum_zacetka DATE NOT NULL DEFAULT now(),
    datum_konca DATE NOT NULL DEFAULT now(),
    emso INTEGER NOT NULL REFERENCES oseba(emso) 
);

CREATE TABLE zaposlen (
    emso INTEGER NOT NULL REFERENCES oseba(emso),
    delovno_mesto TEXT NOT NULL,
    placa INTEGER NOT NULL
);

CREATE TABLE tekma (
    id_tekme INTEGER PRIMARY KEY,
    domaca_ekipa TEXT NOT NULL REFERENCES ekipa(ime),
    tuja_ekipa TEXT NOT NULL REFERENCES ekipa(ime),
    goli_domace INTEGER NOT NULL,
    goli_tuje INTEGER NOT NULL
);

CREATE TABLE goli (
    id_tekme INTEGER REFERENCES tekma(id_tekme),
    strelec INTEGER NOT NULL REFERENCES oseba(emso), 
    podajalec INTEGER NOT NULL REFERENCES oseba(emso) 
);



GRANT ALL ON DATABASE sem2022_jasap TO jasap;
GRANT ALL ON SCHEMA public TO jasap;
GRANT ALL ON ALL TABLES IN SCHEMA public TO jasap;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO jasap;

GRANT ALL ON DATABASE sem2022_jasap TO zigag;
GRANT ALL ON SCHEMA public TO zigag;
GRANT ALL ON ALL TABLES IN SCHEMA public TO zigag;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO zigag;

GRANT ALL ON DATABASE sem2022_jasap TO mykolash;
GRANT ALL ON SCHEMA public TO mykolash;
GRANT ALL ON ALL TABLES IN SCHEMA public TO mykolash;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO mykolash;
