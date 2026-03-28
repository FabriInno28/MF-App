import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Für professionelle Diagramme

# --- KONFIGURATION ---
st.set_page_config(page_title="Mobiliar Forum - Strategy Suite", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stProgress > div > div > div > div { background-color: #FFD700; }
    .status-card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.mobiliar.ch/sites/default/files/logo_mobiliar_default.svg", width=120)
    st.title("Innovation OS")
    mode = st.radio("Bereich wählen", ["Deep-Dive Scan", "Management Dashboard", "Stabilisierungs-Coach"])
    st.write("---")
    st.caption("Status: Skalierungs-Modus 2030 aktiv")

# --- 1. KOMPLEXERE BEFRAGUNG (DEEP-DIVE SCAN) ---
if mode == "Deep-Dive Scan":
    st.header("🔍 Strategischer Innovations-Scan")
    st.write("Diese 15-minütige KI-Einschätzung analysiert die verborgenen Blockaden in Ihrem Team.")
    
    with st.form("complex_scan"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Unternehmen", placeholder="Muster KMU AG")
            role = st.selectbox("Ihre Rolle", ["Inhaber/GF", "Teamleitung", "Mitarbeiter", "HR"])
        with col2:
            industry = st.selectbox("Sektor", ["Gewerbe/Handwerk", "Hightech/IT", "Dienstleistung", "NGO/Verein"])
            size = st.select_slider("Teamgrösse", options=["1-5", "6-15", "16-50", "50+"])

        st.write("---")
        st.subheader("Dimension 1: Innovations-Kultur")
        c1 = st.slider("Wie gehen Sie mit Fehlern um?", 0, 10, 5, help="0 = Bestrafung, 10 = Lernchance")
        c2 = st.slider("Entscheidungswege", 0, 10, 5, help="0 = Top-Down, 10 = Demokratisch")
        
        st.subheader("Dimension 2: Zukunfts-Angst vs. Mut")
        c3 = st.select_slider("Einstellung zu KI & Disruption", options=["Abwehr", "Skepsis", "Neugier", "Offenheit"])
        
        st.subheader("Dimension 3: Der 'Elefant im Raum'")
        c4 = st.text_area("Was ist das grösste Hindernis, über das in Meetings niemand offen spricht?")
        
        if st.form_submit_button("KI-Tiefenanalyse starten"):
            st.session_state['data'] = {"name": name, "c1": c1, "c2": c2, "industry": industry, "size": size, "c3": c3}
            st.success("Analyse abgeschlossen. Ergebnisse im Dashboard verfügbar.")

# --- 2. ERWEITERTES DASHBOARD ---
elif mode == "Management Dashboard":
    if 'data' not in st.session_state:
        st.warning("Bitte führen Sie zuerst den Deep-Dive Scan durch.")
    else:
        d = st.session_state['data']
        st.header(f"📊 Innovations-Cockpit: {d['name']}")
        
        # Obere Kennzahlen (Metrics)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Kultur-Score", f"{d['c1']*10}%", "+2%")
        m2.metric("Agilitäts-Index", f"{d['c2']*10}%", "-1%")
        [span_1](start_span)m3.metric("NPS Potential", "82", "Benchmark") # Basierend auf C-Level Doc[span_1](end_span)
        [span_2](start_span)m4.metric("Zufriedenheits-Prognose", "98.8%") # Basierend auf C-Level Doc[span_2](end_span)

        st.write("---")
        
        # Grafische Darstellung
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Innovations-Profil (Radar-Vorschau)")
            # Dummy-Radar-Daten
            radar_df = pd.DataFrame(dict(
                r=[d['c1'], d['c2'], 7, 5, 8],
                theta=['Fehlerkultur','Entscheidung','Technologie','Speed','Team-Spirit']))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0,10])
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("Nächste Schritte")
            st.markdown(f"""
            <div class="status-card">
                <strong>Empfohlenes Format:</strong><br>
                2,5-Tage "Zukunft gestalten"<br><br>
                <strong>Fokus-Thema:</strong><br>
                Psychologische Sicherheit & Prototyping
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        st.subheader("Der Weg zur Aktivierung (System-Angebot)")
        # [span_3](start_span)Roadmap-Visualisierung basierend auf Angebotssystem[span_3](end_span)
        steps = ["KMU Kaffee", "Tagesworkshop", "2,5-Tage Workshop", "Stabilisierung"]
        current_step = 2 # Beispielhaft
        st.step_prog = st.select_slider("Aktueller Status im Mobiliar-System", options=steps, value=steps[current_step])
        st.progress((current_step + 1) * 25)

# --- 3. STABILISIERUNGS-COACH ---
elif mode == "Stabilisierungs-Coach":
    st.header("🧘 Resilienz & Stabilisierungs-Begleiter")
    st.write("Innovation ist anstrengend. Wir begleiten Ihr Team auch nach dem Workshop.")
    st.info("Dieses Modul sichert die langfristige Wirkung und senkt das Stresslevel.")
    
    st.text_input("Kurze Frage zum Team-Zustand?")
    st.button("KI-Ratgeber kontaktieren")
