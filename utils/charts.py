import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Union

DEFAULT_HEIGHT = 300
DEFAULT_HOLE = 0.3

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
            l=0,
            r=0,
            t=22,
            b=0
        )
    )
    return fig