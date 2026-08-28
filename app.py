from flask import Flask, render_template, abort, redirect, url_for, request

app = Flask(__name__)

LABELS_404 = {
    "it": {
        "titolo_scheda": "404 - Pagina Non Trovata",
        "titolo": "Geroglifico Non Trovato",
        "sottotitolo": "La pagina che cerchi è stata sepolta dalle sabbie del tempo o si trova in una tomba inaccessibile.",
        "bottone": "Ritorna alla Civiltà (Home)"
    },
    "en": {
        "titolo_scheda": "404 - Page Not Found",
        "titolo": "Hieroglyph Not Found",
        "sottotitolo": "The page you are looking for has been buried by the sands of time or lies in an inaccessible tomb.",
        "bottone": "Return to Civilization (Home)"
    },
    "es": {
        "titolo_scheda": "404 - Página No Encontrada",
        "titolo": "Jeroglífico No Encontrado",
        "sottotitolo": "La página que buscas ha sido sepultada por las arenas del tiempo o se encuentra en una tumba inaccesible.",
        "bottone": "Volver a la Civilización (Inicio)"
    },
    "de": {
        "titolo_scheda": "404 - Seite Nicht Gefunden",
        "titolo": "Hieroglyphe Nicht Gefunden",
        "sottotitolo": "Die von Ihnen gesuchte Seite wurde vom Sand der Zeit begraben oder befindet sich in einem unzugänglichen Grab.",
        "bottone": "Zurück zur Zivilisation (Startseite)"
    },
    "fr": {
        "titolo_scheda": "404 - Page Non Trouvée",
        "titolo": "Hiéroglyphe Non Trouvé",
        "sottotitolo": "La page que vous recherchez a été enfouie sous les sables du temps ou se trouve dans une tombe inaccessible.",
        "bottone": "Retour à la Civilisation (Accueil)"
    }
}

LABELS_PROGETTI = {
	"it": {
		"torna_home": "Torna al CV",
		"ruolo": "Ruolo",
		"panoramica_progetto": "Panoramica del Progetto",
		"funzionalita_principali": "Funzionalità Principali",
		"scheda_dettaglio": "Scheda Dettaglio"
	},
	"en": {
		"torna_home": "Back to CV",
		"ruolo": "Role",
		"panoramica_progetto": "Project Overview",
		"funzionalita_principali": "Key Features",
		"scheda_dettaglio": "Detail Sheet"
	},
	"es": {
		"torna_home": "Volver al CV",
		"ruolo": "Rol",
		"panoramica_progetto": "Descripción del Proyecto",
		"funzionalita_principali": "Características Principales",
		"scheda_dettaglio": "Ficha de Detalle"
	},
	"de": {
		"torna_home": "Zurück zum CV",
		"ruolo": "Rolle",
		"panoramica_progetto": "Projektübersicht",
		"funzionalita_principali": "Hauptfunktionen",
		"scheda_dettaglio": "Detailansicht"
	},
	"fr": {
		"torna_home": "Retour au CV",
		"ruolo": "Rôle",
		"panoramica_progetto": "Aperçu du Projet",
		"funzionalita_principali": "Fonctionnalités Principales",
		"scheda_dettaglio": "Fiche Détaillée"
	}
}

LABELS_HOME = {
	"it": {
        "occupazione": "Sviluppatore Full-Stack",
        "profilo": "Profilo Professionale",
        "lingue": "Conoscenze Linguistiche",
        "progetti": "Progetti Realizzati",
        "vedi_dettaglio": "Vedi scheda dettaglio →",
        "competizioni": "Competizioni e Gare Scientifiche",
        "certificazioni": "Certificazioni",
        "istruzione": "Istruzione e Formazione",
        "profitto": "Profitto di rilievo",
        "formazione_extra": "Formazione Specialistica Extra-Scolastica",
        "ente": "Ente",
        "competenze": "Competenze Tecniche",
        "sport": "Attività Extracurriculari & Sport",
        "atleta": "Atleta Agonista Ju-Jitsu"
    },
    "en": {
        "occupazione": "Full-Stack Developer",
        "profilo": "Professional Profile",
        "lingue": "Language Skills",
        "progetti": "Projects",
        "vedi_dettaglio": "View details →",
        "competizioni": "Competitions & Science Fairs",
        "certificazioni": "Certifications",
        "istruzione": "Education & Training",
        "profitto": "Notable achievement",
        "formazione_extra": "Specialized Extra-Curricular Training",
        "ente": "Institution",
        "competenze": "Technical Skills",
        "sport": "Extracurricular Activities & Sports",
        "atleta": "Competitive Ju-Jitsu Athlete"
    },
    "es": {
        "occupazione": "Desarrollador Full-Stack",
        "profilo": "Perfil Profesional",
        "lingue": "Competencias Lingüísticas",
        "progetti": "Proyectos Realizados",
        "vedi_dettaglio": "Ver detalles →",
        "competizioni": "Competiciones y Ferias Científicas",
        "certificazioni": "Certificaciones",
        "istruzione": "Educación y Formación",
        "profitto": "Logro destacado",
        "formazione_extra": "Formación Especializada Extracurricular",
        "ente": "Institución",
        "competenze": "Habilidades Técnicas",
        "sport": "Actividades Extracurriculares y Deportes",
        "atleta": "Atleta Competitivo de Ju-Jitsu"
    },
    "de": {
        "occupazione": "Full-Stack-Entwickler",
        "profilo": "Berufsprofil",
        "lingue": "Sprachkenntnisse",
        "progetti": "Projekte",
        "vedi_dettaglio": "Details anzeigen →",
        "competizioni": "Wettbewerbe und Wissenschaftsmessen",
        "certificazioni": "Zertifizierungen",
        "istruzione": "Ausbildung",
        "profitto": "Besondere Leistung",
        "formazione_extra": "Außerschulische Fachausbildung",
        "ente": "Einrichtung",
        "competenze": "Technische Fähigkeiten",
        "sport": "Außerschulische Aktivitäten & Sport",
        "atleta": "Ju-Jitsu-Wettkampfsportler"
    },
    "fr": {
        "occupazione": "Développeur Full-Stack",
        "profilo": "Profil Professionnel",
        "lingue": "Compétences Linguistiques",
        "progetti": "Projets Réalisés",
        "vedi_dettaglio": "Voir les détails →",
        "competizioni": "Compétitions et Concours Scientifiques",
        "certificazioni": "Certifications",
        "istruzione": "Éducation et Formation",
        "profitto": "Résultat meuble",
        "formazione_extra": "Formation Spécialisée Extra-Scolaire",
        "ente": "Organisme",
        "competenze": "Compétences Techniques",
        "sport": "Activités Extracurriculaires & Sports",
        "atleta": "Athlète Compétiteur de Ju-Jitsu"
    }
}

