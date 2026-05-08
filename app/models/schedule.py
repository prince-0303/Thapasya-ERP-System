from sqlalchemy import  Column,Integer,ForeignKey,Date,Time
from sqlalchemy.orm import relationship
from app.db.base import Base

class Schedule(Base):
    __tablename__="class_schedules"

    id=Column(Integer,primary_key=True,index=True)
    branch_id=Column(Integer,ForeignKey("branches.id"),nullable=False)
    course_id=Column(Integer,ForeignKey("courses.id"),nullable=False)
    staff_id=Column(Integer,ForeignKey("staff.id"),nullable=False)

    class_date=Column(Date,nullable=False)
    class_time=Column(Time,nullable=False)

    branch=relationship("Branch")
    course=relationship("Course")
    staff=relationship("Staff")