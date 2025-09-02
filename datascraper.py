import cloudscraper
from bs4 import BeautifulSoup
import re
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper()

# Make the request


def scrape_from_url(url, df, tournament): 
    # Find the table - adjust the selector based on the actual table structuretable
    response = scraper.get(url)
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='standard_tabelle')  # You might need to adjust this selector



    matches = []
    current_date = None


    if table:
        # Iterate through each row in the table body
        for row in table.find_all('tr')[1:]:  # Skip header row if exists
            columns = row.find_all('td')
            
            if len(columns) < 6:  # Ensure we have enough columns
                continue
            
            # Extract date (first column)
            date_cell = columns[0].get_text(strip=True)
            if date_cell:  # If date cell is not empty, update current date
                current_date = date_cell
            
            # Skip rows that don't have actual match data (like subheaders)
            if not current_date or len(columns) < 7:
                continue
            
            # Extract home team from link (more reliable)
            home_team_link = columns[2].find('a')  # Adjust column index based on actual structure
            home_team = home_team_link['href'].split('/')[-2] if home_team_link and home_team_link.get('href') else columns[2].get_text(strip=True)
            
            # Extract away team from link
            away_team_link = columns[4].find('a')  # Adjust column index
            away_team = away_team_link['href'].split('/')[-2] if away_team_link and away_team_link.get('href') else columns[4].get_text(strip=True)
            
            # Extract score from the last column or score column
            score = columns[-2].get_text(strip=True)  # Usually last column contains score
            score = re.search(r'^(\d+):(\d+)\s?', score)
            if score is not None: 
                home_goals, away_goals = score.groups()
            else: 
                continue
            

            if home_goals > away_goals: 
                result = 'H' 
            elif away_goals > home_goals: 
                result = "A"
            else: 
                result = 'D'
            
            matches.append({
                'date': current_date,
                'home_team': home_team,
                'away_team': away_team,
                'result': result,
                'tournament': tournament
            })

    new_matches = pd.DataFrame(matches)
    return pd.concat([df, new_matches], ignore_index = True)

# Create DataFrame
df = pd.DataFrame([])

def add_tournament(start_year, end_year, tournament_name, base_url, df):
    tournament = "PL"
    current_year = start_year
    while current_year <= (end_year-1): 
        url_year = str(current_year) + "-"+str(current_year+1)
        current_year += 1 
        url = base_url+url_year
        df = scrape_from_url(url, df, tournament_name)
    return df

df = add_tournament(1888, 2025, "PL","https://www.worldfootball.net/all_matches/eng-premier-league-", df )
print("Finished PL")
df = add_tournament(1892, 2025, "CS", "https://www.worldfootball.net/all_matches/eng-championship-", df)
print("Finished CS")
df = add_tournament(1871, 2025, "FA", "https://www.worldfootball.net/all_matches/eng-fa-cup-", df)
print("Finished FA")
df = add_tournament(1960, 2025, "LC", "https://www.worldfootball.net/all_matches/eng-league-cup-", df)
print("Finished LC")
df = add_tournament(1999, 2025, "L1", "https://www.worldfootball.net/all_matches/eng-league-one-", df)
print("Finished L1")
df = add_tournament(1999, 2025, "L2", "https://www.worldfootball.net/all_matches/eng-league-two-", df)
print("Finished L2")




print(df)
df.to_csv('all_games.csv', index = False)

