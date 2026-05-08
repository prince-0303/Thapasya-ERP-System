from sqlalchemy import Column,Integer,ForeignKey,String,Date,Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class SalarySatus(enum.Enum):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"

class SalaryPayment(Base):
    __tablename__="salary_payments"
    
    id = Column(Integer,primary_key=True,index=True)

    staff_id=Column(Integer,ForeignKey("staff.id"))
    staff_course_id=Column(Integer,ForeignKey("staff_courses.id"))

    amount=Column(Integer)
    status=Column(Enum(SalarySatus),nullable=False)

    transaction_id=Column(String,nullable=False)
    created_at=Column(Date)

    staff=relationship("Staff",back_populates="salary_payments")
    staff_course=relationship("StaffCourse",back_populates="salary_payments")
