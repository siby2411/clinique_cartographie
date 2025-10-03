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
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: centre_sante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centre_sante (
    id integer NOT NULL,
    nom character varying(255) NOT NULL,
    adresse character varying(255),
    capacite_lits integer,
    departement_id integer NOT NULL,
    location public.geometry(Point,4326)
);


ALTER TABLE public.centre_sante OWNER TO postgres;

--
-- Name: centre_sante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.centre_sante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.centre_sante_id_seq OWNER TO postgres;

--
-- Name: centre_sante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.centre_sante_id_seq OWNED BY public.centre_sante.id;


--
-- Name: centres_sante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centres_sante (
    id integer NOT NULL,
    nom character varying(150) NOT NULL,
    adresse character varying(255),
    telephone character varying(20),
    capacite_lits integer,
    location public.geography(Point,4326) NOT NULL
);


ALTER TABLE public.centres_sante OWNER TO postgres;

--
-- Name: centres_sante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.centres_sante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.centres_sante_id_seq OWNER TO postgres;

--
-- Name: centres_sante_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.centres_sante_id_seq OWNED BY public.centres_sante.id;


--
-- Name: consultations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.consultations (
    id integer NOT NULL,
    date_consultation timestamp without time zone,
    diagnostic text,
    resultat_examen text,
    patient_id integer NOT NULL,
    medecin_id integer NOT NULL,
    centre_id integer NOT NULL,
    geom_patient_location public.geometry(Point,4326)
);


ALTER TABLE public.consultations OWNER TO postgres;

--
-- Name: consultations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.consultations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.consultations_id_seq OWNER TO postgres;

--
-- Name: consultations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.consultations_id_seq OWNED BY public.consultations.id;


--
-- Name: departement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departement (
    id integer NOT NULL,
    nom character varying(100) NOT NULL
);


ALTER TABLE public.departement OWNER TO postgres;

--
-- Name: departement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.departement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departement_id_seq OWNER TO postgres;

--
-- Name: departement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.departement_id_seq OWNED BY public.departement.id;


--
-- Name: departements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departements (
    id integer NOT NULL,
    nom character varying(100) NOT NULL,
    population integer,
    geometrie public.geometry(MultiPolygon,4326) NOT NULL
);


ALTER TABLE public.departements OWNER TO postgres;

--
-- Name: departements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.departements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departements_id_seq OWNER TO postgres;

--
-- Name: departements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.departements_id_seq OWNED BY public.departements.id;


--
-- Name: medecins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medecins (
    id integer NOT NULL,
    nom character varying(100) NOT NULL,
    specialite character varying(100),
    telephone character varying(20),
    centre_id integer NOT NULL
);


ALTER TABLE public.medecins OWNER TO postgres;

--
-- Name: medecins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medecins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medecins_id_seq OWNER TO postgres;

--
-- Name: medecins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medecins_id_seq OWNED BY public.medecins.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    date_naissance date,
    telephone character varying(20),
    residence_location public.geography(Point,4326),
    sexe character varying(10)
);


ALTER TABLE public.patients OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patients_id_seq OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: utilisateur; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.utilisateur (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(50),
    medecin_id integer
);


ALTER TABLE public.utilisateur OWNER TO postgres;

--
-- Name: utilisateur_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.utilisateur_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.utilisateur_id_seq OWNER TO postgres;

--
-- Name: utilisateur_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.utilisateur_id_seq OWNED BY public.utilisateur.id;


--
-- Name: centre_sante id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centre_sante ALTER COLUMN id SET DEFAULT nextval('public.centre_sante_id_seq'::regclass);


--
-- Name: centres_sante id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centres_sante ALTER COLUMN id SET DEFAULT nextval('public.centres_sante_id_seq'::regclass);


--
-- Name: consultations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultations ALTER COLUMN id SET DEFAULT nextval('public.consultations_id_seq'::regclass);


--
-- Name: departement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departement ALTER COLUMN id SET DEFAULT nextval('public.departement_id_seq'::regclass);


--
-- Name: departements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departements ALTER COLUMN id SET DEFAULT nextval('public.departements_id_seq'::regclass);


