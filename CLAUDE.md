# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install deps: `pip install -r requirements.txt`
- Run the app: `python3 app.py` — serves at http://127.0.0.1:5000 in debug mode (auto-reloads on edit).

No test suite or linter is configured yet.

## Architecture

A minimal Flask to-do app rendered server-side. The entire backend lives in `app.py`:

- **Storage is a flat JSON file** (`tasks.json`, auto-created on first write), read/written in full by `load_tasks()` / `save_tasks()`. There is no database. Each task is `{"id": int, "title": str}`; new ids are assigned as `max(existing ids) + 1`.
- **Two routes drive everything**: `GET /` renders `templates/index.html` with the task list; `POST /add` appends a task and redirects back to `/` (post/redirect/get). Adding a feature like delete or mark-complete means a new route plus a form in the template — the `id` field exists to make those addressable.
- Templates use Jinja2; `index.html` is the only page.
