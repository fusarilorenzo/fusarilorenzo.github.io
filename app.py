# =============================================================
#  PORTFOLIO FUSARI - dati e logica in un unico file
# =============================================================
#  Come funzionano i dati multilingua:
#    - un testo uguale in tutte le lingue si scrive come stringa normale
#    - un testo tradotto si scrive come {"it": "...", "en": "...", "es": "...", "de": "...", "fr": "..."}
#    - se manca una lingua si usa l'inglese, poi l'italiano
#  La funzione t(valore, lingua) risolve tutto in automatico, anche dentro liste e dizionari.
# =============================================================
from flask import Flask, render_template, abort, redirect, url_for, request

app = Flask(__name__)

LANGS = ["it", "en", "es", "de", "fr"]
DEFAULT_LANG = "en"


def t(value, lang):
    """Sceglie la lingua in un valore (stringa, lista o dizionario annidato)."""
    if isinstance(value, dict):
        if value and set(value) <= set(LANGS):
            for code in (lang, DEFAULT_LANG, "it"):
                if value.get(code) not in (None, ""):
                    return t(value[code], lang)
            return t(next(iter(value.values())), lang)
        return {k: t(v, lang) for k, v in value.items()}
    if isinstance(value, list):
        return [t(v, lang) for v in value]
    return value


