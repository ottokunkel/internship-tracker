INSERT INTO job_listings (
    job_title,
    company_name,
    url,
    location,
    posting_date,
    description,
    year_desired,
    experience
)
VALUES (
    %(job_title)s,
    %(company_name)s,
    %(url)s,
    %(location)s,
    %(posting_date)s,
    %(description)s,
    %(year_desired)s,
    %(experience)s
)
ON CONFLICT (job_title, company_name, url) 
DO NOTHING;

