import streamlit as st
from scraper import scrape_remoteok

st.title("🧑‍💻 Remote Job Scraper")
keyword = st.text_input("Search job by keyword:", "")

if st.button("Scrape Jobs"):
    df = scrape_remoteok(keyword)
    st.success(f"Found {len(df)} jobs!")
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "remote_jobs.csv", "text/csv")
