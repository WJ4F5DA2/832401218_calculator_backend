# 832401218 Calculator Backend

The **back end** of a front-end/back-end separated calculator system,
built with Flask + SQLite.
It parses and evaluates expressions, persists calculation history,
and exposes HTTP/JSON APIs.

## Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python 3.10+ |
| Web framework | Flask 3.x |
| Database | SQLite (stdlib sqlite3, no extra install) |
| Expression parsing | Hand-written tokenizer + recursive-descent parser (no eval/exec) |

## Runtime Environment

- Python 3.10 or higher
- No other system dependencies (SQLite ships with Python)

## Installation and Startup

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the service (defaults to 0.0.0.0:5000)
python run.py
```

Once started, verify with `GET http://localhost:5000/api/health`.

## Deployment

The service is deployed on **PythonAnywhere** (free tier):

- **Live API**: https://wj4f5da2.pythonanywhere.com/api
- Health check: `GET https://wj4f5da2.pythonanywhere.com/api/health`
- The front end is served from the same host via a static-files mapping:
  https://wj4f5da2.pythonanywhere.com/

## Database Initialization

No manual setup is needed: on first start the service creates `calculator.db`
in the project root and creates the table automatically.

```sql
CREATE TABLE calculation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT NOT NULL,   -- e.g. (1+2)*3
    result TEXT NOT NULL,       -- e.g. 9
    created_at TEXT NOT NULL    -- e.g. 2026-10-03 19:33:55
);
```

To reset the data, simply delete `calculator.db` and restart the service.

## API Overview

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| POST | `/api/calculate` | Evaluate an expression and store the record |
| GET | `/api/history` | Return all history records (newest first) |
| DELETE | `/api/history/{id}` | Delete one history record |
| DELETE | `/api/history` | Clear all history records (optional feature) |

### Calculate Request Example

Request: `POST /api/calculate`

```json
{ "expression": "(1+2)*3" }
```

Success response (HTTP 200):

```json
{ "success": true, "expression": "(1+2)*3", "result": "9", "id": 1, "created_at": "2026-10-03 19:33:55" }
```

Error response (HTTP 400, e.g. division by zero or invalid expression):

```json
{ "success": false, "message": "Division by zero" }
```

## How the Front End Connects

- The service listens on `0.0.0.0:5000` by default and sends CORS headers,
  so any front end can call it cross-origin.
- Point the front end's API configuration (`API_BASE` in `script.js`)
  at this service's `/api` prefix, e.g. `http://localhost:5000/api`.
- After deployment, just change `API_BASE` to the public back-end URL
  (currently `https://wj4f5da2.pythonanywhere.com/api`).

## Project Structure

```
832401218_calculator_backend/
├── run.py                     # Entry point
├── requirements.txt
├── src/
│   ├── app.py                 # Flask application factory (with CORS)
│   ├── controller/routes.py   # HTTP routes
│   ├── service/
│   │   ├── calculator_service.py  # Expression tokenizer + recursive-descent parser
│   │   └── history_service.py     # Calculation and history business logic
│   └── model/database.py      # SQLite data access layer
└── test_api.py                # API smoke tests (Flask test client)
```

## Testing

```bash
python test_api.py
```

Covers: basic arithmetic, compound expressions (precedence, parentheses,
unary +/-, decimals), invalid expressions, division by zero, history
insert/query/delete, and clearing history.
