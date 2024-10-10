CREATE TABLE job_listings (
  Title VARCHAR(255) NOT NULL,                  -- Job Title that is posted in the listing
  Company VARCHAR(255) NOT NULL,                -- The company which is hiring
  Location VARCHAR(255) DEFAULT NULL,           -- Location of the job, could be remote or in a specific location, or not listed at all
  Description TEXT DEFAULT NULL,                -- A very short summary of the job and what the company is looking for
  Experience INT CHECK (Experience BETWEEN 1 AND 10) DEFAULT NULL, -- 1-10 rating for experience level (1 for intern, 10 for PhD)
  Year_Desired INT DEFAULT NULL                 -- Earliest year of school the listing prefers, if listed
);