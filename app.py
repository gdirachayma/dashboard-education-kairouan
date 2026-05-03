import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import folium
from streamlit_folium import st_folium
import json

# =============================================
# 1. PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title="KPI Éducation – Kairouan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# 2. GLOBAL CSS – Design moderne & lisible
# =============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f2744 100%);
    min-height: 100vh;
}

[data-testid="block-container"] {
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1a2744 100%) !important;
    border-right: 1px solid rgba(56, 189, 248, 0.15);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 8px !important;
}

/* ── Titres ── */
h1 {
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    color: #f8fafc !important;
    font-size: 1.8rem !important;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #e2e8f0 !important;
}

h4 {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 600 !important;
}

/* ── Cartes KPI ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,0.9) 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 8px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
}

.kpi-card:hover {
    border-color: rgba(56, 189, 248, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(56, 189, 248, 0.1);
}

.kpi-label {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 4px;
}

.kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #38bdf8;
    line-height: 1.1;
}

.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 6px;
    display: block;
}

/* ── Cartes délégation ── */
.deleg-card {
    background: linear-gradient(135deg, rgba(51,65,85,0.8) 0%, rgba(30,41,59,0.8) 100%);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 14px;
    padding: 16px 20px;
    margin: 8px 0;
    position: relative;
    overflow: hidden;
}

.deleg-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #818cf8, #f472b6);
}

.deleg-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #a5b4fc;
}

/* ── Section header ── */
.section-header {
    background: linear-gradient(135deg, rgba(56,189,248,0.1) 0%, rgba(129,140,248,0.05) 100%);
    border: 1px solid rgba(56,189,248,0.15);
    border-left: 4px solid #38bdf8;
    border-radius: 0 12px 12px 0;
    padding: 12px 20px;
    margin: 24px 0 16px 0;
}

.section-header h3 {
    margin: 0 !important;
    font-size: 1rem !important;
    color: #38bdf8 !important;
    font-weight: 600 !important;
}

/* ── Badge cycle ── */
.cycle-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0369a1, #0ea5e9);
    color: white !important;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
}

/* ── Page header banner ── */
.page-banner {
    background: linear-gradient(135deg, rgba(3,105,161,0.3) 0%, rgba(79,70,229,0.2) 100%);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}

/* ── Metrics row ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

/* ── Subheader custom ── */
.custom-subheader {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 20px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(56,189,248,0.1) !important;
    border-radius: 12px !important;
}

/* ── Login form ── */
.login-container {
    max-width: 500px;
    margin: 0 auto;
    background: linear-gradient(135deg, rgba(30,41,59,0.95) 0%, rgba(15,23,42,0.95) 100%);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 24px;
    padding: 40px;
    backdrop-filter: blur(20px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.5);
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0369a1, #0ea5e9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(14,165,233,0.35) !important;
}

/* ── Radio buttons ── */
.stRadio > div {
    gap: 8px !important;
}

