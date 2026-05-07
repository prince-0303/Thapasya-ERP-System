import pytz
from datetime import datetime,date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.parent import Parent
from app.models.student import Student
from app.models.student_course import StudentCourse
from app.models.course import Course
from app.models.daily_log import DailyLog
from app.models.schedule import Schedule
from app.models.attendence import Attendance
from app.repositories.user_repository import create_user
from app.core.security import hash_password

# REGISTRATION

def register_student(db: Session, data, current_admin):
    try:
        hashed_password = hash_password(data.password)

        user = create_user(
            db,
            data.username,
            data.email,
            hashed_password,
            data.role_id
        )
        db.flush()

        parent = db.query(Parent).filter(
            Parent.phone == data.parent.phone,
            Parent.name == data.parent.name
        ).first()

        if not parent:
            parent = Parent(
                name=data.parent.name,
                phone=data.parent.phone,
                email=data.parent.email
            )
            db.add(parent)
            db.flush()

        student = Student(
            user_id=user.id,
            parent_id=parent.id,
            branch_id=data.student.branch_id,
            name=data.student.name,
            phone=data.student.phone,
            dob=data.student.dob,
            address=data.student.address
        )
        db.add(student)
        db.flush()

        for course_id in data.course_ids:
            db.add(StudentCourse(
                student_id=student.id,
                course_id=course_id,
                joined_date=date.today()
            ))
        
        db.commit()

        return {"message": "Student registration successful"}
    
    except Exception as e:
        db.rollback()
        raise e

# STUDENT DASHBOARD & COURSE TOGGLE

def get_student_enrolled_courses(db: Session, current_user):
    """Returns the list of courses for the toggle buttons"""
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    courses = db.query(Course).join(StudentCourse).filter(
        StudentCourse.student_id == student.id
    ).all()
    
    return [{"id": c.id, "name": c.name} for c in courses]

def get_student_home_dashboard(db: Session, current_user, course_id: int):
    # Handle timezone (IST)
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(IST)
    hour = now_ist.hour
    
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 17 else "Good Evening"

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")

    is_enrolled = db.query(StudentCourse).filter(
        StudentCourse.student_id == student.id,
        StudentCourse.course_id == course_id
    ).first()

    if not is_enrolled:
        raise HTTPException(status_code=403, detail="Access Denied.")

    attendance_records = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.course_id == course_id
    ).order_by(Attendance.date.desc()).all()

    present_count = sum(1 for a in attendance_records if str(a.status).lower() == "present")

    schedules = db.query(Schedule).filter(
        Schedule.course_id == course_id,
        Schedule.branch_id == student.branch_id,
        Schedule.class_date >= date.today
    ).order_by(Schedule.class_date.asc()).all

    logs = db.query(DailyLog).filter(
        DailyLog.course_id == course_id
    ).order_by(DailyLog.date.desc()).limit(5).all()

    return {
        "user_info": {
            "greeting": greeting, 
            "name": student.name
        },
        "attendance": {
            "total_present": present_count,
            "history": [
                {"date": a.date.strftime("%d %b %Y"), "status": a.status} 
                for a in attendance_records
            ]
        },
        "schedules": [
            {
                "date": s.class_date.strftime("%d %b"), 
                "day": s.class_date.strftime("%A"), 
                "time": s.class_time.strftime("%I:%M %p")
            } for s in schedules
        ],
        "recent_logs": [
            {
                "title": log.topics_covered,
                "summary": log.class_summary,
                "date": log.date.strftime("%d %b")
            } for log in logs
        ]
    }

def get_student_attendance_history(db: Session, current_user, course_id: int):
    """Returns only the attendance records for the calendar view"""
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch all records for the selected course
    records = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.course_id == course_id
    ).order_by(Attendance.date.desc()).all()

    return {
        "course_id": course_id,
        "history": [
            {
                "date": a.date.strftime("%Y-%m-%d"), 
                "status": a.status # present, absent, late, etc.
            } for a in records
        ]
    }