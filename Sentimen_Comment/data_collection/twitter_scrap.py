import snscrape.modules.twitter as sntwitter
import pandas as pd

# Parameter
query = 'konser Coldplay since:2023-11-01 until:2023-11-30 lang:id'
limit = 10000

tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    tweets.append([ 'twitter', tweet.content, tweet.date])

df = pd.DataFrame(tweets, columns=['platform', 'komentar', 'timestamp'])

# Simpan CSV ke folder data
df.to_csv('data/twitter_coldplay.csv', index=False, encoding='utf-8-sig')
