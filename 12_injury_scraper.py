import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Configuration ---
# URL for James Milner's injury page on Transfermarkt
INJURY_URL = "https://www.transfermarkt.com/james-milner/verletzungen/spieler/3333"
PLAYER_NAME = "James Milner"
FILENAME = f"{PLAYER_NAME.replace(' ', '_')}_injuries.csv"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# --- Scrape the Data ---
print(f"Scraping injury data for {PLAYER_NAME} from Transfermarkt...")
response = requests.get(INJURY_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

injury_table = soup.find('div', class_='grid-view')
injuries = []

if injury_table:
    rows = injury_table.find_all('tr', class_=['odd', 'even'])
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 4: # Ensure it's a valid injury row
            season = cols[0].text.strip()
            injury = cols[1].text.strip()
            start_date = cols[2].text.strip()
            end_date = cols[3].text.strip()
            days_missed = cols[4].text.strip().split(' ')[0]
            
            injuries.append({
                'season': season,
                'injury': injury,
                'start_date': start_date,
                'end_date': end_date,
                'days_missed': days_missed
            })
    print(f"Found {len(injuries)} injury records.")
else:
    print("Could not find the injury table.")

# --- Save to CSV ---
if injuries:
    df_injuries = pd.DataFrame(injuries)
    df_injuries.to_csv(FILENAME, index=False)
    print(f"✅ Injury data saved to {FILENAME}")