import streamlit as st
from utils.st_styles import init_styles
from streamlit_extras.mention import mention

def about():

    st.info(
        icon = "🚨",
        body = "For the non-Malaysians: **PRU** == Pilihan Raya Umum == **GE** == General Election"
    )
    
    st.markdown(
    """
    # **About**

    Built over my semester break with the goal of learning **Streamlit**. Had lots of fun rummaging through the gallery looking for inspiration
    and cool components to use.

    Made possible with open data from [**Thevesh**](https://github.com/Thevesh/analysis-election-msia) and [**DOSM**](https://github.com/dosm-malaysia/data-open)

    Here is the project `requirements.txt` for reference of all the components this app uses:

    ```python
    Cython==0.29.32
    folium==0.13.0
    geopandas==0.12.1
    leafmap==0.14.1
    millify==0.1.1
    numpy==1.23.5
    pandas==1.5.2
    plotly==5.11.0
    setuptools==65.5.1
    Shapely==1.8.5.post1
    streamlit==1.16.0
    streamlit_echarts==0.4.0
    streamlit_extras==0.2.4
    ./cartogram_geopandas
    ```

    I used the continous area cartogram algorithm from [Matthieu Viry](https://github.com/mthh/cartogram_geopandas) which is written in `Cython`.
    It requires `Shapely < 2.0.0` and an updated `pyproject.toml` to install & function correctly on Streamlit Cloud.

    #### Links:
    """)

    mention(
        label = "GitHub Repo",
        icon = "github",
        url = "https://github.com/hewliyang/pru-viz"
    )

    mention(
        label = "hewliyang.tech",
        icon = "🌐",
        url = "https://hewliyang.tech"
    )

    mention(
        label = "Twitter",
        icon = "twitter",
        url = "https://twitter.com/hewliyang_"
    )

    mention(
        label = "Reddit",
        icon = "🇷🇪",
        url = "https://www.reddit.com/user/hewliyang9"
    )

if __name__ == "__main__":
    init_styles()
    about()