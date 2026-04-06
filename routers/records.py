from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from auth import get_current_user, require_role
import models, schemas

router = APIRouter()

# ── Create (Admin only) ───────────────────────────────────
@router.post("/", response_model=schemas.RecordResponse)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be income or expense")
    if record.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    new_record = models.FinancialRecord(**record.dict(), created_by=current_user.id)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# ── Read (All roles) ──────────────────────────────────────
@router.get("/")
def get_records(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    )
    if type: query = query.filter(models.FinancialRecord.type == type)
    if category: query = query.filter(models.FinancialRecord.category == category)
    if date_from: query = query.filter(models.FinancialRecord.date >= date_from)
    if date_to: query = query.filter(models.FinancialRecord.date <= date_to)

    total = query.count()
    records = query.offset(skip).limit(limit).all()
    return {"total": total, "records": records}

# ── Update (Admin only) ───────────────────────────────────
@router.put("/{record_id}", response_model=schemas.RecordResponse)
def update_record(
    record_id: int,
    update: schemas.RecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in update.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

# ── Delete (Admin only, soft delete) ─────────────────────
@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.is_deleted = True
    db.commit()
    return {"message": "Record deleted successfully"}