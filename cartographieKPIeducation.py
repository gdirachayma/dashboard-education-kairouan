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
            st.session_state.username = username
            st.session_state.logged_in = True
            st.success("Bienvenue ! Vous êtes connecté ✅ ")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect ❌")




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
# Load data
df=pd.read_csv('streambase    .csv',sep=';',encoding='MacRoman')

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
    df_prim = df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year)]
    df_selected_primaire = df_prim[df_prim['year'] == selected_year]
    df_prim_del=df[(df['niveau'] == "Cycle Primaire") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]
    ################
    #######################
    # Dashboard Main Panel
    col = st.columns((3.5, 2.5), gap='medium')

    with col[0]:
            st.markdown('#### Total élèves')
            heatmap = make_heatmap( df,'year',  'deleg', 'student', altair_palette)
            chart=st.altair_chart(heatmap, use_container_width=True) 

            map=folium.Map(location=[35.69,10.06],zoom_start=8,scrolwheelzoom=False,tiles='CartoDB positron')
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
            st.subheader("🧒 Groupes Préparatoires par Délégation ")
            fig = px.pie(df_selected_primaire , names='deleg', values='prep',
                    color_discrete_sequence=px.colors.sequential.RdBu,
                    title=f"Groupes préparatoires - {selected_year}")
            st.plotly_chart(fig, use_container_width=True)
            # Courbe


    with col[1]:  
        st.markdown("""
                <div style="background-color: #fcf7f7; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;"> Indicateurs Clés -Régionale</h4>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#ff6600;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧒 Élèves<br><strong style="color:#ff6600;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3366cc;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                      👩‍🏫 Enseignants<br><strong style="color:#009966;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        📊 Densité<br><strong style="color:#009966;">{densite}</strong> 
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                      👶🏻 Groupes Préparatoire<br><strong style="color:#009966;">{classes_preparatoires}</strong>
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
                <div style="background-color:#fff3f3 ; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🚀 Indicateurs Clés -Par délégation</h4>{delegationaffichage}</strong>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#ff6600;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        👨🏻‍🎓 Élèves<br><strong style="color:#ff6600;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3366cc;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#009966;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧑🏽‍🤝‍🧑🏽 Densité<br><strong style="color:#009966;">{densite}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🍼🧸 Groupes Préparatoires <br><strong style="color:#009966;">{classes_preparatoires}</strong>
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
    df_seco = df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire")&(df["year"] == selected_year)]
    df_selected_seco= df_seco[df_seco['year'] == selected_year]
    df_seco_del=df[(df['niveau'] == "Cycle Preparatoire(G)& Enseignement Secondaire") & (df["year"] == selected_year) & (df["deleg"] == selected_deleg)]
    
    ################
    # Plots

    #######################
    # Dashboard Main Panel
    col = st.columns((3.5, 2.5), gap='medium')

    with col[0]:
            st.markdown('#### Total élèves')
            heatmap = make_heatmap( df_seco,'year', 'deleg', 'student', altair_palette)
            chart=st.altair_chart(heatmap, use_container_width=True) 

            map=folium.Map(location=[35.69,10.06],zoom_start=8,scrolwheelzoom=False,tiles='CartoDB positron')
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


    with col[1]:  
        st.markdown("""
                <div style="background-color: #fcf7f7; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🔢 Indicateurs Clés -Régionale</h4>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#ff6600;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🧒 Élèves<br><strong style="color:#ff6600;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3366cc;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#009966;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 26px; margin: 8px 0;">
                        📊 Densité<br><strong style="color:#009966;">{densite}</strong>
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
                <div style="background-color:#fff3f3 ; padding: 26px; border-radius: 11px;">
                    <h4 style="text-align:center;">🚀 Indicateurs Clés -Par délégation</h4>{delegationaffichage}</strong>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧮 établissements<br><strong style="color:#ff6600;">{établissemnts}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        👨🏻‍🎓 Élèves<br><strong style="color:#ff6600;">{eleves}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🏫 Classes<br><strong style="color:#3366cc;">{classes}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                       👩‍🏫 Enseignants<br><strong style="color:#009966;">{enseign}</strong>
                    </div>
                    <div style="text-align:center; font-size: 20px; margin: 8px 0;">
                        🧑🏽‍🤝‍🧑🏽 Densité<br><strong style="color:#009966;">{densite}</strong>
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
  
def show_data_analysis_technique():
    st.title("🧑🏻‍🔧 Analyse des Données de Cycle Préparatoire Technique")
    st.write("Ici on va  prendre le cycle préparatoire Technique en considération")
    selected_year = st.session_state.selected_year
    selected_niveau = st.session_state.selected_niveau
    selected_deleg=st.session_state.selected_deleg
    selected_color=st.session_state.selected_color_theme
    color_theme_list =  {"Bleu": ("Blues", "blues"),  "Rouge": ("Reds", "reds"), "Vert": ("Greens", "greens")      }
    folium_palette, altair_palette = color_theme_list[ selected_color]


# === 7. Exécuter la navigation ===

navigate()  # Démarre la fonction de navigation
