import numpy as np
import pickle as pkl
import pandas as pd

with open('teams_dict.pkl', 'rb') as f:
    teams_dict = pkl.load(f)



top100_row = ['team_name', 2000, 'date']

top100 = np.array([top100_row] * 100, dtype = object)


games_df = pd.read_csv("all_games.csv")


def calc_elo(home_team, away_team, result): 
    #All calculations from https://en.wikipedia.org/wiki/Elo_rating_system
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
    
    
    return Ra_ , Rb_


def run_game(home_team, away_team, result, date, top100): 
    teams_dict[home_team]['elo'], teams_dict[away_team]['elo'] = calc_elo(home_team, away_team, result)
    

    if (teams_dict[home_team]['elo'] > teams_dict[home_team]['max_elo']) and (not teams_dict[home_team]['provisional']): 
        teams_dict[home_team]['max_elo'] = teams_dict[home_team]['elo']
        teams_dict[home_team]['max_elo_date'] = date

        if teams_dict[home_team]['elo'] > float(top100[0][1]):
            if home_team in top100[:,0]: 
                mask = top100[:,0] == home_team 
                top100[mask,1] = teams_dict[home_team]['elo']
                top100[mask,2] = date
            else: 
                top100[0] = [home_team, teams_dict[home_team]['elo'], date]
            top100 = top100[top100[:,1].argsort()]


    if (teams_dict[away_team]['elo'] > teams_dict[away_team]['max_elo']) and (not teams_dict[away_team]['provisional']): 
        teams_dict[away_team]['max_elo'] = teams_dict[away_team]['elo']
        teams_dict[away_team]['max_elo_date'] = date

        if teams_dict[away_team]['elo'] > float(top100[0][1]):
            if away_team in top100[:,0]: 
                mask = top100[:,0] == away_team 
                top100[mask,1] = teams_dict[away_team]['elo']
                top100[mask,2] = date
            else: 
                top100[0] = [away_team, teams_dict[away_team]['elo'], date]
            top100 = top100[top100[:,1].argsort()]

            
    teams_dict[home_team]['games_played'] += 1
    teams_dict[away_team]['games_played'] += 1 

    if teams_dict[home_team]['games_played'] >= 100: 
        teams_dict[home_team]['provisional'] = False 
    
    if teams_dict[away_team]['games_played'] >= 100: 
        teams_dict[away_team]['provisional'] = False 
    
    return top100




for row in games_df.itertuples():

    top100 = run_game(row[3], row[4], row[5], row[2], top100)





with open('finished_teams_dict.pkl', 'wb') as f: 
    pkl.dump(teams_dict, f)

with open('finished_top100.pkl', 'wb') as f: 
    pkl.dump(top100, f)

print(top100)



