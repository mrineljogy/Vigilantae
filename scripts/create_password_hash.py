"""Create a bcrypt password hash for login_config.yml without exposing the password."""

from getpass import getpass

import bcrypt


def main() -> None:
    password = getpass("New password: ")
    confirmation = getpass("Confirm password: ")

    if not password:
        print("No password entered. Nothing changed.")
        return
    if password != confirmation:
        print("Passwords did not match. Nothing changed.")
        return

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("\nCopy this entire line into login_config.yml as the password value:\n")
    print(f"'{password_hash}'")


if __name__ == "__main__":
    main()
