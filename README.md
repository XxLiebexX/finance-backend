# Finance Dashboard API

A backend REST API for a finance dashboard system with role-based access control.

## Tech Stack
- Python, FastAPI, SQLite, SQLAlchemy, JWT

## Roles
- **Admin** — full access
- **Analyst** — view records and dashboard
- **Viewer** — view dashboard only

## Setup
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

## API Docs
http://localhost:8000/docs

## Endpoints
- POST /auth/register
- POST /auth/login
- GET/POST/PUT/DELETE /records
- GET /dashboard/summary
- GET /dashboard/category-totals
- GET /dashboard/monthly-trends
- GET /dashboard/recent




start cmd>>
uvicorn main:app --reload --port 8000

start cmd for render>>
uvicorn main:app --host 0.0.0.0 --port $PORT

