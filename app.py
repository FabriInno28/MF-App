import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- INIT ----------------
DEFAULT_STATE = {
    "submitted": False,
    "answers": {},
    "profile": {},
    "focus": "",
    "action": "",
    "owner": "",
    "deadline": "",
    "success_criteria": "",
    "support_needed": ""
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- STYLING ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.insight-box {
    background: #f7f7f7;
    padding: 1rem;
    border-radius: 0.6rem;
    border-left: 6px solid #d6001c;
    margin-bottom: 1rem;
}
.reco-box {
    background: #fff8e8;
    padding: 1rem;
    border-radius: 0.6rem;
    border-left: 6px solid #f2b300;
    margin-bottom: 1rem;
}
.action-box {
    background: #eef6ff;
    padding: 1rem;
    border-radius: 0.6rem;
    border-left: 6px solid #2b6cb0;
    margin-bottom: 1rem;
}
.small-note {
    color: #555;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- QUESTION SET ----------------
DIMENSIONS = {
    "orientierung": {
        "label": "Orientierung",
        "slider_questions": [
            "Wir haben ein klares Bild, wohin wir uns entwickeln wollen.",
            "Wir priorisieren bewusst, was jetzt wirklich wichtig ist.",
            "Unser Team weiss, worauf es aktuell besonders ankommt."
        ]
    },
    "entscheidung": {
        "label": "Entscheidungskraft",
        "slider_questions": [
            "Wichtige Entscheidungen werden rechtzeitig getroffen.",
            "Schwierige Themen bleiben bei uns nicht zu lange liegen.",
            "Zuständigkeiten sind klar genug, damit wir vorwärtskommen."
        ]
    },
    "umsetzung": {
        "label": "Umsetzung",
        "slider_questions": [
            "Zwischen Idee und erstem Schritt vergeht bei uns wenig Zeit.",
            "Wir bringen Vorhaben konsequent in Bewegung.",
            "Wir setzen lieber bewusst um als alles gleichzeitig anzureissen."
        ]
    },
    "kultur": {
        "label": "Zusammenarbeit & Kultur",
        "slider_questions": [
            "Probleme können offen angesprochen werden.",
            "Vertrauen ist stärker als Absicherung.",
            "Auch unter Druck bleiben wir miteinander handlungsfähig."
        ]
    },
    "ki": {
        "label": "KI & Wandel",
        "slider_questions": [
            "Wir sehen konkrete Möglichkeiten, wie KI uns helfen kann.",
            "Wir sind offen dafür, neue Werkzeuge pragmatisch auszuprobieren.",
            "Wir sprechen nicht nur über Wandel, sondern prüfen konkrete Anwendungen."
        ]
    }
}

CONTENT_LIBRARY = {
    "Reaktionsmodus": {
        "video_title": "Warum Teams unter Druck den Fokus verlieren",
        "video_hint": "Kurzer Impuls von 6 bis 8 Minuten zum Thema Priorisierung unter Druck.",
        "podcast_title": "Klarheit vor Aktivität",
        "podcast_hint": "Audio Impuls über Entscheidungen, die zu lange vertagt werden.",
        "website_title": "Checkliste Prioritäten klären",
        "website_hint": "Eine einfache Seite mit Leitfragen für Fokus und Priorisierung.",
        "forum_format": "Tagesworkshop Orientierung schaffen",
        "forum_text": "Wenn ihr merkt, dass euch gemeinsame Klarheit fehlt, ist dieses Format ein starker nächster Schritt."
    },
    "Reflexionsfalle": {
        "video_title": "Vom guten Gespräch ins echte Tun",
        "video_hint": "Impuls dazu, warum Teams oft viel verstehen, aber zu wenig umsetzen.",
        "podcast_title": "Verbindlichkeit statt Dauerreflexion",
        "podcast_hint": "Audio Impuls für Teams, die gute Gespräche führen, aber nicht durchziehen.",
        "website_title": "Mini Guide Umsetzung mit Verantwortung",
        "website_hint": "Kurze Praxisvorlage für nächsten Schritt, Verantwortung und Deadline.",
        "forum_format": "Tagesworkshop Veränderung begleiten",
        "forum_text": "Wenn die Umsetzung euer Engpass ist, unterstützt euch dieses Format bei Verbindlichkeit und Rhythmus."
    },
    "Technologie ohne Richtung": {
        "video_title": "KI im KMU. Wo sie heute wirklich hilft",
        "video_hint": "Praxisnaher Kurzimpuls zu echten Anwendungsfällen statt Hype.",
        "podcast_title": "Technologie mit Nutzen statt Technik um der Technik willen",
        "podcast_hint": "Audio Impuls zur Frage, wie KI im Alltag echte Entlastung bringen kann.",
        "website_title": "Use Case Canvas für KI im Alltag",
        "website_hint": "Einfaches Raster, um Nutzen, Aufwand und ersten Test zu klären.",
        "forum_format": "2.5 Tage Zukunft gestalten",
        "forum_text": "Wenn Offenheit für Neues da ist, aber die Richtung fehlt, kann dieses Format echten Tiefgang bringen."
    },
    "Umsetzungsproblem": {
        "video_title": "Warum gute Ideen im Alltag stecken bleiben",
        "video_hint": "Kurzimpuls zu Priorisierung, Tempo und Umsetzungsdisziplin.",
        "podcast_title": "Vom Vorhaben zur Bewegung",
        "podcast_hint": "Audio Impuls zu Verbindlichkeit im Teamalltag.",
        "website_title": "Start klein. Aber klar.",
        "website_hint": "Praxisseite mit Fokus auf ersten realen Schritt und Checkpoints.",
        "forum_format": "Tagesworkshop Veränderung begleiten",
        "forum_text": "Wenn nicht die Idee, sondern das Dranbleiben das Problem ist, passt dieses Format gut."
    },
    "Stabile Basis": {
        "video_title": "Zukunft aktiv gestalten statt nur reagieren",
        "video_hint": "Kurzimpuls für Teams mit guter Basis und Potenzial für den nächsten Entwicklungsschritt.",
        "podcast_title": "Wachstum durch gezielte Weiterentwicklung",
        "podcast_hint": "Audio Impuls zu Zukunftsthemen, die bewusst angegangen werden.",
        "website_title": "Zukunftsthema schärfen",
        "website_hint": "Praxisleitfaden, um ein Thema auf Fokus, Test und Lernziel herunterzubrechen.",
        "forum_format": "Tagesworkshop Ideen entwickeln",
        "forum_text": "Wenn ihr eine gute Basis habt und nun gezielt weiterkommen wollt, ist dieses Format passend."
    }
}

# ---------------- HELPER ----------------
def compute_scores(answers):
    return {k: round(sum(v) / len(v) * 20, 1) for k, v in answers.items()}

def score_to_level(score):
    if score < 45:
        return "kritisch"
    if score < 60:
        return "fragil"
    if score < 75:
        return "solide"
    return "stark"

def detect_pattern(scores, blockers_choice, ki_choice):
    if scores["orientierung"] < 55 and scores["entscheidung"] < 55:
        return "Reaktionsmodus"
    if scores["kultur"] >= 70 and scores["umsetzung"] < 55:
        return "Reflexionsfalle"
    if scores["ki"] >= 70 and scores["orientierung"] < 60:
        return "Technologie ohne Richtung"
    if scores["umsetzung"] < 55:
        return "Umsetzungsproblem"

    if blockers_choice == "Zu viele Themen gleichzeitig":
        return "Reaktionsmodus"
    if blockers_choice == "Wir reden viel, setzen aber zu wenig um":
        return "Reflexionsfalle"
    if ki_choice == "Wir sind interessiert, sehen aber noch keinen klaren Nutzen":
        return "Technologie ohne Richtung"

    return "Stabile Basis"

def get_pattern_text(pattern):
    mapping = {
        "Reaktionsmodus": {
            "headline": "Hohe Aktivität. Zu wenig Fokus.",
            "assessment": "Euer Team wirkt engagiert. Gleichzeitig fehlt aktuell gemeinsame Klarheit, worauf ihr euch wirklich konzentrieren wollt. Das Risiko ist nicht Stillstand, sondern Verzettelung.",
            "risk": "Wenn alles wichtig ist, wird am Ende zu wenig entschieden.",
            "lever": "Der grösste Hebel liegt in klarer Priorisierung und einer bewusst getroffenen Entscheidung."
        },
        "Reflexionsfalle": {
            "headline": "Gutes Denken. Zu wenig Bewegung.",
            "assessment": "Bei euch ist Reflexion vorhanden. Das ist stark. Gleichzeitig scheint die Übersetzung in konkrete Umsetzung noch zu wenig konsequent zu gelingen.",
            "risk": "Das Team gewinnt Einsicht, aber verliert Tempo.",
            "lever": "Der Hebel liegt in Verantwortung, Verbindlichkeit und einem kleineren ersten Schritt."
        },
        "Technologie ohne Richtung": {
            "headline": "Offen für KI. Aber noch ohne klares Zielbild.",
            "assessment": "Ihr seid neugierig und offen gegenüber neuen Werkzeugen. Gleichzeitig ist noch nicht klar genug, wofür KI bei euch konkret Nutzen stiften soll.",
            "risk": "Interesse bleibt auf der Ebene von Tools statt Wirkung.",
            "lever": "Der grösste Hebel liegt in einem konkreten Use Case mit überschaubarem Test."
        },
        "Umsetzungsproblem": {
            "headline": "Ideen vorhanden. Umsetzung zu schwach.",
            "assessment": "Es scheint weniger an Ideen zu fehlen als an der Fähigkeit, diese mit genug Klarheit und Konsequenz in Bewegung zu bringen.",
            "risk": "Vorhaben starten, aber ohne echten Durchschlag.",
            "lever": "Wirkung entsteht hier über Priorisierung, Checkpoints und klare Verantwortlichkeiten."
        },
        "Stabile Basis": {
            "headline": "Gute Ausgangslage. Jetzt gezielt weiterentwickeln.",
            "assessment": "Bei euch ist bereits viel vorhanden. Das Bild wirkt insgesamt stabil. Nun geht es nicht um Feuerwehr, sondern um einen bewussten nächsten Entwicklungsschritt.",
            "risk": "Stabilität kann auch dazu führen, dass Potenziale zu lange ungenutzt bleiben.",
            "lever": "Der Hebel liegt darin, ein Zukunftsthema bewusst zu wählen und konkret zu testen."
        }
    }
    return mapping[pattern]

def get_development_path(pattern):
    paths = {
        "Reaktionsmodus": {
            "focus": "Eine zentrale Entscheidung treffen und ein Thema bewusst priorisieren.",
            "exercise_title": "Fokus statt Vollgas",
            "exercise_steps": [
                "Jede Person schreibt 3 Themen auf, die aktuell Energie ziehen.",
                "Das Team reduziert gemeinsam auf 1 Thema mit höchster Relevanz.",
                "Für die anderen Themen wird bewusst entschieden: später oder stoppen.",
                "Für das priorisierte Thema wird ein erster Schritt festgelegt."
            ],
            "commitment": "In den nächsten 14 Tagen ist eine zentrale Entscheidung gefällt und ein erster Schritt gestartet.",
            "forum_recommendation": "Mobiliar Forum: Orientierung schaffen"
        },
        "Reflexionsfalle": {
            "focus": "Ein Thema aus der Diskussion in die sichtbare Umsetzung bringen.",
            "exercise_title": "Vom Verstehen ins Tun",
            "exercise_steps": [
                "Wählt ein Thema, über das ihr schon länger sprecht.",
                "Definiert den kleinstmöglichen ersten Schritt.",
                "Legt fest, wer ihn verantwortet.",
                "Vereinbart einen Check in in 14 Tagen."
            ],
            "commitment": "Innert 14 Tagen wurde ein erster sichtbarer Schritt umgesetzt.",
            "forum_recommendation": "Mobiliar Forum: Veränderung begleiten"
        },
        "Technologie ohne Richtung": {
            "focus": "Einen echten KI Anwendungsfall mit Nutzen im Alltag definieren.",
            "exercise_title": "Use Case statt Buzzword",
            "exercise_steps": [
                "Sammelt 3 konkrete Tätigkeiten, die heute Zeit kosten oder repetitiv sind.",
                "Wählt 1 davon aus, bei der KI helfen könnte.",
                "Definiert einen kleinen Test mit klarer Erwartung.",
                "Reflektiert nach zwei Wochen Nutzen und Grenzen."
            ],
            "commitment": "Ein konkreter KI Test wurde gestartet und ausgewertet.",
            "forum_recommendation": "Mobiliar Forum: Zukunft gestalten"
        },
        "Umsetzungsproblem": {
            "focus": "Verbindlichkeit und sichtbaren Fortschritt erhöhen.",
            "exercise_title": "Weniger reden. Klarer starten.",
            "exercise_steps": [
                "Wählt ein laufendes Vorhaben aus.",
                "Definiert die nächste konkrete Etappe.",
                "Legt eine verantwortliche Person fest.",
                "Setzt einen Termin für den ersten Zwischenstand."
            ],
            "commitment": "Ein Vorhaben wurde mit klarer Verantwortung und Checkpoint aktiv weitergeführt.",
            "forum_recommendation": "Mobiliar Forum: Veränderung begleiten"
        },
        "Stabile Basis": {
            "focus": "Ein Zukunftsthema bewusst auswählen und praktisch testen.",
            "exercise_title": "Nächster Entwicklungsschritt",
            "exercise_steps": [
                "Wählt ein Zukunftsthema, das euch wirklich weiterbringen kann.",
                "Sammelt mögliche Ideen oder Ansätze.",
                "Legt einen kleinen Test fest.",
                "Holt Feedback aus dem Alltag oder vom Markt ein."
            ],
            "commitment": "Ein Zukunftsthema wurde konkret angegangen und mit einem ersten Test verbunden.",
            "forum_recommendation": "Mobiliar Forum: Ideen entwickeln"
        }
    }
    return paths[pattern]

def create_management_summary(pattern, scores, blockers_choice, open_bottleneck, open_ki):
    pattern_text = get_pattern_text(pattern)
    weakest_dim = min(scores, key=scores.get)
    weakest_label = DIMENSIONS[weakest_dim]["label"]
    weakest_score = scores[weakest_dim]

    summary = f"""
**Einschätzung**

Das Bild zeigt aktuell vor allem folgendes Muster: **{pattern_text['headline']}**

{pattern_text['assessment']}

Besondere Aufmerksamkeit verdient derzeit der Bereich **{weakest_label}** mit einem Wert von **{weakest_score}**. Das deutet darauf hin, dass hier der grösste unmittelbare Engpass liegt.

**Was das für ein KMU oft bedeutet**

{pattern_text['risk']}

**Wo aktuell der grösste Hebel liegt**

{pattern_text['lever']}
""".strip()

    if blockers_choice:
        summary += f"\n\n**Spürbarer Alltagsblocker**\n{blockers_choice}"

    if open_bottleneck:
        summary += f"\n\n**Hinweis aus der Freitextantwort**\n{open_bottleneck}"

    if open_ki:
        summary += f"\n\n**Hinweis zum Thema KI**\n{open_ki}"

    return summary

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Mobiliar Forum")
    st.caption("Navigator für KMU")
    page = st.radio("Bereich", ["Befragung", "Dashboard", "Entwicklung", "Aktionsplan"])
    st.markdown("---")
    st.write("Vom Verstehen ins Handeln")

# ---------------- PAGE: BEFRAGUNG ----------------
if page == "Befragung":
    st.title("Standortbestimmung für KMU")
    st.write("Die Befragung verbindet schnelle Einschätzung mit konkreten Hinweisen aus eurem Alltag.")

    with st.form("scan_form"):
        st.subheader("1. Einschätzung auf einen Blick")

        answers = {}
        for dim, cfg in DIMENSIONS.items():
            st.markdown(f"### {cfg['label']}")
            vals = []
            for i, question in enumerate(cfg["slider_questions"]):
                vals.append(st.slider(question, 1, 5, 3, key=f"{dim}_{i}"))
            answers[dim] = vals

        st.markdown("---")
        st.subheader("2. Zuspitzung")

        blockers_choice = st.selectbox(
            "Was bremst euch aktuell am stärksten?",
            [
                "Bitte wählen",
                "Zu viele Themen gleichzeitig",
                "Wir reden viel, setzen aber zu wenig um",
                "Entscheidungen bleiben zu lange offen",
                "Es fehlt an gemeinsamer Richtung",
                "Wir sind im Alltag zu stark absorbiert",
                "Nicht die Idee fehlt, sondern die Zeit",
                "Etwas anderes"
            ]
        )

        ki_choice = st.selectbox(
            "Wie erlebt ihr das Thema KI aktuell?",
            [
                "Bitte wählen",
                "Noch kein Thema bei uns",
                "Wir beobachten es von aussen",
                "Wir sind interessiert, sehen aber noch keinen klaren Nutzen",
                "Wir testen erste Anwendungen",
                "Wir nutzen bereits erste konkrete Anwendungen"
            ]
        )

        st.markdown("---")
        st.subheader("3. Kurze Hinweise aus eurem Alltag")

        open_bottleneck = st.text_area(
            "Welche Entscheidung, welches Thema oder welcher Engpass wird bei euch aktuell zu lange mitgetragen?",
            placeholder="Zum Beispiel: Wir reden seit Monaten über Prioritäten, aber niemand entscheidet klar."
        )

        open_ki = st.text_area(
            "Wo könnte KI euch im Alltag konkret helfen?",
            placeholder="Zum Beispiel: Offerten, Protokolle, E Mails, Dokumentation, Auswertungen..."
        )

        submitted = st.form_submit_button("Analyse erstellen")

        if submitted:
            st.session_state.answers = answers
            st.session_state.profile = {
                "blockers_choice": blockers_choice if blockers_choice != "Bitte wählen" else "",
                "ki_choice": ki_choice if ki_choice != "Bitte wählen" else "",
                "open_bottleneck": open_bottleneck.strip(),
                "open_ki": open_ki.strip()
            }
            st.session_state.submitted = True
            st.success("Analyse erstellt. Wechsle jetzt ins Dashboard.")

# ---------------- PAGE: DASHBOARD ----------------
elif page == "Dashboard":
    st.title("Dashboard")
    st.write("Einordnung eurer aktuellen Situation mit Zuspitzung, Kontext und erster Empfehlung.")

    if not st.session_state.submitted:
        st.warning("Bitte zuerst die Befragung ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        blockers_choice = st.session_state.profile.get("blockers_choice", "")
        ki_choice = st.session_state.profile.get("ki_choice", "")
        open_bottleneck = st.session_state.profile.get("open_bottleneck", "")
        open_ki = st.session_state.profile.get("open_ki", "")
        pattern = detect_pattern(scores, blockers_choice, ki_choice)
        pattern_text = get_pattern_text(pattern)
        summary = create_management_summary(pattern, scores, blockers_choice, open_bottleneck, open_ki)

        avg_score = round(sum(scores.values()) / len(scores), 1)
        weakest_dim = min(scores, key=scores.get)
        strongest_dim = max(scores, key=scores.get)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Gesamtbild", avg_score)
        m2.metric("Hauptmuster", pattern)
        m3.metric("Grösster Engpass", DIMENSIONS[weakest_dim]["label"])
        m4.metric("Stärkster Hebel", DIMENSIONS[strongest_dim]["label"])

        st.markdown("---")

        df = pd.DataFrame({
            "Dimension": [DIMENSIONS[k]["label"] for k in scores.keys()],
            "Score": list(scores.values()),
            "Status": [score_to_level(v) for v in scores.values()]
        })

        left, right = st.columns([1.8, 1.2])

        with left:
            fig = px.bar(df, x="Dimension", y="Score", text="Score", range_y=[0, 100])
            fig.update_traces(textposition="outside")
            fig.update_layout(height=430)
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.markdown(f"""
            <div class="insight-box">
            <strong>Hauptmuster</strong><br><br>
            <strong>{pattern_text['headline']}</strong><br><br>
            {pattern_text['assessment']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="reco-box">
            <strong>Wirkungshebel</strong><br><br>
            {pattern_text['lever']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## Management Einschätzung")
        st.markdown(summary)

        st.markdown("## Kurzfazit")
        st.write(
            "Diese Auswertung ist keine wissenschaftliche Diagnose. Sie ist eine ehrliche, praxisnahe Standortbestimmung. "
            "Der Wert entsteht nicht durch die Zahl allein, sondern durch das Gespräch, die Priorisierung und den nächsten Schritt, der daraus folgt."
        )

# ---------------- PAGE: ENTWICKLUNG ----------------
elif page == "Entwicklung":
    st.title("Entwicklungsschritte")
    st.write("Konkrete Impulse für die nächsten 30 Tage.")

    if not st.session_state.submitted:
        st.warning("Bitte zuerst die Befragung ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        blockers_choice = st.session_state.profile.get("blockers_choice", "")
        ki_choice = st.session_state.profile.get("ki_choice", "")
        pattern = detect_pattern(scores, blockers_choice, ki_choice)
        path = get_development_path(pattern)
        content = CONTENT_LIBRARY[pattern]

        st.markdown(f"""
        <div class="insight-box">
        <strong>Fokus für die nächsten 30 Tage</strong><br><br>
        {path['focus']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## Team Übung")
        st.write(f"**{path['exercise_title']}**")
        for step in path["exercise_steps"]:
            st.write(f"• {step}")

        st.markdown("## Impulse zum Weiterdenken")
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("### Video")
            st.write(f"**{content['video_title']}**")
            st.caption(content["video_hint"])

        with c2:
            st.markdown("### Podcast")
            st.write(f"**{content['podcast_title']}**")
            st.caption(content["podcast_hint"])

        with c3:
            st.markdown("### Website")
            st.write(f"**{content['website_title']}**")
            st.caption(content["website_hint"])

        st.markdown("## Commitment")
        st.markdown(f"""
        <div class="action-box">
        {path['commitment']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## Anschluss ans Mobiliar Forum")
        st.info(f"**{content['forum_format']}**\n\n{content['forum_text']}")

# ---------------- PAGE: AKTIONSPLAN ----------------
elif page == "Aktionsplan":
    st.title("Konkreter Aktionsplan")
    st.write("Nicht nur erkennen. Sondern festhalten, was jetzt wirklich passiert.")

    if not st.session_state.submitted:
        st.warning("Bitte zuerst die Befragung ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        blockers_choice = st.session_state.profile.get("blockers_choice", "")
        ki_choice = st.session_state.profile.get("ki_choice", "")
        pattern = detect_pattern(scores, blockers_choice, ki_choice)
        path = get_development_path(pattern)

        st.markdown(f"""
        <div class="reco-box">
        <strong>Empfohlener Fokus</strong><br><br>
        {path['focus']}
        </div>
        """, unsafe_allow_html=True)

        st.session_state.focus = st.text_area(
            "1. Unser Fokus für die nächsten 30 Tage",
            value=st.session_state.focus,
            placeholder="Zum Beispiel: Wir priorisieren ein Zukunftsthema und treffen dazu eine klare Entscheidung."
        )

        st.session_state.action = st.text_area(
            "2. Unser erster konkreter Schritt",
            value=st.session_state.action,
            placeholder="Zum Beispiel: Bis nächste Woche definieren wir das priorisierte Thema und legen den ersten Test fest."
        )

        st.session_state.owner = st.text_input(
            "3. Wer übernimmt die Verantwortung?",
            value=st.session_state.owner,
            placeholder="Zum Beispiel: Geschäftsleitung, Teamlead, Projektverantwortliche Person"
        )

        st.session_state.deadline = st.text_input(
            "4. Bis wann machen wir das sichtbar?",
            value=st.session_state.deadline,
            placeholder="Zum Beispiel: Bis 15. April 2026"
        )

        st.session_state.success_criteria = st.text_area(
            "5. Woran merken wir, dass wir wirklich einen Schritt weiter sind?",
            value=st.session_state.success_criteria,
            placeholder="Zum Beispiel: Eine Entscheidung ist gefällt, ein Test ist gestartet, Verantwortlichkeiten sind geklärt."
        )

        st.session_state.support_needed = st.text_area(
            "6. Welche Unterstützung brauchen wir dafür?",
            value=st.session_state.support_needed,
            placeholder="Zum Beispiel: Zeitfenster, Klarheit in der Führung, Moderation, Workshop, externe Sparringspartner"
        )

        if st.button("Aktionsplan fixieren"):
            st.success("Aktionsplan fixiert. Jetzt geht es um Umsetzung und Dranbleiben.")

        if st.session_state.focus:
            st.markdown("## Eure Vereinbarung")
            st.markdown(f"""
            <div class="action-box">
            <strong>Fokus</strong><br>
            {st.session_state.focus}<br><br>

            <strong>Erster Schritt</strong><br>
            {st.session_state.action}<br><br>

            <strong>Verantwortung</strong><br>
            {st.session_state.owner}<br><br>

            <strong>Zeithorizont</strong><br>
            {st.session_state.deadline}<br><br>

            <strong>Erfolgszeichen</strong><br>
            {st.session_state.success_criteria}<br><br>

            <strong>Benötigte Unterstützung</strong><br>
            {st.session_state.support_needed}
            </div>
            """, unsafe_allow_html=True)
