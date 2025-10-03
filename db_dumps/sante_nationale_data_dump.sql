--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgres_fdw; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgres_fdw WITH SCHEMA public;


--
-- Name: EXTENSION postgres_fdw; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgres_fdw IS 'foreign-data wrapper for remote PostgreSQL servers';


--
-- Name: tablefunc; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;


--
-- Name: EXTENSION tablefunc; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


--
-- Name: dakar_server; Type: SERVER; Schema: -; Owner: postgres
--

CREATE SERVER dakar_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    dbname 'sante_dakar',
    host '192.168.1.99',
    port '5433'
);


ALTER SERVER dakar_server OWNER TO postgres;

--
-- Name: USER MAPPING postgres SERVER dakar_server; Type: USER MAPPING; Schema: -; Owner: postgres
--

CREATE USER MAPPING FOR postgres SERVER dakar_server OPTIONS (
    password '12345',
    "user" 'postgres'
);


--
-- Name: consultations; Type: FOREIGN TABLE; Schema: public; Owner: postgres
--

CREATE FOREIGN TABLE public.consultations (
    id integer NOT NULL,
    date_consultation timestamp without time zone,
    diagnostic text,
    resultat_examen text,
    patient_id integer NOT NULL,
    medecin_id integer NOT NULL,
    centre_id integer NOT NULL,
    geom_patient_location public.geometry(Point,4326)
)
SERVER dakar_server
OPTIONS (
    schema_name 'public',
    table_name 'consultations'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN id OPTIONS (
    column_name 'id'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN date_consultation OPTIONS (
    column_name 'date_consultation'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN diagnostic OPTIONS (
    column_name 'diagnostic'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN resultat_examen OPTIONS (
    column_name 'resultat_examen'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN patient_id OPTIONS (
    column_name 'patient_id'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN medecin_id OPTIONS (
    column_name 'medecin_id'
);
ALTER FOREIGN TABLE ONLY public.consultations ALTER COLUMN centre_id OPTIONS (
    column_name 'centre_id'
);


ALTER FOREIGN TABLE public.consultations OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: national_regions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.national_regions (
    id integer NOT NULL,
    nom_region character varying(100),
    population integer,
    geom public.geometry(MultiPolygon,4326)
);


ALTER TABLE public.national_regions OWNER TO postgres;

--
-- Name: national_regions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.national_regions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.national_regions_id_seq OWNER TO postgres;

--
-- Name: national_regions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.national_regions_id_seq OWNED BY public.national_regions.id;


--
-- Name: patients; Type: FOREIGN TABLE; Schema: public; Owner: postgres
--

CREATE FOREIGN TABLE public.patients (
    id integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    date_naissance date,
    telephone character varying(20),
    residence_location public.geography(Point,4326)
)
SERVER dakar_server
OPTIONS (
    schema_name 'public',
    table_name 'patients'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN id OPTIONS (
    column_name 'id'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN nom OPTIONS (
    column_name 'nom'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN prenom OPTIONS (
    column_name 'prenom'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN date_naissance OPTIONS (
    column_name 'date_naissance'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN telephone OPTIONS (
    column_name 'telephone'
);
ALTER FOREIGN TABLE ONLY public.patients ALTER COLUMN residence_location OPTIONS (
    column_name 'residence_location'
);


ALTER FOREIGN TABLE public.patients OWNER TO postgres;

--
-- Name: national_regions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.national_regions ALTER COLUMN id SET DEFAULT nextval('public.national_regions_id_seq'::regclass);


--
-- Data for Name: national_regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.national_regions (id, nom_region, population, geom) FROM stdin;
1	Dakar	4000000	0106000020E6100000010000000103000000010000000500000000000000000032C00000000000002C4000000000000032C00000000000002E4000000000000031C00000000000002E4000000000000031C00000000000002C4000000000000032C00000000000002C40
2	ThiŠs	2000000	0106000020E6100000010000000103000000010000000500000000000000000031C00000000000002C4000000000000031C00000000000002E4000000000000030C00000000000002E4000000000000030C00000000000002C4000000000000031C00000000000002C40
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Name: national_regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.national_regions_id_seq', 2, true);


--
-- Name: national_regions national_regions_nom_region_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.national_regions
    ADD CONSTRAINT national_regions_nom_region_key UNIQUE (nom_region);


--
-- Name: national_regions national_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.national_regions
    ADD CONSTRAINT national_regions_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

