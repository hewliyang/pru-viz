import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from streamlit_echarts import JsCode, Map
from typing import Tuple
from .constants import alias_to_id_color, id_to_alias_color, vmap_jscode, tooltip_result_jscode, tooltip_cont_jscode

def map_cont_plotly(
    result_df:pd.DataFrame, 
    geojson:dict, 
    target:str) -> go.Figure:
    """ 
    Generates a Plotly choropleth based on a continuous field in 
    the `result` DataFrame
    """
    fig = px.choropleth(result_df, geojson=geojson, color=target,
                        locations="parlimen", featureidkey="properties.parlimen", height=1000
                    )
    # show only geojson boundaries                    
    fig.update_geos(fitbounds="locations", visible=False)
    # shift legend position
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="Size of Voter Base",
            len=0.75,
            orientation="h",
            y=0.85
        ))
    return fig

def map_cont_echarts(
    result_df:pd.DataFrame,
    geojson:dict,
    target:str,
    title:str,
    log: bool = False,
    normalise: bool = False,
    normalise_on: str = None
    ) -> Tuple[Map, dict]:
    """
    @geojson: Need to use a geojson with the key property as 'name' due as per Echarts API

    Returns the Map object and Options dictionary 
    required to plot the Echart
    """

    # prepare data

    prep = result_df.copy()

    # check if normalisation is to be applied (divide by "pengundi_jumlah")
    new_target = None
    if normalise:
        new_target = target + "_%"
        prep[new_target] = prep[target]/(prep["pengundi_jumlah"]-prep["pengundi_tidak_hadir"]) * 100 \
            if not normalise_on else prep[target]/prep[normalise_on] * 100
    else:
        new_target = target

    # check if log transform is to be applied
    if log:
        prep["logged"] = np.log(prep[new_target])
        new_target = "logged"

    prep = prep[["parlimen", new_target]]
    prep.rename(columns= {new_target:"value","parlimen":"name"}, inplace=True)
    series_data = prep.to_dict(orient="records")

    formatter = JsCode(tooltip_cont_jscode).js_code

    map = Map(map_name="Malaysia",geo_json=geojson)

    options = {
        "title": {
            "text": title,
            "subtext": "Data from Thevesh & DOSM",
            "sublink": "https://github.com/dosm-malaysia/data-open",
            "left": "right",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "min": float(prep["value"].min()),
            "max": float(prep["value"].max()),
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["Max", "Min"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "series": [
            {
                "name": target,
                "type": "map",
                "roam": True,
                "map": "Malaysia",
                "emphasis": {"label": {"show": True}},
                "data": series_data
            }
        ],
    }

    return map, options

# to improve
def map_cont_folium(
    result_df:pd.DataFrame,
    geo_df:gpd.GeoDataFrame,
    target:str,
    ) -> Tuple[folium.folium.Map, folium.folium.Map]:
    """
    Returns a folium Map with a choropleth layer that is
    split into east and west as we have an actual map as a base layer 
    """
    merged = pd.merge(result_df, geo_df, on="parlimen")
    east_only=merged.loc[merged.code_state.isin([12,13,15])]
    west_only=merged.loc[~merged.code_state.isin([12,13,15])]
    east_gdf=gpd.GeoDataFrame(east_only)
    west_gdf=gpd.GeoDataFrame(west_only)

    m_west = west_gdf.explore(column=target, tiles="CartoDB positron")
    m_east = east_gdf.explore(column=target, tiles="CartoDB positron")

    return m_west, m_east

def map_results_echarts(
    candidate_df:pd.DataFrame,
    geojson:dict,
    ) -> Tuple[Map, dict]:
    """
    @geojson: Need to use a geojson with the key property as 'name' due as per Echarts API

    Returns the Map object and Options dictionary 
    required to plot the Echart for GE results
    This is a discrete plot as there is a 1-1 mapping between winning party and
    the associated color
    """

    # prepare data

    # find winners
    winners = candidate_df[candidate_df.result == 1][["parlimen", "party_short"]]
    # we exclude parties that won < 3 seats
    include = {"BN", "PH", "PN", "GPS", "GRS", "PAS", "DAP", "WARISAN"}
    replace_with = "OTHER"

    winners_mini = winners.copy()
    winners_mini["party_short"] = winners_mini["party_short"].where(winners_mini["party_short"].isin(include), replace_with)

    winners_mini = winners_mini.assign(
    party_id = lambda df_: df_["party_short"].map(lambda x: alias_to_id_color[x]["id"]),
    color = lambda df_: df_["party_short"].map(lambda x: alias_to_id_color[x]["color"])
    )

    # get series_data
    # for map plotting [{} , ..., {parlimen: party_id}]
    for_map = winners_mini.copy()[["parlimen", "party_id"]]
    for_map.rename(columns={"party_id":"value", "parlimen":"name"}, inplace=True)
    series_data = for_map.to_dict(orient="records")

    # for visualMap - categories
    categories = [int(x) for x in for_map.value.unique()]
    # for visualMap - color
    color = [id_to_alias_color[id]["color"] for id in categories]

    # legend formatter - map id to alias
    # unfortunately some hardcoding + JS one liners is required here. sadge
    vmap_formatter = JsCode(str(vmap_jscode)).js_code

    # prepare map
    
    tooltip_formatter = JsCode(tooltip_result_jscode).js_code

    map = Map(map_name="Malaysia",geo_json=geojson)

    options = {
        "title": {
            "text": "GE15 Results by Parliament (2022)",
            "subtext": "Data from Thevesh & DOSM",
            "sublink": "https://github.com/dosm-malaysia/data-open",
            "left": "right",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": tooltip_formatter,
        },
        "visualMap": {
            "left": "right",
            "right": 0,
            "type": "piecewise",
            "categories": categories,
            "inRange": {
                "color": color 
            },
            "formatter": vmap_formatter,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "series": [
            {
                "name": "Parliamentary Results",
                "type": "map",
                "roam": True,
                "map": "Malaysia",
                "emphasis": {"label": {"show": True}},
                "data": series_data
            }
        ],
    }

    return map, options
