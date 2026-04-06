from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from auth import get_current_user, require_role
import models

router = APIRouter()

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    total_income = sum(r.amount for r in records if r.type == "income")
    total_expense = sum(r.amount for r in records if r.type == "expense")
    net_balance = total_income - total_expense

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expense, 2),
        "net_balance": round(net_balance, 2),
        "total_records": len(records)
    }

@router.get("/category-totals")
def get_category_totals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "analyst"))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    totals = {}
    for r in records:
        if r.category not in totals:
            totals[r.category] = {"income": 0, "expense": 0}
        totals[r.category][r.type] += r.amount

    return totals

@router.get("/monthly-trends")
def get_monthly_trends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "analyst"))
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    trends = {}
    for r in records:
        month = r.date[:7]  # YYYY-MM
        if month not in trends:
            trends[month] = {"income": 0, "expense": 0}
        trends[month][r.type] += r.amount

    return dict(sorted(trends.items()))

@router.get("/recent")
def get_recent(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).order_by(models.FinancialRecord.created_at.desc()).limit(10).all()
    return records