progetti_dettaglio_it = {
	"app-asd": {
		"id": "app-asd",
		"titolo": "App Mobile per ASD Locale",
		"categoria": "Sviluppo Mobile",
		"ruolo": "Sviluppatore Sole / Full-Stack",
		"tecnologie": ["Swift", "Kotlin", "Firebase", "REST API", "Google Apps Script"],
		"descrizione_completa": "Scrittura e pubblicazione di un'applicazione mobile per un'associazione sportiva dillettantistica locale per permettere agli atleti di poter sempre vedere i loro risultati nell'anno sportivo in corso, iscriversi alle gare, vedere tutti gli eventi della loro squadra. Gestione dei dati collegati all'utente con un codice personale generato dal codice alla creazione dell'account. Per comunicare con i servizi Fogli Google è stato usato Google Apps Script con il linguaggio JavaScript. L'applicazione è stata creata usando due linguaggi di codice: per iOS e iPadOS è stato usato Swift con il framework SwiftUI, per Android è stato usato Kotlin con il framework Jetpack Compose.",
		"funzionalita": [
			"Autenticazione utenti e gestione profili atleti",
			"Notifiche push per comunicazioni urgenti e gare",
			"Integrazione calendario con eventi ed allenamenti",
			"Visualizzazione dei risultati dell'anno agonistico",
			"Possibilità di iscrizione alle gare"
		]
	},
	"sito-commissione": {
		"id": "sito-commissione",
		"titolo": "Sito Web su Commissione",
		"categoria": "Sviluppo Web Full-Stack",
		"ruolo": "Web Developer & Designer",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "WordPress7"],
		"descrizione_completa": "Realizzazione di una piattaforma web personalizzata su commissione per cliente privato. Il sito include un totale di quattro pagine, due in italiano e due in inglese. Il sito ricopre la classica forma dei siti vetrina. Organizzato con WordPress e la funzione 'Codice Personalizzato' è stato usato HTML con CSS per la grafica e JavaScript per accedere alla galleria interna di WordPress. Le immagini sono state divise in due categorie usando i plugin offerti dalla comunity in maniera che ogni paggina avesse le proprie immagini senza creare conflitti.",
		"funzionalita": [
			"Design responsive adattabile a tutti i dispositivi",
			"Ottimizzazione SEO on-page per motori di ricerca"
		]
	},
	"sito-matrimonio": {
		"id": "sito-matrimonio",
		"titolo": "Sito Web per Matrimonio",
		"categoria": "Sviluppo Web App Full-Stack",
		"ruolo": "Web Developer & Designer",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "Python3.13", "Flask"],
		"descrizione_completa": "Realizzazione di una web app personalizzata su commissione per un matrimonio. Il sito include due pagine, una per la lingua italiana e una per la lingua francese, in maniera da ricoprire tutti gli invitati con meno fatica possibile. Il sito richiama il tema del matrimonio con i font e la grafica dello sfondo descritta nel CSS. Il testo viene estratto da dei file .txt presenti nei file locali del progetto. Le lettere vengono 'scritte' da una bandiera pirata generata e gestita da uno script JavaScript posto al termine del file HTML.",
		"funzionalita": [
			"Design adattabile a tutti i dispositivi",
			"Header in contrasto con il corpo del sito"
		]
	}
}

progetti_dettaglio_en = {
    "app-asd": {
        "id": "app-asd",
        "titolo": "Mobile App for Local Sports Club",
        "categoria": "Mobile Development",
        "ruolo": "Sole / Full-Stack Developer",
        "tecnologie": ["Swift", "Kotlin", "Firebase", "REST API", "Google Apps Script"],
        "descrizione_completa": "Development and release of a mobile app for a local amateur sports club, allowing athletes to track their current season results, register for competitions, and view team events. User data is managed via a personal identification code generated upon account creation. Google Apps Script with JavaScript was used to communicate with Google Sheets. The application was built natively: Swift with SwiftUI for iOS/iPadOS, and Kotlin with Jetpack Compose for Android.",
        "funzionalita": [
            "User authentication and athlete profile management",
            "Push notifications for urgent announcements and competitions",
            "Calendar integration for events and training sessions",
            "Display of competitive season results",
            "Online competition registration"
        ]
    },
    "sito-commissione": {
        "id": "sito-commissione",
        "titolo": "Commissioned Website",
        "categoria": "Full-Stack Web Development",
        "ruolo": "Web Developer & Designer",
        "tecnologie": ["HTML5/CSS3", "JavaScript", "WordPress"],
        "descrizione_completa": "Creation of a custom web platform commissioned by a private client. The site consists of four pages (two in Italian and two in English) following a showcase website structure. Built on WordPress using custom code, combining HTML and CSS for styling and JavaScript to access WordPress's native media gallery. Images are categorized using community plugins to prevent asset conflicts across languages.",
        "funzionalita": [
            "Responsive design adapted for all devices",
            "On-page SEO optimization for search engines"
        ]
    },
    "sito-matrimonio": {
		"id": "sito-matrimonio",
		"titolo": "Wedding Web App",
		"categoria": "Full-Stack Web App Development",
		"ruolo": "Web Developer & Designer",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "Python3.13", "Flask"],
		"descrizione_completa": "Creation of a custom commissioned web application for a wedding. The site features two language pages (Italian and French) to accommodate all guests seamlessly. The design aligns with the wedding's pirate theme through custom typography and background styling in CSS. Content is dynamically read from local .txt files. Text is rendered using a animated 'writing' pirate flag effect generated and managed by a JavaScript script placed at the bottom of the HTML document.",
		"funzionalita": [
			"Fully responsive design across all devices",
			"High-contrast header styling relative to the main body"
		]
	}
}

