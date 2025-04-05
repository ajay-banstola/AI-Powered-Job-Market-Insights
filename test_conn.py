import psycopg2

DB_PARAMS = {
    "dbname": "job_scraper",
    "user": "ajay",
    "password": "mypass",
    "host": "localhost",
    "port": "5432"
}

try:
    conn = psycopg2.connect(**DB_PARAMS)
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print("Error connecting to database:", e)

