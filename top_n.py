import pandas as pd 

top20 = pd.read_csv("top20_by_month.csv")

n = 6
no_mths = 0
crnt_top_n = []

print("We will find the longest reigning top ", + n, " in history")

for i in range(n):
    print(type(top20.iloc[0][3+i]))
    crnt_top_n.append(top20.iloc[0][3+i][1]) 

print(crnt_top_n)


for row in top20.itertuples():
    print(row)
    print(row[3])
    raise ValueError("debugging")

    if month != current_month: 
        
        #Save top 20 at the end of previous month 
        year = row[2][0] + row[2][1] + row[2][2] + row[2][3]
        top20_by_month = save_top_20(top20_by_month, teams_dict, current_month, year) 
        current_month = month
        
    if season != current_season: 
        top100perfs = calc_perf_rats(top100perfs, teams_dict, current_season)
                                          
        current_season = season

    top100oat = run_game(row[3], row[4], row[5], row[2], top100oat)

