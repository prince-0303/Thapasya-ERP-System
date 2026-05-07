from sqlalchemy import Column,Integer,ForeignKey,Date,String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Payment(Base):
    __tablename__="payments"

    id = Column(Integer,primary_key=True,index=True)

    schedule_id = Column(Integer,ForeignKey("fee_schedules.id"))

    amount_paid=Column(Integer)
    payment_date=Column(Date)

    schedule=relationship("FeeSchedule",back_populates="payments")
