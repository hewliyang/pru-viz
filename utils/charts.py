import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_echarts import JsCode
from typing import List
from millify import millify
from streamlit_extras.metric_cards import style_metric_cards
from utils.constants import attr_voter_type
from utils.constants import (attr_nationality, attr_sex, attr_ethnicity, attr_religion, attr_married, attr_ethnicity_proportion, attr_age_group_proportion,
attr_age_group)

DEFAULT_HEIGHT = 250
DEFAULT_HOLE = 0.4

def pie(
    df: pd.DataFrame,
    attributes: List[str],
    names: List[str],
    title: str,
    sum_flag: bool = True,
    height: int = DEFAULT_HEIGHT,
    hole: float = DEFAULT_HOLE
) -> go.Figure:
    values = df[attributes].sum() if sum_flag else df[attributes].mean()
    fig = px.pie(values=values, names=names, title=title, height=height, hole =hole)
    fig.update_layout(
        legend=dict(
            y = 0.5
        ),
        margin=dict(
            l=38,
            r=0,
            t=22,
            b=10
        )
    )
    return fig

def pie_voter_type_echarts(
    df: pd.DataFrame,
) -> dict:
    values = df[attr_voter_type].sum()
    names = ["Regular", "Early - Army", "Early - Police", "Postal Overseas"]

    data = []
    count = 0

    for index, value in values.items():
        data.append({"value":value, "name":names[count]})
        count += 1
    
    option = {
        "title": {
            "text": "Voter Type",
            "left": "center"
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "top": '10%',
            "left": 'center'
        },
        "series": [
            {
            "name": 'Voter Type',
            "type": 'pie',
            "radius": ['30%', '50%'],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
            },
            "label": {
                "show": False,
                "position": 'center'
            },
            "emphasis": {
                "label": {
                "show": True,
                "fontSize": 20,
                "fontWeight": 'bold'
                }
            },
            "labelLine": {
                "show": False
            },
            "data": data 
            }
        ]
        }
    return option

def population_pyramid_plotly(
    long_df: pd.DataFrame,
    filter: str = ''
) -> go.Figure:

    if not filter: # national case
        n = long_df[["age_group", "sex", "count"]]
    else:
        n = long_df.query(f'parlimen == "{filter}"')[["age_group", "sex", "count"]]

    n = n.groupby(["age_group", "sex"]).sum().reset_index().fillna(0)

    y = n["age_group"].unique()
    x1 = n.query('sex == "male"').groupby("age_group").sum(numeric_only = False)["count"]
    x2 = n.query('sex == "female"').groupby("age_group").sum(numeric_only = False)["count"] * -1
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=y,
            x=x1,
            name="Male",
            orientation="h"
        )
    )

    fig.add_trace(
        go.Bar(
            y=y,
            x=x2,
            name="Female",
            orientation="h"
        )
    )

    if filter:
        title = f"Age Pyramid - {filter}"
    else:
        title = "Age Pyramid - GE15 Voters"

    fig.update_layout(
        title = title,
        title_font_size = 24,
        barmode = 'relative',
        bargap=0.075,
        bargroupgap=0.25,
        xaxis=dict(
            tickvals=[-2000000, -1000000, 0 , 1000000, 2000000],
            ticktext=['2M', '1M', '0', '1M', '2M'],
            title = "Size",
            title_font_size=14
        )
    )   

    return fig

