import psycopg2


DB_PARAMS = {
    "dbname": "job_scraper",
    "user": "ajay",
    "password": "mypass",
    "host": "localhost",
    "port": "5432"
}


def create_table():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS job_listings (
        id SERIAL PRIMARY KEY,
        title TEXT,
        company TEXT,
        location TEXT,
        salary_min FLOAT,
        salary_max FLOAT,
        avg_salary FLOAT,
        description TEXT,
        post_date TIMESTAMP,
        category TEXT
    );
    """
    
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully!")

create_table()

