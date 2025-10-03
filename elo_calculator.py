import numpy as np
import pickle as pkl
import pandas as pd

with open('teams_dict.pkl', 'rb') as f:
    teams_dict = pkl.load(f)




top100_row = ['team_name', 1000, 'date']

top100oat = np.array([top100_row] * 100, dtype = object)
top100perfs = np.array([top100_row] * 100, dtype = object)
top20_by_month = {}



games_df = pd.read_csv("all_games.csv")


def calc_elo(home_team, away_team, result): 
    #All formulas from https://en.wikipedia.org/wiki/Elo_rating_system
    if result == 'H': 
        res = 1 
    elif result == 'D': 
        res = 0.5
    elif result == 'A': 
        res = 0 
    else:
        print(result)
        raise ValueError('Unexpected result of game (Not H, D or A)')
    Ra = teams_dict[home_team]['elo']
    Rb = teams_dict[away_team]['elo']
    Qa = 10**(Ra/400)
    Qb = 10 ** (Rb/400)
    Ea = Qa/(Qa + Qb)
    Eb = Qb/(Qa + Qb)
    if teams_dict[home_team]['provisional']: 
        Ra_ = Ra + 32 * (res - Ea)
    else: 
        Ra_ = Ra + 16 *  (res-Ea)

    if teams_dict[away_team]['provisional']: 
        Rb_ = Rb + 32 * ((1-res) - Eb)
    else: 
        Rb_ = Rb + 16 * ((1-res)-Eb)   
   

    teams_dict[home_team]['opp_rts'].append(teams_dict[away_team]['elo']) 

    teams_dict[away_team]['opp_rts'].append(teams_dict[home_team]['elo'])

    teams_dict[home_team]['pts_in_ssn'] += res
    teams_dict[away_team]['pts_in_ssn'] += (1-res)

    return Ra_ , Rb_


#Two following functions are from https://en.wikipedia.org/wiki/Performance_rating_(chess)

def expected_score(opponent_ratings: list[float], own_rating: float) -> float:
    """How many points we expect to score in a tourney with these opponents"""
    return sum(
        1 / (1 + 10**((opponent_rating - own_rating) / 400))
        for opponent_rating in opponent_ratings
    )


def performance_rating(opponent_ratings: list[float], score: float) -> int:
    """Calculate mathematically perfect performance rating with binary search"""
    lo, hi = 0, 4000

    while hi - lo > 0.001:
        mid = (lo + hi) / 2

        if expected_score(opponent_ratings, mid) < score:
            lo = mid
        else:
            hi = mid

    return mid


def run_game(home_team, away_team, result, date, top100oat): 
    teams_dict[home_team]['elo'], teams_dict[away_team]['elo'] = calc_elo(home_team, away_team, result)
    

    if (teams_dict[home_team]['elo'] > teams_dict[home_team]['max_elo']) and (not teams_dict[home_team]['provisional']): 
        teams_dict[home_team]['max_elo'] = teams_dict[home_team]['elo']
        teams_dict[home_team]['max_elo_date'] = date

        if teams_dict[home_team]['elo'] > float(top100oat[0][1]):
            if home_team in top100oat[:,0]: 
                mask = top100oat[:,0] == home_team 
                top100oat[mask,1] = round(teams_dict[home_team]['elo'], 2)
                top100oat[mask,2] = date
            else: 
                top100oat[0] = [home_team, round(teams_dict[home_team]['elo'], 2), date]
            top100oat = top100oat[top100oat[:,1].argsort()]


    if (teams_dict[away_team]['elo'] > teams_dict[away_team]['max_elo']) and (not teams_dict[away_team]['provisional']): 
        teams_dict[away_team]['max_elo'] = teams_dict[away_team]['elo']
        teams_dict[away_team]['max_elo_date'] = date

        if teams_dict[away_team]['elo'] > float(top100oat[0][1]):
            if away_team in top100oat[:,0]: 
                mask = top100oat[:,0] == away_team 
                top100oat[mask,1] = round(teams_dict[away_team]['elo'],2)
                top100oat[mask,2] = date
            else: 
                top100oat[0] = [away_team, round(teams_dict[away_team]['elo'],2), date]
            top100oat = top100oat[top100oat[:,1].argsort()]

            
    teams_dict[home_team]['games_played'] += 1
    teams_dict[away_team]['games_played'] += 1 

    if teams_dict[home_team]['games_played'] >= 25: 
        teams_dict[home_team]['provisional'] = False 
    
    if teams_dict[away_team]['games_played'] >= 25: 
        teams_dict[away_team]['provisional'] = False 
    
    return top100oat



def save_top_20(top20, teams_dict, month, year):
    teams_that_have_played = {k: v for k,v in teams_dict.items() if v['games_played'] > 0} 

    team_elo_tuples = [(inner_dict['elo'], name) for name, inner_dict in teams_that_have_played.items() if 'elo' in inner_dict]
    sorted_teams = sorted(team_elo_tuples, key=lambda x: x[0], reverse=True)[:20]
    
    y_m_key = year +"-"+ month
    top20[y_m_key] = sorted_teams 
    return top20
    

def calc_perf_rats(top100perfs, teams_dict, season):     
    all_teams = teams_dict.keys()
    for team in all_teams: 
        if teams_dict[team]['pts_in_ssn'] > 0 and  len(teams_dict[team]['opp_rts'])> 10: 
            perf_rat = round(performance_rating(teams_dict[team]['opp_rts'], teams_dict[team]['pts_in_ssn']), 2)
            if perf_rat > float(top100perfs[0][1]):
                top100perfs[0] = [team, perf_rat, season]
                top100perfs = top100perfs[top100perfs[:,1].argsort()]

        teams_dict[team]['pts_in_ssn'] = 0
        teams_dict[team]['opp_rts'] = []

    return top100perfs

            


    
    

current_month = games_df.iloc[0]['date'][5]+ games_df.iloc[0]['date'][6]
current_season = games_df.iloc[0]['season']

for row in games_df.itertuples():
    season = row[7]
    month = row[2][5] + row[2][6]
    if month != current_month: 
        
        #Save top 20 at the end of previous month 
        year = row[2][0] + row[2][1] + row[2][2] + row[2][3]
        top20_by_month = save_top_20(top20_by_month, teams_dict, current_month, year) 
        current_month = month
        
    if season != current_season: 
        top100perfs = calc_perf_rats(top100perfs, teams_dict, current_season)
                                          
        current_season = season

    top100oat = run_game(row[3], row[4], row[5], row[2], top100oat)



top20_df = pd.DataFrame.from_dict(top20_by_month, orient='index', columns = list(range(1,21)))
top20_df.index.name = 'date'
top20_df = top20_df.reset_index()



with open('finished_teams_dict.pkl', 'wb') as f: 
    pkl.dump(teams_dict, f)



top100oat = top100oat[(-top100oat[:,1]).argsort()]
top100perfs = top100perfs[(-top100perfs[:,1]).argsort()]



pd.DataFrame.from_records(top100perfs, columns = ['team', 'performance rating', 'season']).to_csv("top100_performance_ratings.csv")
pd.DataFrame.from_records(top100oat, columns = ['team', 'peak elo', 'date']).to_csv("finished_top100oat.csv")

top20_df.to_csv("top20_by_month.csv")





