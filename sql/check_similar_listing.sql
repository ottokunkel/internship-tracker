SELECT id
FROM job_listings
WHERE
    similarity(job_title, %(job_title)s) > %(title_threshold)s AND
    similarity(company_name, %(company_name)s) > %(company_threshold)s AND
    similarity(url, %(url)s) > %(url_threshold)s AND
    similarity(location, %(location)s) > %(location_threshold)s
ORDER BY
    (similarity(job_title, %(job_title)s) +
     similarity(company_name, %(company_name)s) +
     similarity(url, %(url)s) +
     similarity(location, %(location)s)) DESC
LIMIT 1;