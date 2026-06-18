"""Delete spam / injection-attempt student accounts.

Reuses the same `looks_suspicious_user` heuristic the admin UI uses to flag
accounts (random names, SQL/script payloads in the email, etc.). Only ever
targets unverified student accounts; admins and verified users are never touched.

Dry-run by default — it prints what *would* be deleted. Pass --apply to delete.

    python scripts/cleanup_spam_users.py            # preview
    python scripts/cleanup_spam_users.py --apply    # actually delete
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.api.routes.admin_users import looks_suspicious_user
from app.db.session import get_sessionmaker
from app.repositories.users import USER_ROLE_ADMIN, UserRepository


def find_spam_users(db: Session) -> list:
    repository = UserRepository(db)
    # Pull a large page of the most recent accounts (spam arrives in bursts).
    users = repository.list_users(limit=1000, email_verified=False)
    return [
        user
        for user in users
        if user.role != USER_ROLE_ADMIN and looks_suspicious_user(user)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete. Without this flag the script only previews.",
    )
    args = parser.parse_args()

    with get_sessionmaker()() as db:
        spam_users = find_spam_users(db)

        if not spam_users:
            print("No spam users found.")
            return 0

        print(f"Found {len(spam_users)} suspicious unverified student account(s):")
        for user in spam_users:
            print(f"  - {user.id}  {user.email!r}  name={user.name!r}")

        if not args.apply:
            print("\nDry run. Re-run with --apply to delete these accounts.")
            return 0

        deleted = UserRepository(db).delete_users([user.id for user in spam_users])
        print(f"\nDeleted {len(deleted)} account(s).")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