def population_pyramid_echarts(
    long_df: pd.DataFrame,
    filter: str = ''
) -> dict:

    def get_data():
        if not filter: # national case
            n = long_df[["age_group", "sex", "count"]]
        else:
            n = long_df.query(f'parlimen == "{filter}"')[["age_group", "sex", "count"]]

        n = n.groupby(["age_group", "sex"]).sum().reset_index().fillna(0)

        y = n["age_group"].unique()
        x1 = n.query('sex == "male"').groupby("age_group").sum(numeric_only = False)["count"] * -1
        x2 = n.query('sex == "female"').groupby("age_group").sum(numeric_only = False)["count"] 

        if filter:
            title = filter
        else:
            title = "Malaysia"

        return {
            "y": y,
            "x1": x1,
            "x2": x2,
            "title": title  
        }
    
    data = get_data()

    option = {
        "tooltip": {
            "trigger": 'item',
            "axisPointer": {
                "type": 'shadow'
            },
            "formatter": JsCode('function test(e) {return `<b>${e.seriesName}</b>`+"<br/>"+e.name+": "+ Math.abs(e.value).toLocaleString("en-US")};').js_code,
        },
        "title": {
            "text": "Voter Age Pyramid",
            "subtext": f"{data['title']}",
            "left": "right",
        },
        
        "legend": {
            "itemWidth": 30,
            "itemHeight": 30,
            "data": [
                {
                    "name": 'Male',
                    "icon": 'path://m 146.41936,238.8034 c -5.21101,-1.43402 -7.51545,-6.79358 -6.6619,-11.76943 -0.0588,-45.10952 -0.11757,-90.21905 -0.17635,-135.328563 -5.3022,-1.61412 -3.06375,4.34199 -3.52464,7.58816 -0.0576,14.697923 -0.11511,29.395843 -0.17266,44.093773 -1.72718,6.61806 -12.15586,7.45944 -14.19605,0.88682 -1.42909,-4.98857 -0.22146,-10.60033 -0.62062,-15.83232 0.10773,-15.18837 -0.21551,-30.437173 0.16059,-45.587893 1.91842,-11.228608 12.80383,-20.22421 24.26927,-18.689786 10.60777,1.558898 0.0755,-3.65768 -0.79236,-8.596161 -4.23852,-8.688715 0.80002,-20.073014 9.72708,-23.421847 8.82591,-4.162774 20.30103,1.001172 23.52581,10.108188 2.28945,5.67583 1.4368,12.853955 -2.76118,17.571486 -5.15831,4.024926 -3.94241,5.010805 1.85043,4.362909 13.58742,-1.603119 25.03585,11.840701 23.9554,24.967141 -0.0691,18.213333 -0.13818,36.426673 -0.20726,54.640013 -1.5351,4.55905 -7.30638,6.71543 -11.30858,3.96578 -4.81473,-2.8888 -2.73019,-9.20279 -3.19227,-13.88869 -0.0523,-14.05586 -0.10469,-28.11173 -0.15704,-42.167583 -4.85271,-1.54237 -3.37467,3.24601 -3.51022,6.4208 V 231.02616 c -1.3114,6.77368 -9.29063,10.3384 -15.13544,6.61747 -6.62075,-3.7866 -4.17124,-12.04397 -4.62011,-18.29166 v -70.84935 c -4.85175,-1.54283 -3.39102,3.24111 -3.53094,6.42079 -0.0578,25.5528 -0.11553,51.1056 -0.17329,76.65839 -1.7387,5.48439 -7.13811,8.77105 -12.74767,7.2216 z',
                },
                {
                    "name": 'Female',
                    "icon": 'path://m 39.7122,238.0264 c -5.604205,-1.49359 -5.822698,-7.32898 -5.431108,-11.96235 -0.05932,-18.97406 -0.118632,-37.94813 -0.177948,-56.92219 -7.401109,0.0507 -14.802279,0.16954 -22.203547,0.1438 8.050221,-26.97466 15.83106,-54.03787 24.0791,-80.948455 -6.246873,-1.537447 -5.103818,6.332986 -7.12857,10.198179 -4.203419,12.783656 -7.28462,25.995046 -12.31951,38.467156 C 6.215777,147.43407 -0.93895389,129.58252 6.2279437,121.52707 11.709639,105.71684 15.006783,88.999576 22.521999,73.9779 25.487431,65.143259 38.425956,64.174487 43.879817,63.247984 35.242261,58.307767 32.195248,46.181151 37.843175,37.985287 c 5.35176,-7.73122 16.727442,-10.988636 24.757146,-5.16531 11.321083,6.562216 10.452089,25.024381 -1.135269,30.670395 9.830628,-0.28155 20.086569,3.623662 24.845207,12.765524 3.87086,7.45858 5.12438,16.169298 8.137928,24.037484 2.906124,10.26421 6.922833,20.35157 9.297803,30.70045 1.06345,4.17564 -1.66552,9.02385 -6.181687,9.2796 -7.686885,1.11419 -8.783192,-8.80355 -10.70406,-14.18732 -3.87502,-12.5653 -7.681429,-25.15172 -11.575988,-37.711005 -8.798872,-0.113812 1.949333,13.898795 1.781574,19.941085 6.048408,20.20812 12.13493,40.40517 18.089502,60.64114 -7.392371,0.35953 -14.803078,0.14681 -22.203496,0.20388 -0.06597,21.22546 -0.131933,42.45093 -0.1979,63.67639 -2.103142,7.13406 -13.415648,7.74398 -15.969932,0.84281 -1.418088,-4.77754 -0.245017,-10.18282 -0.655178,-15.20454 l -0.156843,-49.31466 c -4.44248,-1.05339 -5.844521,0.93365 -4.913879,5.25338 -0.162881,19.18788 0.325808,38.44483 -0.244801,57.58947 -0.334387,5.03435 -6.719798,7.8699 -11.101102,6.02234 z',
                }
            ]
        },
        "grid": {
            "left": '2%',
            "right": '5%',
            "bottom": '5%',
            "containLabel": True
        },
        "xAxis": [
            {
                "type": 'value',
                "show": True,
                "axisLabel": {
                "formatter": JsCode('function (params) {return Math.abs(params);}').js_code
                }
            }
        ],
        "yAxis": [
            {
                "type": 'category',
                "axisTick": {
                    "show": False
                },
                "nameLocation": "middle",
                "nameTextStyle": {
                    "fontStyle":'oblique',
                    "fontWeight":'bold'
                    },
                "data": list(data["y"])
            }
        ],
        "series": [
            {
                "name": 'Female',
                "type": 'bar',
                "color": '#ff007f',
                "stack": 'Total',
                "label": {
                    "show": False,
                    "position": 'right'
                },
                "emphasis": {
                    "focus": 'none'
                },
                "data": list(data["x2"])
            },
            {
                "name": 'Male',
                "type": 'bar',
                "color": '#0000ff',
                "stack": 'Total',
                "label": {
                    "show": False,
                    "position": 'left',
                    "formatter": JsCode('function (params) {return Math.abs(params.value);}').js_code
                },
                "emphasis": {
                    "focus": 'none'
                },
                "data": list(data["x1"])
            }
        ]
    }

    return option