progetti_dettaglio_es = {
    "app-asd": {
        "id": "app-asd",
        "titolo": "App Móvil para Club Deportivo Local",
        "categoria": "Desarrollo Móvil",
        "ruolo": "Desarrollador Único / Full-Stack",
        "tecnologie": ["Swift", "Kotlin", "Firebase", "REST API", "Google Apps Script"],
        "descrizione_completa": "Desarrollo y publicación de una aplicación móvil para un club deportivo amateur local, permitiendo a los atletas consultar sus resultados de la temporada actual, inscribirse en competiciones y ver los eventos del equipo. La gestión de datos por usuario se realiza mediante un código personal generado al crear la cuenta. Se utilizó Google Apps Script con JavaScript para interactuar con Google Sheets. La app fue desarrollada de forma nativa: Swift con SwiftUI para iOS/iPadOS y Kotlin con Jetpack Compose para Android.",
        "funzionalita": [
            "Autenticación de usuarios y gestión de perfiles de atletas",
            "Notificaciones push para anuncios urgentes y competiciones",
            "Integración de calendario con eventos y entrenamientos",
            "Visualización de resultados de la temporada competitiva",
            "Inscripción en línea a competiciones"
        ]
    },
    "sito-commissione": {
        "id": "sito-commissione",
        "titolo": "Sitio Web por Encargo",
        "categoria": "Desarrollo Web Full-Stack",
        "ruolo": "Diseñador y Desarrollador Web",
        "tecnologie": ["HTML5/CSS3", "JavaScript", "WordPress"],
        "descrizione_completa": "Creación de una plataforma web personalizada por encargo para un cliente privado. El sitio consta de cuatro páginas (dos en italiano y dos en inglés) siguiendo el formato de un sitio corporativo/escaparate. Estructurado en WordPress con código personalizado (HTML y CSS para la interfaz, JavaScript para interactuar con la galería interna de WordPress). Las imágenes se categorizaron con plugins de la comunidad para evitar conflictos entre secciones.",
        "funzionalita": [
            "Diseño adaptable (responsive) para todos los dispositivos",
            "Optimización SEO on-page para motores de búsqueda"
        ]
    },
    "sito-matrimonio": {
		"id": "sito-matrimonio",
		"titolo": "Aplicación Web para Boda",
		"categoria": "Desarrollo Web App Full-Stack",
		"ruolo": "Diseñador y Desarrollador Web",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "Python3.13", "Flask"],
		"descrizione_completa": "Creación de una aplicación web personalizada por encargo para una boda. El sitio incluye dos páginas (una en italiano y otra en francés) para atender fácilmente a todos los invitados. La interfaz refleja el tema pirata de la boda mediante tipografías y estilos de fondo en CSS. El contenido de texto se extrae de archivos .txt locales del proyecto. Los textos se visualizan con un efecto de 'escritura' mediante una bandera pirata generada y controlada por un script en JavaScript ubicado al final del archivo HTML.",
		"funzionalita": [
			"Diseño adaptable a todo tipo de dispositivos",
			"Encabezado en contraste visual con el cuerpo de la página"
		]
	}
}

progetti_dettaglio_de = {
    "app-asd": {
        "id": "app-asd",
        "titolo": "Mobile App für Lokalen Sportverein",
        "categoria": "Mobile-Entwicklung",
        "ruolo": "Alleinentwickler / Full-Stack",
        "tecnologie": ["Swift", "Kotlin", "Firebase", "REST API", "Google Apps Script"],
        "descrizione_completa": "Entwicklung und Veröffentlichung einer mobilen Anwendung für einen lokalen Amateursportverein. Die App ermöglicht es Athleten, ihre Ergebnisse der aktuellen Saison einzusehen, sich für Wettkämpfe anzumelden und Teamtermine zu verfolgen. Benutzerdaten werden über einen persönlichen Code verwaltet, der bei der Kontoerstellung generiert wird. Für die Kommunikation mit Google Sheets wurde Google Apps Script mit JavaScript verwendet. Die Anwendung wurde nativ entwickelt: Swift mit SwiftUI für iOS/iPadOS und Kotlin mit Jetpack Compose für Android.",
        "funzionalita": [
            "Benutzerauthentifizierung und Verwaltung von Athletenprofilen",
            "Push-Benachrichtigungen für dringende Mitteilungen und Wettkämpfe",
            "Kalenderintegration für Veranstaltungen und Trainingseinheiten",
            "Anzeige der Ergebnisse der Wettkampfsaison",
            "Online-Anmeldung zu Wettkämpfen"
        ]
    },
    "sito-commissione": {
        "id": "sito-commissione",
        "titolo": "Website im Auftrag",
        "categoria": "Full-Stack-Webentwicklung",
        "ruolo": "Webentwickler & Designer",
        "tecnologie": ["HTML5/CSS3", "JavaScript", "WordPress"],
        "descrizione_completa": "Erstellung einer maßgeschneiderten Webplattform im Auftrag eines Privatkunden. Die Website umfasst insgesamt vier Seiten (zwei auf Italienisch und zwei auf Englisch) im klassischen Showcase-Stil. Aufgebaut auf WordPress unter Verwendung von benutzerdefiniertem Code (HTML und CSS für das Design, JavaScript für den Zugriff auf die interne WordPress-Galerie). Bilder wurden mithilfe von Community-Plugins kategorisiert, um Konflikte zwischen den Seiten zu vermeiden.",
        "funzionalita": [
            "Responsives Design für alle Geräte",
            "On-Page-SEO-Optimierung für Suchmaschinen"
        ]
    },
    "sito-matrimonio": {
		"id": "sito-matrimonio",
		"titolo": "Hochzeits-Web-App",
		"categoria": "Full-Stack-Webanwendungsentwicklung",
		"ruolo": "Webentwickler & Designer",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "Python3.13", "Flask"],
		"descrizione_completa": "Erstellung einer maßgeschneiderten Webanwendung im Auftrag für eine Hochzeit. Die Website umfasst zwei Sprachseiten (Italienisch und Französisch), um alle Gäste problemlos zu erreichen. Das Design spiegelt das Piraten-Motto der Hochzeit durch spezielle Schriftarten und Hintergrundgrafiken im CSS wider. Die Textinhalte werden aus lokalen .txt-Dateien des Projekts ausgelesen. Der Text wird mit einem dynamischen 'Schreib-Effekt' durch eine Piratenflagge dargestellt, die von einem JavaScript-Skript am Ende der HTML-Datei gesteuert wird.",
		"funzionalita": [
			"Anpassungsfähiges Design für alle Endgeräte",
			"Kontrastreicher Header im Vergleich zum Hauptbereich"
		]
	}
}

