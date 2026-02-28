from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), default="")
    plan = Column(String(50), default="free")
    credits = Column(Integer, default=3)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)

    analyses = relationship("Analysis", back_populates="user", lazy="selectin")
    transactions = relationship("Transaction", back_populates="user", lazy="selectin")
    api_keys = relationship("ApiKey", back_populates="user", lazy="selectin")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    analysis_type = Column(String(50), nullable=False)
    target_address = Column(String(255), nullable=False)
    network = Column(String(10), default="eth")
    result = Column(Text, nullable=True)
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String(20), nullable=True)
    risk_factors = Column(Text, nullable=True)  # JSON serialized
    processing_time_ms = Column(Integer, nullable=True)
    status = Column(String(20), default="completed")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="analyses")

    __table_args__ = (
        Index("ix_analyses_user_type", "user_id", "analysis_type"),
        Index("ix_analyses_created", "created_at"),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    plan = Column(String(50), nullable=False)
    credits_added = Column(Integer, nullable=False)
    stripe_payment_id = Column(String(255), nullable=True)
    status = Column(String(20), default="completed")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="transactions")


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    api_key = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), default="default")
    is_active = Column(Boolean, default=True)
    requests_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="api_keys")
