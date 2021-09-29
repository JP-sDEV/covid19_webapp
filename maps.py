from folium.map import Tooltip
from folium.plugins.marker_cluster import MarkerCluster
import geopandas as gpd
import streamlit as st
from streamlit_folium import folium_static 
import folium
from folium import Marker, GeoJson, Choropleth, Marker, Popup
from helper_functions import add_buffer

def render_map(map):
    return folium_static(map)

def create_choropleth(df, geo_df, columns, key_on, color, legend_name, legend_alias = ['Neighborhood: ', 'COVID Rate (per 100,000 people): ']):

    choropleth_style = {
        'fillColor': '#000000', 
        'color': '#000000', 
        'width': 1,
        "opacity": 0.01
    }

    choropleth_map = Choropleth(
        geo_data = geo_df,
        data = df,
        columns = columns,
        key_on = key_on,
        fill_color = color,
        fill_opacity = 0.7,
        legend_name = legend_name,
        highlight = True
    )
    folium.features.GeoJson(
        data = df,
        tooltip = folium.features.GeoJsonTooltip(
            fields = columns,
            aliases = legend_alias),
            style_function=lambda x: choropleth_style
            ).add_to(choropleth_map)

    return choropleth_map

def create_cluster(df, buffer_distance = None):
    mc = MarkerCluster()
    for idx, row in df.iterrows():
        info_list = [
                    f"Location Name: {row['location_name']}", 
                    f"Address: {row['address']}, {row['postal_code']}"
                    ]
        new_line_str = '\n'

        marker = Marker(
            [row["latitude"], 
            row["longitude"]], 
            popup = Popup(f"{new_line_str}{new_line_str.join(info_list)}", 
            max_width = len(info_list[0] * 5)
                )
            )
        mc.add_child(marker)

    if buffer_distance:
        buffer = add_buffer(df, distance = buffer_distance)
        buffer.add_to(mc)
    return mc

