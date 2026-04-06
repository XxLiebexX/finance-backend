from fastapi import FastAPI
from database import engine, Base
from routers import users, records, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend for finance dashboard with role-based access control",
    version="1.0.0"
)

app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(records.router, prefix="/records", tags=["Financial Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {
        "message": "Finance Dashboard API",
        "docs": "/docs",
        "roles": ["admin", "analyst", "viewer"]
    }