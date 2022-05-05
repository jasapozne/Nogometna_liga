CREATE TABLE osebe (
    emso INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    rojstvo DATE NOT NULL DEFAULT now()
);

CREATE TABLE igralec (
    pozicija TEXT NOT NULL,
    visina INTEGER NOT NULL,
    teza INTEGER NOT NULL,
    vrednost INTEGER NOT NULL,
    datum_zacetka DATE NOT NULL DEFAULT now(),
    datum_konca DATE NOT NULL DEFAULT now()
);

CREATE TABLE zaposlen (
    delovno_mesto TEXT PRIMARY KEY,
    placa INTEGER NOT NULL
);

CREATE TABLE ekipa (
    ime TEXT PRIMARY KEY,
    mesto TEXT NOT NULL,
    stadion TEXT NOT NULL,
    domaca_ekipa TEXT NOT NULL,  
    gostujoca_ekipa TEXT NOT NULL
);

CREATE TABLE tekma (
    id_tekme INTEGER PRIMARY KEY,
    izid INTEGER NOT NULL
);

CREATE TABLE goli (
    strelec TEXT PRIMARY KEY,
    podajalec TEXT NOT NULL
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
