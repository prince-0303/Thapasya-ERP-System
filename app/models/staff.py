from sqlalchemy import Column,String,Integer,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Staff(Base):
    __tablename__="staff"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    branch_id = Column(Integer,ForeignKey("branches.id"))

    name = Column(String)
    phone = Column(String)
    adhar_url= Column(String)
    address=Column(Text,nullable=True)

    staff_courses = relationship("StaffCourse", back_populates="staff")
    staff_accounts=relationship('StaffAccount',back_populates='staff',uselist=False)
    salary_payments=relationship("SalaryPayment",back_populates="staff")
    user=relationship("User")
    branch=relationship("Branch")

