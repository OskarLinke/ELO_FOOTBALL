import pandas as pd 
import pickle as pkl

df = pd.read_csv("all_games.csv")

all_teams = pd.unique(df[['home_team', 'away_team']].values.ravel('K')) 

#We want to sort the data by date 


all_teams_dict = {}
#for team in all_teams

df_leagues_only = df[df.tournament != "FA"]
df_leagues_only = df_leagues_only[df_leagues_only.tournament != "LC"]

all_teams_in_leagues = pd.unique(df_leagues_only[['home_team', 'away_team']].values.ravel('K'))
for team in all_teams: 
    if team in all_teams_in_leagues: 
      
        appearances = (df_leagues_only['home_team'] == team) | (df_leagues_only['away_team'] == team) 
        first_row_idx = appearances.idxmax()
        first_appearance = df_leagues_only.loc[first_row_idx]

        if first_appearance['tournament'] == "PL": 
            all_teams_dict[team] = {"elo": 2600, "provisional": True, "max_elo": 2600, "max_elo_date": first_appearance['date'], "games_played": 0}
        elif first_appearance['tournament'] == "CS":
            all_teams_dict[team] = {"elo": 2500, "provisional": True, "max_elo": 2500, "max_elo_date": first_appearance['date'], "games_played": 0}
        elif first_appearance['tournament'] == "L1": 
            all_teams_dict[team] = {"elo": 2350, "provisional": True, "max_elo": 2350, "max_elo_date": first_appearance['date'], "games_played": 0}
        elif first_appearance['tournament'] == "L2": 
            all_teams_dict[team] = {"elo": 2200, "provisional": True, "max_elo": 2200, "max_elo_date": first_appearance['date'], "games_played": 0}


    else:
        
        appearances = (df['home_team'] == team) | (df['away_team'] == team) 
        first_row_idx = appearances.idxmax()
        first_appearance = df.loc[first_row_idx]
        all_teams_dict[team] = {"elo": 2000, "provisional": True, "max_elo": 2000, "max_elo_date": first_appearance['date'], "games_played": 0}


all_teams_dict['wolverhampton'] = all_teams_dict.pop('wolverhampton-wanderers')

with open('teams_dict.pkl', 'wb') as f:
    pkl.dump(all_teams_dict, f)
