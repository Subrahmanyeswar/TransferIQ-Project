import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv


# --- Configuration ---
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
PLAYER_NAME = "James Milner"
FILENAME = f"{PLAYER_NAME.replace(' ', '_')}_recent_sentiment.csv"

# --- THE FIX: Use the 'recent' search endpoint, which is available on the free plan ---
search_url = "https://api.twitter.com/2/tweets/search/recent"

headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
# NOTE: The 'recent' endpoint does not use start_time or end_time
query_params = {
    'query': f'"{PLAYER_NAME}" lang:en -is:retweet',
    'max_results': 100,
    'tweet.fields': 'created_at'
}

analyzer = SentimentIntensityAnalyzer()
all_tweets = []

print(f"Collecting recent tweets for {PLAYER_NAME}...")
response = requests.get(search_url, headers=headers, params=query_params)

if response.status_code != 200:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

response_json = response.json()
if 'data' in response_json:
    for tweet in response_json['data']:
        text = tweet['text']
        created_at = tweet['created_at']
        sentiment_scores = analyzer.polarity_scores(text)
        all_tweets.append({
            'date': created_at,
            'tweet': text,
            'sentiment_score': sentiment_scores['compound']
        })
    print(f"Collected {len(all_tweets)} recent tweets.")
else:
    print("No recent tweets found.")

if all_tweets:
    df_sentiment = pd.DataFrame(all_tweets)
    df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])
    df_sentiment.to_csv(FILENAME, index=False)
    print(f"✅ Recent sentiment data saved to {FILENAME}")