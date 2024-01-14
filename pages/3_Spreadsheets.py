import streamlit as st
import pandas as pd
from streamlit_extras.dataframe_explorer import dataframe_explorer

from utils.st_styles import init_styles


@st.cache_data
def load_data():
    results = pd.read_csv("./data/results_parlimen_ge15.csv")
    candidates = pd.read_csv("./data/candidates_ge15.csv")
    census = pd.read_csv("./data/census_parlimen.csv")
    voters = pd.read_csv("./data/voters_ge15.csv")

    return results, candidates, census, voters


def main():
    # display the dataframe in an expander

    results, candidates, census, voters = load_data()

    st.markdown("# **Raw Data**")

    st.markdown(
        """

    Access the raw data used for the previous pages here. Some tips for usage:
    1.  **Filter** by variables - should be self explanatory. 
    2.  **Sort** by clicking on the column name, The arrow indicates whether ascending/descending order.
    3.  Once filtered according to your liking, you may **download** the filtered/sorted data as `.csv` by clicking on the button.

    Happy exploring!
    """
    )

    with st.expander("Explore candidate data!"):
        df_exp = dataframe_explorer(candidates)
        st.dataframe(df_exp, use_container_width=True)

        # make the filtered DF available for download via a button
        csv = df_exp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="candidates_ge15_filtered.csv",
            mime="text/csv",
        )

    with st.expander("Explore result data!"):
        result_exp = dataframe_explorer(results)
        st.dataframe(result_exp, use_container_width=True)

        # make the filtered DF available for download via a button
        csv = result_exp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="results_ge15_filtered.csv",
            mime="text/csv",
        )

    with st.expander("Explore census data!"):
        census_exp = dataframe_explorer(census)
        st.dataframe(census_exp, use_container_width=True)

        # make the filtered DF available for download via a button
        csv = census_exp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="census_filtered.csv",
            mime="text/csv",
        )

    with st.expander("Explore voter data!"):
        voters_exp = dataframe_explorer(voters)
        st.dataframe(voters_exp, use_container_width=True)

        # make the filtered DF available for download via a button
        csv = voters_exp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="voters_filtered.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    init_styles()
    main()