progetti_dettaglio_fr = {
    "app-asd": {
        "id": "app-asd",
        "titolo": "Application Mobile pour Club Sportif Local",
        "categoria": "Développement Mobile",
        "ruolo": "Développeur Unique / Full-Stack",
        "tecnologie": ["Swift", "Kotlin", "Firebase", "REST API", "Google Apps Script"],
        "descrizione_completa": "Conception et publication d'une application mobile pour un club sportif amateur local, permettant aux athlètes de consulter leurs résultats de la saison, de s'inscrire aux compétitions et de suivre les événements de l'équipe. Les données utilisateur sont gérées via un code personnel généré lors de la création du compte. Google Apps Script avec JavaScript a été utilisé pour interagir avec Google Sheets. L'application est développée nativement : Swift avec SwiftUI pour iOS/iPadOS et Kotlin avec Jetpack Compose pour Android.",
        "funzionalita": [
            "Authentification des utilisateurs et gestion des profils d'athlètes",
            "Notifications push pour les annonces urgentes et compétitions",
            "Intégration du calendrier pour les événements et entraînements",
            "Affichage des résultats de la saison sportive",
            "Inscription en ligne aux compétitions"
        ]
    },
    "sito-commissione": {
        "id": "sito-commissione",
        "titolo": "Site Web sur Commande",
        "categoria": "Développement Web Full-Stack",
        "ruolo": "Développeur Web & Designer",
        "tecnologie": ["HTML5/CSS3", "JavaScript", "WordPress"],
        "descrizione_completa": "Réalisation d'une plateforme web personnalisée sur commande pour un client privé. Le site comprend un total de quatre pages (deux en italien et deux en anglais) sous forme de site vitrine. Conçu sur WordPress avec du code personnalisé (HTML et CSS pour le design, JavaScript pour accéder à la galerie interne WordPress). Les images ont été catégorisées à l'aide de plugins de la communauté afin d'éviter les conflits entre les langues.",
        "funzionalita": [
            "Design responsive adapté à tous les appareils",
            "Optimisation SEO on-page pour les moteurs de recherche"
        ]
    },
    "sito-matrimonio": {
		"id": "sito-matrimonio",
		"titolo": "Application Web de Mariage",
		"categoria": "Développement Web App Full-Stack",
		"ruolo": "Développeur Web & Designer",
		"tecnologie": ["HTML5/CSS3", "JavaScript", "Python3.13", "Flask"],
		"descrizione_completa": "Réalisation d'une application web sur mesure pour un mariage. Le site comprend deux pages (une en italien et une en français) afin d'accueillir facilement tous les invités. Le style visuel rappelle le thème des pirates grâce à des polices personnalisées et des graphismes d'arrière-plan en CSS. Les textes sont extraits de fichiers .txt locaux. L'affichage du texte simule une écriture générée par un drapeau pirate, piloté par un script JavaScript placé en bas du fichier HTML.",
		"funzionalita": [
			"Design adaptable à tous les types d'écrans",
			"En-tête en contraste visuel avec le corps de la page"
		]
	}
}

