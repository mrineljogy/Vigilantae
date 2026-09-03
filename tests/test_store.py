import tempfile
import unittest
from pathlib import Path

from core.store import CaseStore


class CaseStoreTests(unittest.TestCase):
    def test_case_and_report_can_be_reviewed(self):
        with tempfile.TemporaryDirectory() as folder:
            store = CaseStore(Path(folder) / "console.db")
            store.initialize()
            store.create_case({"case_id": "VC-TEST", "title": "Test record", "age": 18, "guardian": "", "contact_phone": "", "city": "Chicago, IL", "last_known_location": "Station", "notes": "", "photo_path": None, "created_by": "tester", "created_at": store.now()})
            store.create_report({"report_id": "VR-TEST", "case_id": None, "observer": "Witness", "contact": "", "location": "Chicago, IL", "details": "Saw subject", "photo_path": None, "created_at": store.now()})
            store.assign_report("VR-TEST", "VC-TEST")
            store.set_case_status("VC-TEST", "Resolved")
            self.assertEqual(store.one("SELECT status FROM cases WHERE case_id = 'VC-TEST'")["status"], "Resolved")
            self.assertEqual(store.one("SELECT state FROM reports WHERE report_id = 'VR-TEST'")["state"], "Reviewed")
