# CodeArena — Developer Challenge Lab

A portfolio project designed around software engineering fundamentals: Python, REST APIs, test-case evaluation, debugging feedback, persistent submission records, and a live leaderboard.

## Features
- Three algorithm challenges: Two Sum, Valid Palindrome, First Unique Character
- Python editor with automated test cases and per-test execution timeout
- Flask REST endpoints for challenge listing, submissions, leaderboard and health checks
- SQLite submission history
- Live leaderboard and activity feed refreshed every five seconds
- Responsive HTML/CSS/JavaScript interface

## Run locally in VS Code
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `python -m pip install -r requirements.txt`
5. Run: `python app.py`
6. Visit `http://127.0.0.1:5000`.

The SQLite database is created automatically on first run.

## API endpoints
- `GET /health`
- `GET /api/challenges`
- `POST /api/submit`
- `GET /api/leaderboard`
- `GET /api/submissions`

## Security warning
This is a local portfolio demo, **not a production code execution service**. Submitted Python code runs as a subprocess with a timeout but is not isolated in a hardened sandbox. Use only locally with code you trust. Do not expose it to the public internet or accept untrusted submissions without container/OS sandboxing, resource limits, authentication, and a security review.

## Resume bullets — add only after running and verifying
**CodeArena — Coding Challenge & Test Automation Platform | Python, Flask, REST APIs, SQLite, JavaScript**
- Built a coding challenge web app with a Python editor and automated evaluation across predefined test cases.
- Developed REST endpoints for challenge retrieval, submission processing, health checks, and persistent submission history.
- Implemented a live leaderboard and recent-submission feed using SQLite and periodic client-side refresh.
