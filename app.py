import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

DIMENSIONS = {
    "orientierung": "Orientierung und Zukunftsbild",
    "entscheidungen": "Entscheidungskraft",
    "zusammenarbeit": "Zusammenarbeit und Vertrauen",
    "kundenfokus": "Kunden und Markt",
    "lernkultur": "Lern und Fehlerkultur",
    "umsetzung": "Umsetzungsdisziplin",
    "ki_wandel": "KI und Technologieoffenheit"
}

QUESTIONS = {
    "orientierung": [
        "Wir haben ein klares Bild, welche Themen für unsere Zukunft wirklich entscheidend sind.",
        "Bei Unsicherheit wissen wir, worauf wir uns zuerst fokussieren.",
        "Unsere Mitarbeitenden verstehen, wohin sich das Unternehmen entwickeln soll."
    ],
    "entscheidungen": [
        "Wichtige Entscheidungen werden rechtzeitig getroffen.",
        "Unklare Zuständigkeiten bremsen uns selten.",
        "Wir vertagen Entscheidungen nicht systematisch."
    ],
    "zusammenarbeit": [
        "In schwierigen Situationen sprechen wir Probleme offen an.",
        "Zwischen Teams funktioniert die Zusammenarbeit gut.",
        "Vertrauen ist bei uns höher als Absicherung."
    ],
    "kundenfokus": [
        "Wir verstehen, was unsere Kundinnen und Kunden aktuell wirklich bewegt.",
        "Wir testen neue Ideen nahe am Markt.",
        "Kundenfeedback fliesst sichtbar in Entscheidungen ein."
    ],
    "lernkultur": [
        "Fehler dürfen bei uns besprochen werden, ohne dass sofort Schuld gesucht wird.",
        "Wir reflektieren systematisch, was funktioniert und was nicht.",
        "Lernen ist Teil des Alltags und nicht nur Theorie."
    ],
    "umsetzung": [
        "Wir bringen Vorhaben konsequent in die Umsetzung.",
        "Zwischen Idee und erstem Test vergeht nicht zu viel Zeit.",
        "Wir setzen bewusst Prioritäten statt alles gleichzeitig zu wollen."
    ],
    "ki_wandel": [
        "Wir sehen KI und technologische Veränderungen eher als Chance.",
        "Wir diskutieren aktiv, wie neue Technologien uns nützen können.",
        "Wir probieren neue Werkzeuge pragmatisch aus."
    ]
}

def init_state():
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "profile" not in st.session_state:
        st.session_state.profile = {}

def compute_scores(answers):
    scores = {}
    for dim, vals in answers.items():
        if vals:
            scores[dim] = round(sum(vals) / len(vals) * 20, 1)  # 1-5 -> 20-100
        else:
            scores[dim] = 0
    return scores

def classify_level(score):
    if score < 45:
        return "kritisch"
    elif score < 65:
        return "fragil"
    elif score < 80:
        return "solide"
    return "stark"

def detect_patterns(scores):
    patterns = []

    if scores["orientierung"] < 60 and scores["entscheidungen"] < 60:
        patterns.append("Orientierung fehlt und Entscheidungen werden zu lange hinausgezögert.")
    if scores["lernkultur"] >= 70 and scores["umsetzung"] < 60:
        patterns.append("Reflexion ist vorhanden, aber die Umsetzungskraft bleibt dahinter zurück.")
    if scores["ki_wandel"] >= 70 and scores["orientierung"] < 60:
        patterns.append("Offenheit für Technologie ist da, aber ohne klares Zukunftsbild.")
    if scores["zusammenarbeit"] < 55:
        patterns.append("Zusammenarbeit und Vertrauen sind aktuell ein Engpass.")
    if not patterns:
        patterns.append("Kein akuter Strukturbruch erkennbar. Fokus auf gezielte Weiterentwicklung.")
    return patterns

def recommend_format(scores):
    avg = sum(scores.values()) / len(scores)

    if scores["orientierung"] < 55:
        return {
            "format": "Tagesworkshop Orientierung schaffen",
            "reason": "Das Team braucht zuerst Klarheit, Fokus und gemeinsame Sprache."
        }
    if scores["umsetzung"] < 55 and scores["entscheidungen"] < 60:
        return {
            "format": "Tagesworkshop Veränderung begleiten",
            "reason": "Der Engpass liegt weniger bei Ideen als bei Umsetzung und Entscheidungsfähigkeit."
        }
    if avg >= 70 and scores["ki_wandel"] >= 70:
        return {
            "format": "2,5 Tage Zukunft gestalten",
            "reason": "Es ist genug Offenheit und Reife da, um tiefer an Zukunftsbildern und Lösungen zu arbeiten."
        }
    return {
        "format": "Tagesworkshop Ideen entwickeln",
        "reason": "Es gibt Entwicklungspotenzial, aber auch genug Basis, um aus konkreten Themen Lösungen zu bauen."
    }

init_state()

st.title("Mobiliar Forum Navigator")
page = st.sidebar.radio("Bereich", ["Scan", "Dashboard"])

if page == "Scan":
    st.subheader("Strategischer Scan")

    with st.form("scan_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.profile["unternehmen"] = st.text_input("Unternehmen")
            st.session_state.profile["sektor"] = st.selectbox("Sektor", ["Gewerbe", "Dienstleistung", "Industrie", "NGO"])
        with c2:
            st.session_state.profile["rolle"] = st.selectbox("Rolle", ["Geschäftsleitung", "Teamleitung", "Mitarbeitende"])
            st.session_state.profile["teamgroesse"] = st.selectbox("Teamgrösse", ["1-5", "6-15", "16-50", "50+"])

        st.write("### Einschätzung")
        for dim, label in DIMENSIONS.items():
            st.markdown(f"**{label}**")
            dim_answers = []
            for q in QUESTIONS[dim]:
                val = st.slider(q, 1, 5, 3, key=f"{dim}_{q}")
                dim_answers.append(val)
            st.session_state.answers[dim] = dim_answers
            st.write("")

        submitted = st.form_submit_button("Analyse berechnen")

    if submitted:
        st.success("Analyse berechnet. Wechseln Sie ins Dashboard.")

elif page == "Dashboard":
    if not st.session_state.answers:
        st.warning("Bitte zuerst den Scan ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        patterns = detect_patterns(scores)
        recommendation = recommend_format(scores)

        st.subheader(f"Cockpit: {st.session_state.profile.get('unternehmen', 'Unternehmen')}")

        m1, m2, m3, m4 = st.columns(4)
        avg_score = round(sum(scores.values()) / len(scores), 1)
        critical_count = sum(1 for s in scores.values() if s < 55)

        m1.metric("Gesamtindex", f"{avg_score}")
        m2.metric("Kritische Felder", critical_count)
        m3.metric("Passendes Format", recommendation["format"])
        m4.metric("Nächster Fokus", min(scores, key=scores.get))

        df = pd.DataFrame({
            "Dimension": [DIMENSIONS[k] for k in scores.keys()],
            "Score": list(scores.values())
        })

        c1, c2 = st.columns([2, 1])

        with c1:
            fig = px.bar(df, x="Dimension", y="Score", range_y=[0, 100], text="Score")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("### Management Einordnung")
            for p in patterns:
                st.write(f"• {p}")

            st.markdown("### Empfehlung")
            st.info(f"**{recommendation['format']}**\n\n{recommendation['reason']}")

            st.markdown("### Quick Wins")
            st.write("• Ein Zukunftsthema bewusst priorisieren")
            st.write("• Eine vertagte Entscheidung klären")
            st.write("• Ein kleines Experiment innert 14 Tagen starten")
