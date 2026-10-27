import os
import csv
import psycopg2
from dotenv import load_dotenv

# 1. Read database connection
load_dotenv()
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL not found in .env")

# 2. Connect to Neon PostgreSQL
conn = psycopg2.connect(database_url)

columns = [
    "netid",
    "name",
    "school_year",
    "intro_programming",
    "skill_programming",
    "skill_data_stats",
    "skill_frontend_design",
    "skill_business_pitch",
    "tools",
    "availability",
    "working_style",
    "interests",
    "semester_goal",
    "submitted_at",
]

try:
    with conn.cursor() as cursor:
        # 3. Create table using schema.sql
        with open("schema.sql", "r", encoding="utf-8") as f:
            cursor.execute(f.read())

        print("Table created successfully!")

        # 4. Check for existing data
        cursor.execute("SELECT COUNT(*) FROM students")
        existing = cursor.fetchone()[0]

        if existing > 0:
            raise ValueError(
                f"Table already contains {existing} rows. "
                "Import cancelled to prevent duplicates."
            )

        # 5. Read and import CSV
        with open("data/class_dataset.csv", "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames != columns:
                raise ValueError("CSV columns do not match schema")

            sql = """
                INSERT INTO students (
                    netid, name, school_year,
                    intro_programming, skill_programming,
                    skill_data_stats, skill_frontend_design,
                    skill_business_pitch, tools,
                    availability, working_style,
                    interests, semester_goal, submitted_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
            """

            count = 0

            for row in reader:
                values = [row[col] for col in columns]
                cursor.execute(sql, values)
                count += 1

        # 6. Verify imported rows
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]

        conn.commit()

        print(f"Imported {count} rows successfully!")
        print(f"Total rows in database: {total}")

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
