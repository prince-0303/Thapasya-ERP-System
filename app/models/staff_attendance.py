from sqlalchemy import Column,Integer,ForeignKey,Date,String,UniqueConstraint,Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class StaffAttendance(Base):
    __tablename__="staff_attendance"

    id = Column(Integer, primary_key=True ,index=True)
    staff_course_id=Column(Integer,ForeignKey("staff_courses.id"),nullable=False)
    date=Column(Date,nullable=False)

    status=Column(Enum(AttendanceStatus),nullable=False)

    staff_course=relationship("StaffCourse",back_populates="attendances")

    __table_args__=(
        UniqueConstraint("staff_course_id","date",name="unique_staff_course_date"),
    )
    
