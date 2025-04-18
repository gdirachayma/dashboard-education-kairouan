import pandas as pd
import numpy as np 
import streamlit as st
import plotly.express as px
import altair as alt
import geopandas as gpd
import geoviews as gv
from cartopy import crs
import panel as pn
import folium 
from streamlit_folium import st_folium 
import tempfile
import os
import base64
# === Initialisation des variables de session ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_step" not in st.session_state:
    st.session_state.current_step = 0


#pip install streamlit geoviews holoviews bokeh pandas panel dans bash
#######################
# Configuration-Page
st.set_page_config(
    page_title="dashboardeducationKairouan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable()
#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 2rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #496C9F;
    text-align: center;
    padding: 20px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 35%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 35%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}
            
[data-testid="stAppViewContainer"] > .main {
    background-image: "ecole.jpg";
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
""", unsafe_allow_html=True)



# === Simuler une base d'utilisateurs ===
USER_CREDENTIALS = {
    "admin": "pass123",
    "kairouan": "education2025",
    "chaymaguedira":"290190Ch@yma"
}

# === Authentification de base ===
def login():
    st.title("🔐 Connexion au Dashboard-KPI Education in KAIROUAN")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Bienvenue ! Vous êtes connecté.")
        else:
            st.error("Identifiants incorrects")

# Initialiser la session si elle n'existe pas
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
  
# Afficher login ou dashboard
if not st.session_state.logged_in:
    login()
    st.stop()


# 👉 Le reste de ton app ici...


if st.button("➡️ Accéder au Dashboard Primaire"):
    st.switch_page("pages/1_Dashboardprimaire.py")
if st.button("➡️ Accéder au Dashboard secondaire"):
    st.switch_page("pages/2_Dashboardseco.py")
if st.button("➡️ Accéder au Dashboard Résultats nationaux"):
    st.switch_page("pages/3_Dashboardresultat.py")
 #######################
 
