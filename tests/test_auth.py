import tempfile
import unittest
from pathlib import Path

from core.auth import authenticate, bootstrap_admin, change_password
from core.store import CaseStore


class AuthenticationTests(unittest.TestCase):
    def test_bootstrap_password_can_be_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            store = CaseStore(Path(folder) / "console.db")
            store.initialize()
            bootstrap_admin(store)
            self.assertIsNotNone(authenticate(store, "admin", "ChangeMe!2026"))
            self.assertTrue(change_password(store, "admin", "ChangeMe!2026", "A safer passphrase"))
            self.assertIsNotNone(authenticate(store, "admin", "A safer passphrase"))
