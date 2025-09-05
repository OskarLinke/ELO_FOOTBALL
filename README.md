# ELO_FOOTBALL
A redo of my previous ELO football project - I'm looking to use historical data to assign an ELO-rating to all English football teams

I get all data from https://www.worldfootball.net 

Running datascraper.py gets the games played in the top four leagues, as well as the FA Cup and the League Cup. 

Running team_dicts.py creates a dictionairy of all teams to play at least 1 game. 

Running elo_calculator.py creates .csv files for the top 100 rating peaks achieved, the top 100 performance ratings achieved over the course of a season,
and the top 20 rated teams after each month. 

The three scripts must be run in that order. 

I encourage you to run analysis of these .csv files; 
What team has been rated #1 for the most months? Which team has been rated #1 for most months in a row? Was there a long period of time where the same 6 teams 
occupied the top 6 spots? Etc. 