--
-- Name: medecins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medecins ALTER COLUMN id SET DEFAULT nextval('public.medecins_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: utilisateur id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur ALTER COLUMN id SET DEFAULT nextval('public.utilisateur_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
88e1dd99d642
\.


--
-- Data for Name: centre_sante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.centre_sante (id, nom, adresse, capacite_lits, departement_id, location) FROM stdin;
\.


--
-- Data for Name: centres_sante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.centres_sante (id, nom, adresse, telephone, capacite_lits, location) FROM stdin;
1	Centre Principal Plateau	Avenue Lamine Gueye	\N	\N	0101000020E61000001E166A4DF36E31C012143FC6DC552D40
2	H“pital R‚gional Pikine	Route Nationale 1	\N	\N	0101000020E610000054E3A59BC46031C048E17A14AE872D40
3	Dispensaire de Yoff	Rue de l'A‚roport	\N	\N	0101000020E61000000C022B87167931C0BA490C022B872D40
\.


--
-- Data for Name: consultations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.consultations (id, date_consultation, diagnostic, resultat_examen, patient_id, medecin_id, centre_id, geom_patient_location) FROM stdin;
11	2025-10-02 00:00:00	Paludisme	\N	1	2	2	0101000020E610000000000000008031C00000000000002D40
12	2025-10-02 00:00:00	Paludisme	\N	2	2	2	0101000020E610000000000000008031C00000000000002D40
13	2025-10-02 00:00:00	Paludisme	\N	3	2	2	0101000020E610000000000000008031C00000000000002D40
14	2025-10-02 00:00:00	Paludisme	\N	4	2	2	0101000020E610000000000000008031C00000000000002D40
15	2025-10-02 00:00:00	Paludisme	\N	5	2	2	0101000020E610000000000000008031C00000000000002D40
16	2025-10-02 00:00:00	Chol‚ra	\N	6	3	3	0101000020E610000000000000008030C00000000000002D40
17	2025-10-02 00:00:00	Chol‚ra	\N	7	3	3	0101000020E610000000000000008030C00000000000002D40
18	2025-10-02 00:00:00	Chol‚ra	\N	8	3	3	0101000020E610000000000000008030C00000000000002D40
19	2025-10-02 00:00:00	Chol‚ra	\N	9	3	3	0101000020E610000000000000008030C00000000000002D40
20	2025-10-02 00:00:00	Chol‚ra	\N	10	3	3	0101000020E610000000000000008030C00000000000002D40
\.


--
-- Data for Name: departement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departement (id, nom) FROM stdin;
\.


--
-- Data for Name: departements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departements (id, nom, population, geometrie) FROM stdin;
2	Dakar	1182255	0106000020E610000000000000
3	Pikine	1175647	0106000020E610000000000000
4	Gu‚diawaye	329676	0106000020E610000000000000
5	Rufisque	511000	0106000020E610000000000000
6	ThiŠs	700000	0106000020E610000000000000
\.


--
-- Data for Name: medecins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medecins (id, nom, specialite, telephone, centre_id) FROM stdin;
1	Faye	Generaliste	\N	1
2	Diop	Epidemiologiste	\N	2
3	Ndiaye	Pediatre	\N	3
4	Sow	Generaliste	\N	2
5	Thiam	Generaliste	\N	1
6	Faye	Generaliste	\N	1
7	Diop	Epidemiologiste	\N	2
8	Ndiaye	Pediatre	\N	3
9	Sow	Generaliste	\N	2
10	Thiam	Generaliste	\N	1
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients (id, nom, prenom, date_naissance, telephone, residence_location, sexe) FROM stdin;
1	Diallo	Omar	1990-05-10	\N	0101000020E61000001B2FDD24066131C0D578E92631882D40	\N
2	Sarr	Khady	1985-11-20	\N	0101000020E6100000FED478E9266131C09CC420B072882D40	\N
3	Camara	Lamine	2000-01-01	\N	0101000020E610000037894160E56031C00E2DB29DEF872D40	\N
4	Gueye	Sophie	1975-03-15	\N	0101000020E610000054E3A59BC46031C0D578E92631882D40	\N
5	Mbaye	Fama	1995-07-22	\N	0101000020E6100000E17A14AE476131C048E17A14AE872D40	\N
6	Ba	Moustapha	1980-02-28	\N	0101000020E6100000295C8FC2F57831C08195438B6C872D40	\N
7	Niang	Aicha	2010-09-05	\N	0101000020E61000000C022B87167931C0BA490C022B872D40	\N
8	Diouf	Cheikh	1965-12-12	\N	0101000020E610000046B6F3FDD47831C048E17A14AE872D40	\N
9	Seck	Yacine	1998-04-03	\N	0101000020E610000062105839B47831C02BF697DD93872D40	\N
10	Toure	Pape	1992-06-25	\N	0101000020E6100000F0A7C64B377931C0D734EF3845872D40	\N
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash) FROM stdin;
\.


