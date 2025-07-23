from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

url = 'https://www.tiktok.com/@mdv.channel/video/7495935355493846327'
driver = webdriver.Chrome()  # atau Edge(), Firefox()

driver.get(url)
time.sleep(5)

# Scroll komentar (biar semua muncul)
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

comments_elements = driver.find_elements(By.XPATH, '//p[@data-e2e="comment-level-1"]')

comments = []
for elem in comments_elements:
    comments.append(['tiktok', elem.text, time.strftime('%Y-%m-%d %H:%M:%S')])

driver.quit()

df = pd.DataFrame(comments, columns=['platform', 'komentar', 'timestamp'])
df.to_csv('tiktok_comments.csv', index=False, encoding='utf-8-sig')