LABELS = {
    "ui": {
        "tema": {
            "it": "Cambia tema chiaro/scuro",
            "en": "Toggle light/dark theme",
            "es": "Cambiar tema claro/oscuro",
            "de": "Hell/Dunkel umschalten",
            "fr": "Basculer thème clair/sombre"
        }
    },
    "home": {
        "occupazione": {
            "it": "Sviluppatore Full-Stack",
            "en": "Full-Stack Developer",
            "es": "Desarrollador Full-Stack",
            "de": "Full-Stack-Entwickler",
            "fr": "Développeur Full-Stack"
        },
        "profilo": {
            "it": "Profilo Professionale",
            "en": "Professional Profile",
            "es": "Perfil Profesional",
            "de": "Berufsprofil",
            "fr": "Profil Professionnel"
        },
        "lingue": {
            "it": "Conoscenze Linguistiche",
            "en": "Language Skills",
            "es": "Competencias Lingüísticas",
            "de": "Sprachkenntnisse",
            "fr": "Compétences Linguistiques"
        },
        "progetti": {
            "it": "Progetti Realizzati",
            "en": "Projects",
            "es": "Proyectos Realizados",
            "de": "Projekte",
            "fr": "Projets Réalisés"
        },
        "vedi_dettaglio": {
            "it": "Vedi scheda dettaglio →",
            "en": "View details →",
            "es": "Ver detalles →",
            "de": "Details anzeigen →",
            "fr": "Voir les détails →"
        },
        "competizioni": {
            "it": "Competizioni e Gare Scientifiche",
            "en": "Competitions & Science Fairs",
            "es": "Competiciones y Ferias Científicas",
            "de": "Wettbewerbe und Wissenschaftsmessen",
            "fr": "Compétitions et Concours Scientifiques"
        },
        "certificazioni": {
            "it": "Certificazioni",
            "en": "Certifications",
            "es": "Certificaciones",
            "de": "Zertifizierungen",
            "fr": "Certifications"
        },
        "istruzione": {
            "it": "Istruzione e Formazione",
            "en": "Education & Training",
            "es": "Educación y Formación",
            "de": "Ausbildung",
            "fr": "Éducation et Formation"
        },
        "profitto": {
            "it": "Profitto di rilievo",
            "en": "Notable achievement",
            "es": "Logro destacado",
            "de": "Besondere Leistung",
            "fr": "Résultat remarquable"
        },
        "formazione_extra": {
            "it": "Formazione Specialistica Extra-Scolastica",
            "en": "Specialized Extra-Curricular Training",
            "es": "Formación Especializada Extracurricular",
            "de": "Außerschulische Fachausbildung",
            "fr": "Formation Spécialisée Extra-Scolaire"
        },
        "ente": {
            "it": "Ente",
            "en": "Institution",
            "es": "Institución",
            "de": "Einrichtung",
            "fr": "Organisme"
        },
        "competenze": {
            "it": "Competenze Tecniche",
            "en": "Technical Skills",
            "es": "Habilidades Técnicas",
            "de": "Technische Fähigkeiten",
            "fr": "Compétences Techniques"
        },
        "sport": {
            "it": "Attività Extracurriculari & Sport",
            "en": "Extracurricular Activities & Sports",
            "es": "Actividades Extracurriculares y Deportes",
            "de": "Außerschulische Aktivitäten & Sport",
            "fr": "Activités Extracurriculaires & Sports"
        },
        "atleta": {
            "it": "Atleta Agonista Ju-Jitsu",
            "en": "Competitive Ju-Jitsu Athlete",
            "es": "Atleta Competitivo de Ju-Jitsu",
            "de": "Ju-Jitsu-Wettkampfsportler",
            "fr": "Athlète Compétiteur de Ju-Jitsu"
        },
        "cert_gruppo_ict": {
            "it": "Competenze Digitali (ICDL)",
            "en": "Digital Skills (ICDL)",
            "es": "Competencias Digitales (ICDL)",
            "de": "Digitale Kompetenzen (ICDL)",
            "fr": "Compétences Numériques (ICDL)"
        },
        "cert_gruppo_lingue": {
            "it": "Certificazioni Linguistiche",
            "en": "Language Certifications",
            "es": "Certificaciones de Idiomas",
            "de": "Sprachzertifikate",
            "fr": "Certifications Linguistiques"
        }
    },
    "progetti": {
        "torna_home": {
            "it": "Torna al CV",
            "en": "Back to CV",
            "es": "Volver al CV",
            "de": "Zurück zum CV",
            "fr": "Retour au CV"
        },
        "ruolo": {
            "it": "Ruolo",
            "en": "Role",
            "es": "Rol",
            "de": "Rolle",
            "fr": "Rôle"
        },
        "panoramica_progetto": {
            "it": "Panoramica del Progetto",
            "en": "Project Overview",
            "es": "Descripción del Proyecto",
            "de": "Projektübersicht",
            "fr": "Aperçu du Projet"
        },
        "funzionalita_principali": {
            "it": "Funzionalità Principali",
            "en": "Key Features",
            "es": "Características Principales",
            "de": "Hauptfunktionen",
            "fr": "Fonctionnalités Principales"
        },
        "scheda_dettaglio": {
            "it": "Scheda Dettaglio",
            "en": "Detail Sheet",
            "es": "Ficha de Detalle",
            "de": "Detailansicht",
            "fr": "Fiche Détaillée"
        }
    },
    "achievements": {
        "titolo_pagina": {
            "it": "Achievement Microsoft Learn",
            "en": "Microsoft Learn Achievements",
            "es": "Logros de Microsoft Learn",
            "de": "Microsoft Learn Erfolge",
            "fr": "Réussites Microsoft Learn"
        },
        "sottotitolo": {
            "it": "Certificazioni e traguardi formativi riconosciuti ufficialmente da Microsoft.",
            "en": "Certifications and learning milestones officially recognized by Microsoft.",
            "es": "Certificaciones y logros de aprendizaje reconocidos oficialmente por Microsoft.",
            "de": "Offiziell von Microsoft anerkannte Zertifizierungen und Lernerfolge.",
            "fr": "Certifications et étapes d'apprentissage officiellement reconnues par Microsoft."
        },
        "bottone_verifica": {
            "it": "Vedi su Microsoft Learn",
            "en": "View on Microsoft Learn",
            "es": "Ver en Microsoft Learn",
            "de": "Auf Microsoft Learn ansehen",
            "fr": "Voir sur Microsoft Learn"
        },
        "ufficiale_badge": {
            "it": "Badge Ufficiale Microsoft",
            "en": "Official Microsoft Badge",
            "es": "Insignia Oficial de Microsoft",
            "de": "Offizielles Microsoft-Badge",
            "fr": "Badge Officiel Microsoft"
        },
        "button": {
            "it": "Vedi Tutti",
            "en": "View All",
            "es": "Ver Todo",
            "de": "Alle Anzeigen",
            "fr": "Tout Voir"
        }
    },
    "publications": {
        "titolo_pagina": {
            "it": "Pubblicazioni",
            "en": "Publications",
            "es": "Publicaciones",
            "de": "Veröffentlichungen",
            "fr": "Publications"
        },
        "sottotitolo": {
            "it": "Articoli, preprint e lavori pubblicati.",
            "en": "Articles, preprints and published work.",
            "es": "Artículos, preprints y trabajos publicados.",
            "de": "Artikel, Preprints und veröffentlichte Arbeiten.",
            "fr": "Articles, prépublications et travaux publiés."
        },
        "button": {
            "it": "Vedi Tutte",
            "en": "View All",
            "es": "Ver Todas",
            "de": "Alle Anzeigen",
            "fr": "Tout Voir"
        },
        "autori": {
            "it": "Autori",
            "en": "Authors",
            "es": "Autores",
            "de": "Autoren",
            "fr": "Auteurs"
        },
        "sede": {
            "it": "Pubblicato su",
            "en": "Published in",
            "es": "Publicado en",
            "de": "Veröffentlicht in",
            "fr": "Publié dans"
        },
        "bottone_apri": {
            "it": "Apri pubblicazione",
            "en": "Open publication",
            "es": "Abrir publicación",
            "de": "Veröffentlichung öffnen",
            "fr": "Ouvrir la publication"
        },
        "bottone_pdf": {
            "it": "Scarica PDF",
            "en": "Download PDF",
            "es": "Descargar PDF",
            "de": "PDF herunterladen",
            "fr": "Télécharger le PDF"
        },
        "vuoto": {
            "it": "Nessuna pubblicazione disponibile al momento.",
            "en": "No publications available yet.",
            "es": "Aún no hay publicaciones disponibles.",
            "de": "Noch keine Veröffentlichungen verfügbar.",
            "fr": "Aucune publication disponible pour le moment."
        },
        "in_evidenza": {
            "it": "In evidenza",
            "en": "Featured",
            "es": "Destacado",
            "de": "Hervorgehoben",
            "fr": "À la une"
        }
    },
    "404": {
        "titolo_scheda": {
            "it": "404 - Pagina Non Trovata",
            "en": "404 - Page Not Found",
            "es": "404 - Página No Encontrada",
            "de": "404 - Seite Nicht Gefunden",
            "fr": "404 - Page Non Trouvée"
        },
        "titolo": {
            "it": "Geroglifico Non Trovato",
            "en": "Hieroglyph Not Found",
            "es": "Jeroglífico No Encontrado",
            "de": "Hieroglyphe Nicht Gefunden",
            "fr": "Hiéroglyphe Non Trouvé"
        },
        "sottotitolo": {
            "it": "La pagina che cerchi è stata sepolta dalle sabbie del tempo o si trova in una tomba inaccessibile.",
            "en": "The page you are looking for has been buried by the sands of time or lies in an inaccessible tomb.",
            "es": "La página que buscas ha sido sepultada por las arenas del tiempo o se encuentra en una tumba inaccesible.",
            "de": "Die von Ihnen gesuchte Seite wurde vom Sand der Zeit begraben oder befindet sich in einem unzugänglichen Grab.",
            "fr": "La page que vous recherchez a été enfouie sous les sables du temps ou se trouve dans une tombe inaccessible."
        },
        "bottone": {
            "it": "Ritorna alla Civiltà (Home)",
            "en": "Return to Civilization (Home)",
            "es": "Volver a la Civilización (Inicio)",
            "de": "Zurück zur Zivilisation (Startseite)",
            "fr": "Retour à la Civilisation (Accueil)"
        }
    }
}

