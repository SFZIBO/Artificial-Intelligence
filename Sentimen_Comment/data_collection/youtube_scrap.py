from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime

def get_youtube_comments(video_url, max_comments=2000):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(video_url)

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 800);")  # scroll ke bawah
    time.sleep(3)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    comments_data = []

    while len(comments_data) < max_comments:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)

        comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")
        for el in comment_elements:
            text = el.text
            if text and not any(text == row[1] for row in comments_data):  # cek duplikat
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                comments_data.append(['youtube', text, timestamp])
            if len(comments_data) >= max_comments:
                break

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return comments_data

# Contoh penggunaan
video_url = "https://www.youtube.com/watch?v=e5gGf--7YtU&t=116s"
comments_data = get_youtube_comments(video_url, max_comments=1000)

# Simpan ke CSV format standar (platform | komentar | timestamp)
df = pd.DataFrame(comments_data, columns=['platform', 'komentar', 'timestamp'])
df.to_csv('data/tiktok_comments.csv', index=False, encoding='utf-8-sig')

print(f"Komentar berhasil disimpan. Total: {len(df)}")
