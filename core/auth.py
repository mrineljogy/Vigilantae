"""Local operator authentication with PBKDF2 password digests."""

import hashlib
import hmac
import os


ITERATIONS = 310_000


def _digest(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    payload = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return f"{salt.hex()}${payload.hex()}"


def _matches(password: str, stored: str) -> bool:
    salt_hex, expected = stored.split("$", 1)
    candidate = _digest(password, bytes.fromhex(salt_hex)).split("$", 1)[1]
    return hmac.compare_digest(candidate, expected)


def bootstrap_admin(store):
    if not store.one("SELECT username FROM operators LIMIT 1"):
        store.execute(
            "INSERT INTO operators VALUES (?, ?, ?, ?)",
            ("admin", "System Administrator", _digest("ChangeMe!2026"), store.now()),
        )


def authenticate(store, username: str, password: str):
    user = store.one("SELECT * FROM operators WHERE username = ?", (username.strip(),))
    if user and _matches(password, user["password_digest"]):
        return {"username": user["username"], "display_name": user["display_name"]}
    return None


def change_password(store, username: str, current: str, new: str) -> bool:
    user = store.one("SELECT * FROM operators WHERE username = ?", (username,))
    if not user or len(new) < 10 or not _matches(current, user["password_digest"]):
        return False
    store.execute("UPDATE operators SET password_digest = ? WHERE username = ?", (_digest(new), username))
    return True