CV = {
    "nome": "Lorenzo Fusari",
    "citta": {
        "it": "San Giovanni in Persiceto (BO), Italia",
        "en": "San Giovanni in Persiceto (BO), Italy",
        "es": "San Giovanni in Persiceto (BO), Italia",
        "de": "San Giovanni in Persiceto (BO), Italien",
        "fr": "San Giovanni in Persiceto (BO), Italie"
    },
    "telefono": "+39 371-479-2122",
    "email": "fusarilorenzo@icloud.com",
    "profilo": {
        "it": "Studente del Liceo Scientifico ad indirizzo Scienze Applicate con potenziamento Scientifico e Informatico. Sviluppatore con competenze nell'ambito della programmazione full-stack e nella creazione di applicazioni e siti web.",
        "en": "Applied Sciences High School student with advanced coursework in Computer Science and STEM subjects. Full-stack developer skilled in building web applications, mobile apps, and custom software solutions.",
        "es": "Estudiante de Bachillerato Científico con orientación en Ciencias Aplicadas e Informática. Desarrollador con competencias en programación full-stack y creación de aplicaciones y sitios web.",
        "de": "Schüler des Naturwissenschaftlichen Gymnasiums mit Schwerpunkt Angewandte Wissenschaften und Informatik. Entwickler mit Kenntnissen in Full-Stack-Programmierung und Erstellung von Webanwendungen.",
        "fr": "Élève au Lycée Scientifique (Sciences Appliquées) avec option renforcée en Informatique. Développeur spécialisé en programmation full-stack et création d'applications web et mobiles."
    },
    "istruzione": {
        "it": "Liceo Scientifico opzione Scienze Applicate (potenziamento Informatico) - Liceo A. B. Sabin",
        "en": "Applied Sciences High School (Computer Science Track) - Liceo A. B. Sabin",
        "es": "Bachillerato Científico orientación Ciencias Aplicadas (Informática) - Liceo A. B. Sabin",
        "de": "Naturwissenschaftliches Gymnasium (Schwerpunkt Informatik) - Liceo A. B. Sabin",
        "fr": "Lycée Scientifique option Sciences Appliquées (Spécialité Informatique) - Liceo A. B. Sabin"
    },
    "voti": {
        "it": "Informatica 10/10 Matematica: 8/10",
        "en": "Computer Science: 10/10 | Mathematics: 8/10",
        "es": "Informática: 10/10 | Matemáticas: 8/10",
        "de": "Informatik: 10/10 | Mathematik: 8/10",
        "fr": "Informatique : 10/10 | Mathématiques : 8/10"
    },
    "competenze": [
        {
            "it": "Programmazione Full-Stack",
            "en": "Full-Stack Programming",
            "es": "Programación Full-Stack",
            "de": "Full-Stack-Programmierung",
            "fr": "Programmation Full-Stack"
        },
        {
            "it": "Sviluppo App Mobile",
            "en": "Mobile App Development",
            "es": "Desarrollo de Apps Móviles",
            "de": "Mobile App-Entwicklung",
            "fr": "Développement d'Apps Mobiles"
        },
        {
            "it": "Sviluppo Web",
            "en": "Web Development",
            "es": "Desarrollo Web",
            "de": "Webentwicklung",
            "fr": "Développement Web"
        },
        {
            "it": "Pacchetto Office",
            "en": "Microsoft Office Suite",
            "es": "Paquete Office",
            "de": "Microsoft Office-Paket",
            "fr": "Suite Microsoft Office"
        }
    ],
    "competizioni": [
        {
            "it": "Partecipante Olimpiadi di Informatica (Selezione territoriale) 2026 con punteggio 100",
            "en": "Olympiad in Informatics (Regional Selection) 2026 - Score: 100",
            "es": "Olimpiadas de Informática (Selección Territorial) 2026 - Puntuación: 100",
            "de": "Informatik-Olympiade (Regionalklassifizierung) 2026 - Punktzahl: 100",
            "fr": "Olympiades d'Informatique (Sélection Régionale) 2026 - Score : 100"
        },
        {
            "it": "Partecipante Olimpiadi di informatica (Selezione scolastica) 2026 con punteggio 55",
            "en": "Olympiad in Informatics (School Selection) 2026 - Score: 55",
            "es": "Olimpiadas de Informática (Selección Escolar) 2026 - Puntuación: 55",
            "de": "Informatik-Olympiade (Schulauswahl) 2026 - Punktzahl: 55",
            "fr": "Olympiades d'Informatique (Sélection Scolaire) 2026 - Score : 55"
        },
        {
            "it": "Partecipante Giochi di Archimede ex Olimpiadi di Matematica (Selezione scolastica) 2026 con punteggio 43",
            "en": "Archimedes Contest / Math Olympiad (School Selection) 2026 - Score: 43",
            "es": "Juegos de Arquímedes / Olimpiadas de Matemáticas (Selección Escolar) 2026 - Puntuación: 43",
            "de": "Archimedes-Mathematik-Wettbewerb (Schulauswahl) 2026 - Punktzahl: 43",
            "fr": "Concours d'Archimède / Olympiades de Mathématiques (Sélection Scolaire) 2026 - Score : 43"
        },
        {
            "it": "Partecipante Giochi di Archimede ex Olimpiadi di Matematica (Selezione scolastica) 2025 con punteggio 20",
            "en": "Archimedes Contest / Math Olympiad (School Selection) 2025 - Score: 20",
            "es": "Juegos de Arquímedes / Olimpiadas de Matemáticas (Selección Escolar) 2025 - Puntuación: 20",
            "de": "Archimedes-Mathematik-Wettbewerb (Schulauswahl) 2025 - Punktzahl: 20",
            "fr": "Concours d'Archimède / Olympiades de Mathématiques (Sélection Scolaire) 2025 - Score : 20"
        }
    ],
    "certificazioni": [
        {
            "nome": "ICDL Spreadsheets (Excel)",
            "ente": "AICA",
            "pdf": "icdl_excel.pdf",
            "gruppo": "ict"
        },
        {
            "nome": "ICDL Word Processing",
            "ente": "AICA",
            "pdf": "icdl_word.pdf",
            "gruppo": "ict"
        },
        {
            "nome": "ICDL Presentation",
            "ente": "AICA",
            "pdf": "icdl_presentation.pdf",
            "gruppo": "ict"
        },
        {
            "nome": "ICDL IT-Security/Cyber Security",
            "ente": "AICA",
            "pdf": "icdl_cybersecurity.pdf",
            "gruppo": "ict"
        },
        {
            "nome": "ICDL Computer Essentials",
            "ente": "AICA",
            "pdf": "icdl_computeressentials.pdf",
            "gruppo": "ict"
        },
        {
            "nome": "EF SET English Certificate - C2 Proficient",
            "ente": "EF Standard English Test",
            "pdf": "efset_english.pdf",
            "gruppo": "lingue"
        },
        {
            "nome": "Speexx Español Core - A1",
            "ente": "Speexx Corporate Language Training",
            "pdf": "certificato_spagnolo_a1.pdf",
            "gruppo": "lingue"
        }
    ],
    "sport": [
        {
            "it": "Medaglia di Bronzo ai Campionati Italiani U18 Ju-Jitsu 2026",
            "en": "Bronze Medalist - U18 Ju-Jitsu Italian National Championships 2026",
            "es": "Medalla de Bronce - Campeonato Italiano U18 de Ju-Jitsu 2026",
            "de": "Bronzemedaille - U18 Ju-Jitsu Italienische Meisterschaften 2026",
            "fr": "Médaille de Bronze - Championnat d'Italie U18 de Ju-Jitsu 2026"
        },
        {
            "it": "Campione Regionale FIJLKAM U16 Ju-Jitsu 2025",
            "en": "FIJLKAM U16 Ju-Jitsu Regional Champion 2025",
            "es": "Campeón Regional FIJLKAM U16 de Ju-Jitsu 2025",
            "de": "FIJLKAM U16 Ju-Jitsu Regionalmeister 2025",
            "fr": "Champion Régional FIJLKAM U16 de Ju-Jitsu 2025"
        },
        {
            "it": "9° Posto al Mediterranean Open U16 Ju-Jitsu 2025",
            "en": "9th Place - Mediterranean Open U16 Ju-Jitsu 2025",
            "es": "9º Puesto - Mediterranean Open U16 Ju-Jitsu 2025",
            "de": "9. Platz - Mediterranean Open U16 Ju-Jitsu 2025",
            "fr": "9e Place - Mediterranean Open U16 Ju-Jitsu 2025"
        },
        {
            "it": "Medaglia di Bronzo al Genoa Open U16 Ju-Jitsu 2025",
            "en": "Bronze Medalist - Genoa Open U16 Ju-Jitsu 2025",
            "es": "Medalla de Bronce - Genoa Open U16 Ju-Jitsu 2025",
            "de": "Bronzemedaille - Genoa Open U16 Ju-Jitsu 2025",
            "fr": "Médaille de Bronze - Genoa Open U16 Ju-Jitsu 2025"
        },
        {
            "it": "7° Posto ai Campionati Italiani U16 Ju-jitsu 2025",
            "en": "7th Place - U16 Ju-Jitsu Italian National Championships 2025",
            "es": "7º Puesto - Campeonato Italiano U16 de Ju-Jitsu 2025",
            "de": "7. Platz - U16 Ju-Jitsu Italienische Meisterschaften 2025",
            "fr": "7e Place - Championnat d'Italie U16 de Ju-Jitsu 2025"
        }
    ],
    "social": [
        {
            "nome": "GitHub",
            "url": "https://github.com/fusarilorenzo",
            "icona_class": "fa-brands fa-github"
        },
        {
            "nome": "ORCID",
            "url": "https://orcid.org/0009-0007-4723-2887",
            "icona_class": "fa-brands fa-orcid"
        },
        {
            "nome": "Zenodo",
            "url": "https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Fusari%2C%20Lorenzo%22&l=list&p=1&s=10&sort=bestmatch",
            "icona_class": "fa-solid fa-box-archive"
        },
        {
            "nome": "Google Scholar",
            "url": "https://scholar.google.com/citations?hl=it&user=QRnhSWIAAAAJ",
            "icona_class": "fa-solid fa-graduation-cap"
        },
        {
            "nome": "Microsoft Learn",
            "url": "https://learn.microsoft.com/en-us/users/lorenzofusari-0956/",
            "icona_class": "fa-brands fa-microsoft"
        }
    ],
    "lingue": [
        {
            "lingua": {
                "it": "Italiano",
                "en": "Italian",
                "es": "Italiano",
                "de": "Italienisch",
                "fr": "Italien"
            },
            "livello": {
                "it": "Madrelingua",
                "en": "Native",
                "es": "Nativo",
                "de": "Muttersprache",
                "fr": "Langue maternelle"
            },
            "dettaglio": {
                "it": "Lingua principale",
                "en": "Primary language",
                "es": "Lengua materna",
                "de": "Hauptsprache",
                "fr": "Langue principale"
            }
        },
        {
            "lingua": {
                "it": "Inglese (Reading & Listening)",
                "en": "English (Reading & Listening)",
                "es": "Inglés (Reading & Listening)",
                "de": "Englisch (Reading & Listening)",
                "fr": "Anglais (Reading & Listening)"
            },
            "livello": {
                "it": "C2 Proficient",
                "en": "C2 Proficient",
                "es": "C2 Proficient",
                "de": "C2 Proficient",
                "fr": "C2 Expérimenté"
            },
            "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"
        },
        {
            "lingua": {
                "it": "Spagnolo",
                "en": "Spanish",
                "es": "Español",
                "de": "Spanisch",
                "fr": "Espagnol"
            },
            "livello": {
                "it": "A1 Beginner",
                "en": "A1 Beginner",
                "es": "A1 Principiante",
                "de": "A1 Anfänger",
                "fr": "A1 Débutant"
            },
            "dettaglio": {
                "it": "Certificazione Speexx Business Language 99/100",
                "en": "Speexx Business Language Certification 99/100",
                "es": "Certificación Speexx Business Language 99/100",
                "de": "Speexx Business Language Zertifikat 99/100",
                "fr": "Certification Speexx Business Language 99/100"
            }
        }
    ],
    "corsi_formazione": [
        {
            "titolo": "Python Programming Language",
            "ente": {
                "it": "Kodland (Scuola Internazionale di Programmazione)",
                "en": "Kodland (International Programming School)",
                "es": "Kodland (Escuela Internacional de Programación)",
                "de": "Kodland (Internationale Programmierschule)",
                "fr": "Kodland (École Internationale de Programmation)"
            },
            "periodo": {
                "it": "09/09/2022 - 05/05/2023",
                "en": "09/09/2022 - 05/05/2023",
                "es": "09/09/2022 - 05/05/2023",
                "de": "09.09.2022 - 05.05.2023",
                "fr": "09/09/2022 - 05/05/2023"
            },
            "competenze": [
                "Python",
                "Pgzero / Pygame",
                {
                    "it": "Algoritmi & Logica di Programmazione",
                    "en": "Algorithms & Programming Logic",
                    "es": "Algoritmos y Lógica de Programación",
                    "de": "Algorithmen & Programmierlogik",
                    "fr": "Algorithmes & Logique de Programmation"
                }
            ],
            "descrizione": {
                "it": "Corso di 9 mesi focalizzato sulle basi della programmazione orientata agli oggetti con Python e sulla progettazione di videogiochi 2D usando il framework Pgzero.",
                "en": "9-month course focused on Object-Oriented Programming fundamentals in Python and 2D game design using the Pgzero framework.",
                "es": "Curso de 9 meses enfocado en los fundamentos de programación orientada a objetos con Python y diseño de videojuegos 2D con Pgzero.",
                "de": "9-monatiger Kurs mit Schwerpunkt auf objektorientierter Programmierung in Python und 2D-Spieleentwicklung mit Pgzero.",
                "fr": "Formation de 9 mois axée sur les bases de la programmation orientée objet en Python et le développement de jeux 2D avec Pgzero."
            },
            "diploma": {
                "nome": {
                    "it": "Diploma Livello 1",
                    "en": "Level 1 Diploma",
                    "es": "Diploma Nivel 1",
                    "de": "Diplom Stufe 1",
                    "fr": "Diplôme Niveau 1"
                },
                "file": "kodland_diploma_1.pdf"
            }
        },
        {
            "titolo": "Python Pro",
            "ente": {
                "it": "Kodland (Scuola Internazionale di Programmazione)",
                "en": "Kodland (International Programming School)",
                "es": "Kodland (Escuela Internacional de Programación)",
                "de": "Kodland (Internationale Programmierschule)",
                "fr": "Kodland (École Internationale de Programmation)"
            },
            "periodo": {
                "it": "23/11/2023 - 01/08/2024",
                "en": "23/11/2023 - 01/08/2024",
                "es": "23/11/2023 - 01/08/2024",
                "de": "23.11.2023 - 01.08.2024",
                "fr": "23/11/2023 - 01/08/2024"
            },
            "competenze": [
                "Flask",
                "HTML/CSS",
                "Discord Bot API",
                {
                    "it": "Teachable Machine (AI)",
                    "en": "Teachable Machine (AI)",
                    "es": "Teachable Machine (AI)",
                    "de": "Teachable Machine (KI)",
                    "fr": "Teachable Machine (IA)"
                }
            ],
            "descrizione": {
                "it": "Corso avanzato dalla durata di 9 mesi dedicato al backend web con Flask, creazione di bot interattivi per Discord e integrazione di modelli di Machine Learning per il riconoscimento visivo.",
                "en": "Advanced 9-month course covering backend web development with Flask, interactive Discord bots, and Machine Learning image recognition models.",
                "es": "Curso avanzado de 9 meses sobre desarrollo backend web con Flask, creación de bots para Discord e integración de modelos de Machine Learning.",
                "de": "Fortgeschrittener 9-monatiger Kurs über Web-Backend mit Flask, interaktive Discord-Bots und Einbindung von Machine-Learning-Modellen.",
                "fr": "Formation avancée de 9 mois sur le backend web avec Flask, la création de bots Discord et l'intégration de modèles d'apprentissage automatique."
            },
            "diploma": {
                "nome": {
                    "it": "Diploma Livello 2",
                    "en": "Level 2 Diploma",
                    "es": "Diploma Nivel 2",
                    "de": "Diplom Stufe 2",
                    "fr": "Diplôme Niveau 2"
                },
                "file": "kodland_diploma_2.pdf"
            }
        }
    ]
}


