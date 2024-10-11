from tools.content_loader import load_website_content
from tools.job_data_extractor import extract_job_details
from tools.database_controller import add_job_listing, check_similar_listing, setup_database

import os
from dotenv import load_dotenv
import pandas as pd

import psycopg2
load_dotenv()

def open_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password= os.getenv('DB_PASS')
    )
    return conn

def main(urls):

    links = pd.DataFrame(urls, columns=["urls"])
    status = [] 

    conn = open_connection()
    setup_database(conn)

    for url in links["urls"]:
        try:
            print("\n\n----------------------------------------------------")
            print("url:  ", url)
            content = load_website_content(url)
            job_details = extract_job_details(content, max_tokens=5000)

            if (job_details == None):
                status.append("Too Long")
                continue

            listing = add_job_listing(
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
            status.append(listing)
        except Exception as e:
            status.append(f"ERROR: ${e}")
            print("Error extracting from: ", url)


            print(job_details)
            print("Error listed: ", e) 
            conn.close()
            conn = open_connection()


    links["status"] = status
    
    query = "SELECT * FROM job_listings"
    df = pd.read_sql(query, conn)

    df.to_excel("./output/extracted_listings.xlsx", index=False)
    links.to_excel("./output/link_status.xlsx", index=False)
    
    
if __name__ == "__main__":
    urls_df = pd.read_csv("./input/input.csv")["urls"]
    urls = urls_df[0:100].tolist()
    main(urls)