--
-- Data for Name: utilisateur; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.utilisateur (id, email, password_hash, role, medecin_id) FROM stdin;
4	admin@sante.sn	scrypt:32768:8:1$GduA3mhbT6AWgKCG$3a1c8cf43ea58019b91edeeb4c17a2c1812d4ec5901823de4564f74655c28ef0c03e23f9026ddfb748cb672da631e974a23f861159f61a8c841b1a296ae776e6	admin	\N
2	dr.fall@sante.sn	scrypt:32768:8:1$9WCwKMc7O5C5qETk$7dfc0e2be6d35f10badeba49a7da56698ea1b9e8e04bace87631a8087588d256ab9f74b93f84f38a946a2190e86b8a30405fd3223d855cb73a7e86e96c033cda	doctor	\N
\.


--
-- Name: centre_sante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.centre_sante_id_seq', 1, false);


--
-- Name: centres_sante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.centres_sante_id_seq', 4, true);


--
-- Name: consultations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.consultations_id_seq', 20, true);


--
-- Name: departement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departement_id_seq', 1, false);


--
-- Name: departements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departements_id_seq', 7, true);


--
-- Name: medecins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medecins_id_seq', 10, true);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patients_id_seq', 10, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: utilisateur_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.utilisateur_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: centre_sante centre_sante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centre_sante
    ADD CONSTRAINT centre_sante_pkey PRIMARY KEY (id);


--
-- Name: centres_sante centres_sante_nom_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centres_sante
    ADD CONSTRAINT centres_sante_nom_key UNIQUE (nom);


--
-- Name: centres_sante centres_sante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centres_sante
    ADD CONSTRAINT centres_sante_pkey PRIMARY KEY (id);


--
-- Name: consultations consultations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultations
    ADD CONSTRAINT consultations_pkey PRIMARY KEY (id);


--
-- Name: departement departement_nom_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departement
    ADD CONSTRAINT departement_nom_key UNIQUE (nom);


--
-- Name: departement departement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departement
    ADD CONSTRAINT departement_pkey PRIMARY KEY (id);


--
-- Name: departements departements_nom_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departements
    ADD CONSTRAINT departements_nom_key UNIQUE (nom);


--
-- Name: departements departements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departements
    ADD CONSTRAINT departements_pkey PRIMARY KEY (id);


--
-- Name: medecins medecins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medecins
    ADD CONSTRAINT medecins_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: utilisateur utilisateur_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_email_key UNIQUE (email);


--
-- Name: utilisateur utilisateur_medecin_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_medecin_id_key UNIQUE (medecin_id);


--
-- Name: utilisateur utilisateur_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_pkey PRIMARY KEY (id);


--
-- Name: idx_centre_sante_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_centre_sante_location ON public.centre_sante USING gist (location);


--
-- Name: idx_centres_sante_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_centres_sante_location ON public.centres_sante USING gist (location);


--
-- Name: idx_departements_geometrie; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_departements_geometrie ON public.departements USING gist (geometrie);


--
-- Name: idx_patients_residence_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_patients_residence_location ON public.patients USING gist (residence_location);


--
-- Name: centre_sante centre_sante_departement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centre_sante
    ADD CONSTRAINT centre_sante_departement_id_fkey FOREIGN KEY (departement_id) REFERENCES public.departement(id);


--
-- Name: consultations consultations_centre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultations
    ADD CONSTRAINT consultations_centre_id_fkey FOREIGN KEY (centre_id) REFERENCES public.centres_sante(id);


--
-- Name: consultations consultations_medecin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultations
    ADD CONSTRAINT consultations_medecin_id_fkey FOREIGN KEY (medecin_id) REFERENCES public.medecins(id);


--
-- Name: consultations consultations_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultations
    ADD CONSTRAINT consultations_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: medecins medecins_centre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medecins
    ADD CONSTRAINT medecins_centre_id_fkey FOREIGN KEY (centre_id) REFERENCES public.centres_sante(id);


--
-- Name: utilisateur utilisateur_medecin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_medecin_id_fkey FOREIGN KEY (medecin_id) REFERENCES public.medecins(id);


--
-- PostgreSQL database dump complete
--

