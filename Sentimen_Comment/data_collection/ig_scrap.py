import instaloader
import pandas as pd

# Login
L = instaloader.Instaloader()
L.load_session_from_file('data_collection/rey_scrape')

# Target post (URL)
shortcode = 'https://www.instagram.com/p/DInK1WUhW7k/'  # ambil dari link post IG https://www.instagram.com/p/C2KfEXpF5zL/

post = instaloader.Post.from_shortcode(L.context, shortcode)

comments = []
for comment in post.get_comments():
    comments.append([ 'instagram', comment.text, comment.created_at_utc ])

df = pd.DataFrame(comments, columns=['platform', 'komentar', 'timestamp'])
df.to_csv('data/ig_comments.csv', index=False, encoding='utf-8-sig')
