CREATE INDEX IF NOT EXISTS idx_job_title_trgm ON job_listings USING GIN (job_title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_company_name_trgm ON job_listings USING GIN (company_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_url_trgm ON job_listings USING GIN (url gin_trgm_ops);
