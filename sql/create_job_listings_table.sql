CREATE TABLE IF NOT EXISTS job_listings (
  id SERIAL PRIMARY KEY,
  job_title TEXT NOT NULL,
  company_name TEXT NOT NULL,
  url TEXT NOT NULL,
  location TEXT,
  description TEXT DEFAULT NULL,
  year_desired INTEGER DEFAULT NULL,
  experience INTEGER DEFAULT NULL,
  posting_date DATE DEFAULT NULL,
  UNIQUE (job_title, company_name, url)
);
