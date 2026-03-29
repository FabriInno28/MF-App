import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- INIT ----------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "focus" not in st.session_state:
    st.session_state.focus = ""

if "action" not in st.session_state:
    st.session_state.action = ""

if "owner" not in st.session_state:
    st.session_state.owner = ""

if "deadline" not in st.session_state:
    st.session_state.deadline = ""

# ---------------- DIMENSIONEN ----------------
DIMENSIONS = {
    "orientierung": [
        "Wir haben ein klares Bild, wohin wir uns entwickeln wollen.",
        "Wir priorisieren bewusst, was jetzt wirklich wichtig ist."
    ],
    "entscheidung": [
        "Wichtige Entscheidungen werden rechtzeitig getroffen.",
        "Wir schieben schwierige Themen nicht systematisch vor uns her."
    ],
    "umsetzung": [
        "Wir bringen Dinge konsequent in die Umsetzung.",
        "Zwischen Idee und erstem Schritt vergeht wenig Zeit."
    ],
    "kultur": [
        "Probleme können offen angesprochen werden.",
        "Vertrauen ist stärker als Absicherung."
    ],
    "ki": [
        "Wir sehen konkrete Möglichkeiten, wie KI uns helfen kann.",
        "Wir probieren neue Tools pragmatisch aus."
    ]
}

# ---------------- LOGIK ----------------
def compute_scores(answers):
    return {k: round(sum(v)/len(v)*20,1) for k,v in answers.items()}

def detect_pattern(scores):
    if scores["orientierung"] < 55 and scores["entscheidung"] < 55:
        return "Reaktionsmodus"
    if scores["kultur"] > 70 and scores["umsetzung"] < 55:
        return "Reflexionsfalle"
    if scores["ki"] > 70 and scores["orientierung"] < 60:
        return "Technologie ohne Richtung"
    if scores["umsetzung"] < 55:
        return "Umsetzungsproblem"
    return "Stabile Basis"

def get_path(pattern):
    return {
        "Reaktionsmodus": {
            "text": "Ihr seid stark im Einsatz. Aber es fehlt Klarheit, worauf ihr euch fokussiert.",
            "focus": "Eine Entscheidung treffen",
            "exercise": [
                "Jeder bringt 3 Themen mit",
                "Team reduziert auf 1 Thema",
                "Entscheidung treffen: jetzt / später / nicht"
            ],
            "commitment": "In 14 Tagen ist eine Entscheidung umgesetzt"
        },
        "Reflexionsfalle": {
            "text": "Ihr reflektiert gut. Aber kommt zu wenig ins Tun.",
            "focus": "Vom Denken ins Handeln",
            "exercise": [
                "Ein Thema auswählen",
                "Ersten Schritt definieren",
                "Verantwortung festlegen"
            ],
            "commitment": "Ein erster Schritt wurde umgesetzt"
        },
        "Technologie ohne Richtung": {
            "text": "Interesse an KI ist da. Aber ohne klaren Nutzen.",
            "focus": "Ein konkreter Use Case",
            "exercise": [
                "3 Ideen sammeln",
                "1 auswählen",
                "kleinen Test starten"
            ],
            "commitment": "Ein KI-Test wurde gestartet"
        },
        "Umsetzungsproblem": {
            "text": "Es gibt Ideen. Aber zu wenig Umsetzung.",
            "focus": "Verbindlichkeit erhöhen",
            "exercise": [
                "Ein Projekt auswählen",
                "Deadline setzen",
                "Checkpoints definieren"
            ],
            "commitment": "Ein Projekt wurde konsequent gestartet"
        },
        "Stabile Basis": {
            "text": "Gute Basis. Jetzt geht es um gezielte Weiterentwicklung.",
            "focus": "Ein Zukunftsthema vorantreiben",
            "exercise": [
                "Ein Thema definieren",
                "Ideen sammeln",
                "erste Tests starten"
            ],
            "commitment": "Ein Thema wurde aktiv gestartet"
        }
    }[pattern]

# ---------------- NAV ----------------
page = st.sidebar.radio("Bereich", ["Befragung", "Dashboard", "Entwicklung", "Aktionsplan"])

# ---------------- BEFRAGUNG ----------------
if page == "Befragung":
    st.title("Mobiliar Forum Navigator")

    with st.form("scan"):
        answers = {}

        for dim, questions in DIMENSIONS.items():
            st.subheader(dim.capitalize())
            vals = []
            for i, q in enumerate(questions):
                vals.append(st.slider(q, 1, 5, 3, key=f"{dim}_{i}"))
            answers[dim] = vals

        if st.form_submit_button("Analyse starten"):
            st.session_state.answers = answers
            st.session_state.submitted = True
            st.success("Fertig. Geh ins Dashboard.")

# ---------------- DASHBOARD ----------------
elif page == "Dashboard":
    st.title("Eure Situation")

    if not st.session_state.submitted:
        st.warning("Bitte Befragung ausfüllen")
    else:
        scores = compute_scores(st.session_state.answers)
        pattern = detect_pattern(scores)

        avg = round(sum(scores.values())/len(scores),1)

        st.metric("Gesamtbild", avg)
        st.markdown(f"### Muster: {pattern}")

        st.info("Das ist euer aktuelles Hauptmuster.")

# ---------------- ENTWICKLUNG ----------------
elif page == "Entwicklung":
    st.title("Nächster Schritt")

    if not st.session_state.submitted:
        st.warning("Bitte zuerst Befragung")
    else:
        scores = compute_scores(st.session_state.answers)
        pattern = detect_pattern(scores)
        path = get_path(pattern)

        st.write(path["text"])

        st.markdown("### 🎯 Fokus")
        st.write(path["focus"])

        st.markdown("### 🧠 Übung")
        for s in path["exercise"]:
            st.write(f"• {s}")

        st.markdown("### 🔁 Commitment")
        st.write(path["commitment"])

# ---------------- AKTIONSPLAN ----------------
elif page == "Aktionsplan":
    st.title("Euer nächster konkreter Schritt")

    if not st.session_state.submitted:
        st.warning("Bitte zuerst Befragung")
    else:
        st.session_state.focus = st.text_input("Unser Fokus")
        st.session_state.action = st.text_input("Erster Schritt")
        st.session_state.owner = st.text_input("Verantwortlich")
        st.session_state.deadline = st.text_input("Bis wann")

        if st.button("Speichern"):
            st.success("Fixiert. Jetzt geht es ins Tun.")

        if st.session_state.focus:
            st.markdown("### Eure Vereinbarung")
            st.write(f"Fokus: {st.session_state.focus}")
            st.write(f"Schritt: {st.session_state.action}")
            st.write(f"Verantwortlich: {st.session_state.owner}")
            st.write(f"Deadline: {st.session_state.deadline}")
