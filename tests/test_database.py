"""Focused tests for Vigilantae's database layer using an isolated SQLite file."""

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from sqlmodel import create_engine

from pages.helper import db_queries
from pages.helper.data_models import PublicSubmissions, RegisteredCases


def registered_case(case_id: str, city: str, status: str = "NF") -> RegisteredCases:
    return RegisteredCases(
        id=case_id,
        submitted_by="officer_1",
        name="Test Person",
        guardian_name="Test Guardian",
        age="22",
        complainant_name="Test Complainant",
        complainant_mobile="9876543210",
        complainant_email="test@example.com",
        case_reference="VIG-DEMO-001",
        last_seen="Central Station",
        address="Test Address",
        city=city,
        description="Automated test record",
        face_mesh=json.dumps([0.1, 0.2, 0.3]),
        submitted_on=datetime.now(timezone.utc).replace(tzinfo=None),
        status=status,
        birth_marks="None",
        matched_with="",
    )


class DatabaseQueriesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test.sqlite"
        self.previous_engine = db_queries.engine
        db_queries.engine = create_engine(f"sqlite:///{database_path}")
        RegisteredCases.__table__.create(db_queries.engine)
        PublicSubmissions.__table__.create(db_queries.engine)

    def tearDown(self):
        db_queries.engine.dispose()
        db_queries.engine = self.previous_engine
        self.temp_dir.cleanup()

    def test_register_fetch_and_city_counts(self):
        db_queries.register_new_case(registered_case("case-1", "Kochi", "NF"))
        db_queries.register_new_case(registered_case("case-2", "Kochi", "F"))

        active_cases = db_queries.fetch_registered_cases("officer_1", "Not Found")
        self.assertEqual(len(active_cases), 1)
        self.assertEqual(active_cases[0][0], "case-1")

        counts = db_queries.get_case_counts_by_city()
        self.assertEqual(counts["Kochi"], {"found": 1, "not_found": 1})

    def test_match_status_updates_both_records(self):
        db_queries.register_new_case(registered_case("case-1", "Kochi"))
        db_queries.new_public_case(
            PublicSubmissions(
                id="sighting-1",
                submitted_by="Witness",
                face_mesh=json.dumps([0.1, 0.2, 0.3]),
                location="Kochi",
                mobile="9876543210",
                email="witness@example.com",
                status="NF",
                birth_marks="None",
            )
        )

        db_queries.update_found_status("case-1", "sighting-1")

        found_cases = db_queries.fetch_registered_cases("officer_1", "Found")
        public_cases = db_queries.fetch_public_cases(False, "All")
        self.assertEqual(found_cases[0][3], "F")
        self.assertEqual(found_cases[0][5], "sighting-1")
        self.assertEqual(public_cases[0][1], "F")


if __name__ == "__main__":
    unittest.main()
