import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_echarts import JsCode
from typing import List
from millify import millify
from streamlit_extras.metric_cards import style_metric_cards
from utils.constants import attr_voter_type
from utils.constants import (attr_nationality, attr_sex, attr_ethnicity, attr_religion, attr_married, attr_ethnicity_proportion, attr_age_group_proportion,
attr_age_group, census_agg_map)

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
    fig.update_traces(textposition='inside')
    fig.update_layout(
        legend=dict(
            y = 0.5
        ),
        margin=dict(
            l=38,
            r=0,
            t=22,
            b=10
        ),
        uniformtext_mode='hide',
        uniformtext_minsize=12
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
            "formatter": JsCode('function (e) {return `<b>${e.seriesName}</b>`+"<br/>"+e.name+": "+ Math.abs(e.value).toLocaleString("en-US")};').js_code,
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
                    "icon": "path://M12 2a2 2 0 0 1 2 2a2 2 0 0 1-2 2a2 2 0 0 1-2-2a2 2 0 0 1 2-2m-1.5 5h3a2 2 0 0 1 2 2v5.5H14V22h-4v-7.5H8.5V9a2 2 0 0 1 2-2Z",
                },
                {
                    "name": 'Female',
                    "icon": "path://M12 2a2 2 0 0 1 2 2a2 2 0 0 1-2 2a2 2 0 0 1-2-2a2 2 0 0 1 2-2m-1.5 20v-6h-3l2.59-7.59C10.34 7.59 11.1 7 12 7c.9 0 1.66.59 1.91 1.41L16.5 16h-3v6h-3Z",
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

def make_altair_bar(df: pd.DataFrame,
    metric: str,
    to_highlight:list=[], 
    mean=False):

    def string_builder(to_highlight:list) -> str:
        query = ""
        sep = "||"

        # do the first one manually
        copy = [x for x in to_highlight]
        first_state = copy.pop(0)
        query += f"datum.state == '{first_state}'"

        for state in to_highlight:
            base = f"datum.state == '{state}'"
            query += sep + base
        return query
    
    # check if should agg by mean instead

    if census_agg_map[metric] == "mean":
        mean=True

    c = alt.Chart(
            df, 
            title=f"{metric}"
        ).mark_bar(
            cornerRadius=3
        ).encode(
            y=alt.Y('state', sort='-x', title=""),
            x=alt.X(f'sum({metric})' if not mean else f'mean({metric})', title=""),
        color=alt.condition(
            string_builder(to_highlight) if len(to_highlight) > 0 else "datum.state == ''",
            alt.value("red"),
            alt.value("lightblue")
            )
        )

    return c