.stRadio [data-testid="stMarkdownContainer"] p {
    color: #94a3b8 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Divider ── */
hr {
    border-color: rgba(56,189,248,0.1) !important;
    margin: 16px 0 !important;
}

/* ── Selectbox ── */
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Warning/success ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ── Main content text ── */
p, li, span {
    color: #cbd5e1;
}

/* Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: rgba(56,189,248,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# =============================================
# 3. AUTHENTIFICATION
# =============================================
USER_CREDENTIALS = {
    "admin": "pass12345",
    "kairouan": "education2025",
    "chaymaguedira": "290190Ch@yma"
}


def login():
    # Header centré
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px 0;">
        <div style="font-size: 3rem; margin-bottom: 8px;">🎓</div>
        <h1 style="font-size: 2rem !important; background: linear-gradient(135deg, #38bdf8, #818cf8);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;">
            Dashboard KPI Éducation
        </h1>
        <p style="color: #64748b; font-size: 0.95rem; letter-spacing: 0.05em;">
            Délégation Régionale de l'Éducation – Kairouan
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase;
                  letter-spacing: 0.15em; margin-bottom: 20px; text-align:center;">
            Accès sécurisé
        </p>
        """, unsafe_allow_html=True)

        with st.form(key="login_form"):
            username = st.text_input("👤  Nom d'utilisateur", placeholder="Entrez votre identifiant")
            password = st.text_input("🔑  Mot de passe", type="password", placeholder="••••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Se connecter →", use_container_width=True)

            if submitted:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.success("✅ Bienvenue ! Connexion réussie.")
                    st.rerun()
                else:
                    st.error("❌ Identifiant ou mot de passe incorrect.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Image décorative centrée
    st.markdown("""
    <div style="text-align:center; margin-top: 30px; opacity: 0.4;">
        <img src="https://i.pinimg.com/originals/d7/64/c7/d764c70776b64e523cb4eea2f322db96.gif"
             style="max-width: 600px; width: 80%; border-radius: 12px;">
    </div>
    """, unsafe_allow_html=True)


# =============================================
# 4. GESTION SESSION
# =============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "selected_button" not in st.session_state:
    st.session_state.selected_button = False


# =============================================
# 5. CHARGEMENT DES DONNÉES
# =============================================
@st.cache_data
def load_data():
    return pd.read_csv('streambase .csv', sep=';', encoding='MacRoman')


# =============================================
# 6. HELPERS VISUELS
# =============================================
def kpi_card(icon, label, value, color="#38bdf8"):
    return f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
    </div>
    """


def deleg_card(icon, label, value):
    return f"""
    <div class="deleg-card">
        <div class="kpi-label">{icon} {label}</div>
        <div class="deleg-value">{value}</div>
    </div>
    """


def section_header(icon, title):
    st.markdown(f"""
    <div class="section-header">
        <h3>{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)


def page_banner(icon, title, subtitle, badge_color="#0369a1"):
    st.markdown(f"""
    <div class="page-banner">
        <div style="font-size:2.5rem;">{icon}</div>
        <div>
            <h1 style="margin:0; font-size:1.6rem !important;">{title}</h1>
            <p style="margin:0; color:#64748b; font-size:0.85rem;">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# 7. HEATMAP
# =============================================
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect(
        cornerRadius=3
    ).encode(
        y=alt.Y(f'{input_y}:O',
                axis=alt.Axis(title="Année", titleFontSize=12, titlePadding=10,
                              titleFontWeight=600, labelAngle=0,
                              labelColor='#94a3b8', titleColor='#94a3b8',
                              gridColor='rgba(255,255,255,0.05)')),
        x=alt.X(f'{input_x}:O',
                axis=alt.Axis(title="Délégation", titleFontSize=12, titlePadding=10,
                              titleFontWeight=600, labelAngle=-35,
                              labelColor='#94a3b8', titleColor='#94a3b8')),
        color=alt.Color(f'max({input_color}):Q',
                        legend=alt.Legend(
                            titleColor='#94a3b8',
                            labelColor='#94a3b8',
                            titleFontSize=11
                        ),
                        scale=alt.Scale(scheme=input_color_theme)),
        tooltip=[
            alt.Tooltip(f'{input_y}:O', title='Année'),
            alt.Tooltip(f'{input_x}:O', title='Délégation'),
            alt.Tooltip(f'max({input_color}):Q', title='Élèves', format=',')
        ],
        stroke=alt.value('rgba(255,255,255,0.05)'),
        strokeWidth=alt.value(0.5),
    ).properties(
        width='container',
        height=220
    ).configure_view(
        strokeWidth=0,
        fill='transparent'
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=12
    )
    return heatmap


# =============================================
# 8. CARTE FOLIUM CONFIG
# =============================================
def create_base_map():
    m = folium.Map(
        location=[35.40, 10.06],
        zoom_start=8,
        scrollWheelZoom=False,
        tiles='CartoDB dark_matter'
    )
    return m


# =============================================
# 9. PAGE CYCLE PRIMAIRE
# =============================================
def show_dashboardprim():
    selected_year = st.session_state.selected_year
    selected_deleg = st.session_state.selected_deleg
    selected_color = st.session_state.selected_color_theme

    color_theme_map = {"Bleu": ("Blues", "blues"), "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")}
    folium_palette, altair_palette = color_theme_map[selected_color]
    palette = getattr(px.colors.sequential, folium_palette)
    indices = np.linspace(1, len(palette) - 1, 6, dtype=int)
    custom_palette = [palette[i] for i in indices]

    page_banner("📚", "Cycle Primaire", f"Indicateurs clés · Année {selected_year}")
    st.markdown('<span class="cycle-badge">🏫 ENSEIGNEMENT PRIMAIRE</span>', unsafe_allow_html=True)

    df_p = df[df['niveau'] == "Cycle Primaire"]
    df_prim = df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year)]
    df_selected_primaire = df_prim.copy()
    df_prim_del = df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]

    # Nettoyage densité
    df_selected_primaire['densite'] = df_selected_primaire['densite'].astype(str).str.replace(',', '.').astype(float)
    if 'per nouv 1 ayant ben AP' in df_selected_primaire.columns:
        df_selected_primaire['per nouv 1 ayant ben AP'] = (
            df_selected_primaire['per nouv 1 ayant ben AP']
            .astype(str).str.replace(',', '.').astype(float)
        )
    if len(df_prim_del) > 0:
        df_prim_del = df_prim_del.copy()
        df_prim_del['densite'] = df_prim_del['densite'].astype(str).str.replace(',', '.').astype(float)

    # ── Layout principal ──
    col_main, col_kpi = st.columns([4, 1.8], gap='large')

    with col_kpi:
        # ── KPIs Régionaux ──
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(3,105,161,0.2) 0%, rgba(14,165,233,0.1) 100%);
                    border: 1px solid rgba(56,189,248,0.25); border-radius: 16px;
                    padding: 20px; margin-bottom: 16px;">
            <p style="color:#38bdf8; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:14px;">
                🌍 INDICATEURS RÉGIONAUX
            </p>
        """, unsafe_allow_html=True)

        kpis_reg = [
            ("🏛️", "Établissements", int(df_selected_primaire['nbetabli'].sum()), "#38bdf8"),
            ("👥", "Élèves", f"{int(df_selected_primaire['student'].sum()):,}", "#34d399"),
            ("🏫", "Classes", f"{int(df_selected_primaire['class'].sum()):,}", "#a78bfa"),
            ("👩‍🏫", "Enseignants", f"{int(df_selected_primaire['enseignant'].sum()):,}", "#fb923c"),
            ("📊", "Densité moy.", round(df_selected_primaire['densite'].mean(), 1), "#f472b6"),
            ("🧒", "Écoles avec CP", int(df_selected_primaire['prep'].sum()), "#fbbf24"),
        ]
        for icon, label, val, color in kpis_reg:
            st.markdown(kpi_card(icon, label, val, color), unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── KPIs Délégation ──
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(79,70,229,0.15) 0%, rgba(129,140,248,0.08) 100%);
                    border: 1px solid rgba(129,140,248,0.25); border-radius: 16px;
                    padding: 20px; margin-bottom: 16px;">
            <p style="color:#818cf8; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:4px;">
                📍 DÉLÉGATION
            </p>
            <p style="color:#e2e8f0; font-size:1.1rem; font-weight:700; margin-bottom: 14px;">
                {selected_deleg}
            </p>
        """, unsafe_allow_html=True)

        if len(df_prim_del) > 0:
            kpis_del = [
                ("🏛️", "Établissements", int(df_prim_del['nbetabli'].sum())),
                ("👥", "Élèves", f"{int(df_prim_del['student'].sum()):,}"),
                ("🏫", "Classes", f"{int(df_prim_del['class'].sum()):,}"),
                ("👩‍🏫", "Enseignants", f"{int(df_prim_del['enseignant'].sum()):,}"),
                ("📊", "Densité", round(df_prim_del['densite'].mean(), 1)),
                ("🧒", "Écoles CP", int(df_prim_del['prep'].sum())),
            ]
            for icon, label, val in kpis_del:
                st.markdown(deleg_card(icon, label, val), unsafe_allow_html=True)
        else:
            st.info("Pas de données pour cette délégation.")

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Graphique taux AP ──
        if 'per nouv 1 ayant ben AP' in df_selected_primaire.columns:
            section_header("📈", "Taux bénéficiaires AP")
            df_sorted1 = df_selected_primaire.sort_values(by='per nouv 1 ayant ben AP', ascending=True)
            taux = df_sorted1['per nouv 1 ayant ben AP']
            moyenne = round(taux.mean(), 1)

            fig_ap = go.Figure()
            fig_ap.add_trace(go.Bar(
                y=df_sorted1['deleg'],
                x=taux,
                orientation='h',
                marker=dict(
                    color=['#38bdf8' if val > moyenne else '#334155' for val in taux],
                    line=dict(color='rgba(255,255,255,0.05)', width=0.5)
                ),
                text=[f"{val:.1f}%" for val in taux],
                textposition='outside',
                textfont=dict(color='#94a3b8', size=10)
            ))
            fig_ap.add_vline(
                x=moyenne, line_dash="dot", line_color="#f472b6", line_width=1.5,
                annotation_text=f"Moy: {moyenne}%",
                annotation_position="top",
                annotation_font=dict(size=10, color="#f472b6")
            )
            fig_ap.update_layout(
                title=dict(text="Nouveaux inscrits 1ère année<br>ayant bénéficié de l'AP",
                           font=dict(color='#e2e8f0', size=11)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)',
                           title=dict(text="%", font=dict(color='#64748b', size=10))),
                yaxis=dict(color='#94a3b8', gridcolor='rgba(255,255,255,0.03)'),
                margin=dict(l=0, r=20, t=50, b=10),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig_ap, use_container_width=True)

    with col_main:
        # ── Heatmap ──
        section_header("🗓️", "Évolution des effectifs par délégation et par année")
        heatmap = make_heatmap(df_p, 'year', 'deleg', 'student', altair_palette)
        st.altair_chart(heatmap, use_container_width=True)

        # ── Carte choroplèthe ──
        section_header("🗺️", f"Répartition géographique des élèves – {selected_year}")
        map_obj = create_base_map()
        choropleth = folium.Choropleth(
            geo_data='kai-deleg.json',
            data=df_prim,
            columns=('ref_tn_cod', 'student'),
            key_on='feature.properties.id',
            legend_name=f"Nombre d'élèves ({selected_year})",
            fill_color=folium_palette,
            highlight=True,
            fill_opacity=0.75,
            line_opacity=0.3
        )
        choropleth.geojson.add_to(map_obj)
        student_dict = dict(zip(df_selected_primaire['ref_tn_cod'], df_selected_primaire['student']))
        for feature in choropleth.geojson.data['features']:
            feature['properties']['student'] = student_dict.get(feature["properties"]["id"], 0)
        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr', 'student'], labels=False))
        for feature in choropleth.geojson.data["features"]:
            if feature["properties"]["del_fr"] == selected_deleg:
                folium.GeoJson(
                    data=feature,
                    style_function=lambda x: {'fillColor': '#f43f5e', 'color': '#f43f5e',
                                              'weight': 3, 'fillOpacity': 0.8},
                    tooltip=folium.GeoJsonTooltip(fields=["del_fr", "student"])
                ).add_to(map_obj)
        st_folium(map_obj, width='100%', height=400)

        # ── Row de graphiques ──
        col_g1, col_g2 = st.columns(2, gap='medium')

        with col_g1:
            section_header("📊", f"Densité des classes – {selected_year}")
            df_sorted = df_selected_primaire.sort_values(by='densite', ascending=False)
            fig1 = px.bar(
                df_sorted, x='deleg', y='densite', color='densite',
                color_continuous_scale=[[0, '#1e3a5f'], [0.5, '#0ea5e9'], [1, '#38bdf8']],
                text='densite',
                title=f"Élèves par classe – {selected_year}"
            )
            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.4)',
                xaxis=dict(color='#64748b', tickangle=-30, gridcolor='rgba(255,255,255,0.03)'),
                yaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)'),
                font=dict(color='#94a3b8'),
                title=dict(font=dict(color='#e2e8f0', size=12)),
                coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=40, b=0), height=280
            )
            fig1.update_traces(texttemplate='%{text:.1f}', marker_line_width=0)
            st.plotly_chart(fig1, use_container_width=True)

        with col_g2:
            section_header("🎂", f"Écoles avec CP – {selected_year}")
            fig_pie = px.pie(
                df_selected_primaire, names='deleg', values='prep',
                color_discrete_sequence=['#0ea5e9', '#38bdf8', '#7dd3fc', '#0369a1',
                                         '#075985', '#0c4a6e', '#164e63', '#083344'],
                hole=0.55,
                title=f"Groupes préparatoires – {selected_year}"
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                title=dict(font=dict(color='#e2e8f0', size=12)),
                legend=dict(font=dict(color='#94a3b8', size=10)),
                margin=dict(l=0, r=0, t=40, b=0), height=280
            )
            fig_pie.update_traces(textinfo='percent', textfont=dict(color='white', size=10))
            st.plotly_chart(fig_pie, use_container_width=True)

        # ── Courbe répartition par niveau ──
        section_header("📚", "Répartition des élèves par niveau scolaire (1ère → 6ème année)")
        df_long = df_prim.melt(
            id_vars=["deleg"],
            value_vars=["1ann", "2ann", "3ann", "4ann", "5ann", "6ann"],
            var_name="Niveau", value_name="Élèves"
        )
        fig2 = px.line(
            df_long, x="deleg", y="Élèves", color="Niveau",
            color_discrete_sequence=['#0ea5e9', '#38bdf8', '#34d399', '#a78bfa', '#f472b6', '#fbbf24'],
            markers=True,
            title=f"Élèves par niveau – {selected_year}"
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.4)',
            xaxis=dict(color='#64748b', tickangle=-30, gridcolor='rgba(255,255,255,0.03)'),
            yaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)'),
            font=dict(color='#94a3b8'),
            title=dict(font=dict(color='#e2e8f0', size=12)),
            legend=dict(font=dict(color='#94a3b8', size=10),
                        bgcolor='rgba(15,23,42,0.6)', bordercolor='rgba(56,189,248,0.1)'),
            margin=dict(l=0, r=0, t=40, b=0), height=300
        )
        fig2.update_traces(marker=dict(size=6, line=dict(width=1, color='rgba(255,255,255,0.3)')))
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("ℹ️ À propos des données", expanded=False):
        st.markdown("""
        <p style="color:#64748b; font-size:0.85rem;">
            Source : <a href="http://www.edunet.tn/index.php?id=523&lan=1" target="_blank"
            style="color:#38bdf8;">Bureau de planification et de statistiques – Kairouan</a>
        </p>
        """, unsafe_allow_html=True)


# =============================================
# 10. PAGE SECONDAIRE
# =============================================
def show_data_analysis_Secondaire():
    selected_year = st.session_state.selected_year
    selected_deleg = st.session_state.selected_deleg
    selected_color = st.session_state.selected_color_theme

    color_theme_map = {"Bleu": ("Blues", "blues"), "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")}
    folium_palette, altair_palette = color_theme_map[selected_color]

    page_banner("🏛️", "Cycle Préparatoire & Enseignement Secondaire",
                f"KPI & Orientations par section · Année {selected_year}")
    st.markdown('<span class="cycle-badge">📐 SECONDAIRE & PRÉPARATOIRE GÉNÉRAL</span>', unsafe_allow_html=True)

    df_s = df[df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire"]
    df_seco = df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire") & (df["year"] == selected_year)]
    df_selected_seco = df_seco.copy()
    df_seco_del = df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire") &
                     (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]

    df_selected_seco['densite'] = df_selected_seco['densite'].astype(str).str.replace(',', '.').astype(float)

    col_main, col_kpi = st.columns([4, 1.8], gap='large')

    with col_kpi:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(3,105,161,0.2) 0%, rgba(14,165,233,0.1) 100%);
                    border: 1px solid rgba(56,189,248,0.25); border-radius: 16px;
                    padding: 20px; margin-bottom: 16px;">
            <p style="color:#38bdf8; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:14px;">
                🌍 INDICATEURS RÉGIONAUX
            </p>
        """, unsafe_allow_html=True)

        kpis_reg = [
            ("🏛️", "Établissements", int(df_selected_seco['nbetabli'].sum()), "#38bdf8"),
            ("👥", "Élèves", f"{int(df_selected_seco['student'].sum()):,}", "#34d399"),
            ("🏫", "Classes", f"{int(df_selected_seco['class'].sum()):,}", "#a78bfa"),
            ("👩‍🏫", "Enseignants", f"{int(df_selected_seco['enseignant'].sum()):,}", "#fb923c"),
            ("📊", "Densité moy.", round(df_selected_seco['densite'].mean(), 1), "#f472b6"),
        ]
        for icon, label, val, color in kpis_reg:
            st.markdown(kpi_card(icon, label, val, color), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(79,70,229,0.15) 0%, rgba(129,140,248,0.08) 100%);
                    border: 1px solid rgba(129,140,248,0.25); border-radius: 16px;
                    padding: 20px;">
            <p style="color:#818cf8; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:4px;">
                📍 DÉLÉGATION
            </p>
            <p style="color:#e2e8f0; font-size:1.1rem; font-weight:700; margin-bottom:14px;">
                {selected_deleg}
            </p>
        """, unsafe_allow_html=True)

        if len(df_seco_del) > 0:
            df_seco_del_c = df_seco_del.copy()
            df_seco_del_c['densite'] = df_seco_del_c['densite'].astype(str).str.replace(',', '.').astype(float)
            kpis_del = [
                ("🏛️", "Établissements", int(df_seco_del_c['nbetabli'].sum())),
                ("👥", "Élèves", f"{int(df_seco_del_c['student'].sum()):,}"),
                ("🏫", "Classes", f"{int(df_seco_del_c['class'].sum()):,}"),
                ("👩‍🏫", "Enseignants", f"{int(df_seco_del_c['enseignant'].sum()):,}"),
                ("📊", "Densité", round(df_seco_del_c['densite'].mean(), 1)),
            ]
            for icon, label, val in kpis_del:
                st.markdown(deleg_card(icon, label, val), unsafe_allow_html=True)
        else:
            st.info("Pas de données disponibles.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        section_header("🗓️", "Évolution des effectifs – Secondaire")
        heatmap = make_heatmap(df_s, 'year', 'deleg', 'student', altair_palette)
        st.altair_chart(heatmap, use_container_width=True)

        section_header("🗺️", f"Carte des effectifs – {selected_year}")
        map_obj = create_base_map()
        choropleth = folium.Choropleth(
            geo_data='kai-deleg.json', data=df_seco,
            columns=('ref_tn_cod', 'student'), key_on='feature.properties.id',
            legend_name=f"Nombre d'élèves ({selected_year})",
            fill_color=folium_palette, highlight=True, fill_opacity=0.75, line_opacity=0.3
        )
        choropleth.geojson.add_to(map_obj)
        student_dict = dict(zip(df_selected_seco['ref_tn_cod'], df_selected_seco['student']))
        for feature in choropleth.geojson.data['features']:
            feature['properties']['student'] = student_dict.get(feature["properties"]["id"], 0)
        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr', 'student'], labels=False))
        for feature in choropleth.geojson.data["features"]:
            if feature["properties"]["del_fr"] == selected_deleg:
                folium.GeoJson(
                    data=feature,
                    style_function=lambda x: {'fillColor': '#f43f5e', 'color': '#f43f5e',
                                              'weight': 3, 'fillOpacity': 0.8},
                    tooltip=folium.GeoJsonTooltip(fields=["del_fr", "student"])
                ).add_to(map_obj)
        st_folium(map_obj, width='100%', height=380)

        section_header("📊", f"Densité des classes – {selected_year}")
        df_sorted = df_selected_seco.sort_values(by='densite', ascending=False)
        fig1 = px.bar(
            df_sorted, x='deleg', y='densite', color='densite',
            color_continuous_scale=[[0, '#1e3a5f'], [0.5, '#7c3aed'], [1, '#a78bfa']],
            text='densite', title=f"Densité par délégation – {selected_year}"
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.4)',
            xaxis=dict(color='#64748b', tickangle=-30, gridcolor='rgba(255,255,255,0.03)'),
            yaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)'),
            font=dict(color='#94a3b8'), title=dict(font=dict(color='#e2e8f0', size=12)),
            coloraxis_showscale=False, margin=dict(l=0, r=0, t=40, b=0), height=280
        )
        fig1.update_traces(texttemplate='%{text:.1f}', marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

        # ── Orientations BAC ──
        section_header("🎯", "Orientations par section et délégation")

        df_seco_r = df_seco.rename(columns={
            "per section math": "Math", "per section science": "Science",
            "per section tech": "Technique", "per section info": "Informatique",
            "per section eco": "Économie", "per section sport": "Sport"
        })
        sections = ["Math", "Science", "Technique", "Informatique", "Économie", "Sport"]
        for col_name in sections:
            if col_name in df_seco_r.columns:
                df_seco_r[col_name] = df_seco_r[col_name].astype(str).str.replace(',', '.').astype(float)

        mode = st.radio(
            "Mode de visualisation :",
            ["📊 Diagramme empilé", "🗺️ Carte choroplèthe"],
            horizontal=True
        )

        if mode == "📊 Diagramme empilé":
            avail_sections = [s for s in sections if s in df_seco_r.columns]
            df_long = df_seco_r.melt(
                id_vars=["deleg"], value_vars=avail_sections,
                var_name="Section", value_name="Élèves"
            )
            section_colors = {
                "Math": "#ef4444", "Science": "#f97316", "Technique": "#eab308",
                "Informatique": "#22c55e", "Économie": "#3b82f6", "Sport": "#8b5cf6"
            }
            fig7 = px.bar(
                df_long, x="deleg", y="Élèves", color="Section",
                title=f"Répartition par section – {selected_year}",
                text="Élèves",
                color_discrete_map=section_colors
            )
            fig7.update_layout(
                barmode='stack',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.4)',
                xaxis=dict(color='#64748b', tickangle=-30, gridcolor='rgba(255,255,255,0.03)'),
                yaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)'),
                font=dict(color='#94a3b8'), title=dict(font=dict(color='#e2e8f0', size=12)),
                legend=dict(font=dict(color='#94a3b8', size=10),
                            bgcolor='rgba(15,23,42,0.6)', bordercolor='rgba(56,189,248,0.1)'),
                margin=dict(l=0, r=0, t=40, b=0), height=320
            )
            fig7.update_traces(texttemplate='%{text:.0f}', textposition='inside',
                               textfont=dict(size=9, color='white'), marker_line_width=0)
            st.plotly_chart(fig7, use_container_width=True)

        elif mode == "🗺️ Carte choroplèthe":
            avail_sections = [s for s in sections if s in df_seco_r.columns]
            df_seco_r["Total_orientés"] = df_seco_r[avail_sections].sum(axis=1)
            df_seco_r["Taux_moyen"] = df_seco_r[avail_sections].mean(axis=1)
            m2 = create_base_map()
            try:
                with open("kai-deleg.json", encoding="utf-8") as f:
                    geojson_data = json.load(f)
                for feature in geojson_data["features"]:
                    ref_code = feature["properties"]["id"]
                    row = df_seco_r[df_seco_r["ref_tn_cod"] == ref_code]
                    if not row.empty:
                        for s in avail_sections + ["Taux_moyen"]:
                            if s in row.columns:
                                feature["properties"][s] = round(row.iloc[0][s], 1)
                choropleth2 = folium.Choropleth(
                    geo_data=geojson_data, data=df_seco_r,
                    columns=('ref_tn_cod', "Taux_moyen"), key_on='feature.properties.id',
                    fill_color=folium_palette, legend_name="Taux orientation (%)",
                    highlight=True, fill_opacity=0.75
                )
                choropleth2.geojson.add_to(m2)
                tooltip_fields = ['del_fr'] + [s for s in avail_sections if s in df_seco_r.columns]
                choropleth2.geojson.add_child(folium.GeoJsonTooltip(tooltip_fields, localize=True, sticky=True))
                st_folium(m2, width='100%', height=400)
            except Exception as e:
                st.error(f"Erreur lors du chargement de la carte : {e}")


# =============================================
# 11. PAGE TECHNIQUE
# =============================================
def show_data_analysis_technique():
    selected_year = st.session_state.selected_year
    selected_deleg = st.session_state.selected_deleg
    selected_color = st.session_state.selected_color_theme

    color_theme_map = {"Bleu": ("Blues", "blues"), "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")}
    folium_palette, altair_palette = color_theme_map[selected_color]

    page_banner("🔧", "Cycle Préparatoire Technique",
                f"Indicateurs techniques · Année {selected_year}")
    st.markdown('<span class="cycle-badge" style="background: linear-gradient(135deg, #d97706, #f59e0b);">⚙️ PRÉPARATOIRE TECHNIQUE</span>',
                unsafe_allow_html=True)

    df_tech = df[df['niveau'] == "Cycle Preparatoire(Tech)"]
    df_selected_tech = df_tech[df_tech['year'] == selected_year].copy()
    df_tech_del = df[(df['niveau'] == "Cycle Preparatoire(Tech)") &
                     (df["year"] == selected_year) & (df["deleg"] == selected_deleg)].copy()
    df_selected_tech['densite'] = df_selected_tech['densite'].astype(str).str.replace(',', '.').astype(float)

    col_main, col_kpi = st.columns([4, 1.8], gap='large')

    with col_kpi:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(217,119,6,0.2) 0%, rgba(245,158,11,0.1) 100%);
                    border: 1px solid rgba(245,158,11,0.25); border-radius: 16px;
                    padding: 20px; margin-bottom: 16px;">
            <p style="color:#f59e0b; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:14px;">
                🌍 INDICATEURS RÉGIONAUX
            </p>
        """, unsafe_allow_html=True)
        kpis_reg = [
            ("🏛️", "Établissements", int(df_selected_tech['nbetabli'].sum()), "#f59e0b"),
            ("👥", "Élèves", f"{int(df_selected_tech['student'].sum()):,}", "#34d399"),
            ("🏫", "Classes", f"{int(df_selected_tech['class'].sum()):,}", "#a78bfa"),
            ("👩‍🏫", "Enseignants", f"{int(df_selected_tech['enseignant'].sum()):,}", "#fb923c"),
        ]
        for icon, label, val, color in kpis_reg:
            st.markdown(kpi_card(icon, label, val, color), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(217,119,6,0.1) 0%, rgba(180,83,9,0.1) 100%);
                    border: 1px solid rgba(245,158,11,0.2); border-radius: 16px;
                    padding: 20px;">
            <p style="color:#fbbf24; font-size:0.7rem; text-transform:uppercase;
                      letter-spacing:0.15em; font-weight:600; margin-bottom:4px;">
                📍 DÉLÉGATION
            </p>
            <p style="color:#e2e8f0; font-size:1.1rem; font-weight:700; margin-bottom:14px;">
                {selected_deleg}
            </p>
        """, unsafe_allow_html=True)
        if len(df_tech_del) > 0:
            df_tech_del['densite'] = df_tech_del['densite'].astype(str).str.replace(',', '.').astype(float)
            kpis_del = [
                ("🏛️", "Établissements", int(df_tech_del['nbetabli'].sum())),
                ("👥", "Élèves", f"{int(df_tech_del['student'].sum()):,}"),
                ("🏫", "Classes", f"{int(df_tech_del['class'].sum()):,}"),
                ("👩‍🏫", "Enseignants", f"{int(df_tech_del['enseignant'].sum()):,}"),
            ]
            for icon, label, val in kpis_del:
                st.markdown(deleg_card(icon, label, val), unsafe_allow_html=True)
        else:
            st.info("Pas de données disponibles.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        section_header("🗓️", "Évolution des effectifs techniques")
        heatmap = make_heatmap(df_tech, 'year', 'deleg', 'student', altair_palette)
        st.altair_chart(heatmap, use_container_width=True)

        section_header("🗺️", f"Carte & Établissements – {selected_year}")
        map_obj = create_base_map()
        choropleth = folium.Choropleth(
            geo_data='kai-deleg.json', data=df_selected_tech,
            columns=('ref_tn_cod', 'student'), key_on='feature.properties.id',
            legend_name=f"Élèves ({selected_year})", fill_color=folium_palette,
            highlight=True, fill_opacity=0.75, line_opacity=0.3
        )
        choropleth.geojson.add_to(map_obj)
        student_dict = dict(zip(df_selected_tech['ref_tn_cod'], df_selected_tech['student']))
        densite_dict = dict(zip(df_selected_tech['ref_tn_cod'], df_selected_tech['densite']))
        for feature in choropleth.geojson.data['features']:
            id_d = feature["properties"]["id"]
            feature['properties']['student'] = student_dict.get(id_d, 0)
            feature['properties']['densite'] = densite_dict.get(id_d, 'N/A')
        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr', 'student', 'densite'],
                                                            aliases=['Délégation', 'Élèves', 'Densité'],
                                                            localize=True))
        if 'lat' in df_tech_del.columns and 'lon' in df_tech_del.columns:
            for _, row in df_tech_del.iterrows():
                try:
                    folium.CircleMarker(
                        location=[float(row['lat']), float(row['lon'])],
                        radius=8, color='#f59e0b', fill=True, fill_color='#fbbf24',
                        fill_opacity=0.8,
                        popup=folium.Popup(
                            f"<b>{row.get('nom', 'N/A')}</b><br>👥 {row['student']} élèves<br>📊 {row['densite']} él/cl",
                            max_width=200
                        ),
                        tooltip=row.get('nom', '')
                    ).add_to(map_obj)
                except Exception:
                    pass
        st_folium(map_obj, width='100%', height=380)

        section_header("📊", f"Densité des classes techniques – {selected_year}")
        df_sorted = df_selected_tech.sort_values(by='densite', ascending=False)
        fig2 = px.bar(
            df_sorted, x='deleg', y='densite', color='densite',
            color_continuous_scale=[[0, '#451a03'], [0.5, '#d97706'], [1, '#fbbf24']],
            text='densite', title=f"Densité – {selected_year}"
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.4)',
            xaxis=dict(color='#64748b', tickangle=-30, gridcolor='rgba(255,255,255,0.03)'),
            yaxis=dict(color='#64748b', gridcolor='rgba(255,255,255,0.05)'),
            font=dict(color='#94a3b8'), title=dict(font=dict(color='#e2e8f0', size=12)),
            coloraxis_showscale=False, margin=dict(l=0, r=0, t=40, b=0), height=300
        )
        fig2.update_traces(texttemplate='%{text:.1f}', marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)


# =============================================
# 12. PAGE GPS ÉTABLISSEMENTS
# =============================================
def show_GPS_Etab():
    if st.button("← Retour au dashboard", key="back_btn"):
        st.session_state.selected_button = False
        st.rerun()

    page_banner("📡", "Carte GPS des Établissements Scolaires",
                "Localisation & Projets d'investissement – Kairouan")

    @st.cache_data
    def load_gps():
        df_g = pd.read_csv('GPS.csv', sep=';', encoding='ISO-8859-1',
                           on_bad_lines='skip', dtype={'code_et': str})
        df_g['lat1'] = pd.to_numeric(df_g['lat1'], errors='coerce')
        df_g['lon1'] = pd.to_numeric(df_g['lon1'], errors='coerce')
        df_g = df_g.dropna(subset=['lat1', 'lon1'])
        return df_g

    df_gps = load_gps()
    df_gps['deleg1'] = df_gps['deleg1'].str.strip()
    df_gps['code_et'] = df_gps['code_et'].astype(str).str.strip()

    # Filtres côte à côte
    f1, f2 = st.columns(2, gap='medium')
    with f1:
        delegations = df_gps['deleg1'].dropna().unique().tolist()
        selected_deleg_gps = st.selectbox("📍 Délégation", ["Toutes"] + sorted(delegations))
    with f2:
        filtered_df = df_gps if selected_deleg_gps == "Toutes" else df_gps[df_gps["deleg1"] == selected_deleg_gps]
        etabs = filtered_df["code_et"].dropna().unique().tolist()
        selected_etab = st.selectbox("🏫 Établissement", ["Tous"] + sorted(etabs))

    if selected_etab != "Tous":
        filtered_df = filtered_df[filtered_df["code_et"] == selected_etab]

    # Légende
    st.markdown("""
    <div style="display:flex; gap:20px; padding: 10px 0; flex-wrap:wrap;">
        <span style="color:#64748b; font-size:0.8rem;">
            🔵 <span style="color:#3b82f6">Lycée</span> &nbsp;
            🔴 <span style="color:#ef4444">Collège/Mixte</span> &nbsp;
            🟠 <span style="color:#f97316">Collège Technique</span> &nbsp;
            🟢 <span style="color:#22c55e">École Primaire</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_map, col_table = st.columns([4.3, 3.0], gap='medium')

    with col_map:
        map_gps = folium.Map(location=[35.40, 10.06], zoom_start=8,
                             scrollWheelZoom=False, tiles='CartoDB dark_matter')
        color_map_nature = {
            'lycee': ('blue', 'university'),
            'college': ('red', 'school'),
            'mixte': ('red', 'school'),
            'college technique': ('orange', 'book'),
        }
        for _, row in filtered_df.iterrows():
            nature_c = str(row["nature"]).strip().lower()
            icon_color, icon_name = color_map_nature.get(nature_c, ('green', 'child'))
            popup_text = f"""
            <div style="font-family:sans-serif; min-width:160px;">
                <b style="color:#1e293b;">{row['nature']}</b><br>
                <span style="color:#475569;">📍 {row['deleg1']}</span><br>
                <span style="color:#475569;">🏫 {row['nom']}</span>
            </div>"""
            folium.Marker(
                location=[row["lat1"], row["lon1"]],
                popup=folium.Popup(popup_text, max_width=220),
                icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
            ).add_to(map_gps)
        st_folium(map_gps, width='100%', height=520)

    with col_table:
        st.markdown("""
        <p style="color:#64748b; font-size:0.75rem; text-transform:uppercase;
                  letter-spacing:0.12em; margin-bottom:8px; font-weight:600;">
            📋 DONNÉES DES ÉTABLISSEMENTS
        </p>
        """, unsafe_allow_html=True)
        cols_to_drop = [c for c in ["lat1", "lon1", "ref_tn_cod1", "codedel1"] if c in filtered_df.columns]
        st.dataframe(
            filtered_df.drop(columns=cols_to_drop),
            use_container_width=True, height=300
        )

    # ── Projets d'investissement ──
    try:
        df_pr = pd.read_csv('avanprojets.csv', sep=';', encoding='ISO-8859-1',
                            on_bad_lines='skip', dtype={'code_et': str})
        df_pr['code_et'] = df_pr['code_et'].astype(str).str.strip()
        df_pr['nature'] = df_pr['nature'].astype(str).str.strip().str.lower()
        df_gps['code_et'] = df_gps['code_et'].astype(str).str.strip()
        df_gps['nature'] = df_gps['nature'].astype(str).str.strip().str.lower()
        df_final = df_pr.merge(df_gps, on=["code_et", "nature"], how="left")
        df_filtered = df_final.copy()
        if selected_deleg_gps != "Toutes":
            df_filtered = df_filtered[df_filtered['deleg1'] == selected_deleg_gps]
        if selected_etab != "Tous":
            df_filtered = df_filtered[df_filtered['code_et'] == selected_etab]

        if not df_filtered.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            section_header("💰", "Projets d'Investissement CRE Kairouan")

            pie_colors = ['#0ea5e9', '#38bdf8', '#7dd3fc', '#a78bfa', '#f472b6',
                          '#34d399', '#fbbf24', '#fb923c', '#f87171']

            c1, c2, c3, c4 = st.columns(4, gap='medium')
            charts = [
                ('type_inter', 'Type dintervention', "Par type d'intervention"),
                ('Bailleur', 'Bailleur de Fond', "Par bailleur de fonds"),
                ('Ann_prog', 'Annee', "Par année de programmation"),
            ]
            cols_list = [c1, c2, c3]
            for idx, (field, col_label, title) in enumerate(charts):
                if field in df_filtered.columns:
                    count_df = df_filtered[field].value_counts().reset_index()
                    count_df.columns = [col_label, 'Nombre']
                    fig_p = px.pie(
                        count_df, names=col_label, values='Nombre',
                        hole=0.55, title=title,
                        color_discrete_sequence=pie_colors
                    )
                    fig_p.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#94a3b8', size=10),
                        title=dict(font=dict(color='#e2e8f0', size=11)),
                        legend=dict(font=dict(color='#94a3b8', size=9),
                                    bgcolor='rgba(15,23,42,0.4)'),
                        margin=dict(l=0, r=0, t=35, b=0), height=260
                    )
                    fig_p.update_traces(textinfo='percent', textfont=dict(color='white', size=9))
                    with cols_list[idx]:
                        st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("Aucun projet trouvé pour les filtres sélectionnés.")
    except Exception as e:
        st.warning(f"Données projets non disponibles : {e}")


# =============================================
# 13. NAVIGATION PRINCIPALE
# =============================================
def navigate():
    if not st.session_state.logged_in:
        login()
        return

    df  # s'assure que les données sont chargées

    with st.sidebar:
        # Logo & titre
        try:
            st.image('470202910_1029942125839144_4726740988042572752_n.jpg', use_container_width=True)
        except Exception:
            st.markdown("🎓")
        st.markdown("""
        <div style="text-align:center; padding: 10px 0;">
            <p style="color:#38bdf8; font-size:1rem; font-weight:700; margin:0;">
                DRE Kairouan
            </p>
            <p style="color:#475569; font-size:0.7rem; margin:4px 0 0 0;">
                Tableau de bord éducatif
            </p>
        </div>
        <hr style="border-color:rgba(56,189,248,0.15); margin: 12px 0;">
        """, unsafe_allow_html=True)

        st.markdown('<p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px;">🗓️ Année</p>', unsafe_allow_html=True)
        year_list = sorted(df.year.unique(), reverse=True)
        st.session_state.selected_year = st.selectbox('Année scolaire', year_list, label_visibility='collapsed')

        st.markdown('<p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; margin-top:12px;">🌍 Délégation</p>', unsafe_allow_html=True)
        deleg_list = sorted(df.deleg.unique())
        st.session_state.selected_deleg = st.selectbox('Délégation', deleg_list, label_visibility='collapsed')

        st.markdown('<p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; margin-top:12px;">💡 Cycle</p>', unsafe_allow_html=True)
        niveau_list = df.niveau.unique()
        ordre = ["Cycle Primaire", "Cycle Preparatoire(G)& Enseignement Secondaire", "Cycle Preparatoire(Tech)"]
        niveau_sorted = sorted(niveau_list, key=lambda x: ordre.index(x) if x in ordre else 999)
        st.session_state.selected_niveau = st.selectbox('Cycle', niveau_sorted, label_visibility='collapsed')

        st.markdown('<p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; margin-top:12px;">🎨 Palette</p>', unsafe_allow_html=True)
        color_options = {"🔵 Bleu": "Bleu", "🔴 Rouge": "Rouge", "🟢 Vert": "Vert"}
        selected_label = st.selectbox('Palette', list(color_options.keys()), label_visibility='collapsed')
        st.session_state.selected_color_theme = color_options[selected_label]

        st.markdown('<hr style="border-color:rgba(56,189,248,0.1); margin: 16px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">🧭 Navigation</p>', unsafe_allow_html=True)

        if st.button("📍 GPS des établissements", use_container_width=True):
            st.session_state.selected_button = True

        if st.session_state.selected_button:
            if st.button("⬅️ Retour aux KPI", use_container_width=True):
                st.session_state.selected_button = False
                st.rerun()

        st.markdown('<hr style="border-color:rgba(56,189,248,0.1); margin: 16px 0;">', unsafe_allow_html=True)

        # Utilisateur connecté
        username = st.session_state.get('username', '?')
        st.markdown(f"""
        <div style="background: rgba(56,189,248,0.06); border: 1px solid rgba(56,189,248,0.1);
                    border-radius: 10px; padding: 10px 12px; text-align:center;">
            <span style="color:#64748b; font-size:0.7rem;">Connecté en tant que</span><br>
            <span style="color:#38bdf8; font-weight:600; font-size:0.85rem;">@{username}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Déconnexion", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()

    # ── Routing ──
    if st.session_state.selected_button:
        show_GPS_Etab()
    elif st.session_state.selected_niveau == "Cycle Primaire":
        show_dashboardprim()
    elif st.session_state.selected_niveau == "Cycle Preparatoire(G)& Enseignement Secondaire":
        show_data_analysis_Secondaire()
    elif st.session_state.selected_niveau == "Cycle Preparatoire(Tech)":
        show_data_analysis_technique()


# =============================================
# 14. CHARGEMENT & LANCEMENT
# =============================================
df = load_data()
navigate()
