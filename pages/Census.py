import streamlit as st
from itertools import cycle
from streamlit_extras.badges import badge
from utils.cards import link_card
from utils.st_styles import load_bootstrap_stylesheet, load_css, reduce_top_padding

st.write("Hello World")

def census():
    pass


if __name__ == "__main__":
    load_bootstrap_stylesheet("./styles/bootstrap.min.css")
    load_css("./styles/main.css")

    with st.sidebar:
        st.title("pru-viz")
        st.markdown("### A simple web app to visualise GE15 and census data with maps!")
        badge_columns = cycle(st.columns(3))
        with next(badge_columns): badge(type="github", name="hewliyang/pru-viz")
        with next(badge_columns): badge(type="twitter", name="hewliyang")

        st.markdown("## Data sources:")
        st.markdown(link_card("https://github.com/Thevesh/analysis-election-msia", "Thevesh"), unsafe_allow_html=True)
        st.markdown(link_card("https://github.com/dosm-malaysia/data-open", "Department of Statistics Malaysia"), unsafe_allow_html=True)
    census()