import unittest

from core.scoring import rank_leads


class LeadScoringTests(unittest.TestCase):
    def test_matching_city_and_clues_rank_first(self):
        cases = [
            {"case_id": "VC-1", "title": "Closest", "city": "Miami, FL", "photo_path": None, "evidence_terms": "red jacket, backpack"},
            {"case_id": "VC-2", "title": "Other", "city": "Boston, MA", "photo_path": None, "evidence_terms": "blue car"},
        ]
        report = {"location": "Miami, FL", "photo_path": None, "evidence_terms": "red jacket, backpack"}
        leads = rank_leads(cases, report)
        self.assertEqual(leads[0]["case_id"], "VC-1")
        self.assertEqual(leads[0]["score"], 45)
