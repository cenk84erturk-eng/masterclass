import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    return json.loads(TASKS_FILE.read_text())


def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


@app.route("/")
def index():
    return render_template("index.html", tasks=load_tasks())


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        next_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": next_id, "title": title})
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
