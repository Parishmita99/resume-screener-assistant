
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).with_name("resume_screener.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the analyses table if it does not already exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_analysis(report):
    """Save a validated Pydantic report to SQLite."""
    report_data = report.model_dump()

    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO analyses (
                candidate_name,
                match_score,
                report_json,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            report_data["candidate_name"],
            report_data["match_score"],
            json.dumps(report_data),
            datetime.now().isoformat(timespec="seconds")
        ))

        return cursor.lastrowid


def get_analyses(candidate_name="", min_score=0, max_score=100):
    """Retrieve saved analyses with optional name and score filters."""
    query = """
        SELECT id, candidate_name, match_score, report_json, created_at
        FROM analyses
        WHERE match_score BETWEEN ? AND ?
    """
    params = [min_score, max_score]

    if candidate_name.strip():
        query += " AND candidate_name LIKE ?"
        params.append(f"%{candidate_name.strip()}%")

    query += " ORDER BY created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    results = []

    for row in rows:
        results.append({
            "id": row[0],
            "candidate_name": row[1],
            "match_score": row[2],
            "report": json.loads(row[3]),
            "created_at": row[4]
        })

    return results
