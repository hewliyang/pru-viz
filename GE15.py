import streamlit as st
import pandas as pd
import geopandas as gpd
import re
import json
from streamlit_echarts import st_echarts
from utils.maps import map_cont_echarts, map_results_echarts
from utils.cards import result_card, paginator, total_voter_card
from utils.geometry import morph_geos
from utils.st_styles import init_styles
from streamlit_extras.colored_header import colored_header
from utils.charts import (
    parlimen_voters_wide_to_long,
    population_pyramid_echarts,
    pie_voter_type_echarts,
)


@st.cache_data
def load_data():
    results = pd.read_csv("./data/results_parlimen_ge15.csv")
    geojson = json.load(open("./geo/parlimen_adjusted.geojson"))
    candidates = pd.read_csv("./data/candidates_ge15.csv")
    gdf = gpd.read_file("./geo/parlimen_adjusted.geojson")
    census = pd.read_csv("./data/census_parlimen.csv")
    voters = pd.read_csv("./data/voters_ge15.csv")

    # split party names into the full name ; alias

    # regex helper
    def split(party: str):
        r = re.split(r"\((.*?)\)", party)
        return r[0], r[1]

    candidates = candidates.assign(
        party_short=lambda df_: df_["party"].map(lambda x: split(x)[1]),
        party=lambda df_: df_["party"].map(lambda x: split(x)[0]),
    )

    return results, geojson, candidates, gdf, census, voters


def main():
    st.markdown("# **GE15 Maps**")

    # read in data
    results, geojson, candidates, gdf, census, voters = load_data()

    options = [
        "Results",
        "Registered Voters",
        "Turnout",
        "Undi Rosak",
        "Majoriti",
        "Undi Tolak",
        "Absentees",
    ]
    index = 0

    selected_map = st.selectbox(label="Select metric:", options=options, index=index)
    # display log transform option if selected ~results
    if selected_map != "Results":
        log = st.checkbox("Log Transform")
    else:
        c1, c2, _, _, _ = st.columns(5)
        with c1:
            morph = st.checkbox("Adjust for consituency size [make cartogram]")
        with c2:
            n = st.number_input(
                label="Number of iterations", min_value=1, max_value=100
            )

    col1, col2 = st.columns((3, 1))
    with col1:
        colored_header(
            label="Interactive Map",
            description="Click on the legends, they are interactive!. Click on a region to display the corresponding breakdown!",
            color_name="light-blue-70",
        )
        if selected_map == options[0]:
            map, options = (
                map_results_echarts(
                    candidate_df=candidates, geojson=morph_geos(gdf, results, n)
                )
                if morph
                else map_results_echarts(candidate_df=candidates, geojson=geojson)
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key="result",
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[1]:
            target = "pengundi_jumlah"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Registered Voters (2022)",
                log=log,
                discrete=True,
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[2]:
            target = "peratus_keluar"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Voter Turnout (%) (2022)",
                log=log,
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[3]:
            target = "undi_rosak"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Undi Rosak (%) (2022)",
                log=log,
                normalise=True,
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[4]:
            target = "majoriti"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Majoriti (%) (2022)",
                log=log,
                normalise=True,
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[5]:
            target = "undi_tolak"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Undi Tolak (%) (2022)",
                log=log,
                normalise=True,
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )
        elif selected_map == options[6]:
            target = "pengundi_tidak_hadir"
            map, options = map_cont_echarts(
                result_df=results,
                geojson=geojson,
                target=target,
                title="GE15 Absentees (%) (2022)",
                log=log,
                normalise=True,
                normalise_on="pengundi_jumlah",
            )
            clicked_state = st_echarts(
                options,
                map=map,
                height=850,
                key=target,
                events={"click": "function(params) {return params.name}"},
            )

    if clicked_state is None:
        with col2:
            colored_header(
                label="Results",
                description="Personal information in the order: age, sex, race",
                color_name="violet-70",
            )
            st.info("Click on a region to display the results")
    else:
        filtered_df = results[results.parlimen == clicked_state]
        filtered_candidates = candidates[
            candidates.parlimen == clicked_state
        ].sort_values(by="votes", ascending=False)

        # results to be conditionally rendered
        with col2:
            colored_header(
                label="Results",
                description="Personal information in the order: age, sex, race",
                color_name="violet-70",
            )
            # st.dataframe(filtered_df)
            # st.dataframe(filtered_candidates)

            # display state + parlimen
            st.markdown(
                f"""##### **{filtered_df["state"].iloc[0]} - {filtered_df["parlimen"].iloc[0]}**"""
            )

            # create cards
            cards = []
            for _, row in filtered_candidates.iterrows():
                card = result_card(
                    candidate_name=row["name_display"],
                    party_name=row["party"] + f" ({row['party_short']})",
                    vote_count=row["votes"],
                    result=row["result"],
                    result_desc=row["result_desc"],
                    candidate_age=row["age"],
                    candidate_sex=row["sex"],
                    candidate_race=row["ethnicity"],
                )
                cards.append(card)

            # display cards with paginator

            for card in paginator(cards, "curr_page", 4):
                st.markdown(card, unsafe_allow_html=True)

    # voter statistics

    colored_header(
        label="Voter Summary",
        description=f"For {'Malaysia' if not clicked_state else clicked_state}",
        color_name="red-70",
    )
    v3, v1, v2 = st.columns([1, 3, 2])

    with v1:
        voters_long = parlimen_voters_wide_to_long(voters)

        if clicked_state is None:
            options = population_pyramid_echarts(voters_long)
        else:
            options = population_pyramid_echarts(voters_long, filter=clicked_state)

        st_echarts(options)

    with v3:
        st.markdown(
            "<h4 style='text-align:center;'> Total Voters </h4>", unsafe_allow_html=True
        )
        # get total voters for each GE

        if clicked_state is not None:
            voters = voters.query(f"parlimen == '{clicked_state}'")

        ge15_voters = voters["total"].sum()
        ge14_voters = voters["total_ge14"].sum()

        st.markdown(
            total_voter_card(ge15_voters=ge15_voters, ge14_voters=ge14_voters),
            unsafe_allow_html=True,
        )

    with v2:
        if clicked_state is not None:
            voters = voters.query(f"parlimen == '{clicked_state}'")

        options = pie_voter_type_echarts(voters)
        st_echarts(options)


if __name__ == "__main__":
    init_styles()
    main()
