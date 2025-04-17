# Choropleth principale
choropleth = folium.Choropleth(
    geo_data='kai-deleg.json',
    data=df,
    columns=('ref_tn_cod', 'student'),
    key_on='feature.properties.id',
    legend_name=f"Nombre d'élèves ({selected_year})",
    fill_color=folium_palette,
    fill_opacity=0.7,
    line_opacity=0.2,
    highlight=True
)
choropleth.geojson.add_to(map)

# Ajout des infos tooltip
student_dict = dict(zip(df_selected_year['ref_tn_cod'], df_selected_year['student']))
df_indexed = df.set_index('ref_tn_cod')

for feature in choropleth.geojson.data['features']:
    id_dele = feature["properties"]["id"]
    feature['properties']['student'] = student_dict.get(id_dele, 0)

# Ajouter les info-bulles
choropleth.geojson.add_child(folium.GeoJsonTooltip(['del_fr', 'student'], labels=False))

# 🎯 Highlight de la délégation choisie
with open("kai-deleg.json", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    if feature["properties"]["del_fr"] == selected_deleg:
        folium.GeoJson(
            data=feature,
            style_function=lambda x: {
                'fillColor': 'orange',
                'color': 'red',
                'weight': 3,
                'fillOpacity': 0.9
            },
            tooltip=folium.GeoJsonTooltip(fields=["del_fr", "del_ar"])
        ).add_to(map)

# Affichage de la carte
st.subheader(f'📍 Répartition des élèves par délégation - Année {selected_year}')
st_folium(map, width=850, height=450)
