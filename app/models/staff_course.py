from sqlalchemy import Column,Integer,String,ForeignKey,Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class StaffCourse(Base):
    __tablename__="staff_courses"

    id= Column(Integer,primary_key=True,index=True)
    staff_id=Column(Integer,ForeignKey("staff.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))

    assigned_date=Column(Date,nullable=False)

    monthly_salary=Column(Integer,nullable=False)

    staff=relationship("Staff",back_populates='staff_courses')
    course=relationship("Course",back_populates='staff_courses')
    attendances = relationship("StaffAttendance", back_populates="staff_course")
    salary_payments=relationship("SalaryPayment",back_populates="staff_course")
    attendances = relationship("StaffAttendance", back_populates="staff_course")
