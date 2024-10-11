import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def load_sql(query_name):
    with open(f'sql/{query_name}.sql', 'r') as file:
        return file.read()


def execute_query(conn, query, params=None):
  with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    cursor.execute(query, params)
    if cursor.description:  # If the query returns data
      return cursor.fetchall()
    else:
      conn.commit()
      return None

def setup_database(conn):
  # Enable pg_trgm extension
  query = load_sql('enable_pg_trgm')
  execute_query(conn, query)

  # Create job_listings table
  query = load_sql('create_job_listings_table')
  execute_query(conn, query)

  # Create indexes
  query = load_sql('create_trgm_indexes')
  execute_query(conn, query)

def check_similar_listing(conn, location, job_title, company_name, url):
  query = load_sql('check_similar_listing')

  # Set similarity thresholds
  title_threshold = 0.7
  company_threshold = 0.7
  url_threshold = 0.9
  location_threshold = .9

  params = {
    'job_title': job_title,
    'company_name': company_name,
    'url': url,
    'location': location,
    'title_threshold': title_threshold,
    'company_threshold': company_threshold,
    'url_threshold': url_threshold,
    'location_threshold': location_threshold
  }

  # Set the similarity threshold for the session
  with conn.cursor() as cursor:
    cursor.execute("SET pg_trgm.similarity_threshold = %s;", [min(title_threshold, company_threshold, url_threshold)])

  results = execute_query(conn, query, params)
  return results[0] if results else None

def add_job_listing(
  conn,
  job_title,
  company_name, 
  description,
  year_desired,
  experience,
  url, 
  location=None, 
  posting_date=None
):
  existing_listing = check_similar_listing(conn, location, job_title, company_name, url)
  if existing_listing:
    print(f"A similar job listing already exists with ID: {existing_listing['id']}")
  
    return f"Already in List"
    # Optionally update the existing listing here
  else:
    query = load_sql('insert_job_listing')
    params = {
      'job_title': job_title,
      'company_name': company_name,
      'url': url,
      'location': location,
      'posting_date': posting_date,
      'description': description,
      'year_desired': year_desired,
      'experience': experience
    }
    execute_query(conn, query, params)
    print("The job listing was added.")

    return "Sucess"