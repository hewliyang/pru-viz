import numpy as np
import streamlit as st

def result_card(
    candidate_name: str,
    party_name: str,
    vote_count: int,
    result: bool,
    result_desc: str,
    candidate_age: int,
    candidate_sex: str,
    candidate_race: str 
    ) -> str: 
    lost_deposit = True if result_desc == "lost_deposit" else False
    return f"""
    <div class="card text-center">
        <div class="card-body">
            <h5 class="card-title mb-0 font-weight-bold">{candidate_name}</h5>
            <h6 class="card-subtitle mb-1 text-muted">{int(candidate_age) if not np.isnan(candidate_age) else "Unknown"} {candidate_sex.capitalize()} {candidate_race.capitalize()}</h6>
            <p class="card-text">{party_name}</p>
            <p class="card-text font-weight-bold {"text-success" if result else "text-warning" if lost_deposit else "text-danger"}">{"WON" if result else "LOST DEPOSIT" if lost_deposit else "LOST"} - {vote_count}</p>
        </div>
    </div>
    """

def link_card(
    url: str,
    display: str,
    description: str = None
) -> str:
    return f'''
    <a href="{url}" class="btn btn-primary btn-sm active text-wrap" role="button" aria-pressed="true">{display}
    <span class="badge badge-light text-wrap">{description}</span></a>
    '''

def total_voter_card(
    ge15_voters: int,
    ge14_voters: int
) -> str :

    TIE = "blue"
    GREATER = "green"
    LESSER = "red"

    if ge15_voters > ge14_voters:
        ge15_color = GREATER
        ge14_color = LESSER
    elif ge15_voters < ge14_voters:
        ge15_color = LESSER
        ge14_color = GREATER        
    else:
        ge15_color = TIE
        ge14_color = TIE
    
    return f"""
    <div style="text-align:center;padding:0.8rem,0rem,3rem,0rem; margin-bottom:2rem; margin-top:0.25rem;">
        <h2 style="font-size:1.4rem; font-weight:600; padding:0;">GE15</h2>
        <big style="font-size:2rem; font-weight:800; line-height:1;color:{ge15_color};">{ge15_voters:,.0f}</big>
    </div>
    <div style="text-align:center; padding:0.8rem,0rem, 3rem, 0rem; margin-top:0.5rem;">
        <h2 style="font-size:1.4rem; font-weight:600; padding:0;">GE14</h2>
        <big style="font-size:2rem; font-weight:800; line-height:1;color:{ge14_color}">{ge14_voters:,.0f}</big>
    </div>
    """


def paginator(
    values: list,
    state_key: str,
    page_size: int
) -> list:

    total_pages = -(-len(values) // page_size)

    if total_pages > 1:
        selected_page = st.selectbox(
            label="Select page",
            options=range(1, total_pages+1),
        )
    else:
        selected_page=1

    page_start = (selected_page-1) * page_size
    page_end = page_start + page_size

    return values[page_start:page_end]
