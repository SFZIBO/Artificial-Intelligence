import pandas as pd

# Load data dari semua platform
#df1 = pd.read_csv('data/twitter_coldplay.csv')
df2 = pd.read_csv('data/ig_comments.csv')
df3 = pd.read_csv('data/tiktok_comments.csv')
df4 = pd.read_csv('data/youtube_comments.csv')

# Gabungkan semua data
combined_df = pd.concat([df2, df3, df4], ignore_index=True)

# Simpan gabungan dataset ke folder data
combined_df.to_csv('data/dataset_komentar.csv', index=False, encoding='utf-8-sig')
print(f'Selesai! Total komentar: {len(combined_df)}')
print(combined_df.head())  # Tampilkan 5 data teratas untuk verifikasi