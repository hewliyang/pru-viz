import streamlit as st
import geopandas as gpd
import pandas as pd
import leafmap.foliumap as leafmap
from streamlit_extras.colored_header import colored_header
from utils.st_styles import init_styles
from utils.charts import pie_array, pie_array_ns

PARLIMEN_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_0_parlimen.geojson"
DUN_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_1_dun.geojson"
STATE_URL = "https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/administrative_1_state.geojson"

@st.experimental_memo
def load_data():
    # geo census_parlimen_df
    parlimen_gdf = gpd.read_file(PARLIMEN_URL)
    dun_gdf = gpd.read_file(DUN_URL)    
    state_gdf = gpd.read_file(STATE_URL)

    census_parlimen_df = pd.read_csv("./data/census_parlimen.csv")
    census_dun_df = pd.read_csv("./data/census_dun.csv")
    census_district_df = pd.read_csv("./data/census_district.csv").query('year == 2020')

    return parlimen_gdf, dun_gdf, state_gdf, census_parlimen_df, census_dun_df, census_district_df

    
def census():
    st.markdown("# **Census 2020**")
    st.markdown("""
    This section is essentially a recreation of **[KAWASANKU](https://kawasanku.dosm.gov.my/)**, 
    a very nice open source visualisation project by
    the **Department of Statistics, Malaysia** built with **NextJS** and **Nivo** which is a plotting 
    library for **ReactJS**.

    Here, we will be using the fantastic **Leafmap** package by **Qisheng Wu** & of course **Plotly Express**
    which should allow for greater interactivity. **(and in Python!)**
    """)
    ################ census_parlimen_df Prep
    parlimen_gdf, dun_gdf, state_gdf, census_parlimen_df, census_dun_df, census_district_df  = load_data()

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
        
        # case for state only selection
        if selected_geo_filter == "State": # state case

            census_parlimen_df = census_parlimen_df.query(f'state == "{selected_state}"')
            census_district_df = census_district_df.query(f'state == "{selected_state}"')

            pie_array_ns(census_district_df=census_district_df, census_parlimen_df=census_parlimen_df)

        elif selected_geo_filter == "Parlimen": # parlimen case

            census_parlimen_df = census_parlimen_df.query(f'parlimen == "{selected_area}"')
            pie_array(census_parlimen_df=census_parlimen_df)

        else: # DUN case

            census_dun_df = census_dun_df.query(f'dun == "{selected_area}"')
            census_dun_df.live_births = census_dun_df["live_births"].str.replace(',','')
            pie_array(census_dun_df=census_dun_df)


    else: # national case
       
       pie_array_ns(census_district_df=census_district_df, census_parlimen_df=census_parlimen_df)

if __name__ == "__main__":
    init_styles()
    census()