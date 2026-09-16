# FlowForge API

Server-driven UI configuration platform built with FastAPI and PostgreSQL.

## Architecture
- **Backend:** FastAPI, Python, SQLAlchemy 2.x, PostgreSQL
- **Config:** Dynamic forms, pages, layouts, and components served to frontend
- **Auth:** JWT and Role-Based Access Control

## Installation & Running

1. `docker compose up --build -d`
2. Apply migrations: `docker compose exec api alembic upgrade head`
3. View OpenAPI docs at `http://localhost:8000/docs`

