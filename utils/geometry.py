import pandas as pd
import geopandas as gpd
import streamlit as st
import warnings
from shapely.errors import ShapelyDeprecationWarning
from cartogram_geopandas import make_cartogram

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


@st.cache_data
def morph_geos(_gdf: gpd.GeoDataFrame, result_df: pd.DataFrame, n: int) -> dict:
    """
    Runs the cartogram algorithm for n iterations
    Returns: geojson with the morphed geometries
    Extracted from https://github.com/mthh/cartogram_geopandas
    Copyright (C) 2015 mthh
    Copyright (C) 2013 Carson Farmer
    """
    result_df = result_df.rename(columns={"parlimen": "name"})
    join = pd.merge(result_df, _gdf, on="name")
    join_geo = gpd.GeoDataFrame(join)
    transformed_geo = make_cartogram(join_geo, "pengundi_jumlah", n, inplace=False)
    transformed_geo = transformed_geo.rename(columns={"state_x": "state"})
    return transformed_geo.to_json()
