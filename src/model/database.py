"""SQLite data access for calculation history."""
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "calculator.db")


def get_connection():
    """Open a connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the calculation history table if it does not exist."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_record(expression, result):
    """Insert a calculation record and return it as a dict."""
    conn = get_connection()
    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.execute(
            "INSERT INTO calculation_history (expression, result, created_at)"
            " VALUES (?, ?, ?)",
            (expression, result, created_at),
        )
        conn.commit()
        return {
            "id": cursor.lastrowid,
            "expression": expression,
            "result": result,
            "created_at": created_at,
        }
    finally:
        conn.close()


def fetch_all_records():
    """Return all history records, newest first."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, expression, result, created_at"
            " FROM calculation_history ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def delete_record(record_id):
    """Delete one record by id. Returns True if a row was removed."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM calculation_history WHERE id = ?", (record_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def clear_all_records():
    """Delete every history record. Returns the number of rows removed."""
    conn = get_connection()
    try:
        cursor = conn.execute("DELETE FROM calculation_history")
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
