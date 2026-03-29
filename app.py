import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- KMU STYLING ----------------
st.markdown("""
<style>
    .reportview-container { background: #f4f4f4; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .kmu-card { background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #d6001c; margin-bottom: 20px; }
    h1, h2, h3 { color: #d6001c; }
</style>
""", unsafe_allow_html=True)

# ---------------- FRAGEN-LOGIK (KMU SORGENBAROMETER) ----------------
# Wir fragen nach Symptomen, nicht nach Theorie
QUESTIONS = {
    "Personal": "Finden wir aktuell kaum Leute oder verlieren gute Mitarbeiter?",
    "Zeit": "Frisst das Tagesgeschäft (Papierkrieg) die Zeit für Neues komplett auf?",
    "Entscheidung": "Bleiben wichtige Entscheide liegen, weil wir uns unsicher sind?",
    "Kosten": "Machen uns die steigenden Fixkosten (Energie, Miete) schlaflose Nächte?",
    "Zukunft": "Fehlt uns ein klarer Plan, wo wir in 5 Jahren stehen wollen?"
}

# ---------------- PAGE 1: DER REALITÄTS-CHECK ----------------
if "step" not in st.session_state: st.session_state.step = "Scan"

if st.session_state.step == "Scan":
    st.title("Der KMU-Realitäts-Check")
    st.write("Ehrliche Standortbestimmung – dauert 3 Minuten.")

    with st.form("kmu_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Firma / Organisation")
            sector = st.selectbox("Branche", ["Bau/Gewerbe", "Detailhandel", "Dienstleistung", "Gastro/Hotellerie", "Industrie"])
        with col2:
            size = st.selectbox("Teamgrösse", ["1-10 (Kleinbetrieb)", "11-50 (KMU)", "50+ (Grossbetrieb)"])
        
        st.markdown("---")
        st.subheader("Wo drückt der Schuh?")
        st.write("1 = Alles im Griff | 5 = Hier brennt es")
        
        results = {}
        for key, q in QUESTIONS.items():
            results[key] = st.select_slider(q, options=[1, 2, 3, 4, 5], value=3)
            
        if st.form_submit_button("Auswertung anzeigen"):
            st.session_state.data = results
            st.session_state.profile = {"company": company, "sector": sector}
            st.session_state.step = "Dashboard"
            st.rerun()

# ---------------- PAGE 2: DAS UNTERNEHMER-COCKPIT ----------------
elif st.session_state.step == "Dashboard":
    st.title(f"Unternehmer-Cockpit: {st.session_state.profile['company']}")
    
    d = st.session_state.data
    
    # RADAR CHART (Der "Strategie-Look")
    categories = list(QUESTIONS.keys())
    # Invertieren für Radar (5 = schlecht, also 6-d)
    values = [6-d[cat] for cat in categories] 
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=values,
          theta=categories,
          fill='toself',
          fillcolor='rgba(214, 0, 28, 0.3)',
          line=dict(color='#d6001c'),
          name='Ist-Zustand'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    
    col_chart, col_metrics = st.columns([1.5, 1])
    
    with col_chart:
        st.plotly_chart(fig, use_container_width=True)
        
    with col_metrics:
        avg_score = sum(d.values()) / len(d)
        status = "KRITISCH" if avg_score > 3.5 else "STABIL" if avg_score < 2.5 else "GEFORDERT"
        color = "#d6001c" if status == "KRITISCH" else "#f2b300" if status == "GEFORDERT" else "#27ae60"
        
        st.markdown(f"""
            <div style="background:{color}; color:white; padding:20px; border-radius:10px; text-align:center;">
                <h2 style="color:white; margin:0;">STATUS: {status}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.metric("Handlungsbedarf", "HOCH" if avg_score > 3 else "MITTEL")
        st.metric("NPS Forum Benchmark", "82", "Ihr Ziel")

    st.markdown("---")
    
    # HANDLUNGSEMPFEHLUNG
    st.subheader("Nächste Schritte für den Patron")
    
    recos = {
        "Personal": "Mitarbeiter-Befähigung (Workshop Veränderung begleiten)",
        "Zeit": "Prozess-Entschlackung (Tagesworkshop Ideen entwickeln)",
        "Entscheidung": "Führungs-Klarheit (Orientierung schaffen)",
        "Kosten": "Resilienz-Check & Geschäftsmodell-Review",
        "Zukunft": "Zukunft gestalten (2.5 Tage Intensiv-Workshop)"
    }
    
    # Den grössten Schmerzpunkt finden (höchster Wert)
    main_pain = max(d, key=d.get)
    
    st.markdown(f"""
        <div class="kmu-card">
            <h4>💡 Fokus-Empfehlung</h4>
            Ihr grösster Engpass liegt aktuell im Bereich <strong>{main_pain}</strong>.<br><br>
            <strong>Vorschlag:</strong> {recos[main_pain]}<br>
            Das Ziel: Den Kopf wieder frei bekommen für das Wesentliche.
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Direkt Buchung anfragen"):
        st.write("Leite weiter zu www.mobiliarforum.ch...")

    if st.button("Zurück zum Scan"):
        st.session_state.step = "Scan"
        st.rerun()
