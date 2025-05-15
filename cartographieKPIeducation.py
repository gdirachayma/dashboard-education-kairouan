#pip install streamlit geoviews holoviews bokeh pandas panel dans bash
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
from streamlit.components.v1 import html
import plotly.graph_objects as go
import json
#######################
# === 1. Page configuration ===
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
/* Réduit l'espace général au-dessus du contenu principal */
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}
/* Réduit l’espace à l’intérieur du bloc principal */
[data-testid="block-container"] {
    background-color: rgba(255, 255, 255, 0.85);
    padding-top: 0.01rem !important;  /* ⬅️ Réduit l’espace interne en haut */
    padding-right: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0,0,0,0.1);
    margin-top: 0 !important;
}
/* Réduit encore l’espace au-dessus du titre */
h1 {
    margin-top: -0.1 !important;
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
    col1, col2 = st.columns((1.3,5.0), gap='medium')
    with col1:
         st.image("470202910_1029942125839144_4726740988042572752_n.jpg", use_container_width=True)
    with col2:
        st.title("🔐 Connexion au Dashboard-KPI Education in KAIROUAN")
        with st.form(key="login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
             
            if st.form_submit_button("Se connecter"):
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.success("Bienvenue ! Vous êtes connecté ✅ ")
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect ❌")
    st.image("https://i.pinimg.com/originals/d7/64/c7/d764c70776b64e523cb4eea2f322db96.gif", use_container_width=True)
         
# === 4. Gestion de la session ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

def navigate():
    # Page de login ou page après connexion
    if not st.session_state.logged_in:
        login()  # Si l'utilisateur n'est pas connecté, afficher la page de login
    else:
        with st.sidebar:    
            st.image('470202910_1029942125839144_4726740988042572752_n.jpg')
            st.title('Indicateurs éducatifs de Kairouan ')
            st.title('Kairouan en Chiffres')
            year_list = list(df.year.unique())[::1]
            st.session_state.selected_year = st.selectbox('🗓️ Select a year', year_list)
            df_selected_year = df[df.year == st.session_state.selected_year]
            df_selected_year_sorted = df_selected_year.sort_values(by="student", ascending=False)

            deleg_list = list(df.deleg.unique())[::1]
            st.session_state.selected_deleg = st.selectbox('🌎 Select a delegation', deleg_list)
            df_selected_deleg = df[df.deleg == st.session_state.selected_deleg]

            niveau_list = list(df.niveau.unique())[::-1]
            ordre_personnalise=["Cycle Primaire","Cycle Preparatoire(G)& Enseignement Secondaire","Cycle Preparatoire(Tech)"]
            niveau_list_sorted=sorted(niveau_list,key=lambda x: ordre_personnalise.index(x) if x in ordre_personnalise else 999)
            st.session_state.selected_niveau = st.selectbox('💡 Select a cycle', niveau_list_sorted)
            df_selected_niveau = df[df.niveau== st.session_state.selected_niveau]
            
            color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
            st.session_state.selected_color_theme = st.selectbox('🖌️ Select a color theme', list(color_theme_list.keys()))
            color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
            folium_palette, altair_palette = color_theme_list[ st.session_state.selected_color_theme]
             
        if st.session_state.selected_niveau == "Cycle Primaire":
            show_dashboardprim()
        elif st.session_state.selected_niveau == "Cycle Preparatoire(G)& Enseignement Secondaire":
            show_data_analysis_Secondaire()  # Afficher une autre page (exemple: analyse des données)
        elif st.session_state.selected_niveau == "Cycle Preparatoire(Tech)":
            show_data_analysis_technique()  # Afficher une troisième page (exemple: rapports)
        

          
#######



 #######################
# Load data  se fait en écrivant cette formule df=pd.read_csv('streambase    .csv',sep=';',encoding='MacRoman')
#mais on va l'ecrire comme ci dessous pour charger et automatiser le calcul sans retard

@st.cache_data
def load_data():
    return pd.read_csv('streambase    .csv',sep=';',encoding='MacRoman')

df = load_data()

# 👉 Le reste de ton app ici...

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
        heatmap = alt.Chart(input_df).mark_rect().encode(
                y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
                x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
                color=alt.Color(f'max({input_color}):Q',
                                legend=None,
                                scale=alt.Scale(scheme=input_color_theme)),
                stroke=alt.value('black'),
                strokeWidth=alt.value(0.25),
            ).properties(width=900
            ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
            ) 
        # height=300
        return heatmap


##1-creation des pages-page de cycle primaire

def show_dashboardprim():
    # 🎉 Si connecté, afficher le dashboard :
 
    st.title("📊 Dashboard Éducation - Kairouan-KPI")
    

    # Sidebar-page.
    
        
    st.write("Bienvenue dans le tableau de bord. Vous pouvez consulter les données d'éducation ici.")
   
    #######################
    st.header("Key Performance Indicators  Of Education in Kairouan- Cycle Primaire 📚")
    #################
    selected_year = st.session_state.selected_year
    selected_niveau = st.session_state.selected_niveau
    selected_deleg=st.session_state.selected_deleg
    selected_color=st.session_state.selected_color_theme
    color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
    folium_palette, altair_palette = color_theme_list[ selected_color]
    #######################
    df_p=df[(df['niveau'] == "Cycle Primaire")]
    df_prim = df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year)]
    df_selected_primaire = df_prim[df_prim['year'] == selected_year]
    df_prim_del=df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]
    ################
    #######################
    # Dashboard Main Panel
    col = st.columns((4.0, 2.0), gap='large')

    with col[0]:
            st.markdown('#### Total élèves')
            heatmap = make_heatmap( df_p,'year',  'deleg', 'student', altair_palette)
            chart=st.altair_chart(heatmap, use_container_width=True) 

            map=folium.Map(location=[35.40,10.06],zoom_start=7,scrolwheelzoom=False,tiles='CartoDB positron')
            choropleth=folium.Choropleth(geo_data='kai-deleg.json',data=df_prim,columns=('ref_tn_cod','student'),key_on='feature.properties.id',legend_name=f"Nombre d'élèves ({selected_year})",fill_color=folium_palette,highlight=True)
            choropleth.geojson.add_to(map)
            
            student_dict = dict(zip(df_selected_primaire ['ref_tn_cod'], df_selected_primaire ['student']))
            df_indexed = df.set_index('ref_tn_cod')
            
            for feature in choropleth.geojson.data['features']:
                id_dele=feature["properties"]["id"]
                feature['properties']['student']=student_dict.get(id_dele, 0)       

            choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr','student'],labels=False))

            # 🎯 Highlight de la délégation choisie
            for feature in choropleth.geojson.data["features"]:
                if feature["properties"]["del_fr"] == selected_deleg:
                    folium.GeoJson(
                        data=feature,
                        style_function=lambda x: {
                            'fillColor': 'red',
                            'color': 'red',
                            'weight': 4,
                            'fillOpacity': 0.9
                        },
                        tooltip=folium.GeoJsonTooltip(fields=["del_fr", "student"])
                    ).add_to(map)
            # Affichage de la carte
            st.subheader(f'📍 Répartition des élèves par délégation - Année {selected_year}')
            st_fol=st_folium(map, width=850, height=450)
            #Affichage de  l'histogramme densité
            st.subheader("🏫 Densité des classes par Délégation") 
            # Nettoyage des virgules + conversion en float
            df_selected_primaire ['densite'] = df_selected_primaire ['densite'].str.replace(',', '.').astype(float)       
            # Trier les délégations par densité (desc)
            df_sorted = df_selected_primaire .sort_values(by='densite', ascending=False)
            # Histogramme
            fig1 = px.bar(
                df_sorted,
                x='deleg',
                y='densite',
                color='deleg',
                color_discrete_sequence=px.colors.sequential.RdBu_r,
                text='densite',
                title=f"Densité des classes par Délégation - {selected_year}")
            # Mise en forme
            fig1.update_layout(
                title_x=0.03,
                xaxis_title="Délégation",
                yaxis_title="Densité (élèves par classe)",
                coloraxis_showscale=False
            )

            fig1.update_traces(texttemplate='%{text:.1f}')
            # Affichage
            st.plotly_chart(fig1, use_container_width=True)
            # Restructurer les colonnes 1ann → 6ann en format long (melt)
            df_long = df_prim.melt(id_vars=["deleg"], 
                            value_vars=["1ann", "2ann", "3ann", "4ann", "5ann", "6ann"],
                            var_name="Niveau", 
                            value_name="Élèves")
            # Tracer la courbe
            fig2= px.line(df_long, x="deleg", y="Élèves", color="Niveau", markers=True,
                        title=f"📚 Répartition des élèves par niveau (1ère à 6ème année)– {selected_year}")

            fig2.update_layout(
                xaxis_title="delegation",
                yaxis_title="Nombre d'élèves",
                title_x=0.5,
                template="plotly_white"
            )

            st.plotly_chart(fig2, use_container_width=True)

            # camembert des classes préparatoires
            st.subheader("🧒 % Ecoles ayant des CP par rapport à la totalité des écoles contenant des CP")
            fig = px.pie(df_selected_primaire , names='deleg', values='prep',
                    color_discrete_sequence=px.colors.sequential.RdBu,
                    title=f"Groupes préparatoires - {selected_year}")
            st.plotly_chart(fig, use_container_width=True)
            # Courbe

    with col[1]:  
        st.markdown("""
                <div style="background-color: #659db8; padding: 60px; border-radius: 11px;">
                    <h4 style="text-align:center;"> Indicateurs Clés -Régionale</h4>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#fefcfb;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧒 Élèves<br><strong style="color:#fefcfb;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#fefcfb;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                      👩‍🏫 Enseignants<br><strong style="color:#fefcfb;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        📊 Densité<br><strong style="color:#fefcfb;">{densite}</strong> 
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                      👶🏻 Nb d'écoles ayant des CP<br><strong style="color:#fefcfb;">{classes_preparatoires}</strong>
                    </div>
                </div>
            """.format(
                établissemnts=int(df_selected_primaire ['nbetabli'].sum()),
                eleves=int(df_selected_primaire ['student'].sum()),
                classes=int(df_selected_primaire ['class'].sum()),
                densite=round(df_selected_primaire ['densite'].replace(',', '.').astype(float).mean(),2),
                classes_preparatoires=int(df_selected_primaire ['prep'].sum()),
                enseign=int(df_selected_primaire ['enseignant'].sum())
                ), unsafe_allow_html=True) 
        st.markdown("""
                <div style="background-color:#f3f4fb ; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🚀 Indicateurs Clés -Par délégation</h4>{delegationaffichage}</strong>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#3f678c;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        👨🏻‍🎓 Élèves<br><strong style="color:#3f678c;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3f678c;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#3f678c;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧑🏽‍🤝‍🧑🏽 Densité<br><strong style="color:#3f678c;">{densite}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🍼🧸 Nb d'écoles ayant des CP <br><strong style="color:#3f678c;">{classes_preparatoires}</strong>
                    </div>
                </div>
            """.format(
                delegationaffichage=str(selected_deleg),
                établissemnts=int(df_prim_del ['nbetabli'].sum()),
                eleves=int(df_prim_del ['student'].sum()),
                classes=int(df_prim_del ['class'].sum()),
                densite=round(df_prim_del ['densite'].str.replace(',', '.').astype(float).mean(),2),
                enseign=int(df_prim_del ['enseignant'].sum()),
                classes_preparatoires=int(df_prim_del ['prep'].sum())), unsafe_allow_html=True) 

        # Nettoyage des données
        df_selected_primaire['per nouv 1 ayant ben AP'] = (
            df_selected_primaire['per nouv 1 ayant ben AP']
            .replace(',', '.', regex=True)
            .astype(float)
        )

        # Trier les délégations
        df_sorted1 = df_selected_primaire.sort_values(by='per nouv 1 ayant ben AP', ascending=True)

        delegations = df_sorted1['deleg']
        taux = df_sorted1['per nouv 1 ayant ben AP']
        moyenne = round(taux.mean(), 1)

        # Créer figure vide
        fig = go.Figure()

        # Ajouter barres horizontales
        fig.add_trace(go.Bar(
            y=delegations,                # <- Délégations en Y
            x=taux,                       # <- Taux en X
            orientation='h',             # <- Orientation horizontale
            marker_color=['#153160' if val > moyenne else '#3f678c' for val in taux],
            text=[f"{val:.1f} %" for val in taux],
            textposition='auto',
            insidetextanchor='start'
        ))

        # Zone SOUS la moyenne
        fig.add_shape(
            type="rect",
            xref="x", yref="paper",   # <- Inversé : X pour le taux
            x0=0, x1=moyenne,
            y0=0, y1=1,
            fillcolor="white",
            opacity=0.2,
            layer="below",
            line_width=0,
        )

        # Zone AU-DESSUS de la moyenne
        fig.add_shape(
            type="rect",
            xref="x", yref="paper",
            x0=moyenne, x1=max(taux),
            y0=0, y1=1,
            fillcolor="green",
            opacity=0.15,
            layer="below",
            line_width=0,
        )

        # Ligne verticale de la moyenne
        fig.add_vline(
            x=moyenne,
            line_dash="dot",
            line_color="white",
            line_width=2,
            annotation_text=f"Moyenne : {moyenne} %",
            annotation_position="top left",
            annotation_font=dict(size=13, color="white", family="Arial Black")
        )

        # Mise en page
        fig.update_layout(
            title=f"Taux des nouveaux inscrits en 1ère année ayant bénéficié de l'année préparatoire – {selected_year}",
            title_x=0.05,
            xaxis_title="Taux (%)",
            yaxis_title="Délégation",
            height=600
        )

        # Affichage dans Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    with st.expander('About', expanded=True):
                st.write('''
                    - Data: [Bureau de planification et de statistiques à Kairouan](http://www.edunet.tn/index.php?id=523&lan=1).
                    ''')
                
