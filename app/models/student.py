from sqlalchemy import Column,String,Integer,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Student(Base):
    __tablename__="students"

    id=Column(Integer,primary_key=True,index=True)

    user_id=Column(Integer,ForeignKey("users.id"))
    parent_id=Column(Integer,ForeignKey("parents.id"))
    branch_id=Column(Integer,ForeignKey("branches.id"))

    name=Column(String)
    phone=Column(String)
    dob=Column(String)
    address=Column(Text,nullable=True)

    user = relationship("User", back_populates="student_profile")
    parent=relationship("Parent")
    branch=relationship("Branch")