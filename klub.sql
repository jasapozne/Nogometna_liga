CREATE TABLE mostvo (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    rojstvo DATE NOT NULL DEFAULT now(),
    drzavljanstvo TEXT NOT NULL,
    polozaj TEXT NOT NULL,
    visina INTEGER NOT NULL,
    teza INTEGER NOT NULL
);

CREATE TABLE pogodbe (
    id INTEGER PRIMARY KEY,
    datum_zacetka DATE NOT NULL DEFAULT now(),
    datum_konca DATE NOT NULL DEFAULT now(),  
    vrednost INTEGER NOT NULL,
);

CREATE TABLE vodstvo (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,  
    polozaj TEXT NOT NULL,
);

CREATE TABLE statistika (
    emso INTEGER PRIMARY KEY,
    goli INTEGER NOT NULL,
    podaje INTEGER NOT NULL,  
    ocene INTEGER NOT NULL,
);

CREATE TABLE dresi (
    id INTEGER PRIMARY KEY,
    stevilo_dresa INTEGER NOT NULL,
    cena INTEGER NOT NULL,  
    prodani_dresi INTEGER NOT NULL
);

CREATE TABLE rezultati (
    id_tekme INTEGER PRIMARY KEY,
    izid INTEGER NOT NULL,
    domaca_ekipa TEXT NOT NULL,  
    gostujoca_ekipa TEXT NOT NULL,
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
