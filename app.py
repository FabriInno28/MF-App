import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- INIT & SESSION STATE ----------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------- STYLING ----------------
st.markdown("""
<style>
    .insight-box { background: #fdfdfd; padding: 1.2rem; border-radius: 0.8rem; border-left: 6px solid #d6001c; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .reco-box { background: #fffcf0; padding: 1.2rem; border-radius: 0.8rem; border-left: 6px solid #f2b300; margin-bottom: 1rem; }
    .stButton>button { background-color: #d6001c; color: white; border-radius: 5px; width: 100%; font-weight: bold; }
    @media print { .no-print { display: none !important; } }
</style>
""", unsafe_allow_html=True)

# ---------------- DATEN & SORGENBAROMETER ----------------
DIMENSIONS = {
    "resilienz": {
        "label": "Wirtschaftliche Resilienz",
        "questions": [
            "Wir fühlen uns gewappnet gegen steigende Energiekosten & Inflation.",
            "Fachkräftemangel beeinträchtigt unsere Lieferfähigkeit aktuell kaum.",
            "Regulatorische Hürden (Bürokratie) bremsen unseren Alltag nicht aus."
        ]
    },
    "entscheidung": {
        "label": "Entscheidungskraft",
        "questions": [
            "Wichtige Weichenstellungen werden bei uns rechtzeitig getroffen.",
            "Zuständigkeiten sind klar, damit wir bei Marktänderungen schnell reagieren.",
            "Schwierige Themen werden bei uns nicht systematisch vertagt."
        ]
    },
    "zukunft": {
        "label": "Zukunftsfähigkeit",
        "questions": [
            "Wir haben ein klares Bild, wo wir in 3 Jahren stehen wollen.",
            "Wir investieren genug Zeit in Innovation statt nur ins Tagesgeschäft.",
            "Die Nachfolgeplanung oder langfristige Strategie ist bei uns geklärt."
        ]
    }
}

# ---------------- HELPER ----------------
def compute_scores(answers):
    return {k: round(sum(v) / len(v) * 20, 1) for k, v in answers.items()}

def get_recommendation(scores, sector, size):
    avg = sum(scores.values()) / len(scores)
    # Branchen-spezifischer Fokus
    focus = "Prozess-Optimierung" if sector == "Industrie" else "Kundenbindung & Effizienz"
    
    if avg < 55:
        return "Tagesworkshop Orientierung", "Fokus: Prioritäten setzen & Ballast abwerfen.", focus
    elif avg < 75:
        return "Tagesworkshop Ideen entwickeln", "Fokus: Neue Wege finden trotz Fachkräftemangel.", focus
    else:
        return "2.5 Tage Zukunft gestalten", "Fokus: Radikale Innovation & langfristige Resilienz.", focus

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://www.mobiliar.ch/sites/default/files/logo_mobiliar_default.svg", width=120)
    st.title("Forum Navigator")
    page = st.radio("Navigation", ["1. Standortbestimmung", "2. Management Dashboard", "3. Impulse & Buchung"])
    st.markdown("---")
    st.caption("Ein Service des Mobiliar Forums")

# ---------------- PAGE 1: SCAN ----------------
if page == "1. Standortbestimmung":
    st.title("Strategische Standortbestimmung")
    st.write("Basierend auf den grössten Herausforderungen der Schweizer KMU (Sorgenbarometer).")

    with st.form("scan_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Unternehmen", placeholder="Muster KMU AG")
            sector = st.selectbox("Sektor", ["Gewerbe", "Dienstleistung", "Industrie", "NGO"])
        with col2:
            size = st.selectbox("Teamgrösse", ["1-5", "6-15", "16-50", "50+"])
            role = st.selectbox("Ihre Rolle", ["Inhaber/GF", "Teamleitung", "Mitarbeitende"])

        st.write("---")
        local_answers = {}
        for dim, cfg in DIMENSIONS.items():
            st.subheader(cfg["label"])
            vals = []
            for q in cfg["questions"]:
                vals.append(st.slider(q, 1, 5, 3))
            local_answers[dim] = vals
        
        if st.form_submit_button("Analyse erstellen"):
            st.session_state.answers = local_answers
            st.session_state.profile = {"company": company, "sector": sector, "size": size}
            st.session_state.submitted = True
            st.balloons()

# ---------------- PAGE 2: DASHBOARD ----------------
elif page == "2. Management Dashboard":
    if not st.session_state.submitted:
        st.warning("Bitte zuerst die Standortbestimmung ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        rec_format, rec_text, sector_focus = get_recommendation(scores, st.session_state.profile["sector"], st.session_state.profile["size"])

        st.title(f"Dashboard: {st.session_state.profile['company']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Resilienz-Index", f"{scores['resilienz']}%")
        m2.metric("Zukunfts-Score", f"{scores['zukunft']}%")
        m3.metric("NPS Benchmark", "82", "Top-Level")

        # Bar Chart
        df = pd.DataFrame({"Dimension": [DIMENSIONS[k]["label"] for k in scores.keys()], "Score": list(scores.values())})
        fig = px.bar(df, x="Dimension", y="Score", range_y=[0,100], color_discrete_sequence=['#d6001c'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4>Analyse-Ergebnis</h4>
            Ihr grösster Hebel liegt aktuell im Bereich <strong>{min(scores, key=scores.get)}</strong>. <br>
            Als Unternehmen im Sektor <strong>{st.session_state.profile['sector']}</strong> sollten Sie den Fokus auf <em>{sector_focus}</em> legen.
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 TIPP: Nutzen Sie die Druckfunktion Ihres Browsers (Strg+P), um dieses Dashboard als PDF zu speichern.")

# ---------------- PAGE 3: IMPULSE & BUCHUNG ----------------
elif page == "3. Impulse & Buchung":
    if not st.session_state.submitted:
        st.warning("Bitte zuerst den Scan ausfüllen.")
    else:
        scores = compute_scores(st.session_state.answers)
        rec_format, rec_text, _ = get_recommendation(scores, st.session_state.profile["sector"], st.session_state.profile["size"])

        st.title("Nächste Schritte")
        
        st.markdown(f"""
        <div class="reco-box">
            <h3>Unsere Empfehlung: {rec_format}</h3>
            <p>{rec_text}</p>
            <a href="https://www.mobiliarforum.ch" target="_blank">
                <button style="background-color: #d6001c; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    Jetzt Termin anfragen
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        st.subheader("Inspirations-Quellen für Ihr Team")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Video (SRF Impact)**")
            st.write("Fachkräftemangel: Wie KMU neue Wege gehen.")
            st.markdown("[Zum Video](https://www.srf.ch/play/tv/sendung/impact?id=d7e35791-2090-410a-8105-0a3a41160918)")
        with c2:
            st.markdown("**Podcast (SRF Trend)**")
            st.write("Wirtschaft im Wandel – Was KMU jetzt wissen müssen.")
            st.markdown("[Zum Podcast](https://www.srf.ch/audio/trend)")
        with c3:
            st.markdown("**Ratgeber Mobiliar**")
            st.write("Leitfaden für Resilienz & Nachfolge.")
            st.markdown("[Zum Ratgeber](https://www.mobiliar.ch/versicherungen-und-vorsorge/unternehmen/ratgeber)")
