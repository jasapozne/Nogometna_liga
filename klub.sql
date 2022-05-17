DROP TABLE IF EXISTS ekipa;
DROP TABLE IF EXISTS goli;
DROP TABLE IF EXISTS igralec;
DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS tekma;
DROP TABLE IF EXISTS zaposlen;

CREATE TABLE oseba (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    rojstvo DATE NOT NULL DEFAULT now(),
    ekipa TEXT NOT NULL
);

CREATE TABLE igralec (
    pozicija TEXT NOT NULL,
    visina INTEGER NOT NULL,
    teza INTEGER NOT NULL,
    vrednost INTEGER NOT NULL,
    datum_zacetka DATE NOT NULL DEFAULT now(),
    datum_konca DATE NOT NULL DEFAULT now(),
    emso INTEGER NOT NULL REFERENCES osebe(emso) 
);

CREATE TABLE zaposlen (
    emso INTEGER osebe(emso),
    delovno_mesto TEXT NOT NULL,
    placa INTEGER NOT NULL
);

CREATE TABLE ekipa (
    ime TEXT PRIMARY KEY,
    mesto TEXT NOT NULL,
    stadion TEXT NOT NULL
);

CREATE TABLE goli (
    id_tekme INTEGER PRIMARY KEY REFERENCES tekma(id_tekme),
    strelec INTEGER NOT NULL REFERENCES osebe(emso), 
    podajalec INTEGER NOT NULL REFERENCES osebe(emso) 
);

CREATE TABLE tekma (
    id_tekme INTEGER PRIMARY KEY
    domaca_eikpa TEXT NOT NULL,
    tuja_ekipa TEXT NOT NULL,
    goli_domace INTEGER NOT NULL,
    goli_tuje INTEGER NOT NULL
);

GRANT ALL ON DATABASE sem2022_jasap TO jasap;
GRANT ALL ON SCHEMA public TO jasap;
GRANT ALL ON ALL TABLES IN SCHEMA public TO jasap;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO jasap;

GRANT ALL ON DATABASE sem2022_jasap TO zigag;
GRANT ALL ON SCHEMA public TO zigag;
GRANT ALL ON ALL TABLES IN SCHEMA public TO zigag;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO zigag;

GRANT ALL ON DATABASE ssem2022_jasap TO mykolas;
GRANT ALL ON SCHEMA public TO mykolas;
GRANT ALL ON ALL TABLES IN SCHEMA public TO mykolas;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO mykolas;
