import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

# Buat folder output kalau belum ada
output_folder = 'static/images'
os.makedirs(output_folder, exist_ok=True)

# Baca dataset
df = pd.read_csv('data/dataset_komentar_labeled.csv')  # Pastikan ada kolom 'comment' dan 'sentiment'

# Pastikan kolom yang dibutuhkan ada
required_columns = {'comment', 'sentiment'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV harus punya kolom: {required_columns}")

# ======== Tambahan: daftar stopwords custom (bisa diedit Master) ========
custom_stopwords = {
    'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'itu', 'ini',
    'saya', 'kamu', 'dia', 'mereka', 'kami', 'kita',
    'ada', 'adalah', 'akan', 'jadi', 'sudah', 'belum', 'bisa', 'tidak',
    'pada', 'juga', 'atau', 'seperti',
    'gw', 'gue', 'loe', 'lu', 'elo', 'lo',
    'yg', 'gk', 'ga', 'nggak', 'tdk', 'udh', 'udah', 'blm', 'belom',
    'aja', 'kok', 'nih', 'sih', 'deh', 'dong', 'pun',
    'nya', 'lah', 'mah', 'eh', 'yaa', 'ya',
    'dgn', 'dr', 'sm', 'sy', 'sbg', 'dll',
    'kata1', 'kata2', 'kata3'
}


# Gabungkan dengan stopwords bawaan WordCloud (bahasa Inggris)
all_stopwords = STOPWORDS.union(custom_stopwords)

# Fungsi bantu buat WordCloud per sentimen
def generate_and_save_wordcloud(df, sentiment_label, output_filename):
    # Filter komentar sesuai sentimen
    filtered_comments = df[df['sentiment'] == sentiment_label]['comment'].dropna()
    
    # Gabungkan komentar jadi 1 teks
    text = " ".join(str(comment) for comment in filtered_comments)
    
    # Skip kalau kosong
    if not text.strip():
        print(f"[WARNING] Tidak ada komentar dengan sentimen '{sentiment_label}'. File tidak dibuat.")
        return
    
    # Generate WordCloud (dengan stopwords)
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        collocations=False,
        stopwords=all_stopwords
    ).generate(text)
    
    # Simpan gambar
    output_path = os.path.join(output_folder, output_filename)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    print(f"[INFO] WordCloud '{sentiment_label}' disimpan di {output_path}")

# Generate wordcloud untuk masing-masing sentimen
generate_and_save_wordcloud(df, 'positif', 'wordcloud_positif.png')
generate_and_save_wordcloud(df, 'negatif', 'wordcloud_negatif.png')
generate_and_save_wordcloud(df, 'netral', 'wordcloud_netral.png')

print("[SUCCESS] Semua WordCloud selesai dibuat!")
