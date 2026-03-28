import streamlit as st
import pandas as pd
import random

# --- KONFIGURATION & BRANDING ---
st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# Custom CSS für den "Mobiliar-Look" (Gelb/Schwarz/Weiss)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #FFD700; color: black; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://www.mobiliar.ch/sites/default/files/logo_mobiliar_default.svg", width=150)
    st.title("Forum Companion")
    choice = st.radio("Menü", ["1. KI-Innovation Scan", "2. Mein Dashboard", "3. KI-Coach (Beta)"])

# --- MODUL 1: KI-INNOVATION SCAN ---
if choice == "1. KI-Innovation Scan":
    st.header("🚀 KI-Innovation Scan (15 Min)")
    st.write("Bereite dein Team auf die 25 Standorte 2026 vor.")
    
    with st.container():
        name = st.text_input("Name deines Unternehmens / Vereins")
        sector = st.selectbox("Branche", ["Gewerbe", "Dienstleistung", "NGO/Verein", "Industrie"])
        st.write("---")
        st.subheader("Wo steht ihr aktuell?")
        q1 = st.select_slider("Wie innovationsfreudig ist das Team?", options=["Blockiert", "Abwartend", "Offen", "Pioniere"])
        q2 = st.text_area("Was ist eure grösste Hürde (z.B. Zeit, Budget, Mindset)?")
        
        if st.button("Analyse generieren"):
            st.session_state['scan_done'] = True
            st.session_state['name'] = name
            st.session_state['sector'] = sector
            st.balloons()
            st.success("KI-Einschätzung erstellt! Gehe jetzt zu 'Mein Dashboard'.")

# --- MODUL 2: INDIVIDUELLES DASHBOARD ---
elif choice == "2. Mein Dashboard":
    if 'scan_done' not in st.session_state:
        st.warning("Bitte führe zuerst den KI-Innovation Scan durch!")
    else:
        st.header(f"📊 Dashboard: {st.session_state['name']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Aktivierungs-Level", "Bereit für Tag 1", "Stark")
        col2.metric("Resilienz-Score", "74%", "+5%")
        col3.metric("Format", "2,5 Tage", "Empfohlen")

        st.subheader("Deine massgeschneiderte Roadmap 2026")
        
        # Dynamische Empfehlung basierend auf dem Scan
        roadmap = {
            "Phase": ["Einstieg (Kaffee)", "Aktivierung (Workshop)", "Stabilisierung (Follow-up)"],
            "Status": ["Erledigt ✅", "In Planung 🗓️", "Ausstehend ⏳"],
            "Fokus": ["Bedarfsanalyse", "Prototyping & Design Thinking", "Resilienz & Stress-Check"]
        }
        st.table(pd.DataFrame(roadmap))
        
        st.info(f"**KI-Tipp für {st.session_state['sector']}:** Euer Fokus sollte auf 'schlanken Prozessen' liegen. Nutzt den Standort in eurer Nähe für den 2,5-Tage-Workshop.")

# --- MODUL 3: KI-COACH ---
elif choice == "3. KI-Coach (Beta)":
    st.header("🤖 Dein KI-Innovations-Coach")
    st.write("Stell eine Frage zu eurer Transformation oder dem Mobiliar Forum.")
    
    user_input = st.text_input("Deine Frage (z.B. Wie motiviere ich mein Team für Innovation?)")
    if user_input:
        # Simulierter KI-Response (Hier käme später die API-Anbindung an GPT-4 oder Gemini)
        responses = [
            "Innovation startet bei der psychologischen Sicherheit. Im Mobiliar Forum schaffen wir diesen Raum.",
            "Versuch es mit kleinen Prototypen. 'Fail fast' ist unser Motto im 2,5-Tage Workshop.",
            "Für euer Gewerbe ist es wichtig, die Kunden direkt in den Prozess einzubeziehen."
        ]
        st.chat_message("assistant").write(random.choice(responses))

