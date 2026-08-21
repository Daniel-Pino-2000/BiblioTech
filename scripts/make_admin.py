"""
Promote an existing user to admin.

Deliberately a CLI script and not an HTTP endpoint: granting admin is a
privileged, infrequent operation, so it shouldn't be reachable from the
running app at all -- only from whoever has direct access to the database
(or its connection string).

Usage:
    python scripts/make_admin.py <username>

Runs against whatever DATABASE_URL/.env is active, so it works the same way
locally or against a deployed database (point DATABASE_URL at it temporarily).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models.user import User  # noqa: E402


def make_admin(username: str) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"No user found with username '{username}'.")
            raise SystemExit(1)
        if user.is_admin:
            print(f"'{username}' is already an admin.")
            return
        user.is_admin = True
        db.commit()
        print(f"'{username}' is now an admin.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username")
    args = parser.parse_args()
    make_admin(args.username)
