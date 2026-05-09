from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("fee_schedules.id"))
    
    amount_paid = Column(Integer)
    payment_date = Column(Date, nullable=True)

    razorpay_order_id = Column(String(100), unique=True, index=True, nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    # Status: "PENDING", "PAID", "FAILED"
    status = Column(String(20), default="PENDING")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    schedule = relationship("FeeSchedule", back_populates="payments")