# -------------------------------------------------------------
#  PROGETTI (scheda dettaglio + descrizione breve per la home)
# -------------------------------------------------------------
PROJECTS = {
    "app-asd": {
        "id": "app-asd",
        "titolo": {
            "it": "App Mobile per ASD Locale",
            "en": "Mobile App for Local Sports Club",
            "es": "App Móvil para Club Deportivo Local",
            "de": "Mobile App für Lokalen Sportverein",
            "fr": "Application Mobile pour Club Sportif Local"
        },
        "categoria": {
            "it": "Sviluppo Mobile",
            "en": "Mobile Development",
            "es": "Desarrollo Móvil",
            "de": "Mobile-Entwicklung",
            "fr": "Développement Mobile"
        },
        "ruolo": {
            "it": "Sviluppatore Sole / Full-Stack",
            "en": "Sole / Full-Stack Developer",
            "es": "Desarrollador Único / Full-Stack",
            "de": "Alleinentwickler / Full-Stack",
            "fr": "Développeur Unique / Full-Stack"
        },
        "tecnologie": [
            "Swift",
            "Kotlin",
            "Firebase",
            "REST API",
            "Google Apps Script"
        ],
        "descrizione_completa": {
            "it": "Scrittura e pubblicazione di un'applicazione mobile per un'associazione sportiva dilettantistica locale per permettere agli atleti di poter sempre vedere i loro risultati nell'anno sportivo in corso, iscriversi alle gare, vedere tutti gli eventi della loro squadra. Gestione dei dati collegati all'utente con un codice personale generato dal codice alla creazione dell'account. Per comunicare con i servizi Fogli Google è stato usato Google Apps Script con il linguaggio JavaScript. L'applicazione è stata creata usando due linguaggi di codice: per iOS e iPadOS è stato usato Swift con il framework SwiftUI, per Android è stato usato Kotlin con il framework Jetpack Compose.",
            "en": "Development and release of a mobile app for a local amateur sports club, allowing athletes to track their current season results, register for competitions, and view team events. User data is managed via a personal identification code generated upon account creation. Google Apps Script with JavaScript was used to communicate with Google Sheets. The application was built natively: Swift with SwiftUI for iOS/iPadOS, and Kotlin with Jetpack Compose for Android.",
            "es": "Desarrollo y publicación de una aplicación móvil para un club deportivo amateur local, permitiendo a los atletas consultar sus resultados de la temporada actual, inscribirse en competiciones y ver los eventos del equipo. La gestión de datos por usuario se realiza mediante un código personal generado al crear la cuenta. Se utilizó Google Apps Script con JavaScript para interactuar con Google Sheets. La app fue desarrollada de forma nativa: Swift con SwiftUI para iOS/iPadOS y Kotlin con Jetpack Compose para Android.",
            "de": "Entwicklung und Veröffentlichung einer mobilen Anwendung für einen lokalen Amateursportverein. Die App ermöglicht es Athleten, ihre Ergebnisse der aktuellen Saison einzusehen, sich für Wettkämpfe anzumelden und Teamtermine zu verfolgen. Benutzerdaten werden über einen persönlichen Code verwaltet, der bei der Kontoerstellung generiert wird. Für die Kommunikation mit Google Sheets wurde Google Apps Script mit JavaScript verwendet. Die Anwendung wurde nativ entwickelt: Swift mit SwiftUI für iOS/iPadOS und Kotlin mit Jetpack Compose für Android.",
            "fr": "Conception et publication d'une application mobile pour un club sportif amateur local, permettant aux athlètes de consulter leurs résultats de la saison, de s'inscrire aux compétitions et de suivre les événements de l'équipe. Les données utilisateur sont gérées via un code personnel généré lors de la création du compte. Google Apps Script avec JavaScript a été utilisé pour interagir avec Google Sheets. L'application est développée nativement : Swift avec SwiftUI pour iOS/iPadOS et Kotlin avec Jetpack Compose pour Android."
        },
        "funzionalita": [
            {
                "it": "Autenticazione utenti e gestione profili atleti",
                "en": "User authentication and athlete profile management",
                "es": "Autenticación de usuarios y gestión de perfiles de atletas",
                "de": "Benutzerauthentifizierung und Verwaltung von Athletenprofilen",
                "fr": "Authentification des utilisateurs et gestion des profils d'athlètes"
            },
            {
                "it": "Notifiche push per comunicazioni urgenti e gare",
                "en": "Push notifications for urgent announcements and competitions",
                "es": "Notificaciones push para anuncios urgentes y competiciones",
                "de": "Push-Benachrichtigungen für dringende Mitteilungen und Wettkämpfe",
                "fr": "Notifications push pour les annonces urgentes et compétitions"
            },
            {
                "it": "Integrazione calendario con eventi ed allenamenti",
                "en": "Calendar integration for events and training sessions",
                "es": "Integración de calendario con eventos y entrenamientos",
                "de": "Kalenderintegration für Veranstaltungen und Trainingseinheiten",
                "fr": "Intégration du calendrier pour les événements et entraînements"
            },
            {
                "it": "Visualizzazione dei risultati dell'anno agonistico",
                "en": "Display of competitive season results",
                "es": "Visualización de resultados de la temporada competitiva",
                "de": "Anzeige der Ergebnisse der Wettkampfsaison",
                "fr": "Affichage des résultats de la saison sportive"
            },
            {
                "it": "Possibilità di iscrizione alle gare",
                "en": "Online competition registration",
                "es": "Inscripción en línea a competiciones",
                "de": "Online-Anmeldung zu Wettkämpfen",
                "fr": "Inscription en ligne aux compétitions"
            }
        ],
        "descrizione_breve": {
            "it": "Progettazione, sviluppo e pubblicazione negli store ufficiali di un'app per un'associazione sportiva dilettantistica.",
            "en": "Design, development, and publishing to official stores of a mobile application for an amateur sports club.",
            "es": "Diseño, desarrollo y publicación en tiendas oficiales de una aplicación para un club deportivo aficionado.",
            "de": "Konzeption, Entwicklung und Veröffentlichung einer mobilen Anwendung für einen Amateursportverein in den offiziellen Stores.",
            "fr": "Conception, développement et publication sur les stores officiels d'une application mobile pour un club sportif amateur."
        }
    },
    "sito-commissione": {
        "id": "sito-commissione",
        "titolo": {
            "it": "Sito Web su Commissione",
            "en": "Commissioned Website",
            "es": "Sitio Web por Encargo",
            "de": "Website im Auftrag",
            "fr": "Site Web sur Commande"
        },
        "categoria": {
            "it": "Sviluppo Web Full-Stack",
            "en": "Full-Stack Web Development",
            "es": "Desarrollo Web Full-Stack",
            "de": "Full-Stack-Webentwicklung",
            "fr": "Développement Web Full-Stack"
        },
        "ruolo": {
            "it": "Web Developer & Designer",
            "en": "Web Developer & Designer",
            "es": "Diseñador y Desarrollador Web",
            "de": "Webentwickler & Designer",
            "fr": "Développeur Web & Designer"
        },
        "tecnologie": [
            "HTML5/CSS3",
            "JavaScript",
            "WordPress"
        ],
        "descrizione_completa": {
            "it": "Realizzazione di una piattaforma web personalizzata su commissione per cliente privato. Il sito include un totale di quattro pagine, due in italiano e due in inglese. Il sito ricopre la classica forma dei siti vetrina. Organizzato con WordPress e la funzione 'Codice Personalizzato' è stato usato HTML con CSS per la grafica e JavaScript per accedere alla galleria interna di WordPress. Le immagini sono state divise in due categorie usando i plugin offerti dalla comunity in maniera che ogni pagina avesse le proprie immagini senza creare conflitti.",
            "en": "Creation of a custom web platform commissioned by a private client. The site consists of four pages (two in Italian and two in English) following a showcase website structure. Built on WordPress using custom code, combining HTML and CSS for styling and JavaScript to access WordPress's native media gallery. Images are categorized using community plugins to prevent asset conflicts across languages.",
            "es": "Creación de una plataforma web personalizada por encargo para un cliente privado. El sitio consta de cuatro páginas (dos en italiano y dos en inglés) siguiendo el formato de un sitio corporativo/escaparate. Estructurado en WordPress con código personalizado (HTML y CSS para la interfaz, JavaScript para interactuar con la galería interna de WordPress). Las imágenes se categorizaron con plugins de la comunidad para evitar conflictos entre secciones.",
            "de": "Erstellung einer maßgeschneiderten Webplattform im Auftrag eines Privatkunden. Die Website umfasst insgesamt vier Seiten (zwei auf Italienisch und zwei auf Englisch) im klassischen Showcase-Stil. Aufgebaut auf WordPress unter Verwendung von benutzerdefiniertem Code (HTML und CSS für das Design, JavaScript für den Zugriff auf die interne WordPress-Galerie). Bilder wurden mithilfe von Community-Plugins kategorisiert, um Konflikte zwischen den Seiten zu vermeiden.",
            "fr": "Réalisation d'une plateforme web personnalisée sur commande pour un client privé. Le site comprend un total de quatre pages (deux en italien et deux en anglais) sous forme de site vitrine. Conçu sur WordPress avec du code personnalisé (HTML et CSS pour le design, JavaScript pour accéder à la galerie interne WordPress). Les images ont été catégorisées à l'aide de plugins de la communauté afin d'éviter les conflits entre les langues."
        },
        "funzionalita": [
            {
                "it": "Design responsive adattabile a tutti i dispositivi",
                "en": "Responsive design adapted for all devices",
                "es": "Diseño adaptable (responsive) para todos los dispositivos",
                "de": "Responsives Design für alle Geräte",
                "fr": "Design responsive adapté à tous les appareils"
            },
            {
                "it": "Ottimizzazione SEO on-page per motori di ricerca",
                "en": "On-page SEO optimization for search engines",
                "es": "Optimización SEO on-page para motores de búsqueda",
                "de": "On-Page-SEO-Optimierung für Suchmaschinen",
                "fr": "Optimisation SEO on-page pour les moteurs de recherche"
            }
        ],
        "descrizione_breve": {
            "it": "Realizzazione di un sito web strutturato su commissione per cliente privato.",
            "en": "Full end-to-end design and deployment of a responsive website commissioned by a private client.",
            "es": "Desarrollo completo de un sitio web estructurado por encargo para un cliente privado.",
            "de": "Erstellung einer strukturierten Website im Auftrag eines privaten Kunden.",
            "fr": "Réalisation complète d'un site web structuré sur commande pour un client privé."
        }
    },
}


