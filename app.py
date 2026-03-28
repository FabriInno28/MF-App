import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------- INIT ----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------- CONFIG ----------
DIMENSIONS = {
    "orientierung": {
        "label": "Orientierung",
        "questions": [
            "Wir haben ein klares Bild, wohin wir uns entwickeln wollen.",
            "Wir priorisieren Zukunftsthemen bewusst.",
            "Unklarheit führt bei uns selten zu Stillstand."
        ]
    },
    "entscheidung": {
        "label": "Entscheidungskraft",
        "questions": [
            "Wichtige Entscheidungen werden rechtzeitig gefällt.",
            "Zuständigkeiten sind klar genug.",
            "Wir vertagen unangenehme Themen nicht systematisch."
        ]
    },
    "umsetzung": {
        "label": "Umsetzung",
        "questions": [
            "Wir bringen Vorhaben konsequent in die Umsetzung.",
            "Zwischen Idee und Test vergeht wenig Zeit.",
            "Wir setzen bewusst Prioritäten."
        ]
    },
    "kultur": {
        "label": "Kultur",
        "questions": [
            "Probleme können offen angesprochen werden.",
            "Fehler führen eher zu Lernen als zu Schuld.",
            "Vertrauen ist stärker als Absicherung."
        ]
    },
    "ki": {
        "label": "KI und Wandel",
        "questions": [
            "Wir diskutieren konkrete KI Anwendungen.",
            "Wir erkennen, wo KI echten Nutzen bringen könnte.",
            "Wir probieren neue Werkzeuge pragmatisch aus."
        ]
    }
}

def compute_scores(answers: dict) -> dict:
    scores = {}
    for dim, vals in answers.items():
        if vals:
            scores[dim] = round(sum(vals) / len(vals) * 20, 1)  # 1-5 -> 20-100
        else:
            scores[dim] = 0.0
    return scores

def detect_patterns(scores: dict) -> list[str]:
    patterns = []

    if scores.get("orientierung", 0) < 55 and scores.get("entscheidung", 0) < 55:
        patterns.append("Viel Unsicherheit, wenig Klarheit in den Entscheidungen.")
    if scores.get("kultur", 0) >= 70 and scores.get("umsetzung", 0) < 55:
        patterns.append("Es wird reflektiert, aber zu wenig konsequent umgesetzt.")
    if scores.get("ki", 0) >= 70 and scores.get("orientierung", 0) < 55:
        patterns.append("Interesse an KI ist da, aber ohne klares Zukunftsbild.")
    if scores.get("kultur", 0) < 55:
        patterns.append("Zusammenarbeit und Vertrauen sind ein möglicher Engpass.")

    if not patterns:
        patterns.append("Kein akuter Strukturbruch sichtbar. Fokus auf gezielte Weiterentwicklung.")

    return patterns

def recommend(scores: dict) -> tuple[str, str]:
    if scores.get("orientierung", 0) < 55:
        return (
            "Tagesworkshop Orientierung schaffen",
            "Zuerst braucht es Fokus, Prioritäten und ein gemeinsames Verständnis der Lage."
        )
    if scores.get("umsetzung", 0) < 55:
        return (
            "Tagesworkshop Veränderung begleiten",
            "Der Engpass liegt weniger bei Ideen als bei Verbindlichkeit und Umsetzung."
        )
    if scores.get("ki", 0) >= 70 and scores.get("orientierung", 0) >= 60:
        return (
            "2.5 Tage Zukunft gestalten",
            "Es ist genug Offenheit da, um tiefer an Zukunftsbildern und Lösungen zu arbeiten."
        )
    return (
        "Tagesworkshop Ideen entwickeln",
        "Es gibt genügend Basis, um konkrete Lösungsansätze gemeinsam zu entwickeln."
    )

# ---------- SIDEBAR ----------
page = st.sidebar.radio("Bereich", ["Scan", "Dashboard"])

# ---------- PAGE: SCAN ----------
if page == "Scan":
    st.title("Mobiliar Forum Navigator")
    st.subheader("Strategischer Scan")

    with st.form("scan_form"):
        c1, c2 = st.columns(2)

        with c1:
            company = st.text_input("Unternehmen", placeholder="Muster KMU AG")
            sector = st.selectbox("Sektor", ["Gewerbe", "Dienstleistung", "Industrie", "NGO"])

        with c2:
            role = st.selectbox("Rolle", ["Geschäftsleitung", "Teamleitung", "Mitarbeitende"])
            size = st.selectbox("Teamgrösse", ["1-5", "6-15", "16-50", "50+"])

        st.write("### Einschätzung")

        local_answers = {}

        for dim, cfg in DIMENSIONS.items():
            st.markdown(f"**{cfg['label']}**")
            values = []
            for i, question in enumerate(cfg["questions"]):
                key = f"{dim}_{i}"
                values.append(st.slider(question, 1, 5, 3, key=key))
            local_answers[dim] = values
            st.write("")

        submitted = st.form_submit_button("Analyse berechnen")

        if submitted:
            st.session_state.profile = {
                "company": company,
                "sector": sector,
                "role": role,
                "size": size,
            }
            st.session_state.answers = local_answers
            st.session_state.submitted = True

    if st.session_state.submitted:
        st.success("Analyse berechnet. Wechsle links ins Dashboard.")

# ---------- PAGE: DASHBOARD ----------
if page == "Dashboard":
    st.title("Management Dashboard")

    if not st.session_state.submitted or not st.session_state.answers:
        st.warning("Bitte zuerst den Scan ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        patterns = detect_patterns(scores)
        rec_title, rec_reason = recommend(scores)

        avg_score = round(sum(scores.values()) / len(scores), 1)
        weakest = min(scores, key=scores.get)

        m1, m2, m3 = st.columns(3)
        m1.metric("Gesamtindex", avg_score)
        m2.metric("Kritische Felder", sum(1 for v in scores.values() if v < 55))
        m3.metric("Grösster Engpass", DIMENSIONS[weakest]["label"])

        df = pd.DataFrame({
            "Dimension": [DIMENSIONS[k]["label"] for k in scores.keys()],
            "Score": list(scores.values())
        })

        fig = px.bar(df, x="Dimension", y="Score", text="Score", range_y=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        left, right = st.columns([2, 1])

        with left:
            st.subheader("Erkannte Muster")
            for p in patterns:
                st.write(f"• {p}")

        with right:
            st.subheader("Empfehlung")
            st.info(f"**{rec_title}**\n\n{rec_reason}")

            st.subheader("Quick Wins")
            st.write("• Eine vertagte Entscheidung aktiv klären")
            st.write("• Ein Zukunftsthema bewusst priorisieren")
            st.write("• Ein kleines Experiment in 14 Tagen starten")
