from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    min_age = Column(Integer, default=5, nullable=False)
    description = Column(Text, nullable=True)
    fee = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)

    staff_courses = relationship("StaffCourse", back_populates="course")