# -------------------------------------------------------------
#  ACHIEVEMENT MICROSOFT LEARN
#  "data": anno ("2026") oppure data completa ("2026-03-14"); piu' e' precisa,
#  piu' e' giusto l'ordine "ultimi 3" in home. Il primo della lista vince a parita' di data.
# -------------------------------------------------------------
ACHIEVEMENTS_DATA = [
    {"id": "t01", "titolo": "GitHub Foundations 2 of 2", "badge_icon": "fa-github", "categoria": "GitHub Learning Paths", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/9AK44T9U?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "t02", "titolo": "GitHub fundamentals - Administration basics and procedures Part 1 of 2", "badge_icon": "fa-github", "categoria": "GitHub Learning Paths", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/9AK44YTU?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "t03", "titolo": "GitHub Foundations Part 1 of 2", "badge_icon": "fa-github", "categoria": "GitHub Learning Paths", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/FEL5SG9X?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b01", "titolo": "Using GitHub Copilot with Python", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/FEL559NX?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b02", "titolo": "Search and organize repository history by using GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/3ZDBBJLH?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b03", "titolo": "Manage repository changes by using pull requests on GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/9AK4448U?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b04", "titolo": "Authenticate and authorize user identities on GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/H2JDDPW8?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b05", "titolo": "Introduction to GitHub administration", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/8VTJJZLW?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b06", "titolo": "Maintain a secure repository using GitHub best practices", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/NQ5SS73F?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b07", "titolo": "Manage an InnerSource program by using GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/VS8H3VXM?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b08", "titolo": "Contribute to an open-source project on GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/8VTJD9MW?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b09", "titolo": "Communicate effectively GitHub using Markdown", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/H2JDBT58?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b10", "titolo": "Manage your work with GitHub Projects", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/D37AXW3J?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b11", "titolo": "Code with GitHub Codespaces", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/4CYX8R7K?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b12", "titolo": "Introduction to GitHub Copilot", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/U7BKQKW3?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b13", "titolo": "Responsible AI with GitHub Copilot", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/9AK4MACU?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b14", "titolo": "Configure code scanning on GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/9AK4MNSU?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b15", "titolo": "Introduction to GitHub's products", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/8VTJERCW?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b16", "titolo": "Introduction to GitHub", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/3ZDBVTAH?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b17", "titolo": "Introduction to Git", "badge_icon": "fa-github", "categoria": "GitHub", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/JHZ78AJT?sharingId=B2FB6AE8EAE1BC15"},
    {"id": "b18", "titolo": "Write your first C# code", "badge_icon": "fa-microsoft", "categoria": "Microsoft C# Code Language", "data": "2026", "link": "https://learn.microsoft.com/api/achievements/share/en-us/LorenzoFusari-0956/EGF3AHZP?sharingId=B2FB6AE8EAE1BC15"},
]

# -------------------------------------------------------------
#  PUBBLICAZIONI  -  qui aggiungi / modifichi tu i dati
# -------------------------------------------------------------
#  Ogni pubblicazione e' un dizionario dentro la lista PUBLICATIONS.
#  Per aggiungerne una: copia il TEMPLATE qui sotto, incollalo dentro la lista e compila i campi.
#
#  Campi:
#    id            identificativo breve, univoco
#    titolo        titolo della pubblicazione
#    anno          es. "2026"  (in pagina l'ordine e' dal piu' recente)
#    tipo          "Articolo", "Preprint", "Tesi"...  (stringa oppure dict per lingua)
#    autori        es. "Lorenzo Fusari, Mario Rossi"
#    sede          "Zenodo", "UniBo", rivista, conferenza...  (la parola Zenodo / UniBo / Bologna
#                  mette in automatico l'icona giusta)
#    doi           OPZIONALE, es. "10.5281/zenodo.1234567"  (se manca "link" usa https://doi.org/<doi>)
#    link          OPZIONALE, URL della pubblicazione
#    pdf           OPZIONALE, nome di un file in static/pdf/
#    descrizione   dict lingua -> testo (it, en, es, de, fr). Lingua mancante: si usa en, poi it.
#    tag           OPZIONALE, lista di parole chiave
#    in_evidenza   OPZIONALE, True = in home compare per prima, in grande, con il badge "In evidenza"
#
#  TEMPLATE:
#  {
#      "id": "mia-pubblicazione",
#      "titolo": "Titolo",
#      "anno": "2026",
#      "tipo": {"it": "Articolo", "en": "Article", "es": "Artículo", "de": "Artikel", "fr": "Article"},
#      "autori": "Lorenzo Fusari",
#      "sede": "UniBo",
#      "doi": "",
#      "link": "https://...",
#      "pdf": "file.pdf",
#      "descrizione": {"it": "...", "en": "...", "es": "...", "de": "...", "fr": "..."},
#      "tag": ["Python"],
#      "in_evidenza": False,
#  },

PUBLICATIONS = [
    {
        "id": "sub-quadratic1",
        "titolo": "Sub-Quadratic O(N) Context Scaling via Vectorized Selective State Space Models",
        "anno": "2026",
        "tipo": {"it": "Articolo", "en": "Article", "es": "Artículo", "de": "Artikel", "fr": "Article"},
        "autori": "Lorenzo Fusari",
        "sede": "Zenodo",
        "doi": "10.5281/zenodo.23195265",
        "link": "https://zenodo.org/records/23195265",
        "pdf": "sub-quadratic1.pdf",
        "descrizione": {
            "en": "Theoretical Foundations, hardware Kernels, Empirical Apple Silicon Benchmarks, and Extreme Scaling Horizons to Library-Scale (~800B Tokens)"
        },
        "tag": ["Python", "AI", "SSMs"],
        "in_evidenza": True,
    },
]

# icona in base alla sede (parola contenuta nel campo "sede", minuscolo)
VENUE_ICONS = {
    "zenodo": "fa-solid fa-box-archive",
    "unibo": "fa-solid fa-building-columns",
    "bologna": "fa-solid fa-building-columns",
}
DEFAULT_VENUE_ICON = "fa-solid fa-book"


# -------------------------------------------------------------
#  LOGICA
# -------------------------------------------------------------
CERT_GROUPS = ["ict", "lingue"]  # ordine dei gruppi di certificazioni


def get_labels(section, lang):
    return t(LABELS[section], lang)


def get_cv(lang):
    cv = t(CV, lang)
    labels = get_labels("home", lang)
    cv["progetti"] = [
        {"id": pid, "titolo": p["titolo"], "descrizione_breve": p["descrizione_breve"]}
        for pid, p in t(PROJECTS, lang).items()
    ]
    cv["certificazioni_gruppi"] = [
        {"titolo": labels["cert_gruppo_" + g], "elenco": [c for c in cv["certificazioni"] if c["gruppo"] == g]}
        for g in CERT_GROUPS
        if any(c["gruppo"] == g for c in cv["certificazioni"])
    ]
    return cv


def get_achievements():
    """Dal piu' recente. A parita' di data resta l'ordine della lista (primo = piu' recente)."""
    return sorted(ACHIEVEMENTS_DATA, key=lambda a: a.get("data", ""), reverse=True)


def get_achievement_groups():
    groups = {}
    for a in get_achievements():
        groups.setdefault(a["categoria"], []).append(a)
    return [{"nome": nome, "icona": items[0]["badge_icon"], "elenco": items} for nome, items in groups.items()]


def get_publications(lang):
    """Pubblicazioni gia' tradotte in `lang`, dalla piu' recente."""
    result = []
    for pub in PUBLICATIONS:
        item = t(pub, lang)
        if not item.get("link") and item.get("doi"):
            item["link"] = "https://doi.org/" + item["doi"]
        sede = str(item.get("sede", "")).lower()
        item["sede_icona"] = next((icon for key, icon in VENUE_ICONS.items() if key in sede), DEFAULT_VENUE_ICON)
        item.setdefault("tag", [])
        result.append(item)
    result.sort(key=lambda p: str(p.get("anno", "")), reverse=True)
    return result


def render_home(lang, is_root=False):
    pubs = get_publications(lang)
    # in evidenza per prime, poi le piu' recenti; in home al massimo 3
    anteprima = [p for p in pubs if p.get("in_evidenza")] + [p for p in pubs if not p.get("in_evidenza")]
    return render_template(
        'index.html',
        cv=get_cv(lang),
        labels=get_labels("home", lang),
        current_lang=lang,
        is_root=is_root,
        achievements=get_achievements()[:3],
        labels_achievements=get_labels("achievements", lang),
        publications=anteprima[:3],
        labels_publications=get_labels("publications", lang),
    )


@app.context_processor
def inject_ui():
    parts = request.path.strip('/').split('/')
    lang = parts[0] if parts and parts[0] in LANGS else DEFAULT_LANG
    return {"ui": get_labels("ui", lang), "langs": LANGS}


@app.route('/')
def home_default():
    return render_home(DEFAULT_LANG, is_root=True)


@app.route('/<lang>/')
def home(lang):
    if lang not in LANGS:
        return redirect(url_for('home', lang=DEFAULT_LANG))
    return render_home(lang)


@app.route('/<lang>/progetto/<id_progetto>/')
def dettaglio_progetto(lang, id_progetto):
    if lang not in LANGS:
        lang = DEFAULT_LANG
    progetto = t(PROJECTS, lang).get(id_progetto)
    if not progetto:
        abort(404)
    return render_template('dettaglio_progetto.html', progetto=progetto, labels=get_labels("progetti", lang), cv=get_cv(lang), current_lang=lang)


@app.route('/<lang>/achievements/')
def achievements(lang):
    if lang not in LANGS:
        return redirect(url_for('achievements', lang=DEFAULT_LANG))
    return render_template('achievements.html', groups=get_achievement_groups(), total=len(ACHIEVEMENTS_DATA), cv=get_cv(lang), labels=get_labels("achievements", lang), current_lang=lang)


@app.route('/<lang>/publications/')
def publications(lang):
    if lang not in LANGS:
        return redirect(url_for('publications', lang=DEFAULT_LANG))
    return render_template('publications.html', publications=get_publications(lang), cv=get_cv(lang), labels=get_labels("publications", lang), current_lang=lang)


@app.errorhandler(404)
def page_not_found(e):
    parts = request.path.strip('/').split('/')
    lang = parts[0] if parts and parts[0] in LANGS else DEFAULT_LANG
    return render_template('404.html', labels=get_labels("404", lang), current_lang=lang), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
