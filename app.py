from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import csv
import io
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

DB = os.path.join(os.path.dirname(__file__), "ongadi.db")


def db():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            school TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school TEXT,
            admission TEXT,
            name TEXT,
            grade TEXT,
            gender TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER,
            subject TEXT,
            score REAL,
            term TEXT,
            year INTEGER
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) AS n FROM users"
    ).fetchone()["n"]

    if count == 0:
        connection.execute(
            "INSERT INTO users(username,password,school) VALUES(?,?,?)",
            ("admin", "admin123", "Demo School")
        )

    connection.commit()
    connection.close()


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        connection = db()

        user = connection.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        connection.close()

        if user:
            session["user"] = user["username"]
            session["school"] = user["school"]

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():

    school = session["school"]

    connection = db()

    learners = connection.execute(
        "SELECT * FROM learners WHERE school=? ORDER BY name",
        (school,)
    ).fetchall()

    score_summary = connection.execute("""
        SELECT COUNT(*) AS n,
               COALESCE(AVG(score),0) AS avg
        FROM scores
        JOIN learners ON learners.id = scores.learner_id
        WHERE learners.school=?
    """, (school,)).fetchone()

    top = connection.execute("""
        SELECT learners.name,
               learners.grade,
               AVG(scores.score) AS avg
        FROM learners
        JOIN scores ON scores.learner_id = learners.id
        WHERE learners.school=?
        GROUP BY learners.id
        ORDER BY avg DESC
        LIMIT 5
    """, (school,)).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        learners=learners,
        scores=score_summary,
        top=top
    )


@app.route("/learners", methods=["GET", "POST"])
@login_required
def learners():

    school = session["school"]

    connection = db()

    if request.method == "POST":

        connection.execute("""
            INSERT INTO learners
            (school, admission, name, grade, gender)
            VALUES (?, ?, ?, ?, ?)
        """, (
            school,
            request.form["admission"],
            request.form["name"],
            request.form["grade"],
            request.form["gender"]
        ))

        connection.commit()

        flash("Learner added successfully.")

    learner_list = connection.execute(
        "SELECT * FROM learners WHERE school=? ORDER BY name",
        (school,)
    ).fetchall()

    connection.close()

    return render_template(
        "learners.html",
        learners=learner_list
    )


@app.route("/scores", methods=["GET", "POST"])
@login_required
def scores():

    school = session["school"]

    connection = db()

    learner_list = connection.execute(
        "SELECT * FROM learners WHERE school=? ORDER BY name",
        (school,)
    ).fetchall()

    if request.method == "POST":

        learner_id = int(request.form["learner_id"])
        subject = request.form["subject"]
        score = float(request.form["score"])
        term = request.form["term"]
        year = int(request.form["year"])

        if 0 <= score <= 100:

            connection.execute("""
                INSERT INTO scores
                (learner_id, subject, score, term, year)
                VALUES (?, ?, ?, ?, ?)
            """, (
                learner_id,
                subject,
                score,
                term,
                year
            ))

            connection.commit()

            flash("Score saved successfully.")

        else:

            flash("Score must be between 0 and 100.")

    score_list = connection.execute("""
        SELECT scores.*,
               learners.name,
               learners.admission
        FROM scores
        JOIN learners ON learners.id = scores.learner_id
        WHERE learners.school=?
        ORDER BY scores.id DESC
        LIMIT 100
    """, (school,)).fetchall()

    connection.close()

    return render_template(
        "scores.html",
        learners=learner_list,
        scores=score_list
    )


@app.route("/analysis")
@login_required
def analysis():

    school = session["school"]

    connection = db()

    subject_analysis = connection.execute("""
        SELECT subject,
               COUNT(*) AS n,
               ROUND(AVG(score),2) AS avg,
               ROUND(
                   SUM(
                       CASE
                           WHEN score >= 50 THEN 1
                           ELSE 0
                       END
                   ) * 100.0 / COUNT(*),1
               ) AS pass
        FROM scores
        JOIN learners ON learners.id = scores.learner_id
        WHERE learners.school=?
        GROUP BY subject
        ORDER BY subject
    """, (school,)).fetchall()

    learner_analysis = connection.execute("""
        SELECT learners.name,
               learners.grade,
               ROUND(AVG(scores.score),2) AS avg
        FROM learners
        JOIN scores ON scores.learner_id = learners.id
        WHERE learners.school=?
        GROUP BY learners.id
        ORDER BY avg DESC
    """, (school,)).fetchall()

    connection.close()

    return render_template(
        "analysis.html",
        rows=subject_analysis,
        learner=learner_analysis
    )


@app.route("/import", methods=["GET", "POST"])
@login_required
def import_csv():

    if request.method == "POST":

        file = request.files.get("file")

        if not file:
            flash("Please select a CSV file.")
            return redirect(url_for("import_csv"))

        text = file.read().decode("utf-8-sig")

        reader = csv.DictReader(io.StringIO(text))

        connection = db()

        school = session["school"]

        count = 0

        for row in reader:

            name = row.get("name", "").strip()

            if not name:
                continue

            cursor = connection.execute("""
                INSERT INTO learners
                (school, admission, name, grade, gender)
                VALUES (?, ?, ?, ?, ?)
            """, (
                school,
                row.get("admission", ""),
                name,
                row.get("grade", ""),
                row.get("gender", "")
            ))

            learner_id = cursor.lastrowid

            subjects = [
                "English",
                "Kiswahili",
                "Mathematics",
                "Integrated Science",
                "Social Studies",
                "Agriculture",
                "Pre-Technical Studies",
                "Creative Arts",
                "CRE"
            ]

            for subject in subjects:

                value = row.get(subject, "").strip()

                if value:

                    try:

                        connection.execute("""
                            INSERT INTO scores
                            (learner_id, subject, score, term, year)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            learner_id,
                            subject,
                            float(value),
                            row.get("term", "Term 1"),
                            int(row.get("year", "2026"))
                        ))

                    except ValueError:
                        pass

            count += 1

        connection.commit()
        connection.close()

        flash(f"Imported {count} learners.")

        return redirect(url_for("dashboard"))

    return render_template("import.html")


@app.route("/health")
def health():

    return {
        "status": "ok",
        "app": "ONGADI CBE ANALYSER"
    }


init_db()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
Step 3
Scroll down and tap Commit changes.
For the commit message, you can enter:
Add main ONGADI CBE ANALYSER application
Then commit the file.
After you have committed app.py, tell me “done”. I'll give you the next file, and we'll build the project directly inside your GitHub repository step-by-step.
