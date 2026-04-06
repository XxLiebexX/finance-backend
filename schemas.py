from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ── Auth ──────────────────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "viewer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ── Financial Records ─────────────────────────────────────
class RecordCreate(BaseModel):
    amount: float
    type: str  # income or expense
    category: str
    date: str
    notes: Optional[str] = None

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: str
    notes: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True