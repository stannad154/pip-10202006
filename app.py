import os
import psycopg2
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    database_url = os.getenv("DATABASE_URL")

    with psycopg2.connect(database_url) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT name FROM students ORDER BY name")
        names = [row[0] for row in cursor.fetchall()]

    return render_template("index.html", names=names)


if __name__ == "__main__":
    app.run(debug=True)
