"""Database engine, session management, and models for ReconcileX."""
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/reconcilex"
)

# SQLAlchemy 2.0 with psycopg3 driver compatibility
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Order(Base):
    """Internal store orders placed by customers."""
    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), nullable=False)
    amount_sen = Column(Integer, nullable=False)  # stored in sen/cents to avoid float rounding
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, PAID, CANCELLED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    discrepancies = relationship("Discrepancy", back_populates="order")


class Payment(Base):
    """Payment gateway transactions reported by payment provider (e.g. Stripe, FPX)."""
    __tablename__ = "payments"

    payment_id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=True)
    amount_sen = Column(Integer, nullable=False)
    fee_sen = Column(Integer, default=0, nullable=False)
    status = Column(String(20), nullable=False, default="SUCCESS")  # SUCCESS, FAILED, REFUNDED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="payments")
    settlement = relationship("Settlement", back_populates="payment", uselist=False)


class Settlement(Base):
    """Bank settlement records indicating funds deposited into merchant bank account."""
    __tablename__ = "settlements"

    settlement_id = Column(String(50), primary_key=True)
    payment_id = Column(String(50), ForeignKey("payments.payment_id"), nullable=True)
    amount_sen = Column(Integer, nullable=False)  # net amount settled
    status = Column(String(20), nullable=False, default="SETTLED")  # SETTLED, PENDING
    settled_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payment = relationship("Payment", back_populates="settlement")


class Discrepancy(Base):
    """Audit table logging any issues flagged by the ReconcileX matching engine."""
    __tablename__ = "discrepancies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=True)
    discrepancy_type = Column(String(50), nullable=False)  # e.g. AMOUNT_MISMATCH, DUPLICATE_PAYMENT, UNMATCHED
    details = Column(String(255), nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="discrepancies")


# ---------------------------------------------------------------------------
# Database Utilities
# ---------------------------------------------------------------------------

def init_db():
    """Create all tables in the configured database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a database session, guaranteeing cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
