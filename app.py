import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Mobiliar Forum Navigator", layout="wide")

# ---------------- CONFIG ----------------
MOBILIAR_FORUM_URL = "https://www.mobiliarforum.ch"
KMU_KAFFEE_EXAMPLE_URL = "https://www.mobiliar.ch/kmukaffee-biel"

# Diese Links kannst du laufend austauschen oder erweitern
RESOURCE_LIBRARY = {
    "Orientierung schaffen": {
        "podcast_title": "Podcast zur Orientierung in unsicheren Zeiten",
        "podcast_url": "https://www.srf.ch/audio",
        "video_title": "Videoimpuls: Zukunft im KMU greifbar machen",
        "video_url": "https://www.youtube.com",
        "article_title": "Mobiliar Forum",
        "article_url": MOBILIAR_FORUM_URL,
        "exercise_title": "Praxisimpuls: Die 3 grössten Unsicherheiten benennen",
        "exercise_text": "Sammeln Sie im Führungsteam die 3 grössten Unsicherheiten. Ordnen Sie diese in beeinflussbar, teilweise beeinflussbar oder nicht beeinflussbar. Priorisieren Sie danach genau 1 Thema."
    },
    "Ideen entwickeln": {
        "podcast_title": "Podcast zu Innovation und Ideenentwicklung",
        "podcast_url": "https://www.srf.ch/audio",
        "video_title": "Videoimpuls: Von der Idee zum ersten Test",
        "video_url": "https://www.youtube.com",
        "article_title": "Mobiliar Forum",
        "article_url": MOBILIAR_FORUM_URL,
        "exercise_title": "Praxisimpuls: 3 Ideen in 20 Minuten",
        "exercise_text": "Formulieren Sie 3 konkrete Ideen, die innerhalb von 30 Tagen testbar wären. Bewerten Sie jede Idee nach Nutzen, Umsetzbarkeit und Wirkung."
    },
    "Veränderung begleiten": {
        "podcast_title": "Podcast zu Führung, Team und Veränderung",
        "podcast_url": "https://www.srf.ch/audio",
        "video_title": "Videoimpuls: Teams unter Druck führen",
        "video_url": "https://www.youtube.com",
        "article_title": "Mobiliar Forum",
        "article_url": MOBILIAR_FORUM_URL,
        "exercise_title": "Praxisimpuls: Stoppen, Starten, Stärken",
        "exercise_text": "Notieren Sie im Team 3 Dinge: Was stoppen wir sofort, was starten wir bewusst, was stärken wir gezielt. Wählen Sie danach genau 1 Massnahme pro Bereich."
    }
}

QUESTIONS = {
    "Markt": "Wie stark spüren Sie Druck durch Konkurrenz oder neue Technologien?",
    "Personal": "Wie kritisch ist die Situation bei Fachkräften und im Team?",
    "Prozesse": "Wie sehr bremsen veraltete Abläufe oder IT Probleme den Alltag?",
    "Finanzen": "Wie stark belasten steigende Kosten Ihr Geschäft?",
    "Strategie": "Wie klar ist Ihre langfristige Ausrichtung über das Tagesgeschäft hinaus?"
}

