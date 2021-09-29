import os
import geopandas as gpd
import pandas as pd
from folium import GeoJson
from pathlib import Path

dirname = os.path.dirname(__file__)
covid_rates_path = os.path.join(dirname, "data/covid_rates.geojson")
testing_path = os.path.join(dirname, "data/testing_sites.geojson")
info_path = os.path.join(dirname, "info.md")

def load_covid_rates():
    covid_rates = gpd.read_file(covid_rates_path)

    return covid_rates

def load_testing_sites():
    testing_sites = gpd.read_file(testing_path)

    return testing_sites

def load_info_page():
    info_page = Path(info_path).read_text()
    
    return info_page

def epsg_format(original_dataset, epsg_code = 4326):
    """
    reformat geojson to epsg = 4326
    """
    dataset = original_dataset.to_crs(epsg_code)
    return dataset

def add_buffer(dataset, distance = 1000):
    buffer = dataset["geometry"].buffer(distance = distance)
    buffer = GeoJson(buffer.to_crs(epsg = 4326))
    return buffer