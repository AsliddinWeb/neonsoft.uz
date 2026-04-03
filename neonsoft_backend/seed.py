"""
Superadmin yaratish skripti.
Ishlatish: docker compose exec api python seed.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models import *  # noqa: F401, F403 — all models must be imported
from app.models.user import User, UserRole
from app.utils.security import hash_password


async def seed() -> None:
    if not settings.SUPERADMIN_EMAIL:
        print("ERROR: SUPERADMIN_EMAIL is not set in .env")
        sys.exit(1)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == settings.SUPERADMIN_EMAIL)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"[SKIP] Superadmin already exists: {settings.SUPERADMIN_EMAIL}")
            return

        superadmin = User(
            email=settings.SUPERADMIN_EMAIL,
            password_hash=hash_password(settings.SUPERADMIN_PASSWORD),
            full_name=settings.SUPERADMIN_NAME or "Super Admin",
            role=UserRole.superadmin,
            is_active=True,
        )
        db.add(superadmin)
        await db.commit()
        print(f"[OK] Superadmin created: {settings.SUPERADMIN_EMAIL}")


if __name__ == "__main__":
    asyncio.run(seed())
