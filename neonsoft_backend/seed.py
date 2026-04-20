"""
Production seed script.
Usage: docker compose exec api python seed.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models import *  # noqa: F401, F403
from app.models.user import User, UserRole
from app.models.service import Service
from app.models.about import About
from app.models.site_setting import SiteSetting
from app.utils.security import hash_password
from app.utils.slug import generate_unique_slug


async def seed_superadmin(db) -> None:
    if not settings.SUPERADMIN_EMAIL:
        return
    result = await db.execute(select(User).where(User.email == settings.SUPERADMIN_EMAIL))
    if result.scalar_one_or_none():
        print(f"[SKIP] Superadmin: {settings.SUPERADMIN_EMAIL}")
        return
    db.add(User(
        email=settings.SUPERADMIN_EMAIL,
        password_hash=hash_password(settings.SUPERADMIN_PASSWORD),
        full_name=settings.SUPERADMIN_NAME or "Super Admin",
        role=UserRole.superadmin,
        is_active=True,
    ))
    print(f"[OK] Superadmin: {settings.SUPERADMIN_EMAIL}")


async def seed_settings(db) -> None:
    result = await db.execute(select(SiteSetting))
    if result.scalar_one_or_none():
        print("[SKIP] Site settings")
        return
    db.add(SiteSetting(
        company_name="NeonSoft IT Solutions",
        tagline="Biz kelajakni yaratamiz",
        description="NeonSoft — O'zbekistonda raqamli yechimlar yaratuvchi texnologik kompaniya. "
                    "Startapdan yirik korporatsiyagacha — har qanday biznesni raqamlashtirish bo'yicha ishonchli hamkoringiz.",
        email="hello@neonsoft.uz",
        phone="+998 94 202 55 11",
        address="Toshkent sh., Mirzo Ulug'bek tumani, Amir Temur shoh ko'chasi 108",
        telegram="https://t.me/neonsoft_uz",
        instagram="https://instagram.com/neonsoft.uz",
        linkedin="https://linkedin.com/company/neonsoft-uz",
        github="https://github.com/neonsoft-uz",
        meta_title="NeonSoft — IT Kompaniya | Sayt, Ilova va Biznes Yechimlar",
        meta_description="NeonSoft — O'zbekistonda web saytlar, mobil ilovalar, Telegram botlar va biznes avtomatizatsiyasi. Bepul konsultatsiya olish uchun bog'laning.",
        meta_keywords="NeonSoft, IT kompaniya, sayt yaratish, mobil ilova, Telegram bot, biznes avtomatizatsiya, Toshkent",
    ))
    print("[OK] Site settings")


async def seed_about(db) -> None:
    result = await db.execute(select(About))
    if result.scalar_one_or_none():
        print("[SKIP] About")
        return
    db.add(About(
        title="NeonSoft",
        subtitle="texnologiya orqali o'sish",
        description="Biz shunchaki kod yozmaymiz — biznesingiz uchun ishlaydigon mahsulot yaratamiz. "
                    "Har bir loyihani chuqur tahlil qilamiz, mijoz maqsadini tushunamiz va natijaga "
                    "yo'naltirilgan yechim taklif etamiz. 3 yildan ortiq tajriba, 50+ muvaffaqiyatli "
                    "loyiha va 30+ mamnun mijoz — bu bizning ishonch kafolatimiz.",
        stat_projects=50,
        stat_clients=30,
        stat_years=3,
        stat_team=12,
    ))
    print("[OK] About")


SERVICES_DATA = [
    {
        "title": "Web Dasturlash",
        "icon": "Globe",
        "short_description": "Tez, zamonaviy va foydalanuvchiga qulay web platformalar",
        "description": "Korporativ saytdan tortib murakkab CRM tizimlarigacha — Vue.js, React, Django va FastAPI "
                       "texnologiyalari asosida responsive, SEO-optimallashtirilgan va yuqori tezlikdagi web "
                       "ilovalar ishlab chiqamiz. Har bir piksel puxta o'ylab chiqiladi.",
        "order": 1,
    },
    {
        "title": "Mobil Ilovalar",
        "icon": "Smartphone",
        "short_description": "iOS va Android uchun bitta koddan ishlaydigan ilovalar",
        "description": "Flutter va React Native yordamida ikkala platforma uchun tez va sifatli mobil ilovalar "
                       "yaratamiz. UI/UX dizayndan App Store va Play Market'ga joylashtirishgacha — to'liq tsikl "
                       "xizmati. Push-bildirishnomalar, oflayn rejim va real vaqt sinxronizatsiya.",
        "order": 2,
    },
    {
        "title": "Biznes Avtomatizatsiyasi",
        "icon": "Settings",
        "short_description": "Jarayonlarni raqamlashtiring — vaqt va pul tejang",
        "description": "Ombor hisobi, mijozlar bazasi, xodimlar boshqaruvi, hisobotlar — bularning barchasini "
                       "qo'lda qilishni to'xtating. Biznesingizga moslashtirilgan ERP va CRM tizimlarini ishlab "
                       "chiqamiz. Avtomatizatsiya orqali xarajatlarni 40% gacha kamaytirish mumkin.",
        "order": 3,
    },
    {
        "title": "Telegram Bot Yaratish",
        "icon": "Bot",
        "short_description": "Mijozlaringiz bilan 24/7 aloqada bo'ling",
        "description": "Buyurtma qabul qilish, to'lov tizimi, mijozlar qo'llab-quvvatlashi va ichki jarayonlarni "
                       "boshqarish uchun aqlli Telegram botlar yaratamiz. Payme, Click integratsiyasi, admin "
                       "panel va analitika bilan to'liq yechim.",
        "order": 4,
    },
]


async def seed_services(db) -> None:
    result = await db.execute(select(Service))
    if result.scalars().first():
        print("[SKIP] Services")
        return
    for data in SERVICES_DATA:
        slug = await generate_unique_slug(db, Service, data["title"])
        db.add(Service(slug=slug, is_active=True, **data))
    print(f"[OK] Services ({len(SERVICES_DATA)})")


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        await seed_superadmin(db)
        await seed_settings(db)
        await seed_about(db)
        await seed_services(db)
        await db.commit()
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(seed())
