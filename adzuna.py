import requests
import psycopg2
from psycopg2.extras import execute_values

APP_ID = "de5c925d"
APP_KEY = "f660da2e142f5e2339f764e81a8efa37"
COUNTRY = "us"  # Change based on target location
PAGE = 1

API_URL = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{PAGE}?app_id={APP_ID}&app_key={APP_KEY}"

def fetch_jobs():
    response = requests.get(API_URL)
    if response.status_code == 200:
        jobs = response.json().get("results", [])
        return jobs
    else:
        print("Error fetching jobs:", response.status_code)
        return []

def process_jobs(jobs):
    job_data = []
    for job in jobs:
        job_data.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "description": job.get("description"),
            "post_date": job.get("created"),
            "category": job.get("category", {}).get("label"),
        })
    return job_data


DB_PARAMS = {
    "dbname": "job_scraper",
    "user": "ajay",
    "password": "mypass",
    "host": "localhost",
    "port": "5432"
}

def store_jobs(job_data):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    query = """
    INSERT INTO job_listings (title, company, location, salary_min, salary_max, description, post_date, category)
    VALUES %s
    """

    values = [(job["title"], job["company"], job["location"], job["salary_min"], 
               job["salary_max"], job["description"], job["post_date"], job["category"]) 
              for job in job_data]

    execute_values(cur, query, values)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    jobs = fetch_jobs()
    processed_jobs = process_jobs(jobs)
    store_jobs(processed_jobs)

