"""Persistence designed specifically for Vigilantae's review workflow."""

import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path


DATABASE_PATH = Path("data/vigilantae.db")


class CaseStore:
    def __init__(self, database_path: Path | str = DATABASE_PATH):
        self.database_path = Path(database_path)

    def initialize(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS operators (
                    username TEXT PRIMARY KEY, display_name TEXT NOT NULL,
                    password_digest TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY, title TEXT NOT NULL, age INTEGER,
                    guardian TEXT, contact_phone TEXT, city TEXT NOT NULL,
                    last_known_location TEXT NOT NULL, notes TEXT, status TEXT NOT NULL,
                    photo_path TEXT, evidence_terms TEXT, created_by TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reports (
                    report_id TEXT PRIMARY KEY, case_id TEXT, observer TEXT NOT NULL,
                    contact TEXT, location TEXT NOT NULL, details TEXT, state TEXT NOT NULL,
                    photo_path TEXT, evidence_terms TEXT, created_at TEXT NOT NULL, reviewed_at TEXT
                );
            """)
            self._add_column_if_missing(db, "cases", "photo_path", "TEXT")
            self._add_column_if_missing(db, "reports", "photo_path", "TEXT")
            self._add_column_if_missing(db, "cases", "evidence_terms", "TEXT")
            self._add_column_if_missing(db, "reports", "evidence_terms", "TEXT")

    @staticmethod
    def _add_column_if_missing(db, table: str, column: str, definition: str):
        columns = {row[1] for row in db.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.database_path)
        db.row_factory = sqlite3.Row
        try:
            yield db
            db.commit()
        finally:
            db.close()

    def one(self, sql, values=()):
        with self.connection() as db:
            row = db.execute(sql, values).fetchone()
        return dict(row) if row else None

    def many(self, sql, values=()):
        with self.connection() as db:
            rows = db.execute(sql, values).fetchall()
        return [dict(row) for row in rows]

    def execute(self, sql, values=()):
        with self.connection() as db:
            db.execute(sql, values)

    def create_case(self, record: dict):
        record.setdefault("photo_path", None)
        record.setdefault("evidence_terms", "")
        self.execute(
            """INSERT INTO cases
            (case_id, title, age, guardian, contact_phone, city, last_known_location, notes, status, photo_path, evidence_terms, created_by, created_at)
            VALUES (:case_id, :title, :age, :guardian, :contact_phone, :city, :last_known_location, :notes, 'Open', :photo_path, :evidence_terms, :created_by, :created_at)""",
            record,
        )

    def create_report(self, record: dict):
        record.setdefault("photo_path", None)
        record.setdefault("evidence_terms", "")
        self.execute(
            """INSERT INTO reports
            (report_id, case_id, observer, contact, location, details, state, photo_path, evidence_terms, created_at)
            VALUES (:report_id, :case_id, :observer, :contact, :location, :details, 'Pending', :photo_path, :evidence_terms, :created_at)""",
            record,
        )

    def assign_report(self, report_id: str, case_id: str):
        self.execute(
            "UPDATE reports SET case_id = ?, state = 'Reviewed', reviewed_at = ? WHERE report_id = ?",
            (case_id, self.now(), report_id),
        )

    def set_case_status(self, case_id: str, status: str):
        self.execute("UPDATE cases SET status = ? WHERE case_id = ?", (status, case_id))

    @staticmethod
    def now():
        return datetime.now(UTC).isoformat()
