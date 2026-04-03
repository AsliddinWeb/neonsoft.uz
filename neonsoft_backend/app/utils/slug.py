import re
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def slugify(text: str) -> str:
    text = text.lower().strip()
    # Transliterate common Uzbek/Cyrillic chars
    replacements = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
        "ğ": "g", "ş": "sh", "ç": "ch", "ı": "i", "ö": "o", "ü": "u",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text


async def generate_unique_slug(
    db: AsyncSession,
    model,
    title: str,
    exclude_id: Optional[int] = None,
) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 2

    while True:
        query = select(model).where(model.slug == slug)
        if exclude_id is not None:
            query = query.where(model.id != exclude_id)
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        if not existing:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1
