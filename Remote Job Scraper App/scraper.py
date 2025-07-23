import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_remoteok(keyword=None):
    url = "https://remoteok.com/remote-dev-jobs" #website yang bisa di scrape
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('tr', class_='job')
    
    job_list = []
    for job in jobs:
        title = job.find('h2')
        company = job.find('h3')
        link = job.get('data-href')
        
        if title and company and link:
            job_data = {
                'Title': title.text.strip(),
                'Company': company.text.strip(),
                'Link': 'https://remoteok.com' + link
            }
            job_list.append(job_data)

    df = pd.DataFrame(job_list)
    
    # Optional: Filter by keyword
    if keyword:
        df = df[df['Title'].str.contains(keyword, case=False, na=False)]

    return df
