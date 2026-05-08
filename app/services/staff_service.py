from app.models.staff import Staff
from app.models.staff_account import StaffAccount
from app.models.staff_course import StaffCourse
from app.repositories.user_repository import create_user
from app.core.security import hash_password
from fastapi import HTTPException


from app.models.staff import Staff
from app.models.course import Course
from app.models.student_course import StudentCourse
from app.models.student import Student
from app.models.staff_course import StaffCourse
from app.core.dependencies import check_user_role
from app.models.attendence import Attendance

from app.utils.seeds import today

def register_staff(db,data,current_admin):
    try:
        hashed_password=hash_password(data.password)

        user = create_user(
            db,
            data.username,
            data.email,
            hashed_password,
            data.role_id
        )
        db.flush()

        staff = Staff(
            user_id=user.id,
            name=data.staff.name,
            phone=data.staff.phone,
            branch_id=data.staff.branch_id,
            adhar_url=data.staff.aadhar_url,
            address=data.staff.address
        )
        db.add(staff)
        db.flush()

        for course_id in data.course_ids:
            db.add(StaffCourse(
                staff_id = staff.id,
                course_id = course_id,
                assigned_date=today()
            ))

        account= StaffAccount(
            staff_id=staff.id,
            account_number = data.account.account_number,
            ifsc = data.account.ifsc
        )
        db.add(account)

        db.commit()

        return {"message":"staff registerd successfully"}
    
    except Exception as e:
        db.rollback()
        raise e
    
def staff_course_toggle(db,current_user):
    
    role=check_user_role(db,current_user)
    if role != "staff":
        raise HTTPException(status_code=403,detail="staff only can access")

    staff=db.query(Staff).filter(Staff.user_id == current_user.id).first()

    courses = db.query(Course).join(StaffCourse).filter(StaffCourse.staff_id == staff.id).all()

    return courses

def get_my_students_service(course_id,branch_id,db,current_user):

    role=check_user_role(db,current_user)
    if role !="staff":
        raise HTTPException(status_code=403, detail="Only staff can access")
    
    students=db.query(StudentCourse).join(Student,Student.id == StudentCourse.student_id).filter(
        Student.branch_id == branch_id,
        StudentCourse.course_id == course_id
    ).all()

    if not students:
        return {
            "message":"No Students Found"
        }

    return [
        {
            "id":s.student.id,
            "name":s.student.name
        }
        for s in students
    ]
    

def mark_attendance_service(data,db,current_user):
    try:
        role= check_user_role(db,current_user)
        if role !="staff":
            raise HTTPException(status_code=403, detail="Only staff can access")

        attendance=Attendance(
            student_id = data.student_id,
            course_id= data.course_id,
            date=today(),
            status=data.status
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return attendance

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

