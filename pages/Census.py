import streamlit as st
import geopandas as gpd
import pandas as pd
import leafmap.foliumap as leafmap
import plotly.express as px
from millify import millify
from itertools import cycle
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from utils.cards import link_card
from utils.st_styles import load_bootstrap_stylesheet, load_css, reduce_top_padding
from utils.constants import attr_nationality, attr_sex, attr_ethnicity, attr_deaths, attr_age_group, attr_births
from utils.charts import pie

PARLIMEN_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_0_parlimen.geojson"
DUN_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_1_dun.geojson"
STATE_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/administrative_1_state.geojson"

@st.experimental_memo
def load_data():
    # geo census_parlimen_df
    parlimen_gdf = gpd.read_file(PARLIMEN_URL)
    dun_gdf = gpd.read_file(DUN_URL)    
    state_gdf = gpd.read_file(STATE_URL)
    # parlimen_geojson = parlimen_gdf.to_json()
    # dun_geojson = dun_gdf.to_json()
    # state_geojson = state_gdf.to_json()

    # census census_parlimen_df
    census_parlimen_df = pd.read_csv("./data/census_parlimen.csv")
    census_dun_df = pd.read_csv("./data/census_dun.csv")

    return parlimen_gdf, dun_gdf, state_gdf, census_parlimen_df, census_dun_df

def census():
    st.markdown("# **Census 2020** **:red[[WIP]]**")
    st.markdown("""
    This section is essentially a recreation of **[KAWASANKU](https://kawasanku.dosm.gov.my/)**, 
    a very nice open source visualisation project by
    the **Department of Statistics, Malaysia** built with **NextJS** and **Nivo** which is a plotting 
    library for **ReactJS**.

    Here, we will be using the fantastic **Leafmap** package by **Qisheng Wu** & of course **Plotly Express**
    which should allow for greater interactivity. **(and in Python!)**
    """)
    ################ census_parlimen_df Prep
    parlimen_gdf, dun_gdf, state_gdf, census_parlimen_df, census_dun_df  = load_data()

    # get the state names, parlimen and DUN will be generated based on the state selected
    state_list = sorted(list(parlimen_gdf.state.unique()))

    col1, col2 = st.columns([1,4])
    with col1:
        st.markdown("### 🧭 **Find my area**")
        st.markdown("----")

        selected_geo_filter = st.selectbox(
            "Select constituency level",
            ["DUN", "Parlimen", "State"],
            index=2
        )

        filter_flag = st.checkbox(label = "Apply filter")
        #### Selections

        if selected_geo_filter:
            selected_state = st.selectbox(
                "Select your state",
                state_list,
            )
            if selected_geo_filter:
                if selected_geo_filter == "DUN":
                    filtered_dun = dun_gdf[dun_gdf["state"]==selected_state]
                else:
                    filtered_parlimen = parlimen_gdf[parlimen_gdf["state"]==selected_state]

                if selected_geo_filter == "State":
                    selected_area = selected_state
                else:
                    selected_area = st.selectbox(
                        "Select area",
                        sorted(list(filtered_dun.dun.unique())) if selected_geo_filter == "DUN" else \
                            sorted(list(filtered_parlimen.parlimen.unique())) if selected_geo_filter == "Parlimen" else \
                                list()
                    )
    
    with col2:
        m = leafmap.Map(google_map="ROADMAP", locate_control=True)
        if not filter_flag:
            selected_area_df = dun_gdf if selected_geo_filter == "DUN" else parlimen_gdf \
                if selected_geo_filter == "Parlimen" else state_gdf
        else:
            selected_area_df = dun_gdf[dun_gdf["dun"] == selected_area] if selected_geo_filter == "DUN" else \
                parlimen_gdf[parlimen_gdf["parlimen"] == selected_area] if selected_geo_filter == "Parlimen" else \
                    state_gdf[state_gdf["state"] == selected_state]
    
        m.add_gdf(selected_area_df)
        m.to_streamlit()


    ##### Demographic Summary for Area
    colored_header(
        label = "Demographic Summary",
        description = f"""
        Charts describing the distribution of demographic data for 
        {selected_area if filter_flag else "Malaysia"}
        """,
        color_name = "red-70"
    )
    if filter_flag:
        pass
    else:
        c1, c2, c3, c4 = st.columns([2,2,2,2], gap = "medium")

        with c2:
            st.write("")
            st.write("")           
            fig = pie(census_parlimen_df, attributes=attr_nationality, names=["Citizen", "Non-Citizen"],
                title="Nationality")
            st.plotly_chart(fig, use_container_width=True)

        with c3:
            st.write("")
            st.write("")                       
            fig = pie(census_parlimen_df, attributes=attr_sex, names=["Male", "Female"],
                title="Sex")
            st.plotly_chart(fig, use_container_width=True)

        with c4:
            st.write("")
            st.write("")                      
            fig = pie(census_parlimen_df, attributes=attr_ethnicity, names=["Bumiputera", "Chinese", "Indian", "Other"],
                title="Ethnicity (%)", sum_flag=False)
            st.plotly_chart(fig, use_container_width=True)

        c5, c6, c7, c8 = st.columns([2,2,2,2], gap = "medium")

        with c6:
            st.write("")
            st.write("")                    
            fig = pie(census_parlimen_df, attributes=attr_age_group, names=["0-14", "15-64", ">=65"],
                title="Age Group", sum_flag=False)
            st.plotly_chart(fig, use_container_width=True)

        with c7:
            st.write("")
            st.write("")                  
            fig = pie(census_parlimen_df, attributes=attr_births, names=["Male", "Female"],
                title="Births")
            st.plotly_chart(fig, use_container_width=True)   

        with c8:
            st.write("")
            st.write("")
            fig = pie(census_parlimen_df, attributes=attr_deaths, names=["Male", "Female"],
                title="Deaths")
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








if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Census", page_icon="./public/malaysia.ico")
    load_bootstrap_stylesheet("./styles/bootstrap.min.css")
    # load_css("./styles/main.css")
    reduce_top_padding()

    with st.sidebar:
        st.markdown('<h1>pru-viz <span class="badge badge-secondary">Beta</span></h1>',
        unsafe_allow_html=True)
        st.markdown("### A simple web app to visualise GE15 and census data with maps!")       
        badge_columns = cycle(st.columns(3))
        with next(badge_columns): badge(type="github", name="hewliyang/pru-viz")
        with next(badge_columns): badge(type="twitter", name="hewliyang")

        st.markdown("## Data sources")
        st.markdown(link_card("https://github.com/Thevesh/analysis-election-msia", "Thevesh", "Election"), unsafe_allow_html=True)
        st.markdown(link_card("https://github.com/dosm-malaysia/census_parlimen_df-open", "Department of Statistics <br/> Malaysia", "Census"), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('## About')
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/hewliyang">@hewliyang</a></h6>',
            unsafe_allow_html=True,
        )
 
    census()