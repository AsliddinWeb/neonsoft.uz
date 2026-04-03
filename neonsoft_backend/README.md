# NeonSoft Backend API

FastAPI + PostgreSQL + SQLAlchemy 2.x (async) backend for NeonSoft.uz

---

## Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.12 |
| FastAPI | ≥ 0.111 |
| SQLAlchemy | 2.x (async) |
| asyncpg | PostgreSQL async driver |
| Alembic | Migrations |
| python-jose | JWT tokens |
| passlib[bcrypt] | Password hashing |
| Docker / Compose | Containerization |

---

## Setup

### 1. `.env` faylini yarating

```bash
cp .env.example .env
```

`.env` ni to'ldiring:

```env
APP_ENV=local
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

POSTGRES_USER=neonsoft
POSTGRES_PASSWORD=strongpassword
POSTGRES_DB=neonsoft_db
DB_PORT=5432

API_PORT=8000

ALLOWED_ORIGINS=http://localhost:5173,https://neonsoft.uz

MEDIA_DIR=media
MEDIA_URL=/media

SUPERADMIN_EMAIL=admin@neonsoft.uz
SUPERADMIN_PASSWORD=Admin@12345
SUPERADMIN_NAME=Super Admin
```

---

## Commands

### Local ishga tushirish

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.local.yml up --build
```

### Production

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

### Migration — local

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.local.yml exec api alembic upgrade head
```

### Migration — prod

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.prod.yml exec api alembic upgrade head
```

### Yangi migration yaratish

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.local.yml exec api \
  alembic revision --autogenerate -m "describe changes"
```

---

### Superadmin yaratish

```bash
# Local
cd docker
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.local.yml exec api python seed.py

# Prod
docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.prod.yml exec api python seed.py
```

---

## API Documentation

Dastur ishga tushgandan so'ng:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/login` | Login → access + refresh token |
| POST | `/api/auth/refresh` | Refresh token → yangi access token |
| GET | `/api/auth/me` | Joriy foydalanuvchi |

### Public
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/services` | Faol xizmatlar |
| GET | `/api/services/{slug}` | Xizmat detail |
| GET | `/api/projects?featured=true&page=1&limit=10` | Loyihalar |
| GET | `/api/projects/{slug}` | Loyiha detail |
| GET | `/api/team` | Jamoa a'zolari |
| GET | `/api/blog?page=1&limit=10&tag=xyz` | Blog postlar |
| GET | `/api/blog/{slug}` | Blog post (views++) |
| POST | `/api/contact` | Xabar yuborish |
| GET | `/api/settings` | Sayt sozlamalari |

### Admin (Bearer token kerak)
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/api/admin/services` | Xizmatlar boshqaruvi |
| PUT/DELETE | `/api/admin/services/{id}` | Xizmat tahrirlash/o'chirish |
| GET/POST | `/api/admin/projects` | Loyihalar boshqaruvi |
| PUT/DELETE | `/api/admin/projects/{id}` | Loyiha tahrirlash/o'chirish |
| GET/POST | `/api/admin/team` | Jamoa boshqaruvi |
| PUT/DELETE | `/api/admin/team/{id}` | A'zo tahrirlash/o'chirish |
| GET/POST | `/api/admin/blog` | Blog boshqaruvi |
| PUT/DELETE | `/api/admin/blog/{id}` | Post tahrirlash/o'chirish |
| GET | `/api/admin/contacts` | Xabarlar ro'yxati |
| PATCH | `/api/admin/contacts/{id}/read` | O'qilgan deb belgilash |
| DELETE | `/api/admin/contacts/{id}` | Xabar o'chirish |
| GET/PUT | `/api/admin/settings` | Sayt sozlamalari |
| POST | `/api/upload/image` | Rasm yuklash |

### Superadmin only
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/api/admin/users` | Foydalanuvchilar |
| PATCH | `/api/admin/users/{id}/toggle-active` | Aktivlik holati |
| DELETE | `/api/admin/users/{id}` | Foydalanuvchi o'chirish |

---

## Project Structure

```
neonsoft_backend/
├── app/
│   ├── main.py           # FastAPI app, routers, middleware
│   ├── config.py         # Pydantic BaseSettings (.env)
│   ├── database.py       # Async engine, session, Base
│   ├── dependencies.py   # get_current_user, get_superadmin
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic schemas (in/out)
│   ├── routers/          # API route handlers
│   └── utils/
│       ├── security.py   # JWT, password hashing
│       └── slug.py       # Slug generator
├── docker/
│   ├── docker-compose.yml        # Base
│   ├── docker-compose.local.yml  # Local (--reload, ports)
│   └── docker-compose.prod.yml   # Prod (--workers 4, restart)
├── alembic/              # DB migrations
├── Dockerfile
├── seed.py               # Superadmin yaratish
├── requirements.txt
├── .env.example
└── README.md
```

---

## Notes

- `DATABASE_URL` Docker compose `environment:` orqali inject qilinadi, `.env`dan emas
- `media/` papkasi Docker volume sifatida mount — konteyner o'chsa ham fayllar saqlanadi
- Pagination: `page` + `limit` (max 50)
- Slug: title'dan auto-generatsiya, mavjud bo'lsa `-2`, `-3` qo'shiladi
- `SiteSetting` — singleton (faqat 1 qator, get_or_create pattern)
- Blog `GET /{slug}` — views avtomatik +1 (atomic UPDATE)
- `.env` `.gitignore`da — faqat `.env.example` commit qilinadi
