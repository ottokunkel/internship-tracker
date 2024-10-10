from tools.content_loader import load_website_content
from tools.job_data_extractor import extract_job_details
from tools.export import export_to_csv

import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3


load_dotenv()

def main(urls):

    conn = sqlite3.connect("/database/application.db")

    c = conn.cursor()

    job_data = []
    for url in urls:
        try:
            content = load_website_content(url)
            job_details = extract_job_details(content, max_tokens=3000)
            job_data.append(job_details)
            job_details['url'] = url
        except:
            print("Error extracting from: ", url)
            print("Error listed: ")
    export_to_csv(job_data, "./tables/listings.csv") 
    
if __name__ == "__main__":
    urls = pd.read_csv("./input.csv")["urls"].tolist()
    main(urls)