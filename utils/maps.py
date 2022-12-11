import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from streamlit_echarts import JsCode, Map
from typing import Tuple
from .constants import alias_to_id_color, id_to_alias_color

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
    log_flag: bool
    ) -> Tuple[Map, dict]:
    """
    @geojson: Need to use a geojson with the key property as 'name' due as per Echarts API

    Returns the Map object and Options dictionary 
    required to plot the Echart
    """

    # prepare data

    prep = result_df.copy()
    prep = prep[["parlimen", target]]

    # check if log transform is to be applied
    if log_flag:
        prep["logged"] = np.log(prep[target])
        target = "logged"

    prep.rename(columns= {target:"value","parlimen":"name"}, inplace=True)
    series_data = prep.to_dict(orient="records")

    formatter = JsCode(
    "function (params) {"
    + "var value = (params.value + '').split('.');"
    + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
    + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
    ).js_code

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
                "name": "Total Voters",
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
    vmap_formatter = JsCode(
        str('function test(a){return({0:{alias:"OTHER",color:"#FFFFFF"},1:{alias:"BN",color:"#031A93"},2:{alias:"PAS",color:"#6CB332"},3:{alias:"DAP",color:"#E30911"},4:{alias:"BERJASA",color:"#005121"},5:{alias:"PBB",color:"ADADAD"},6:{alias:"KIMMA",color:"#DE8801"},7:{alias:"PRM",color:"FE8591"},8:{alias:"PBS",color:"#763B37"},9:{alias:"UPKO",color:"#2A0E72"},10:{alias:"PPM",color:"CC9900"},20:{alias:"BEBAS",color:"#993300"},12:{alias:"GERAKAN",color:"#FE2514"},13:{alias:"LDP",color:"#AB3D1A"},14:{alias:"PMS",color:"#FBFD0B"},15:{alias:"AMIPF",color:"#E30300"},16:{alias:"MAP",color:"#F6EB19"},17:{alias:"UMNO",color:"#A03232"},18:{alias:"MCA",color:"#07257F"},19:{alias:"MIC",color:"#00A55E"},11:{alias:"SUPP",color:"#FFFF00"},21:{alias:"PBRS",color:"#6666FF"},22:{alias:"PDP",color:"#0000FD"},23:{alias:"PKR",color:"#04A0D1"},24:{alias:"PRS",color:"#186D43"},25:{alias:"PEJUANG",color:"#09618A"},26:{alias:"PFP",color:"#E45035"},27:{alias:"PN",color:"#043253"},28:{alias:"GAGASAN",color:"#e9d720"},29:{alias:"ASPIRASI",color:"#BD354D"},30:{alias:"PBDS",color:"#0B46C8"},31:{alias:"PH",color:"#D7292F"},32:{alias:"GPS",color:"#1F2C45"},33:{alias:"USNO",color:"#1A740A"},34:{alias:"PUTRA",color:"#FEFE00"},35:{alias:"PSB",color:"#A13C33"},36:{alias:"MUDA",color:"#000000"},37:{alias:"IMAN",color:"#EC1F26"},38:{alias:"SEDAR",color:"#C3B62B"},39:{alias:"M.M.S.P.",color:"#EF8812"},40:{alias:"BERSAMA",color:"#FF66FF"},41:{alias:"PCM",color:"#F4E50E"},42:{alias:"PBM",color:"#323467"},43:{alias:"PSM",color:"#C0110D"},44:{alias:"MCC",color:"#C92725"},45:{alias:"AMANAH",color:"#F79220"},46:{alias:"PPRS",color:"#0000FF"},47:{alias:"ANAKNEGERI",color:"#F6E13A"},48:{alias:"PEACE",color:"#FEF200"},49:{alias:"TERAS",color:"#310051"},50:{alias:"PKS",color:"#3567B2"},51:{alias:"SAPU",color:"#FC771F"},52:{alias:"PAP",color:"#08334C"},53:{alias:"PCS",color:"#DE1E14"},54:{alias:"WARISAN",color:"#5BC5F0"},55:{alias:"BERSATU",color:"#E30007"},56:{alias:"STARSABAH",color:"#0095DB"},57:{alias:"HR",color:"#6F92BF"},58:{alias:"PBK",color:"#672D34"},59:{alias:"IKATAN",color:"#F6E816"},60:{alias:"MU",color:"#ED1D24"},61:{alias:"PERPADUAN",color:"#01AC5C"},62:{alias:"SPP",color:"#c7e011"},63:{alias:"GRS",color:"#6285a8"},64:{alias:"KDM",color:"#EB7389"},65:{alias:"PUR",color:"#ff030b"},66:{alias:"PRIM",color:"#fff"}})[a].alias}')
    ).js_code

    # prepare map
    
    tooltip_formatter = JsCode(
    "function (params) {"
    + "var value = (params.value + '').split('.');"
    + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
    + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
    ).js_code

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
