import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
    .main { background-color: #f9f9f9; }
    .kmu-card { background: white; padding: 25px; border-radius: 12px; border-left: 8px solid #d6001c; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 25px; }
    .stButton>button { background-color: #d6001c; color: white; border-radius: 6px; height: 3em; font-weight: bold; }
    h1, h2, h3 { color: #d6001c; font-family: 'Arial Narrow', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ---------------- FRAGEN ----------------
QUESTIONS = {
    "Markt": "Wie stark spüren Sie Druck durch Konkurrenz oder neue Technologien?",
    "Personal": "Wie kritisch ist die Situation bei Fachkräften und im Team?",
    "Prozesse": "Wie sehr bremsen veraltete Abläufe oder IT-Probleme?",
    "Finanzen": "Wie stark belasten steigende Kosten Ihr Geschäft?",
    "Strategie": "Wie klar ist Ihre langfristige Ausrichtung?"
}

# ---------------- ANALYSE ----------------
def analyze_profile(data, text):
    text = text.lower()

    dominant = max(data, key=data.get)

    # Muster erkennen
    if data["Strategie"] >= 4 and data["Markt"] >= 4:
        pattern = "Zukunft ist da, aber nicht klar greifbar."
        recommendation = "Orientierung schaffen"
        reason = "Hoher Marktdruck trifft auf fehlende strategische Klarheit."
    elif data["Personal"] >= 4 and data["Prozesse"] >= 4:
        pattern = "Das Tagesgeschäft dominiert. Das Team läuft am Limit."
        recommendation = "Veränderung begleiten"
        reason = "Operative Belastung blockiert Entwicklung."
    elif data["Markt"] >= 4 and data["Strategie"] <= 3:
        pattern = "Chancen sind da, aber sie werden nicht systematisch genutzt."
        recommendation = "Ideen entwickeln"
        reason = "Marktdynamik ist hoch, aber Ideen fehlen oder werden nicht priorisiert."
    else:
        pattern = "Mehrere Spannungsfelder gleichzeitig."
        recommendation = "Orientierung schaffen"
        reason = "Keine klare Priorisierung erkennbar."

    # Text Hinweise
    if any(w in text for w in ["zeit", "stress", "überlastet"]):
        pattern += " Zusätzlich zeigt sich ein klarer Ressourcenengpass."
    if any(w in text for w in ["unklar", "wohin", "ziel"]):
        pattern += " Die strategische Richtung ist aktuell nicht ausreichend geschärft."

    return dominant, pattern, recommendation, reason

def get_action_plan(format_type):
    if format_type == "Orientierung schaffen":
        return [
            "Die drei grössten Unsicherheiten im Führungsteam offen benennen",
            "Gemeinsam priorisieren, wo wirklich Handlungsbedarf besteht",
            "Ein klares Zukunftsthema definieren"
        ], [
            "Mit dem Team einen Tag raus aus dem Alltag gehen",
            "Die wichtigsten Spannungsfelder strukturiert bearbeiten",
            "Konkrete nächste Schritte festlegen"
        ]
    elif format_type == "Ideen entwickeln":
        return [
            "Bestehende Ideen sammeln und sichtbar machen",
            "Kundenperspektive bewusst einnehmen",
            "1–2 Ideen auswählen und schärfen"
        ], [
            "Ideen strukturiert testen",
            "Erste Prototypen oder Experimente starten",
            "Verantwortlichkeiten klären"
        ]
    else:
        return [
            "Die grössten operativen Blockaden sichtbar machen",
            "Verantwortlichkeiten klären",
            "Erste Entlastung schaffen"
        ], [
            "Arbeitsweise im Team reflektieren",
            "Klare Prioritäten setzen",
            "Veränderung aktiv begleiten"
        ]

# ---------------- NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Scan"

# ---------------- PAGE 1 ----------------
if st.session_state.page == "Scan":
    st.title("Mobiliar Forum Navigator")
    st.write("Standortbestimmung für Geschäftsleitungen von KMU.")

    with st.form("scan"):
        results = {}
        for key, q in QUESTIONS.items():
            results[key] = st.slider(q, 1, 5, 3)

        text = st.text_area("Was hindert Sie aktuell am meisten daran, Ihr Unternehmen weiterzuentwickeln?")

        if st.form_submit_button("Analyse starten"):
            st.session_state.data = results
            st.session_state.text = text
            st.session_state.page = "Dashboard"
            st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.page == "Dashboard":
    st.title("Ihre Standortbestimmung")

    d = st.session_state.data
    text = st.session_state.text

    dominant, pattern, rec, reason = analyze_profile(d, text)

    # RADAR
    categories = list(d.keys())
    values = list(d.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color='#d6001c')
    ))

    st.plotly_chart(fig, use_container_width=True)

    # SUMMARY
    st.markdown(f"""
    <div class="kmu-card">
    <h3>Einordnung</h3>
    <p><strong>Grösster Druck:</strong> {dominant}</p>
    <p><strong>Muster:</strong> {pattern}</p>
    </div>
    """, unsafe_allow_html=True)

    # EMPFEHLUNG
    st.markdown(f"""
    <div class="kmu-card">
    <h3>Empfohlenes Format</h3>
    <p><strong>{rec}</strong></p>
    <p>{reason}</p>
    <p>Ein Tag im Mobiliar Forum hilft, genau diese Situation strukturiert zu klären und konkrete nächste Schritte zu definieren.</p>
    </div>
    """, unsafe_allow_html=True)

    # AKTIONSPLAN
    short, mid = get_action_plan(rec)

    st.subheader("Nächste Schritte")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**In den nächsten 14 Tagen**")
        for s in short:
            st.write("•", s)

    with col2:
        st.markdown("**In den nächsten 30 Tagen**")
        for m in mid:
            st.write("•", m)

    # RESSOURCEN
    st.subheader("Impulse")

    if rec == "Orientierung schaffen":
        st.write("Podcast: Zukunft gestalten in unsicheren Zeiten")
        st.write("Reflexionsfrage: Woran messen wir in 12 Monaten, ob wir auf dem richtigen Weg sind?")
    elif rec == "Ideen entwickeln":
        st.write("Podcast: Von der Idee zur Umsetzung")
        st.write("Übung: 3 Ideen in 30 Minuten skizzieren")
    else:
        st.write("Podcast: Teams unter Druck führen")
        st.write("Übung: Was stoppen wir sofort?")

    if st.button("Neue Analyse starten"):
        st.session_state.page = "Scan"
        st.rerun()
