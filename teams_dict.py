import pandas as pd 
import pickle as pkl

df = pd.read_csv("all_games.csv")

all_teams = df['home_team'].unique() 

#We want to sort the data by date 


all_teams_dict = {}
#for team in all_teams

df_leagues_only = df[df.tournament != "FA"]
df_leagues_only = df_leagues_only[df_leagues_only.tournament != "LC"]

all_teams_in_leagues = df_leagues_only['home_team'].unique()


print(len(all_teams))
print(len(all_teams_in_leagues))
for team in all_teams_in_leagues: 
    first_appearance = df_leagues_only[df_leagues_only['home_team'] == team].iloc[0]

    if first_appearance['tournament'] == "PL": 
        all_teams_dict[team] = {"elo": 2600, "provisional": True, "max_elo": 2600, "max_elo_date": first_appearance['date']}
    elif first_appearance['tournament'] == "CS":
        all_teams_dict[team] = {"elo": 2500, "provisional": True, "max_elo": 2500, "max_elo_date": first_appearance['date']}
    elif first_appearance['tournament'] == "L1": 
        all_teams_dict[team] = {"elo": 2350, "provisional": True, "max_elo": 2350, "max_elo_date": first_appearance['date']}
    elif first_appearance['tournament'] == "L2": 
        all_teams_dict[team] = {"elo": 2200, "provisional": True, "max_elo": 2200, "max_elo_date": first_appearance['date']}


for team in all_teams: 
    if team in all_teams_in_leagues: 
        continue 
    else: 
        first_appearance = df[df['home_team'] == team].iloc[0]
        all_teams_dict[team] = {"elo": 2000, "provisional": True, "max_elo": 2000, "max_elo_date": first_appearance['date']}

print(all_teams_dict)

with open('teams_dict.pkl', 'wb') as f:
    pkl.dump(all_teams_dict, f)