cv_data_it = {
	"nome": "Lorenzo Fusari",
	"citta": "San Giovanni in Persiceto (BO)",
	"telefono": "+39 371-479-2122",
	"email": "fusarilorenzo@icloud.com",
	"profilo": "Studente del Liceo Scientifico ad indirizzo Scienze Applicate con potenziamento Scientifico e Informatico. Sviluppatore con competenze nell'ambito della programmazione full-stack e nella creazione di applicazioni e siti web.",
	"istruzione": "Liceo Scientifico opzione Scienze Applicate (potenziamento Informatico) - Liceo A. B. Sabin",
	"voti": "Informatica 10/10 Matematica: 8/10",
	"competenze": ["Programmazione Full-Stack", "Sviluppo App Mobile", "Sviluppo Web", "Pacchetto Office"],
	"competizioni": [
		"Partecipante Olimpiadi di Informatica (Selezione territoriale) 2026 con punteggio 100",
		"Partecipante Olimpiadi di informatica (Selezione scolastica) 2026 con punteggio 55",
		"Partecipante Giochi di Archimede ex Olimpiadi di Matematica (Selezione scolastica) 2026 con punteggio 43",
		"Partecipante Giochi di Archimede ex Olimpiadi di Matematica (Selezione scolastica) 2025 con punteggio 20"
	],
	"certificazioni": [
		{"nome": "ICDL Spreadsheets (Excel)", "ente": "AICA", "pdf": "icdl_excel.pdf"},
		{"nome": "ICDL Word Processing", "ente": "AICA", "pdf": "icdl_word.pdf"},
		{"nome": "ICDL Presentation", "ente": "AICA", "pdf": "icdl_presentation.pdf"},
		{"nome": "ICDL IT-Security/Cyber Security", "ente": "AICA", "pdf": "icdl_cybersecurity.pdf"},
		{"nome": "ICDL Computer Essentials", "ente": "AICA", "pdf": "icdl_computeressentials.pdf"},
		{"nome": "EF SET English Certificate - C2 Proficient", "ente": "EF Standard English Test", "pdf": "efset_english.pdf"},
		{"nome": "Speexx Español Core - A1", "ente": "Speexx Corporate Language Training", "pdf": "certificato_spagnolo_a1.pdf"}
	],
	"sport": [
		"Medaglia di Bronzo ai Campionati Italiani U18 Ju-Jitsu 2026",
		"Campione Regionale FIJLKAM U16 Ju-Jitsu 2025",
		"9° Posto al Mediterranean Open U16 Ju-Jitsu 2025",
		"Medaglia di Bronzo al Genoa Open U16 Ju-Jitsu 2025",
		"7° Posto ai Campionati Italiani U16 Ju-jitsu 2025"
	],
	"progetti": [
		{
			"id": "app-asd",
			"titolo": "App Mobile per ASD Locale",
			"descrizione_breve": "Progettazione, sviluppo e pubblicazione negli store ufficiali di un'app per un'associazione sportiva dillettantistica."
		},
		{
			"id": "sito-commissione",
			"titolo": "Sito Web su Comissione",
			"descrizione_breve": "Realizzazione di un sito web strutturato su commissione per cliente privato."
		},
		{
			"id": "sito-matrimonio",
			"titolo": "Sito Web per Matrimonio",
			"descrizione_breve": "Realizzazione di un sito web in Flask per un matrimonio a tema pirati."
		}
	],
	"social": [
		{"nome": "GitHub", "url": "https://github.com/fusarilorenzo", "icona_class": "fa-brands fa-github"},
		{"nome": "ORCID", "url": "https://orcid.org/0009-0007-4723-2887", "icona_class": "fa-brands fa-orcid"},
		{"nome": "Zenodo", "url": "https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Fusari%2C%20Lorenzo%22&l=list&p=1&s=10&sort=bestmatch", "icona_class": "fa-solid fa-box-archive"},
		{"nome": "Google Scholar", "url": "https://scholar.google.com/citations?hl=it&user=QRnhSWIAAAAJ", "icona_class": "fa-solid fa-graduation-cap"}
	],
	"lingue": [
		{"lingua": "Italiano", "livello": "Madrelingua", "dettaglio": "Lingua principale"},
		{"lingua": "Inglese (Reading & Listening)", "livello": "C2 Proficient", "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"},
		{"lingua": "Spagnolo", "livello": "A1 Beginner", "dettaglio": "Certificazione Speexx Business Language 99/100"}
	],
	"corsi_formazione": [
		{
			"titolo": "Python Programming Language",
			"ente": "Kodland (Scuola Internazionale di Programmazione)",
			"periodo": "09/09/2022 - 05/05/2023",
			"competenze": ["Python", "Pgzero / Pygame", "Algoritmi & Logica di Programmazione"],
			"descrizione": "Corso di 9 mesi focalizzato sulle basi della programmazione orientata agli oggetti con Python e sulla progettazione di videogiochi 2D usando il framework Pgzero.",
			"diploma": {
				"nome": "Diploma Livello 1",
				"file": "kodland_diploma_1.pdf"
			}
		},
		{
			"titolo": "Python Pro",
			"ente": "Kodland (Scuola Internazionale di Programmazione)",
			"periodo": "23/11/2023 - 01/08/2024",
			"competenze": ["Flask", "HTML/CSS", "Discord Bot API", "Teachable Machine (AI)"],
			"descrizione": "Corso avanzato dalla durata di 9 mesi dedicato al backend web con Flask, creazione di bot interattivi per Discord e integrazione di modelli di Machine Learning per il riconoscimento visivo.",
			"diploma": {
				"nome": "Diploma Livello 2",
				"file": "kodland_diploma_2.pdf"
			}
		}
	]
}

cv_data_en = {
    "nome": "Lorenzo Fusari",
    "citta": "San Giovanni in Persiceto (BO), Italy",
    "telefono": "+39 371-479-2122",
    "email": "fusarilorenzo@icloud.com",
    "profilo": "Applied Sciences High School student with advanced coursework in Computer Science and STEM subjects. Full-stack developer skilled in building web applications, mobile apps, and custom software solutions.",
    "istruzione": "Applied Sciences High School (Computer Science Track) - Liceo A. B. Sabin",
    "voti": "Computer Science: 10/10 | Mathematics: 8/10",
    "competenze": ["Full-Stack Programming", "Mobile App Development", "Web Development", "Microsoft Office Suite"],
    "competizioni": [
        "Olympiad in Informatics (Regional Selection) 2026 - Score: 100",
        "Olympiad in Informatics (School Selection) 2026 - Score: 55",
        "Archimedes Contest / Math Olympiad (School Selection) 2026 - Score: 43",
        "Archimedes Contest / Math Olympiad (School Selection) 2025 - Score: 20"
    ],
    "certificazioni": [
        {"nome": "ICDL Spreadsheets (Excel)", "ente": "AICA", "pdf": "icdl_excel.pdf"},
        {"nome": "ICDL Word Processing", "ente": "AICA", "pdf": "icdl_word.pdf"},
        {"nome": "ICDL Presentation", "ente": "AICA", "pdf": "icdl_presentation.pdf"},
        {"nome": "ICDL IT-Security/Cyber Security", "ente": "AICA", "pdf": "icdl_cybersecurity.pdf"},
        {"nome": "ICDL Computer Essentials", "ente": "AICA", "pdf": "icdl_computeressentials.pdf"},
        {"nome": "EF SET English Certificate - C2 Proficient", "ente": "EF Standard English Test", "pdf": "efset_english.pdf"},
        {"nome": "Speexx Español Core - A1", "ente": "Speexx Corporate Language Training", "pdf": "certificato_spagnolo_a1.pdf"}
    ],
    "sport": [
        "Bronze Medalist - U18 Ju-Jitsu Italian National Championships 2026",
        "FIJLKAM U16 Ju-Jitsu Regional Champion 2025",
        "9th Place - Mediterranean Open U16 Ju-Jitsu 2025",
        "Bronze Medalist - Genoa Open U16 Ju-Jitsu 2025",
        "7th Place - U16 Ju-Jitsu Italian National Championships 2025"
    ],
    "progetti": [
        {
            "id": "app-asd",
            "titolo": "Mobile App for Local Sports Association",
            "descrizione_breve": "Design, development, and publishing to official stores of a mobile application for an amateur sports club."
        },
        {
            "id": "sito-commissione",
            "titolo": "Custom Freelance Website",
            "descrizione_breve": "Full end-to-end design and deployment of a responsive website commissioned by a private client."
        },
        {
			"id": "sito-matrimonio",
			"titolo": "Wedding Website",
			"descrizione_breve": "Development of a Flask web platform for a pirate-themed wedding."
		}
    ],
    "social": cv_data_it["social"],
    "lingue": [
        {"lingua": "Italian", "livello": "Native", "dettaglio": "Primary language"},
        {"lingua": "English (Reading & Listening)", "livello": "C2 Proficient", "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"},
        {"lingua": "Spanish", "livello": "A1 Beginner", "dettaglio": "Speexx Business Language Certification 99/100"}
    ],
    "corsi_formazione": [
        {
            "titolo": "Python Programming Language",
            "ente": "Kodland (International Programming School)",
            "periodo": "09/09/2022 - 05/05/2023",
            "competenze": ["Python", "Pgzero / Pygame", "Algorithms & Programming Logic"],
            "descrizione": "9-month course focused on Object-Oriented Programming fundamentals in Python and 2D game design using the Pgzero framework.",
            "diploma": {
                "nome": "Level 1 Diploma",
                "file": "kodland_diploma_1.pdf"
            }
        },
        {
            "titolo": "Python Pro",
            "ente": "Kodland (International Programming School)",
            "periodo": "23/11/2023 - 01/08/2024",
            "competenze": ["Flask", "HTML/CSS", "Discord Bot API", "Teachable Machine (AI)"],
            "descrizione": "Advanced 9-month course covering backend web development with Flask, interactive Discord bots, and Machine Learning image recognition models.",
            "diploma": {
                "nome": "Level 2 Diploma",
                "file": "kodland_diploma_2.pdf"
            }
        }
    ]
}

