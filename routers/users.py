from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import hash_password, verify_password, create_token, get_current_user, require_role
import models, schemas

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    token = create_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users", dependencies=[Depends(require_role("admin"))])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.put("/users/{user_id}/role", dependencies=[Depends(require_role("admin"))])
def update_role(user_id: int, role: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    user.role = role
    db.commit()
    return {"message": f"Role updated to {role}"}

@router.put("/users/{user_id}/status", dependencies=[Depends(require_role("admin"))])
def update_status(user_id: int, is_active: bool, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = is_active
    db.commit()
    return {"message": f"User status updated to {'active' if is_active else 'inactive'}"}