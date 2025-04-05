DB_PARAMS = {
    "dbname": "job_scraper",
    "user": "ajay",
    "password": "mypass",
    "host": "localhost",
    "port": "5432"
}

import re
from datetime import datetime
from dateutil.parser import parse
import requests
import psycopg2
from psycopg2.extras import execute_values

def clean_description(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Lowercase
    text = text.lower()
    # Remove non-word characters
    text = re.sub(r"[^\w\s]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_avg_salary(min_salary, max_salary):
    if min_salary and max_salary:
        return (min_salary + max_salary) / 2
    elif min_salary:
        return min_salary
    elif max_salary:
        return max_salary
    else:
        return None



def parse_date(value):
    if isinstance(value, datetime):
        return value  # already parsed
    if not value:
        return None   # empty or null
    try:
        return parse(str(value))  # force string conversion
    except Exception as e:
        print("Failed to parse:", value, "| Error:", e)
        return None

def clean_and_update_jobs():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    cur.execute("SELECT id, description, salary_min, salary_max, avg_salary, post_date FROM job_listings")
    jobs = cur.fetchall()

    for job in jobs:
        job_id, desc, sal_min, sal_max, avg_salaary, created = job
        cleaned_desc = clean_description(desc)
        avg_salary = get_avg_salary(sal_min, sal_max)
        created_at = parse_date(created)

        # Update the job record
        cur.execute("""
            UPDATE job_listings
            SET description = %s,
                salary_min = %s,
                salary_max = %s,
                avg_salary = %s,
                post_date = %s
            WHERE id = %s
        """, (cleaned_desc, sal_min, sal_max, avg_salary, created_at, job_id))

    conn.commit()
    print('done')
    cur.close()
    conn.close()


clean_and_update_jobs()