cv_data_es = {
    "nome": "Lorenzo Fusari",
    "citta": "San Giovanni in Persiceto (BO), Italia",
    "telefono": "+39 371-479-2122",
    "email": "fusarilorenzo@icloud.com",
    "profilo": "Estudiante de Bachillerato Científico con orientación en Ciencias Aplicadas e Informática. Desarrollador con competencias en programación full-stack y creación de aplicaciones y sitios web.",
    "istruzione": "Bachillerato Científico orientación Ciencias Aplicadas (Informática) - Liceo A. B. Sabin",
    "voti": "Informática: 10/10 | Matemáticas: 8/10",
    "competenze": ["Programación Full-Stack", "Desarrollo de Apps Móviles", "Desarrollo Web", "Paquete Office"],
    "competizioni": [
        "Olimpiadas de Informática (Selección Territorial) 2026 - Puntuación: 100",
        "Olimpiadas de Informática (Selección Escolar) 2026 - Puntuación: 55",
        "Juegos de Arquímedes / Olimpiadas de Matemáticas (Selección Escolar) 2026 - Puntuación: 43",
        "Juegos de Arquímedes / Olimpiadas de Matemáticas (Selección Escolar) 2025 - Puntuación: 20"
    ],
    "certificazioni": [
        {"nome": "ICDL Spreadsheets (Excel)", "ente": "AICA", "pdf": "icdl_excel.pdf"},
        {"nome": "ICDL Word Processing", "ente": "AICA", "pdf": "icdl_word.pdf"},
        {"nome": "ICDL Presentation", "ente": "AICA", "pdf": "icdl_presentation.pdf"},
        {"nome": "ICDL IT-Security/Cyber Security", "ente": "AICA", "pdf": "icdl_cybersecurity.pdf"},
        {"nome": "ICDL Computer Essentials", "ente": "AICA", "pdf": "icdl_computeressentials.pdf"},
        {"nome": "EF SET English Certificate - C2 Proficient", "ente": "EF Standard English Test", "pdf": "efset_english.pdf"},
        {"nome": "Speexx Español Core - A1", "ente": "Speexx Corporate Language Training", "pdf": "certificato_spagnolo_a1.pdf"}
    ],
    "sport": [
        "Medalla de Bronce - Campeonato Italiano U18 de Ju-Jitsu 2026",
        "Campeón Regional FIJLKAM U16 de Ju-Jitsu 2025",
        "9º Puesto - Mediterranean Open U16 Ju-Jitsu 2025",
        "Medalla de Bronce - Genoa Open U16 Ju-Jitsu 2025",
        "7º Puesto - Campeonato Italiano U16 de Ju-Jitsu 2025"
    ],
    "progetti": [
        {
            "id": "app-asd",
            "titolo": "App Móvil para Asociación Deportiva Local",
            "descrizione_breve": "Diseño, desarrollo y publicación en tiendas oficiales de una aplicación para un club deportivo aficionado."
        },
        {
            "id": "sito-commissione",
            "titolo": "Sitio Web por Encargo",
            "descrizione_breve": "Desarrollo completo de un sitio web estructurado por encargo para un cliente privado."
        },
        {
			"id": "sito-matrimonio",
			"titolo": "Sitio Web de Boda",
			"descrizione_breve": "Desarrollo de un sitio web en Flask para una boda con temática pirata."
		}
    ],
    "social": cv_data_it["social"],
    "lingue": [
        {"lingua": "Italiano", "livello": "Nativo", "dettaglio": "Lengua materna"},
        {"lingua": "Inglés (Reading & Listening)", "livello": "C2 Proficient", "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"},
        {"lingua": "Español", "livello": "A1 Principiante", "dettaglio": "Certificación Speexx Business Language 99/100"}
    ],
    "corsi_formazione": [
        {
            "titolo": "Python Programming Language",
            "ente": "Kodland (Escuela Internacional de Programación)",
            "periodo": "09/09/2022 - 05/05/2023",
            "competenze": ["Python", "Pgzero / Pygame", "Algoritmos y Lógica de Programación"],
            "descrizione": "Curso de 9 meses enfocado en los fundamentos de programación orientada a objetos con Python y diseño de videojuegos 2D con Pgzero.",
            "diploma": {
                "nome": "Diploma Nivel 1",
                "file": "kodland_diploma_1.pdf"
            }
        },
        {
            "titolo": "Python Pro",
            "ente": "Kodland (Escuela Internacional de Programación)",
            "periodo": "23/11/2023 - 01/08/2024",
            "competenze": ["Flask", "HTML/CSS", "Discord Bot API", "Teachable Machine (AI)"],
            "descrizione": "Curso avanzado de 9 meses sobre desarrollo backend web con Flask, creación de bots para Discord e integración de modelos de Machine Learning.",
            "diploma": {
                "nome": "Diploma Nivel 2",
                "file": "kodland_diploma_2.pdf"
            }
        }
    ]
}

