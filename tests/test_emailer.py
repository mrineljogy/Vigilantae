"""Email notification behavior is tested without contacting a real SMTP server."""

import unittest
from unittest.mock import MagicMock, patch

from pages.helper import emailer


class EmailerTests(unittest.TestCase):
    def test_skips_when_smtp_is_not_configured(self):
        with patch.object(emailer, "_setting", return_value=None):
            self.assertFalse(emailer.send_match_notification("case-1", ("Person",)))

    def test_sends_when_smtp_is_configured(self):
        settings = {
            "SMTP_HOST": "smtp.example.com",
            "SMTP_PORT": "587",
            "SMTP_USER": "operations@example.com",
            "SMTP_PASSWORD": "app-password",
            "NOTIFY_EMAIL": "fallback@example.com",
        }

        with patch.object(emailer, "_setting", side_effect=lambda key, default=None: settings.get(key, default)):
            with patch("smtplib.SMTP") as smtp:
                server = MagicMock()
                smtp.return_value.__enter__.return_value = server
                sent = emailer.send_match_notification(
                    "case-1",
                    ("Test Person", "9876543210", "case@example.com", "22", "Kochi", "None"),
                )

        self.assertTrue(sent)
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("operations@example.com", "app-password")
        server.sendmail.assert_called_once()


if __name__ == "__main__":
    unittest.main()
