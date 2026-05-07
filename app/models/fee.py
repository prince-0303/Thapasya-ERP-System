from sqlalchemy import Column,Integer,String,ForeignKey,Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class FeeSchedule(Base):
    __tablename__="fee_schedules"

    id = Column(Integer,primary_key=True, index=True)

    student_id=Column(Integer,ForeignKey("students.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))

    due_date=Column(Date,nullable=False)
    amount=Column(Integer,nullable=False)

    status=Column(String,default="pending")

    student=relationship("Student")
    course=relationship("Course")

    payments = relationship("Payment", back_populates="schedule")