# === 6. Fonction pour afficher différentes pages ===
def show_data_analysis_Secondaire():
    st.title("📈 Analyse des Données de Cycle Préparatoire et Enseignement Secondaire")
    st.write("Ici on va  mettre en lumiére sur les données de manière détaillée.")
    
     #######################
    st.header("Key Performance Indicators  Of Education in Kairouan- Cycle Prep(G)& Enseignement Seco 📚")
    #######################
    selected_year = st.session_state.selected_year
    selected_niveau = st.session_state.selected_niveau
    selected_deleg=st.session_state.selected_deleg
    selected_color=st.session_state.selected_color_theme
   
    color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
    folium_palette, altair_palette = color_theme_list[ selected_color]
    #########################
    df_s=df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire")]
    df_seco = df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire")&(df["year"] == selected_year)]
    df_selected_seco= df_seco[df_seco['year'] == selected_year]
    df_seco_del=df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]
    
    ################
    # Plots

    #######################
    # Dashboard Main Panel
    col1, col2 = st.columns((4.5, 2.0), gap='large')
    with col1:
        st.markdown('#### Total élèves')
        heatmap = make_heatmap( df_s,'year', 'deleg', 'student', altair_palette)
        chart=st.altair_chart(heatmap, use_container_width=True) 

        map=folium.Map(location=[35.40,10.06],zoom_start=7,scrolwheelzoom=False,tiles='CartoDB positron')
        choropleth=folium.Choropleth(geo_data='kai-deleg.json',data=df_seco,columns=('ref_tn_cod','student'),key_on='feature.properties.id',legend_name=f"Nombre d'élèves ({selected_year})",fill_color=folium_palette,highlight=True)
        choropleth.geojson.add_to(map)
            
        student_dict = dict(zip(df_selected_seco ['ref_tn_cod'], df_selected_seco ['student']))
        df_indexed = df.set_index('ref_tn_cod')
            
        for feature in choropleth.geojson.data['features']:
            id_dele=feature["properties"]["id"]
            feature['properties']['student']=student_dict.get(id_dele, 0)       

        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr','student'],labels=False))

        # 🎯 Highlight de la délégation choisie
        for feature in choropleth.geojson.data["features"]:
            if feature["properties"]["del_fr"] == selected_deleg:
                folium.GeoJson(
                    data=feature,
                    style_function=lambda x: {
                        'fillColor': 'red',
                        'color': 'red',
                        'weight': 4,
                        'fillOpacity': 0.9
                        },
                    tooltip=folium.GeoJsonTooltip(fields=["del_fr", "student"])
                    ).add_to(map)

        # Affichage de la carte
        st.subheader(f'📍 Répartition des élèves par délégation - Année {selected_year}')
        st_fol=st_folium(map, width=850, height=450)
        st.subheader("🏫 Densité des classes par Délégation") 
        # Nettoyage des virgules + conversion en float
        df_selected_seco ['densite'] = df_selected_seco ['densite'].str.replace(',', '.').astype(float)       
        # Trier les délégations par densité (desc)
        df_sorted = df_selected_seco .sort_values(by='densite', ascending=False)

        # Histogramme
        fig1 = px.bar(
                df_sorted,
                x='deleg',
                y='densite',
                color='deleg',
                color_discrete_sequence=px.colors.sequential.RdBu_r,
                text='densite',
                title=f"Densité des classes par Délégation - {selected_year}")

            # Mise en forme
        fig1.update_layout(
                title_x=0.03,
                xaxis_title="Délégation",
                yaxis_title="Densité (élèves par classe)",
                coloraxis_showscale=False
            )

        fig1.update_traces(texttemplate='%{text:.1f}')
        # Affichage
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:  
            st.markdown("""
                <div style="background-color: #659db8; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🔢 Indicateurs Clés -Régionale</h4>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#fefcfb;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧒 Élèves<br><strong style="color:#fefcfb;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#fefcfb;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#fefcfb;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        📊 Densité<br><strong style="color:#fefcfb;">{densite}</strong>
                    </div>
                </div>
            """.format(
                établissemnts=int(df_selected_seco['nbetabli'].sum()),
                eleves=int(df_selected_seco ['student'].sum()),
                classes=int(df_selected_seco ['class'].sum()),
                densite=round(df_selected_seco ['densite'].replace(',', '.').astype(float).mean(),2),
                enseign=int(df_selected_seco ['enseignant'].sum())
                ), unsafe_allow_html=True) 
            st.markdown("""
                <div style="background-color:#f3f4fb ; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🚀 Indicateurs Clés -Par délégation</h4>{delegationaffichage}</strong>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#3f678c;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        👨🏻‍🎓 Élèves<br><strong style="color:#3f678c;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3f678c;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#3f678c;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧑🏽‍🤝‍🧑🏽 Densité<br><strong style="color:#3f678c;">{densite}</strong>
                    </div>
                </div>
            """.format(
                delegationaffichage=str(selected_deleg),
                établissemnts=int(df_seco_del ['nbetabli'].sum()),
                eleves=int(df_seco_del ['student'].sum()),
                classes=int(df_seco_del ['class'].sum()),
                densite=round(df_seco_del ['densite'].str.replace(',', '.').astype(float).mean(),2),
                enseign=int(df_seco_del ['enseignant'].sum())
                ), unsafe_allow_html=True) 
    #creer une carte ou diagramme selon choix à la fin de page 
    # Renommer les colonnes
    df_seco_renamed = df_seco.rename(columns={
            "per section math": "Math",
            "per section science": "Science",
            "per section tech": "Technique",
            "per section info": "Informatique",
            "per section eco": "Économie",
            "per section sport": "Sport"
        })
        
    # Nettoyer les données (convertir virgules en points)
    for col in ["Math", "Science", "Technique", "Informatique", "Économie", "Sport"]:
         df_seco_renamed[col] = df_seco_renamed[col].replace(',', '.', regex=True).astype(float)

    # Total des élèves orientés par délégation
    df_seco_renamed["Total_orientés"] = df_seco_renamed[["Math", "Science", "Technique", "Informatique", "Économie", "Sport"]].sum(axis=1)

    # Calcul des pourcentages
    for col in ["Math", "Science", "Technique", "Informatique", "Économie", "Sport"]:
         df_seco_renamed[col] = round(df_seco_renamed[col] / df_seco_renamed["Total_orientés"] * 100, 1)

    # Créer la carte ou le diagramme
    st.markdown("""
    <p style="font-weight:bold; color:#111111; font-size:18px;">
        Choisissez le mode de visualisation :
    </p>
    """, unsafe_allow_html=True)
    mode = st.radio("Choisissez le mode de visualisation :", ["🗺️ Carte", "📊 Diagramme empilé"])
        
    if mode == "🗺️ Carte":
        st.subheader("Carte du taux moyen d’orientation (toutes sections) par délégation")
        # Moyenne du taux d’orientation toutes sections (optionnel)
        df_seco_renamed["Taux_moyen_orientation"] = df_seco_renamed[["Math", "Science", "Technique", "Informatique", "Économie", "Sport"]].mean(axis=1)
        m = folium.Map(location=[35.40, 10.06], zoom_start=8, tiles='CartoDB positron')
        with open("kai-deleg.json", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Fusionner les données dans les features du GeoJSON
        for feature in geojson_data["features"]:
            ref_code = feature["properties"]["id"]
            row = df_seco_renamed[df_seco_renamed["ref_tn_cod"] == ref_code]
            if not row.empty:
                for col in ["Taux_moyen_orientation", "Math", "Science", "Technique", "Informatique", "Économie", "Sport"]:
                    val = row.iloc[0][col]
                    feature["properties"][col] = round(val, 1)
        choropleth = folium.Choropleth(
                geo_data=geojson_data,
                data=df_seco_renamed,
                columns=('ref_tn_cod', "Taux_moyen_orientation"),
                key_on='feature.properties.id',
                fill_color=folium_palette,
                legend_name="Taux orientation en bac (%)",
                highlight=True
            )
        choropleth.geojson.add_to(m)
        choropleth.geojson.add_child(folium.GeoJsonTooltip(
                fields=['del_fr', 'Math', 'Science', 'Technique', 'Informatique', 'Économie', 'Sport'],
                aliases=[
                    'Délégation',
                    'Math (%)',
                    'Science (%)',
                    'Technique (%)',
                    'Informatique (%)',
                    'Économie (%)',
                    'Sport (%)'
                ],
                localize=True,
                sticky=True
            ))

        st_folium(m, width=900, height=500)

    elif mode == "📊 Diagramme empilé":
        st.subheader("Diagramme empilé des % d’orientation par section et par délégation")

        df_long = df_seco_renamed.melt(
                id_vars=["deleg"],
                value_vars=["Math", "Science", "Technique", "Informatique", "Économie", "Sport"],
                var_name="Section",
                value_name="Pourcentage"
            )

        fig7 = px.bar(
                df_long,
                x="deleg",
                y="Pourcentage",
                color="Section",
                title="Orientation des élèves par délégation et section (%)",
                text="Pourcentage",
                labels={"deleg": "Délégation", "Pourcentage": "%"},
                color_discrete_sequence=["rgb(132,29,34)",  # Rouge foncé-math
                             "rgb(205,66,68)",  # rouge moins foncé-science
                             "rgb(221,93,54)",  # rouge orange-technique
                             "rgb(255,203,117)",  # jaune -informatique
                             "rgb(48,97,165)",  # bleue-economie
                             "rgb(51,51,51)"]   # Gris anthracite (Dark)-sport
            )
        fig7.update_layout(barmode='stack')
        fig7.update_traces(texttemplate='%{text:.1f}%', textposition='inside')

        st.plotly_chart(fig7, use_container_width=True)
          
def show_data_analysis_technique():
    st.title("🧑🏻‍🔧 Analyse des Données de Cycle Préparatoire Technique")
    st.write("Ici on va  prendre le cycle préparatoire Technique en considération")
    selected_year = st.session_state.selected_year
    selected_niveau = st.session_state.selected_niveau
    selected_deleg=st.session_state.selected_deleg
    selected_color=st.session_state.selected_color_theme
    color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
    folium_palette, altair_palette = color_theme_list[ selected_color]
    df_tech = df[(df['niveau'] == "Cycle Preparatoire(Tech)")]
    df_selected_tech = df_tech[df_tech['year'] == selected_year]
    df_tech_del=df[(df['niveau'] == "Cycle Preparatoire(Tech)") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]  
    df_selected_tech['densite'] = df_selected_tech ['densite'].str.replace(',', '.').astype(float)       
    # Trier les délégations par densité (desc)
    df_sorted = df_selected_tech .sort_values(by='densite', ascending=False)
    #######################
    # Dashboard Main Panel
    col = st.columns((4.5,2.0), gap='large')

    with col[0]:
        st.markdown('#### Total élèves')
        heatmap = make_heatmap( df_tech,'year', 'deleg', 'student', altair_palette)
        chart=st.altair_chart(heatmap, use_container_width=True)
        # Ajout du choropleth
        # Création de la carte Folium
        map=folium.Map(location=[35.40,10.06],zoom_start=7,scrolwheelzoom=False,tiles='CartoDB positron')
        choropleth=folium.Choropleth(geo_data='kai-deleg.json',data=df_tech_del,columns=('ref_tn_cod','student'),key_on='feature.properties.id',legend_name=f"Nombre d'élèves ({selected_year})",fill_color=folium_palette,highlight=True)
        choropleth.geojson.add_to(map)
        # Création d’un dictionnaire pour retrouver les infos
        student_dict = dict(zip(df_tech_del['ref_tn_cod'], df_tech_del['student']))
        deleg_dict = dict(zip(df_tech_del['ref_tn_cod'], df_tech_del['deleg']))
        densite_dict = dict(zip(df_tech_del['ref_tn_cod'], df_tech_del['densite']))
        # Ajout du tooltip (au survol)
        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr', 'student'], labels=False))
        # Ajout du popup (au clic)
        for feature in choropleth.geojson.data['features']:
            id_dele = feature["properties"]["id"]
            feature['properties']['student'] = student_dict.get(id_dele, "N/A")
            feature['properties']['densite'] = densite_dict.get(id_dele, "N/A")
            feature['properties']['deleg'] = deleg_dict.get(id_dele, "N/A")

        # 4. Ajout des tooltips (infos au survol)
        choropleth.geojson.add_child(folium.GeoJsonTooltip(
            fields=['del_fr', 'student', 'densite'],
            aliases=['Délégation', 'Nombre élèves', 'Densité'],
            localize=True
            ))
        # 5. Ajout des popups (au clic)
        for index, row in df_tech_del.iterrows():
            popup_content = f"""
            <b>🏫 {row['nom']}</b><br>
            👥 Élèves : {row['student']}<br>
            🏫 Classes : {row['class']}<br>
            📊 Densité : {row['densite']}
            """
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=row['nom'],
                icon=folium.Icon(color="purple", icon="sign")
            ).add_to(map)

        # Affichage de la carte dans Streamlit
        st.subheader(f"🗺️ Cartographie élève-délégation – {selected_year}")
        st_folium(map, width='100%', height=450)
        # Histogramme
        fig2 = px.bar(
                df_sorted,
                x='deleg',
                y='densite',
                color='deleg',
                color_discrete_sequence=px.colors.sequential.RdBu_r,
                text='densite',
                title=f"Densité de classes des collèges techniques par Délég- {selected_year}")

            # Mise en forme
        fig2.update_layout(
                title_x=0.03,
                xaxis_title="Délégation",
                yaxis_title="Densité (élèves par classe)",
                coloraxis_showscale=False
            )

        fig2.update_traces(texttemplate='%{text:.1f}')

            # Affichage
        st.plotly_chart(fig2, use_container_width=True)


    with col[1]:
            st.markdown("""
                <div style="background-color: #f3f4fb; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🔢 Indicateurs Clés -Régionale</h4>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#3f678c;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧒 Élèves<br><strong style="color:#3f678c;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3f678c;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#3f678c;">{enseign}</strong>
                    </div>
                </div>
            """.format(
                établissemnts=int(df_selected_tech['nbetabli'].sum()),
                eleves=int(df_selected_tech ['student'].sum()),
                classes=int(df_selected_tech ['class'].sum()),
                enseign=int(df_selected_tech ['enseignant'].sum())
                ), unsafe_allow_html=True) 
            st.markdown("""
                <div style="background-color:#659db8 ; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🚀 Indicateurs Clés -Par délégation</h4>{delegationaffichage}</strong>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#f3f4fb;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        👨🏻‍🎓 Élèves<br><strong style="color:#f3f4fb;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#f3f4fb;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#f3f4fb;">{enseign}</strong>
                    </div>
                </div>
            """.format(
                delegationaffichage=str(selected_deleg),
                établissemnts=int(df_tech_del['nbetabli'].sum()),
                eleves=int(df_tech_del ['student'].sum()),
                classes=int(df_tech_del ['class'].sum()),
                enseign=int(df_tech_del ['enseignant'].sum())
                ), unsafe_allow_html=True) 
        
# === 7. Exécuter la navigation ===
navigate()  # Démarre la fonction de navigation
