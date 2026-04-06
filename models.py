from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"

class TypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="viewer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    date = Column(String)
    notes = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())