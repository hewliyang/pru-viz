import numpy as np

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
    <div class="card text-center" style="margin:0.2rem">
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