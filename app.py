import streamlit as st
import pandas as pd
import random

# --- KONFIGURATION & BRANDING ---
st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# Custom CSS für den Mobiliar-Look
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #FFD700; color: black; border-radius: 5px; width: 100%; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Mobiliar Forum")
    st.subheader("Innovations-Begleiter")
    choice = st.radio("Menü", ["1. KI-Innovation Scan", "2. Mein Dashboard", "3. KI-Coach"])
    st.info("Ziel 2030: 25'000 KMU jährlich aktivieren.")

# --- MODUL 1: KI-INNOVATION SCAN (15 MINUTEN) ---
if choice == "1. KI-Innovation Scan":
    st.header("🚀 KI-Innovation Scan")
    st.write("Identifiziere die Lücken in eurem System und starte die Aktivierung.")
    
    with st.form("scan_form"):
        name = st.text_input("Name des KMU / Vereins")
        sector = st.selectbox("Branche", ["Gewerbe", "Dienstleistung", "NGO", "Industrie"])
        st.write("---")
        st.subheader("Selbsteinschätzung")
        q1 = st.select_slider("Wie bereit ist das Team für Veränderung?", 
                              options=["Blockiert", "Abwartend", "Bereit", "Vollgas"])
        q2 = st.text_area("Was ist eure grösste Hürde beim Starten?")
        
        if st.form_submit_button("KI-Analyse erstellen"):
            st.session_state['scan_done'] = True
            st.session_state['name'] = name
            st.session_state['sector'] = sector
            st.session_state['q1'] = q1
            st.success("Analyse abgeschlossen! Wechseln Sie zum 'Dashboard'.")

# --- MODUL 2: INDIVIDUELLES DASHBOARD ---
elif choice == "2. Mein Dashboard":
    if 'scan_done' not in st.session_state:
        st.warning("Bitte führen Sie zuerst den KI-Innovation Scan durch.")
    else:
        st.header(f"📊 Dashboard: {st.session_state['name']}")
        
        # Kennzahlen aus der Analyse
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Aktivierungs-Status", st.session_state['q1'])
        with col2:
            st.metric("NPS Benchmark", "82", "Top-Wert")
        with col3:
            st.metric("Zufriedenheits-Ziel", "98.8%")

        st.subheader("Eure massgeschneiderte Entwicklung")
        
        # Das System-Angebot abbilden
        roadmap = {
            "Phase": ["Einstieg: KMU Kaffee", "Aktivierung: Tagesworkshop", "Vertiefung: 2,5-Tage", "Stabilisierung"],
            "Inhalt": ["Bedarf klären", "Erste Ideen", "Zukunft gestalten", "Resilienz & Stress"],
            "Status": ["✅ Erledigt", "⏳ Nächster Schritt", "⚪ Geplant", "⚪ Geplant"]
        }
        st.table(pd.DataFrame(roadmap))
        
        st.info(f"**KI-Empfehlung:** Da ihr im Bereich '{st.session_state['sector']}' tätig seid, liegt euer Fokus auf der 'Stabilisierung'.")

# --- MODUL 3: KI-COACH ---
elif choice == "3. KI-Coach":
    st.header("🤖 KI-Coach für KMU-Teams")
    st.write("Fragen zur Transformation oder Resilienz?")
    
    user_q = st.text_input("Deine Frage an den Coach:")
    if user_q:
        responses = [
            "Das Mobiliar Forum hilft euch, die Lücke zwischen Idee und Umsetzung zu schliessen.",
            "Innovation braucht psychologische Sicherheit. Startet mit einem KMU Kaffee.",
            "Resilienz ist der Schlüssel zum langfristigen Erfolg nach dem Workshop."
        ]
        st.chat_message("assistant").write(random.choice(responses))