def parlimen_voters_wide_to_long(
    wide_df: pd.DataFrame
) -> pd.DataFrame:
    wide_df = wide_df \
        .drop(columns={"votertype_regular", "votertype_early_army", "votertype_early_police", "votertype_postal_overseas", "total_ge14", "total", "dun"}) \
        .groupby(["state", "parlimen"]) \
        .sum() \
        .reset_index() 
    long_df = pd.melt(
        frame = wide_df,
        id_vars = ["state", "parlimen"],
        var_name = "age_group",
        value_name = "count"
    )
    long_df[["sex", "age_group"]] = long_df["age_group"].str.split("_", n=1, expand=True)
    return long_df

def pie_array(
    census_parlimen_df: pd.DataFrame = None,
    census_dun_df: pd.DataFrame = None,
    census_district_df: pd.DataFrame = None
):
    c1, c2, c3, c4 = st.columns([2.5,3,3,3], gap = "medium")

    if census_parlimen_df is not None:
        target_df = census_parlimen_df
    elif census_dun_df is not None:
        target_df = census_dun_df
    else:
        target_df = census_district_df

    with c2:
        st.write("")
        st.write("")     
        st.write("")
        st.write("")                 
        fig = pie(target_df, attributes=attr_nationality, names=["Citizen", "Non-Citizen"],
            title="Nationality")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.write("")
        st.write("") 
        st.write("")
        st.write("")                                  
        fig = pie(target_df, attributes=attr_sex, names=["Male", "Female"],
            title="Sex")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.write("")
        st.write("")    
        st.write("")
        st.write("")                              
        fig = pie(target_df, attributes=attr_ethnicity_proportion, names=["Bumiputera", "Chinese", "Indian", "Other"],
            title="Ethnicity")
        st.plotly_chart(fig, use_container_width=True)

    c5, c6, c7, c8 = st.columns([2.5,3,3,3], gap = "medium")

    with c6:
        st.write("")
        st.write("")                    
        fig = pie(target_df, attributes=attr_age_group_proportion, names=["0-14", "15-64", ">=65"],
            title="Age Group")
        st.plotly_chart(fig, use_container_width=True)

    # metric stuff
    
    with st.container():
        with c1:
            # get metrics

            total_population = target_df["population_total"].sum()
            income_avg = target_df["income_avg"].mean()
            income_median = target_df["income_median"].mean()
            household_size = target_df["household_size_avg"].mean()
            births = target_df["live_births"].sum()
            deaths = target_df["deaths"].sum()

            # display metrics

            st.metric(label="Total population" ,value = millify(total_population, precision=2))
            st.metric(label="Average Household Income" ,value = millify(income_avg, precision=3))
            st.metric(label="Median Household Income" ,value = millify(income_median, precision=3))
        with c5:
            st.metric(label="Average Household Size" ,value = millify(household_size, precision=2))
            st.metric(label="Births" ,value = millify(births))
            st.metric(label="Deaths" ,value = millify(deaths))
        
        style_metric_cards()