cv_data_de = {
    "nome": "Lorenzo Fusari",
    "citta": "San Giovanni in Persiceto (BO), Italien",
    "telefono": "+39 371-479-2122",
    "email": "fusarilorenzo@icloud.com",
    "profilo": "Schüler des Naturwissenschaftlichen Gymnasiums mit Schwerpunkt Angewandte Wissenschaften und Informatik. Entwickler mit Kenntnissen in Full-Stack-Programmierung und Erstellung von Webanwendungen.",
    "istruzione": "Naturwissenschaftliches Gymnasium (Schwerpunkt Informatik) - Liceo A. B. Sabin",
    "voti": "Informatik: 10/10 | Mathematik: 8/10",
    "competenze": ["Full-Stack-Programmierung", "Mobile App-Entwicklung", "Webentwicklung", "Microsoft Office-Paket"],
    "competizioni": [
        "Informatik-Olympiade (Regionalklassifizierung) 2026 - Punktzahl: 100",
        "Informatik-Olympiade (Schulauswahl) 2026 - Punktzahl: 55",
        "Archimedes-Mathematik-Wettbewerb (Schulauswahl) 2026 - Punktzahl: 43",
        "Archimedes-Mathematik-Wettbewerb (Schulauswahl) 2025 - Punktzahl: 20"
    ],
    "certificazioni": [
        {"nome": "ICDL Spreadsheets (Excel)", "ente": "AICA", "pdf": "icdl_excel.pdf"},
        {"nome": "ICDL Word Processing", "ente": "AICA", "pdf": "icdl_word.pdf"},
        {"nome": "ICDL Presentation", "ente": "AICA", "pdf": "icdl_presentation.pdf"},
        {"nome": "ICDL IT-Security/Cyber Security", "ente": "AICA", "pdf": "icdl_cybersecurity.pdf"},
        {"nome": "ICDL Computer Essentials", "ente": "AICA", "pdf": "icdl_computeressentials.pdf"},
        {"nome": "EF SET English Certificate - C2 Proficient", "ente": "EF Standard English Test", "pdf": "efset_english.pdf"},
        {"nome": "Speexx Español Core - A1", "ente": "Speexx Corporate Language Training", "pdf": "certificato_spagnolo_a1.pdf"}
    ],
    "sport": [
        "Bronzemedaille - U18 Ju-Jitsu Italienische Meisterschaften 2026",
        "FIJLKAM U16 Ju-Jitsu Regionalmeister 2025",
        "9. Platz - Mediterranean Open U16 Ju-Jitsu 2025",
        "Bronzemedaille - Genoa Open U16 Ju-Jitsu 2025",
        "7. Platz - U16 Ju-Jitsu Italienische Meisterschaften 2025"
    ],
    "progetti": [
        {
            "id": "app-asd",
            "titolo": "Mobile App für lokalen Sportverein",
            "descrizione_breve": "Konzeption, Entwicklung und Veröffentlichung einer mobilen Anwendung für einen Amateursportverein in den offiziellen Stores."
        },
        {
            "id": "sito-commissione",
            "titolo": "Auftrags-Website",
            "descrizione_breve": "Erstellung einer strukturierten Website im Auftrag eines privaten Kunden."
        },
        {
			"id": "sito-matrimonio",
			"titolo": "Hochzeits-Website",
			"descrizione_breve": "Erstellung einer Flask-Webanwendung für eine Hochzeit im Piraten-Stil."
		}
    ],
    "social": cv_data_it["social"],
    "lingue": [
        {"lingua": "Italienisch", "livello": "Muttersprache", "dettaglio": "Hauptsprache"},
        {"lingua": "Englisch (Reading & Listening)", "livello": "C2 Proficient", "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"},
        {"lingua": "Spanisch", "livello": "A1 Anfänger", "dettaglio": "Speexx Business Language Zertifikat 99/100"}
    ],
    "corsi_formazione": [
        {
            "titolo": "Python Programming Language",
            "ente": "Kodland (Internationale Programmierschule)",
            "periodo": "09.09.2022 - 05.05.2023",
            "competenze": ["Python", "Pgzero / Pygame", "Algorithmen & Programmierlogik"],
            "descrizione": "9-monatiger Kurs mit Schwerpunkt auf objektorientierter Programmierung in Python und 2D-Spieleentwicklung mit Pgzero.",
            "diploma": {
                "nome": "Diplom Stufe 1",
                "file": "kodland_diploma_1.pdf"
            }
        },
        {
            "titolo": "Python Pro",
            "ente": "Kodland (Internationale Programmierschule)",
            "periodo": "23.11.2023 - 01.08.2024",
            "competenze": ["Flask", "HTML/CSS", "Discord Bot API", "Teachable Machine (KI)"],
            "descrizione": "Fortgeschrittener 9-monatiger Kurs über Web-Backend mit Flask, interaktive Discord-Bots und Einbindung von Machine-Learning-Modellen.",
            "diploma": {
                "nome": "Diplom Stufe 2",
                "file": "kodland_diploma_2.pdf"
            }
        }
    ]
}