# ---------------- STYLING ----------------
st.markdown("""
<style>
    .main {
        background-color: #f7f7f7;
    }

    .hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f6 100%);
        padding: 28px;
        border-radius: 18px;
        border-left: 10px solid #d6001c;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    }

    .kmu-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border-left: 8px solid #d6001c;
        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
        margin-bottom: 22px;
    }

    .soft-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .metric-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 14px;
    }

    .priority-high {
        color: #d6001c;
        font-weight: 700;
    }

    .priority-medium {
        color: #9b4d00;
        font-weight: 700;
    }

    .priority-low {
        color: #1f6f43;
        font-weight: 700;
    }

    .stButton > button {
        background-color: #d6001c;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 700;
        border: none;
    }

    .stDownloadButton > button {
        background-color: #d6001c;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 700;
        border: none;
    }

    h1, h2, h3 {
        color: #d6001c;
    }

    .small-note {
        color: #666666;
        font-size: 0.92rem;
    }

</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def classify_score(score):
    if score >= 4:
        return "hoch"
    elif score == 3:
        return "mittel"
    return "niedrig"

def build_priority_label(score):
    level = classify_score(score)
    if level == "hoch":
        return f"<span class='priority-high'>{score}/5 · hoher Druck</span>"
    elif level == "mittel":
        return f"<span class='priority-medium'>{score}/5 · mittlerer Druck</span>"
    return f"<span class='priority-low'>{score}/5 · tiefer Druck</span>"

def analyze_text(text):
    text = (text or "").lower()

    flags = {
        "zeitdruck": any(w in text for w in ["zeit", "keine zeit", "alltag", "überlastet", "stress", "druck", "kaum"]),
        "strategie": any(w in text for w in ["unklar", "wohin", "ziel", "strategie", "ausrichtung", "nachfolge", "zukunft"]),
        "ideen": any(w in text for w in ["ideen", "innovation", "entwickeln", "neue angebote", "wachstum", "chancen"]),
        "team": any(w in text for w in ["team", "fachkräfte", "mitarbeitende", "fluktuation", "führung"]),
        "prozesse": any(w in text for w in ["prozess", "ablauf", "it", "digitalisierung", "system", "schnittstelle"])
    }
    return flags

def get_top_fields(data, n=2):
    return sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]

def determine_pattern(data, flags):
    markt = data["Markt"]
    personal = data["Personal"]
    prozesse = data["Prozesse"]
    finanzen = data["Finanzen"]
    strategie = data["Strategie"]

    if strategie >= 4 and markt >= 4:
        return {
            "pattern_title": "Zukunftsdruck ohne gemeinsame Orientierung",
            "pattern_text": "Der Aussenruck ist spürbar. Gleichzeitig fehlt eine ausreichend klare gemeinsame Richtung. Das Risiko ist nicht Stillstand. Das Risiko ist Aktivität ohne Fokus.",
            "format": "Orientierung schaffen",
            "reason": "Wenn Marktdruck und strategische Unklarheit zusammenkommen, braucht es zuerst Klarheit. Nicht noch mehr Aktionismus."
        }

    if personal >= 4 and prozesse >= 4:
        return {
            "pattern_title": "Operativer Druck frisst Entwicklung",
            "pattern_text": "Das Team läuft. Aber es läuft zu stark im Alltag. Prozesse, Rollen oder Abläufe bremsen. Entwicklung wird auf später verschoben.",
            "format": "Veränderung begleiten",
            "reason": "Wenn Menschen und Alltag gleichzeitig unter Druck stehen, braucht es ein Format, das Veränderung greifbar und machbar macht."
        }

    if markt >= 4 and strategie <= 3:
        return {
            "pattern_title": "Chancen sind da. Sie werden aber nicht systematisch genutzt",
            "pattern_text": "Der Markt bewegt sich. Es gibt Potenzial. Doch Ideen werden noch zu wenig geschärft, priorisiert oder getestet.",
            "format": "Ideen entwickeln",
            "reason": "Wenn der Markt in Bewegung ist, aber der nächste Schritt noch fehlt, hilft ein strukturierter Innovations und Ideenprozess."
        }

    if finanzen >= 4 and prozesse >= 3:
        return {
            "pattern_title": "Kosten und Effizienz drücken gleichzeitig",
            "pattern_text": "Die Belastung kommt nicht nur von aussen. Sie zeigt sich auch im System. Jeder unnötige Aufwand kostet doppelt.",
            "format": "Veränderung begleiten",
            "reason": "Wenn Kosten und Effizienzfragen dominieren, braucht es Fokus auf Zusammenarbeit, Prioritäten und konkrete Veränderung."
        }

    if flags["strategie"] and strategie >= 3:
        return {
            "pattern_title": "Die Richtung ist noch nicht scharf genug",
            "pattern_text": "Es fehlt weniger an Engagement als an gemeinsamer Schärfe. Ohne klares Bild zieht jeder mit bestem Willen in eine leicht andere Richtung.",
            "format": "Orientierung schaffen",
            "reason": "Strategische Unschärfe lässt sich selten im Alltag lösen. Dafür braucht es bewusst Raum."
        }

    if flags["ideen"] and markt >= 3:
        return {
            "pattern_title": "Es gibt Suchbewegung, aber noch keinen klaren Entwicklungsfokus",
            "pattern_text": "Das Unternehmen spürt, dass etwas möglich ist. Jetzt braucht es Struktur, damit aus Ideen konkrete nächste Schritte werden.",
            "format": "Ideen entwickeln",
            "reason": "Ideen brauchen nicht zuerst Perfektion. Sie brauchen einen guten Rahmen."
        }

    return {
        "pattern_title": "Mehrere Spannungsfelder gleichzeitig",
        "pattern_text": "Es gibt nicht das eine Problem. Mehrere Themen wirken zusammen. Genau deshalb lohnt sich eine strukturierte Standortbestimmung mit Priorisierung.",
        "format": "Orientierung schaffen",
        "reason": "Wenn mehrere Spannungsfelder parallel wirken, braucht es zuerst Ordnung und Fokus."
    }

def build_management_summary(data, text_flags, pattern_info):
    top_fields = get_top_fields(data, 2)
    top_1 = top_fields[0][0]
    top_2 = top_fields[1][0]

    summary = f"Der grösste Druck liegt aktuell bei {top_1} und {top_2}. "
    summary += pattern_info["pattern_text"] + " "

    if text_flags["zeitdruck"]:
        summary += "Im Freitext zeigt sich zusätzlich ein klarer Hinweis auf Zeit und Ressourcenengpässe. "

    if text_flags["team"]:
        summary += "Das spricht dafür, dass nicht nur das Thema, sondern auch die gemeinsame Arbeitsweise betrachtet werden sollte. "

    summary += f"Der sinnvollste nächste Schritt ist deshalb: {pattern_info['format']}."
    return summary

def get_action_plan(format_name):
    if format_name == "Orientierung schaffen":
        return {
            "14_tage": [
                "Die 3 grössten Unsicherheiten im Führungsteam offen benennen",
                "Jedes Thema in dringend, wichtig oder ablenkend einordnen",
                "Genau 1 Zukunftsthema priorisieren, das jetzt gemeinsame Aufmerksamkeit braucht"
            ],
            "30_tage": [
                "Mit 2 bis 4 Personen einen Tag bewusst aus dem Alltag gehen",
                "Im Mobiliar Forum Spannungsfelder strukturieren und ein gemeinsames Bild schaffen",
                "Konkrete nächste Schritte und Verantwortlichkeiten festlegen"
            ],
            "workshop_outcome": "Mehr Klarheit, eine gemeinsame Richtung und ein priorisierter nächster Schritt"
        }

    if format_name == "Ideen entwickeln":
        return {
            "14_tage": [
                "Bestehende Ideen, Chancen und Kundenbeobachtungen sammeln",
                "Die 2 bis 3 spannendsten Ansätze nach Wirkung und Umsetzbarkeit bewerten",
                "Für 1 Idee eine erste Testfrage formulieren"
            ],
            "30_tage": [
                "Mit dem Team einen strukturierten Entwicklungstag nutzen",
                "Ideen schärfen, priorisieren und auf echte Umsetzbarkeit prüfen",
                "Einen ersten Test oder Prototyp definieren"
            ],
            "workshop_outcome": "Weniger Bauchgefühl, mehr Fokus und ein konkreter Entwicklungsschritt"
        }

    return {
        "14_tage": [
            "Die grössten Blockaden im Alltag sichtbar machen",
            "Klar benennen, was stoppt, was trägt und was entlastet",
            "1 bis 2 Bereiche auswählen, in denen sofort Verbesserung möglich ist"
        ],
        "30_tage": [
            "Mit dem Team Veränderung bewusst besprechbar machen",
            "Zusammenarbeit, Rollen und Prioritäten schärfen",
            "Einen realistischen Veränderungsschritt verbindlich starten"
        ],
        "workshop_outcome": "Mehr Handlungsfähigkeit im Team und weniger Reibungsverlust im Alltag"
    }

def build_resource_bundle(format_name):
    return RESOURCE_LIBRARY[format_name]

def build_follow_up_text(format_name):
    if format_name == "Orientierung schaffen":
        return "Geeignet für Teams, die spüren, dass sie zuerst Klarheit brauchen, bevor sie an Lösungen arbeiten."
    if format_name == "Ideen entwickeln":
        return "Geeignet für Teams, die Potenziale sehen und aus ersten Ideen konkrete Ansätze machen wollen."
    return "Geeignet für Teams, die Veränderung nicht nur verstehen, sondern im Alltag besser tragen wollen."

def radar_chart(data):
    categories = list(data.keys())
    values = list(data.values())
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name='Standortbestimmung',
        line=dict(color='#d6001c', width=3),
        fillcolor='rgba(214,0,28,0.18)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5]
            )
        ),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height=460
    )
    return fig

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Scan"

if "data" not in st.session_state:
    st.session_state.data = None

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "open_text" not in st.session_state:
    st.session_state.open_text = ""

# ---------------- PAGE 1 ----------------
if st.session_state.page == "Scan":
    st.markdown("""
    <div class="hero-card">
        <h1>Mobiliar Forum Navigator</h1>
        <p style="font-size:1.08rem;">
            Ein digitaler Einstieg für KMU, die ihre Zukunft nicht einfach dem Alltag überlassen wollen.
        </p>
        <p class="small-note">
            Standortbestimmung. Einordnung. Passender nächster Schritt.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("forum_scan"):
        col1, col2 = st.columns(2)

        with col1:
            company = st.text_input("Unternehmen oder Organisation")
            sector = st.selectbox(
                "Branche",
                ["Bau und Handwerk", "Detailhandel", "Dienstleistung", "Industrie", "Gesundheit", "NGO", "Andere"]
            )

        with col2:
            size = st.selectbox(
                "Unternehmensgrösse",
                ["1 bis 10 Mitarbeitende", "11 bis 50 Mitarbeitende", "51 bis 250 Mitarbeitende", "250+"]
            )
            role = st.text_input("Ihre Funktion")

        st.markdown("### Quantitative Einschätzung")
        st.caption("1 = gering, 5 = hoch")

        results = {}
        left, right = st.columns(2)
        for i, (key, question) in enumerate(QUESTIONS.items()):
            with left if i % 2 == 0 else right:
                results[key] = st.select_slider(question, options=[1, 2, 3, 4, 5], value=3)

        st.markdown("### Qualitative Einordnung")
        open_text = st.text_area(
            "Was hindert Sie aktuell am meisten daran, Ihr Unternehmen weiterzuentwickeln?",
            height=140,
            placeholder="Zum Beispiel: Wir verlieren zu viel Zeit im Alltag. Es gibt gute Ideen, aber keine Priorisierung. Oder: Wir spüren Druck im Markt, aber die Richtung ist noch nicht klar."
        )

        submitted = st.form_submit_button("Standortbestimmung erstellen")

        if submitted:
            st.session_state.data = results
            st.session_state.profile = {
                "company": company.strip() if company else "Ihre Organisation",
                "sector": sector,
                "size": size,
                "role": role.strip() if role else "Geschäftsleitung"
            }
            st.session_state.open_text = open_text
            st.session_state.page = "Dashboard"
            st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.page == "Dashboard":
    data = st.session_state.data
    profile = st.session_state.profile
    open_text = st.session_state.open_text

    text_flags = analyze_text(open_text)
    pattern_info = determine_pattern(data, text_flags)
    summary = build_management_summary(data, text_flags, pattern_info)
    action_plan = get_action_plan(pattern_info["format"])
    resources = build_resource_bundle(pattern_info["format"])
    follow_up_text = build_follow_up_text(pattern_info["format"])
    top_fields = get_top_fields(data, 5)

    st.markdown(f"""
    <div class="hero-card">
        <h1>Standortbestimmung für {profile['company']}</h1>
        <p style="font-size:1.05rem;">
            Einordnung für {profile['role']} · {profile['sector']} · {profile['size']}
        </p>
        <p class="small-note">
            Das Ziel ist nicht mehr Analyse um der Analyse willen. Das Ziel ist ein nächster Schritt, der trägt.
        </p>
    </div>
    """, unsafe_allow_html=True)

    top_col1, top_col2, top_col3 = st.columns([1.15, 1, 1])

    with top_col1:
        st.plotly_chart(radar_chart(data), use_container_width=True)

    with top_col2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem; color:#666;">Dominantes Muster</div>
            <div style="font-size:1.15rem; font-weight:700; margin-top:6px;">{pattern_info['pattern_title']}</div>
        </div>
        """, unsafe_allow_html=True)

        strongest = get_top_fields(data, 1)[0]
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem; color:#666;">Grösster Druck</div>
            <div style="font-size:1.15rem; font-weight:700; margin-top:6px;">{strongest[0]}</div>
            <div style="margin-top:6px;">{build_priority_label(strongest[1])}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:0.95rem; color:#666;">Empfohlenes Format</div>
            <div style="font-size:1.15rem; font-weight:700; margin-top:6px;">{pattern_info['format']}</div>
        </div>
        """, unsafe_allow_html=True)

    with top_col3:
        st.markdown("""
        <div class="soft-card">
            <h3 style="margin-top:0;">Belastungsbild</h3>
        """, unsafe_allow_html=True)

        for field, score in top_fields:
            st.markdown(f"<p><strong>{field}</strong><br>{build_priority_label(score)}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Management Summary")
    st.markdown(f"""
    <div class="kmu-card">
        <p><strong>Einordnung:</strong> {summary}</p>
        <p><strong>Warum dieses Format:</strong> {pattern_info['reason']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("## Was jetzt sinnvoll ist")
        st.markdown(f"""
        <div class="kmu-card">
            <h3 style="margin-top:0;">{pattern_info['format']}</h3>
            <p>{follow_up_text}</p>
            <p><strong>Was ein Team danach konkret hat:</strong> {action_plan['workshop_outcome']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("## Mobiliar Forum als nächster Schritt")
        st.markdown(f"""
        <div class="kmu-card">
            <p><strong>Hauptpfad:</strong> Mobiliar Forum</p>
            <p>Wenn Sie aus der Analyse in einen echten Teamprozess gehen wollen, ist das der passende nächste Schritt.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Zum Mobiliar Forum", MOBILIAR_FORUM_URL, use_container_width=True)

    st.markdown("## Konkreter Aktionsplan")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="soft-card">
            <h3 style="margin-top:0;">In den nächsten 14 Tagen</h3>
        """, unsafe_allow_html=True)
        for item in action_plan["14_tage"]:
            st.write(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="soft-card">
            <h3 style="margin-top:0;">In den nächsten 30 Tagen</h3>
        """, unsafe_allow_html=True)
        for item in action_plan["30_tage"]:
            st.write(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Impulse und niederschwellige Einstiege")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.markdown("""
        <div class="soft-card">
            <h3 style="margin-top:0;">Mobiliar Forum</h3>
            <p>Der direkte Weg vom Erkennen ins gemeinsame Arbeiten.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Website öffnen", MOBILIAR_FORUM_URL, use_container_width=True)

    with r2:
        st.markdown("""
        <div class="soft-card">
            <h3 style="margin-top:0;">KMU Kaffee</h3>
            <p>Ein niederschwelliger Einstieg mit Impulsen, Austausch und ersten Denkanstössen.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Beispiel ansehen", KMU_KAFFEE_EXAMPLE_URL, use_container_width=True)

    with r3:
        st.markdown(f"""
        <div class="soft-card">
            <h3 style="margin-top:0;">Podcast</h3>
            <p><strong>{resources['podcast_title']}</strong></p>
            <p>Ein ergänzender Impuls für den Kopf. Kein Ersatz für Teamarbeit, aber ein guter Denkstarter.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Podcast öffnen", resources["podcast_url"], use_container_width=True)

    with r4:
        st.markdown(f"""
        <div class="soft-card">
            <h3 style="margin-top:0;">Video</h3>
            <p><strong>{resources['video_title']}</strong></p>
            <p>Kurzer Impuls zum Vertiefen oder als Einstieg für ein Gespräch im Team.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Video öffnen", resources["video_url"], use_container_width=True)

    st.markdown("## Praxisimpuls für sofort")
    st.markdown(f"""
    <div class="kmu-card">
        <h3 style="margin-top:0;">{resources['exercise_title']}</h3>
        <p>{resources['exercise_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Freitext aus der Analyse nochmals ansehen"):
        if open_text.strip():
            st.write(open_text)
        else:
            st.write("Kein Freitext erfasst.")

    st.markdown("## Weiterdenken")
    st.markdown(f"""
    <div class="kmu-card">
        <p><strong>Wichtig:</strong> Diese Standortbestimmung ersetzt keinen Workshop. Sie schafft Orientierung, zeigt ein Muster und hilft, den passenden Einstieg zu wählen.</p>
        <p><strong>Niederschwelliger Einstieg:</strong> Wer noch nicht direkt mit dem Team in ein Tagesformat einsteigen will, kann über einen KMU Kaffee erste Impulse mitnehmen.</p>
        <p><strong>Nächster echter Schritt:</strong> {pattern_info['format']} im Mobiliar Forum.</p>
    </div>
    """, unsafe_allow_html=True)

    bottom1, bottom2 = st.columns(2)

    with bottom1:
        if st.button("Neue Analyse starten"):
            st.session_state.page = "Scan"
            st.session_state.data = None
            st.session_state.profile = {}
            st.session_state.open_text = ""
            st.rerun()

    with bottom2:
        st.link_button("Direkt zum Mobiliar Forum", MOBILIAR_FORUM_URL, use_container_width=True)
