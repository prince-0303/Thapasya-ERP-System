from fastapi import HTTPException
from app.models.student import Student
from sqlalchemy.orm import Session
from sqlalchemy import func,extract

from app.models.student_course import StudentCourse
from app.models.fee import FeeSchedule

from app.models.staff import Staff
from app.models.staff_course import StaffCourse
from app.models.payment import Payment

from app.models.branch import Branch

from app.models.staff_attendance import StaffAttendance

from app.utils.seeds import today

# student datas


def student_list(db : Session ,current_admin):
    try:
        student=db.query(Student).all()

        if not student:
            return {"message":"No students Found"}
        
        return [
            {
            "id":s.id,
            "name":s.name,
            "user_name":s.user.username,
            "branch":s.branch.name
        }
        for s in student
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
def get_student_details(student_id, db: Session , current_admin):
    try:
        student=db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return{"message":"Student not found"}
        
        stud_course= db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()

        fee_details=db.query(FeeSchedule).filter(FeeSchedule.student_id == student_id).limit(5).all()
        
        return{
            "name":student.name,
            "phone":student.phone,
            "dob":student.dob,
            "address":student.address,
            "courses":[
                {"name":c.course.name}
                for c in stud_course
            ],
            "fee_details":[{
                "course":f.course.name,
                "amount":f.amount,
                "due":f.due_date,
                "status":f.status

            }
            for f in fee_details
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


#Dashboard 

def get_dashborad_data(db : Session ,current_admin):
    try:
        student_count=db.query(Student).count()
        staff_count=db.query(Staff).count()
        total_revenue=db.query(func.sum(Payment.amount_paid)).scalar()

        return {
            "students":student_count,
            "staffs":staff_count,
            "total_earning":total_revenue if total_revenue else 0
        }
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

def get_monthly_revenue(db : Session, current_admin):
    try:
        result=(db.query(
            extract('year',Payment.payment_date).label('year'),
            extract('month',Payment.payment_date).label('month'),
            func.sum(Payment.amount_paid).label('total')
        ).group_by(
            extract('year',Payment.payment_date),
            extract('month',Payment.payment_date)
        ).order_by(
            extract('year',Payment.payment_date),
            extract('month',Payment.payment_date)
        ).all()
        )

        return result
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))



# staff datas

def get_staff_service(db : Session,current_admin):
    try:
        staffs=db.query(Staff).all()
        return [{
            "id":staff.id,
            "name":staff.name,
            "branch":staff.branch.name
        }
        for staff in staffs
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    


def get_staff_details_service(db: Session,current_admin,staff_id):

    try:
        staff=db.query(Staff).get(staff_id)

        total_salary=db.query(func.sum(StaffCourse.monthly_salary)).filter(StaffCourse.staff_id ==  staff_id).scalar()

        return {
            "name":staff.name,
            "phone":staff.phone,
            "address":staff.address,
            "useid":staff.user.username,
            "email":staff.user.email,
            "branch":staff.branch.name,
            "account_details":{
                "acc_no":staff.staff_accounts.account_number,
                "ifsc":staff.staff_accounts.ifsc
            },
            "salary_data":[
                {
                    "course":sal.course.name,
                    "salary":sal.monthly_salary
                }
                for sal in staff.staff_courses
            ],
            "total_salary":total_salary if total_salary else 0
        }
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    


# staff attendance


def get_branch_service(db : Session,current_admin):
    try:
        branchs=db.query(Branch).all()
        return [
            {
                "id":branch.id,
                "name":branch.name
            }
            for branch in branchs
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

def get_staff_basedbranch_service(db :Session, current_admin,branch_id):
    try:
        staffs=db.query(Staff).filter(Staff.branch_id == branch_id).all()

        if not staffs:
            raise HTTPException(status_code=404,detail="Staffs not found in this branch")

        return [
            {
                "name":staff.name,
                "course":[
                    {
                        "id":staff_course.course.id,
                        "name":staff_course.course.name
                    }
                    for staff_course in staff.staff_courses
                ]
            }
            for staff in staffs
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))




def staff_attedence_service(data,db: Session , current_admin):
    try:
        attendance=StaffAttendance(
            staff_course_id=data.staff_course_id,
            date=today(),
            status=data.status
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return attendance
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


def staff_attendance_log(db : Session, current_admin, staff_id):
    try:
        attendances=db.query(StaffAttendance).join(StaffCourse).filter(
            StaffCourse.staff_id == staff_id
        ).limit(10).all()

        if not attendances:
            raise HTTPException(status_code=404,detail="Attendance Log not available")
        
        return[
            {
                "date":attendance.date,
                "course":attendance.staff_course.course.name,
                "status":attendance.status
            }
            for attendance in attendances
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

