from scraper import scrape_remoteok

if __name__ == "__main__":
    keyword = input("Keyword (e.g., Python, Backend, Data): ")
    df = scrape_remoteok(keyword)
    df.to_csv('remote_jobs.csv', index=False)
    print(f"Scraped {len(df)} jobs. Saved to remote_jobs.csv")