cv_data_fr = {
    "nome": "Lorenzo Fusari",
    "citta": "San Giovanni in Persiceto (BO), Italie",
    "telefono": "+39 371-479-2122",
    "email": "fusarilorenzo@icloud.com",
    "profilo": "Élève au Lycée Scientifique (Sciences Appliquées) avec option renforcée en Informatique. Développeur spécialisé en programmation full-stack et création d'applications web et mobiles.",
    "istruzione": "Lycée Scientifique option Sciences Appliquées (Spécialité Informatique) - Liceo A. B. Sabin",
    "voti": "Informatique : 10/10 | Mathématiques : 8/10",
    "competenze": ["Programmation Full-Stack", "Développement d'Apps Mobiles", "Développement Web", "Suite Microsoft Office"],
    "competizioni": [
        "Olympiades d'Informatique (Sélection Régionale) 2026 - Score : 100",
        "Olympiades d'Informatique (Sélection Scolaire) 2026 - Score : 55",
        "Concours d'Archimède / Olympiades de Mathématiques (Sélection Scolaire) 2026 - Score : 43",
        "Concours d'Archimède / Olympiades de Mathématiques (Sélection Scolaire) 2025 - Score : 20"
    ],
    "certificazioni": [
        {"nome": "ICDL Spreadsheets (Excel)", "ente": "AICA", "pdf": "icdl_excel.pdf"},
        {"nome": "ICDL Word Processing", "ente": "AICA", "pdf": "icdl_word.pdf"},
        {"nome": "ICDL Presentation", "ente": "AICA", "pdf": "icdl_presentation.pdf"},
        {"nome": "ICDL IT-Security/Cyber Security", "ente": "AICA", "pdf": "icdl_cybersecurity.pdf"},
        {"nome": "ICDL Computer Essentials", "ente": "AICA", "pdf": "icdl_computeressentials.pdf"},
        {"nome": "EF SET English Certificate - C2 Proficient", "ente": "EF Standard English Test", "pdf": "efset_english.pdf"},
        {"nome": "Speexx Español Core - A1", "ente": "Speexx Corporate Language Training", "pdf": "certificato_spagnolo_a1.pdf"}
    ],
    "sport": [
        "Médaille de Bronze - Championnat d'Italie U18 de Ju-Jitsu 2026",
        "Champion Régional FIJLKAM U16 de Ju-Jitsu 2025",
        "9e Place - Mediterranean Open U16 Ju-Jitsu 2025",
        "Médaille de Bronze - Genoa Open U16 Ju-Jitsu 2025",
        "7e Place - Championnat d'Italie U16 de Ju-Jitsu 2025"
    ],
    "progetti": [
        {
            "id": "app-asd",
            "titolo": "App Mobile pour Association Sportive Locale",
            "descrizione_breve": "Conception, développement et publication sur les stores officiels d'une application mobile pour un club sportif amateur."
        },
        {
            "id": "sito-commissione",
            "titolo": "Site Web Sur Mesure",
            "descrizione_breve": "Réalisation complète d'un site web structuré sur commande pour un client privé."
        },
        {
			"id": "sito-matrimonio",
			"titolo": "Site Web de Mariage",
			"descrizione_breve": "Création d'un site web en Flask pour un mariagesur le thème des pirates."
		}
    ],
    "social": cv_data_it["social"],
    "lingue": [
        {"lingua": "Italien", "livello": "Langue maternelle", "dettaglio": "Langue principale"},
        {"lingua": "Anglais (Reading & Listening)", "livello": "C2 Expérimenté", "dettaglio": "EF SET 2-Skills: Reading 73/100, Listening 76/100"},
        {"lingua": "Espagnol", "livello": "A1 Débutant", "dettaglio": "Certification Speexx Business Language 99/100"}
    ],
    "corsi_formazione": [
        {
            "titolo": "Python Programming Language",
            "ente": "Kodland (École Internationale de Programmation)",
            "periodo": "09/09/2022 - 05/05/2023",
            "competenze": ["Python", "Pgzero / Pygame", "Algorithmes & Logique de Programmation"],
            "descrizione": "Formation de 9 mois axée sur les bases de la programmation orientée objet en Python et le développement de jeux 2D avec Pgzero.",
            "diploma": {
                "nome": "Diplôme Niveau 1",
                "file": "kodland_diploma_1.pdf"
            }
        },
        {
            "titolo": "Python Pro",
            "ente": "Kodland (École Internationale de Programmation)",
            "periodo": "23/11/2023 - 01/08/2024",
            "competenze": ["Flask", "HTML/CSS", "Discord Bot API", "Teachable Machine (IA)"],
            "descrizione": "Formation avancée de 9 mois sur le backend web avec Flask, la création de bots Discord et l'intégration de modèles d'apprentissage automatique.",
            "diploma": {
                "nome": "Diplôme Niveau 2",
                "file": "kodland_diploma_2.pdf"
            }
        }
    ]
}

LANGUAGES_MAP = {
	"it": cv_data_it,
	"en": cv_data_en,
	"es": cv_data_es,
	"de": cv_data_de,
	"fr": cv_data_fr
}

LANGUAGES_MAP_PROGETTI = {
	"it": progetti_dettaglio_it,
	"en": progetti_dettaglio_en,
	"es": progetti_dettaglio_es,
	"de": progetti_dettaglio_de,
	"fr": progetti_dettaglio_fr
}

@app.route('/')
def home_default():
	cv_selezionato = LANGUAGES_MAP['en']
	label_selezionato = LABELS_HOME.get('en', LABELS_HOME['en'])
	return render_template('index.html', cv=cv_selezionato, labels=label_selezionato, current_lang='en')

@app.route('/<lang>/')
def home(lang):
	if lang not in LANGUAGES_MAP:
		return redirect(url_for('home', lang='en'))
	
	cv_selezionato = LANGUAGES_MAP[lang]
	label_selezionato = LABELS_HOME.get(lang, LABELS_HOME['en'])
	return render_template('index.html', cv=cv_selezionato, labels=label_selezionato, current_lang=lang)

@app.route('/<lang>/progetto/<id_progetto>/')
def dettaglio_progetto(lang, id_progetto):
	if lang not in LANGUAGES_MAP_PROGETTI:
		lang = 'en'
		
	all = LANGUAGES_MAP_PROGETTI.get(lang, LANGUAGES_MAP_PROGETTI['en'])
	progetto = all.get(id_progetto)
	if not progetto:
		abort(404)
	
	cv_selezionato = LANGUAGES_MAP[lang]
	label_selezionato = LABELS_PROGETTI.get(lang, LABELS_PROGETTI['en'])
	return render_template('dettaglio_progetto.html', progetto=progetto, labels=label_selezionato, cv=cv_selezionato, current_lang=lang)
	
@app.errorhandler(404)
def page_not_found(e):
	path_parts = request.path.strip('/').split('/')
	lang = path_parts[0] if path_parts and path_parts[0] in LANGUAGES_MAP else 'en'
	
	label_selezionato = LABELS_404.get(lang, LABELS_404['en'])
	
	return render_template('404.html', labels=label_selezionato, current_lang=lang), 404
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
