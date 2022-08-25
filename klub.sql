GRANT ALL ON DATABASE sem2022_zigag TO jasap WITH GRANT OPTION;
GRANT ALL ON DATABASE sem2022_zigag TO mykolash WITH GRANT OPTION;

GRANT ALL ON SCHEMA public TO mykolash;
GRANT ALL ON SCHEMA public TO jasap;

GRANT CONNECT ON DATABASE sem2022_zigag TO javnost;
GRANT USAGE ON SCHEMA public to javnost;


DROP TABLE IF EXISTS ekipa ;
DROP TABLE IF EXISTS goli;
DROP TABLE IF EXISTS igralec;
DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS tekma;
DROP TABLE IF EXISTS zaposlen;

CREATE TABLE ekipa (
    ime TEXT UNIQUE PRIMARY KEY,
    mesto TEXT NOT NULL,
    stadion TEXT NOT NULL
);

CREATE TABLE oseba (
    emso TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    rojstni_dan DATE NOT NULL DEFAULT now(),
    ekipa TEXT NOT NULL REFERENCES ekipa(ime) ON UPDATE CASCADE,
    uporabnisko_ime TEXT UNIQUE DEFAULT NULL,
    geslo TEXT DEFAULT NULL
);

CREATE TABLE igralec (
    pozicija TEXT NOT NULL,
    visina TEXT NOT NULL,
    teza TEXT NOT NULL,
    vrednost TEXT NOT NULL,
    zacetek_pogodbe DATE NOT NULL DEFAULT now(),
    konec_pogodbe DATE NOT NULL DEFAULT now(),
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY
);

CREATE TABLE zaposlen (
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY,
    delovno_mesto TEXT NOT NULL,
    placa TEXT NOT NULL
);

CREATE TABLE tekma (
    id_tekme INTEGER PRIMARY KEY,
    domaca_ekipa TEXT NOT NULL REFERENCES ekipa(ime) ON UPDATE CASCADE,
    tuja_ekipa TEXT NOT NULL REFERENCES ekipa(ime) ON UPDATE CASCADE,
    goli_domace INTEGER NOT NULL,
    goli_tuje INTEGER NOT NULL
);

CREATE TABLE goli (
    id_gol INTEGER PRIMARY KEY,
    id_tekme INTEGER NOT NULL REFERENCES tekma(id_tekme),
    strelec INTEGER NOT NULL REFERENCES oseba(emso), 
    podajalec INTEGER NOT NULL REFERENCES oseba(emso) 
);



GRANT ALL ON ALL TABLES IN SCHEMA public TO zigag;
GRANT ALL ON ALL TABLES IN SCHEMA public TO jasap;
GRANT ALL ON ALL TABLES IN SCHEMA public TO mykolash;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO zigag;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO jasap;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO mykolash;

GRANT SELECT ON ALL TABLES IN SCHEMA public to javnost;
GRANT UPDATE ON ALL TABLES IN SCHEMA public to javnost;
GRANT DELETE ON ALL TABLES IN SCHEMA public to javnost;
GRANT INSERT ON ALL TABLES IN SCHEMA public to javnost;
