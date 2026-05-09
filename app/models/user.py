from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String)
    password=Column(String)
    role_id=Column(Integer,ForeignKey("roles.id"))
    is_active=Column(Boolean,default=True)

    role=relationship("Role")
    
    device_tokens = relationship("UserDeviceToken", back_populates="user", cascade="all, delete-orphan")
    student_profile = relationship("Student", back_populates="user", uselist=False)