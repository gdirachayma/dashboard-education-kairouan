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
import base64



#pip install streamlit geoviews holoviews bokeh pandas panel dans bash
#######################
# Configuration-Page
st.set_page_config(
    page_title="dashboardeducationKairouan",
    page_icon="🏂",
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
    padding-top: 1rem;
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

#######################
# Load data
df=pd.read_csv('streambase    .csv',sep=';',encoding='MacRoman')
#######################
st.header("Education Dashboard in Kairouan")
#######################
# Sidebar-page.
with st.sidebar:
    st.image('470202910_1029942125839144_4726740988042572752_n.jpg')
    st.title('Indicateurs éducatifs de Kairouan ')
    st.title('Kairouan en Chiffres')
    year_list = list(df.year.unique())[::-1]
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="student", ascending=False)

    deleg_list = list(df.deleg.unique())[::-1]
    selected_deleg = st.selectbox('Select a delegation', deleg_list)
    df_selected_deleg = df[df.deleg == selected_deleg]

    niveau_list = list(df.niveau.unique())[::-1]
    selected_niveau = st.selectbox('Select a cycle', niveau_list)
    df_selected_niveau = df[df.niveau== selected_niveau]

    color_theme_list = ['blues',  'greens',  'reds']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
#######################
# Plots

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


#######################
# Dashboard Main Panel
col = st.columns((4.5, 2.5), gap='medium')

with col[0]:
        st.markdown('#### Total élèves')
        heatmap = make_heatmap( df,'year',  'deleg', 'student', selected_color_theme)
        st.altair_chart(heatmap, use_container_width=True) 
        map=folium.Map(location=[35.69,10.06],zoom_start=8,scrolwheelzoom=False,tiles='CartoDB positron')
        choropleth=folium.Choropleth(geo_data='kai-deleg.json',data=df,columns=('ref_tn_cod','student'),key_on='feature.properties.id',highlight=True )       
        choropleth.geojson.add_to(map)
        df_indexed = df.set_index('ref_tn_cod')
        for feature in choropleth.geojson.data['features']:
            id_dele=feature["properties"]["id"]
            feature['properties']['effeleve']='التلاميذ :' + '{:,}'.format(df_indexed.loc[id_dele, 'student'][6]) if id_dele in list(df_indexed.index) else ''
        st.header(f'{selected_year}')
        choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_ar','effeleve'],labels=False))
        st_fol=st_folium(map,width=850,height=450)

with col[1]:
       st.markdown('#### Top delegation')
       st.header(f'{selected_year}')
       st.write(df_selected_year['densite'])
        
with st.expander('About', expanded=True):
            st.write('''
                - Data: [Bureau de planification et de statistiques à Kairouan](http://www.edunet.tn/index.php?id=523&lan=1).
                 ''')
