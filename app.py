import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DB_PATH = Path(__file__).parent / "tasks.db"


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with get_db() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, completed INTEGER NOT NULL DEFAULT 0)"
        )


init_db()


@app.route("/")
def index():
    with get_db() as db:
        tasks = db.execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        with get_db() as db:
            db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    with get_db() as db:
        db.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
