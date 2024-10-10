from tools.content_loader import load_website_content
from tools.job_data_extractor import extract_job_details
from tools.database_controller import add_job_listing, check_similar_listing, setup_database

import os
from dotenv import load_dotenv
import pandas as pd

import psycopg2

load_dotenv()

def main(urls):

    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password= os.getenv('DB_PASS')
    )

    setup_database(conn)


    for url in urls:
        try:
            content = load_website_content(url)
            job_details = extract_job_details(content, max_tokens=5000)
            print(job_details)
            print(job_details["job_title"])

            add_job_listing(
                conn,
                job_title=job_details["job_title"],
                company_name=job_details["company_name"],
                description=job_details["description"],
                url=url, 
                location=job_details["location"], 
                posting_date=job_details["posting_date"],
                year_desired=job_details["year_desired"],
                experience=job_details["experience"],
            )

        except Exception as e:
            print("Error extracting from: ", url)
            print("Error listed: ", e) 
    
    
if __name__ == "__main__":
    # urls = pd.read_csv("./input/input.csv")["urls"].tolist()
    urls = ["https://job-boards.greenhouse.io/verkada/jobs/4538383007?utm_source=Simplify&ref=Simplify"]
    main(urls)

