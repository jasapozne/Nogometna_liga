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
    vrednost INTEGER NOT NULL,
    zacetek_pogodbe DATE NOT NULL DEFAULT now(),
    konec_pogodbe DATE NOT NULL DEFAULT now(),
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY
);

CREATE TABLE zaposlen (
    emso TEXT NOT NULL REFERENCES oseba(emso) PRIMARY KEY,
    delovno_mesto TEXT NOT NULL,
    placa INTEGER NOT NULL
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
    strelec TEXT NOT NULL REFERENCES oseba(emso), 
    podajalec TEXT NOT NULL REFERENCES oseba(emso) 
);

CREATE VIEW domaca_lestvica AS
SELECT domaca_ekipa AS ekipa, sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END)+ sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) + sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END)
AS tekme,sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END) AS zmage, sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS remi,
sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS porazi, sum(CASE WHEN goli_domace > goli_tuje THEN 3 ELSE 0 END)+sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS tocke 
FROM tekma
GROUP BY domaca_ekipa;
            
CREATE VIEW gostujoca_lestvica AS
SELECT tuja_ekipa AS ekipa, sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END)+ sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) + sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS tekme,
sum(CASE WHEN goli_domace < goli_tuje THEN 1 ELSE 0 END) AS zmage, sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS remi,
sum(CASE WHEN goli_domace > goli_tuje THEN 1 ELSE 0 END) AS porazi,
sum(CASE WHEN goli_domace < goli_tuje THEN 3 ELSE 0 END)+sum(CASE WHEN goli_domace = goli_tuje THEN 1 ELSE 0 END) AS tocke FROM tekma
GROUP BY tuja_ekipa;



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
