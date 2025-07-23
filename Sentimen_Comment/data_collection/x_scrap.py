import time
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from textblob import TextBlob

tiktok_url = input("Masukkan URL TikTok: ")

driver = webdriver.Chrome()
driver.get(tiktok_url)
time.sleep(5) 

input("Tekan Enter setelah halaman tujuan terbuka untuk memulai scraping...")

comments = []
comment_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'content')]")
for elem in comment_elements:
    comments.append(elem.text.strip())

driver.quit()

if not comments:
    print("Tidak ada komentar ditemukan. Pastikan tautan TikTok yang diberikan benar.")
    exit()

def is_valid_comment(comment):
    return bool(re.search(r'[a-zA-Z]', comment)) 

valid_comments = [comment for comment in comments if is_valid_comment(comment)]

excluded_words = {"live", "iklan", "promo", "subscribe", "follow", "beli", "gratis",
    "lihat", "balasan", "reply", "komen", "like", "suka", "pas", "habis", "cek", "bang",
    "foto", "kamera", "teknologi", "bayar", "jual", "diskon", "order", "dm",
    "gratis", "jualan", "brand", "wkwk", "anjay", "santuy", "gabut", "gue",
    "lu", "bro", "sis", "bestie", "cuy", "gak", "kan", "nih", "dong", "yaudah"
}

def remove_names(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text) 
    text = re.sub(r'\b[A-Z][a-z]+\b', '', text)  
    return text

nltk.download("stopwords")
nltk.download("punkt")
stop_words = set(stopwords.words("indonesian"))

def preprocess_text(text):
    text = remove_names(text) 
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words and word not in excluded_words]
    return " ".join(tokens)

cleaned_comments = [preprocess_text(comment) for comment in valid_comments]

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positif"
    elif sentiment_score < 0:
        return "Negatif"
    else:
        return "Netral"

sentiments = [get_sentiment(comment) for comment in cleaned_comments]

df = pd.DataFrame({
    "No": range(1, len(valid_comments) + 1),
    "Original Comment": valid_comments,
    "Cleaned Comment": cleaned_comments,
    "Sentiment": sentiments
})

df.to_csv("etle_comments_analysis.csv", index=False, encoding='utf-8-sig')

print("Dataset otomatis terstruktur dalam 'etle_comments_analysis.csv'!")


text_data = " ".join(cleaned_comments)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)


plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("WordCloud Komentar TikTok tentang ETLE")
plt.show()

print("WordCloud berhasil dibuat dan ditampilkan!")