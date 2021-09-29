import streamlit as st
import folium
from helper_functions import load_covid_rates, load_testing_sites, load_info_page, epsg_format
from maps import create_choropleth, create_cluster, render_map
from streamlit_styling import page_config, responsive_style

# initial states
page_config()

datasets = {
    "testing_sites": load_testing_sites(),
    "covid_rates": load_covid_rates()
}

main_map = folium.Map(
    location = [43.6532, -79.3832], # Toronto Coordinates
    tiles = 'openstreetmap',
    zoom_start = 11
)

def toggle_choropleth(original_dataset, color = "OrRd"):
    """
    choropleth map only applies to the covid rates
    """
    dataset = epsg_format(original_dataset)
    choropleth_map = create_choropleth(
        df = dataset, 
        geo_df = dataset,
        columns = ["Neighbourhood_Name", "Rate_per_100,000_people"],
        key_on = "feature.properties.Neighbourhood_Name",
        color = color,
        legend_name = "COVID-19 Rates per 100,000 people"
    )

    return choropleth_map.add_to(main_map)
    
# sidebar components
def toggle_cluster_map(dataset, buffer_distance = None):
    cluster_map = create_cluster(
        df = dataset, 
        buffer_distance = buffer_distance
    )
    return cluster_map.add_to(main_map)

st.sidebar.header("📍 Toggle datasets")

covid_rates_toggle = st.sidebar.checkbox("🦠 Covid Rates", value=True)
if covid_rates_toggle:
    choropleth_color =  st.sidebar.radio(
        "Choropleth Map Color (Covid Rates)",
        ("Orange-Red", "Blue-Purple", "Purple-Red", "Yellow-Brown"),
        index =  0
    )
    
    color_codes = {
        "Orange-Red": "OrRd",
        "Blue-Purple": "BuPu",
        "Purple-Red": "PuRd",
        "Yellow-Brown": "YlOrBr"
    }

    toggle_choropleth(
        datasets["covid_rates"],
        color = color_codes[choropleth_color]
    )

testing_sites_toggle = st.sidebar.checkbox("💉 Testing Sites")
if testing_sites_toggle:
    st.sidebar.radio(
        "Map Type (Testing Sites)",
        ("Markcluster",)
    )
    buffer_slider = st.sidebar.slider("Testing Location Radius (meters)", min_value = 0, max_value = 5000, step = 100, value = 1000)
    toggle_cluster_map(datasets["testing_sites"], buffer_slider)

# page styling
st.markdown(responsive_style(), unsafe_allow_html=True)
st.header("Toronto COVID-19 Visualizer")
render_map(main_map)
st.markdown(load_info_page(), unsafe_allow_html = True)