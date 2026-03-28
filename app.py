import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# --- KONFIGURATION & BRANDING ---
st.set_page_config(page_title="Mobiliar Forum - Innovation OS", layout="wide")

# Custom CSS für den Mobiliar-Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #FFD700; color: black; border-radius: 5px; width: 100%; font-weight: bold; }
    .status-card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Mobiliar Forum")
    st.subheader("Innovation OS")
    mode = st.radio("Bereich wählen", ["Deep-Dive Scan", "Management Dashboard", "Stabilisierungs-Coach"])
    st.write("---")
    st.info("Ziel 2030: 25'000 KMU jährlich aktivieren.")

# --- 1. KOMPLEXER SCAN ---
if mode == "Deep-Dive Scan":
    st.header("🔍 Strategischer Innovations-Scan")
    st.write("Diese 15-minütige KI-Einschätzung analysiert die Potenziale Ihres Teams.")
    
    with st.form("complex_scan"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Unternehmen", placeholder="Muster KMU AG")
            industry = st.selectbox("Sektor", ["Gewerbe", "Dienstleistung", "Industrie", "NGO"])
        with col2:
            role = st.selectbox("Ihre Rolle", ["Geschäftsleitung", "Teamleitung", "Mitarbeiter"])
            size = st.select_slider("Teamgrösse", options=["1-5", "6-15", "16-50", "50+"])

        st.write("---")
        st.subheader("Analyse-Dimensionen")
        c1 = st.slider("Fehlerkultur (0=Angst, 10=Lernen)", 0, 10, 5)
        c2 = st.slider("Entscheidungs-Speed (0=Langsam, 10=Agil)", 0, 10, 5)
        c3 = st.select_slider("Einstellung zu KI & Wandel", options=["Abwehr", "Skepsis", "Neugier", "Offenheit"])
        
        if st.form_submit_button("KI-Analyse starten"):
            st.session_state['data'] = {"name": name, "c1": c1, "c2": c2, "industry": industry, "c3": c3}
            st.success("Analyse abgeschlossen! Wechseln Sie zum Dashboard.")

# --- 2. MANAGEMENT DASHBOARD ---
elif mode == "Management Dashboard":
    if 'data' not in st.session_state:
        st.warning("Bitte führen Sie zuerst den Scan durch.")
    else:
        d = st.session_state['data']
        st.header(f"📊 Cockpit: {d['name']}")
        
        # [span_0](start_span)Kennzahlen aus der C-Level Analyse[span_0](end_span)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Kultur-Index", f"{d['c1']*10}%")
        m2.metric("Agilitäts-Score", f"{d['c2']*10}%")
        m3.metric("NPS Benchmark", "82")
        m4.metric("Zufriedenheits-Ziel", "98.8%")

        st.write("---")
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Innovations-Profil")
            radar_df = pd.DataFrame(dict(
                r=[d['c1'], d['c2'], 7, 6, 8],
                theta=['Kultur','Speed','Technologie','Team','Vision']))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,10])
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("Status & Empfehlung")
            st.markdown(f"""
                <div class="status-card">
                    <strong>Format:</strong> 2,5-Tage Workshop<br>
                    <strong>Fokus:</strong> Zukunft gestalten<br><br>
                    <em>Empfehlung basierend auf Sektor {d['industry']}.</em>
                </div>
            """, unsafe_allow_html=True)

# --- 3. COACH ---
elif mode == "Stabilisierungs-Coach":
    st.header("🤖 Stabilisierungs-Coach")
    st.write("Sicherung der langfristigen Wirkung nach dem Workshop.")
    st.text_input("Frage zur Team-Resilienz:")
    if st.button("Antwort generieren"):
        st.info("Innovation braucht Ausdauer. Fokus auf kleine Siege (Quick Wins) legen.")