def pie_array_ns(
    census_parlimen_df: pd.DataFrame,
    census_district_df: pd.DataFrame 
):
    """
    A copy of pie_array() but suited for national & state level statistics
    """
    c1, c2, c3, c4 = st.columns([2.5,3,3,3], gap = "medium")
    with c2:
        st.write("")
        st.write("")     
        st.write("")
        st.write("")                 
        fig = pie(census_parlimen_df, attributes=attr_nationality, names=["Citizen", "Non-Citizen"],
            title="Nationality")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.write("")
        st.write("") 
        st.write("")
        st.write("")                                  
        fig = pie(census_parlimen_df, attributes=attr_sex, names=["Male", "Female"],
            title="Sex")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.write("")
        st.write("")    
        st.write("")
        st.write("")                              
        fig = pie(census_district_df, attributes=attr_ethnicity, names=["Bumiputera", "Chinese", "Indian", "Other"],
            title="Ethnicity")
        st.plotly_chart(fig, use_container_width=True)

    c5, c6, c7, c8 = st.columns([2.5,3,3,3], gap = "medium")

    with c6:
        st.write("")
        st.write("")                    
        fig = pie(census_district_df, attributes=attr_age_group, names=["0-14", "15-64", ">=65"],
            title="Age Group")
        st.plotly_chart(fig, use_container_width=True)

    with c7:
        st.write("")
        st.write("")                  
        fig = pie(census_district_df, attributes=attr_married, names=["Never Married", "Married", "Widowed", "Seperated", "Unknown"],
            title="Maritial Status")
        st.plotly_chart(fig, use_container_width=True)   

    with c8:
        st.write("")
        st.write("")
        fig = pie(census_district_df, attributes=attr_religion, names=["Muslim", "Christian", "Buddhist", "Hindu", "Other", "Atheist", "Unknown"],
            title="Religion")
        st.plotly_chart(fig, use_container_width=True)


    # metric stuff
    
    with st.container():
        with c1:
            # get metrics

            total_population = census_parlimen_df["population_total"].sum()
            income_avg = census_parlimen_df["income_avg"].mean()
            income_median = census_parlimen_df["income_median"].mean()
            household_size = census_parlimen_df["household_size_avg"].mean()
            births = census_parlimen_df["live_births"].sum()
            deaths = census_parlimen_df["deaths"].sum()

            # display metrics

            st.metric(label="Total population" ,value = millify(total_population, precision=2))
            st.metric(label="Average Household Income" ,value = millify(income_avg, precision=3))
            st.metric(label="Median Household Income" ,value = millify(income_median, precision=3))
        with c5:
            st.metric(label="Average Household Size" ,value = millify(household_size, precision=2))
            st.metric(label="Births" ,value = millify(births))
            st.metric(label="Deaths" ,value = millify(deaths))
        
        style_metric_cards()