import pandas as pd
from textblob import TextBlob

# Baca dataset komentar (pastikan file ini ada)
df = pd.read_csv('data/dataset_komentar.csv')

# Fungsi untuk label sentimen
def get_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'positif'
    elif polarity < -0.1:
        return 'negatif'
    else:
        return 'netral'

# Buat kolom sentiment otomatis
df['sentiment'] = df['comment'].apply(get_sentiment)

# Simpan dataset baru
output_path = 'data/dataset_komentar_labeled.csv'
df.to_csv(output_path, index=False)

print(f"Sukses! Dataset dengan label sentimen tersimpan di: {output_path}")
