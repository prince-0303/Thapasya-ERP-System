from fastapi import HTTPException
from sqlalchemy import func

from app.models.staff_course import StaffCourse
from app.models.staff_attendance import StaffAttendance
from app.models.staff_account import StaffAccount

from app.models.salary import SalaryPayment

from datetime import timedelta
from app.utils.seeds import today
from app.models.staff_attendance import AttendanceStatus
from app.models.salary import SalarySatus

import uuid

def calculate_staff_salary(db , staff_course_id, current_admin):
    try:
        staff_course=db.query(StaffCourse).filter(
            StaffCourse.id == staff_course_id
            ).first()

        account_details=db.query(StaffAccount).filter(StaffAccount.staff_id==staff_course.staff_id).first()


        if not staff_course:
            raise HTTPException(status_code=404,detail="staff Course not found")
    
        end_date=today()
        start_date=end_date - timedelta(days=30)

        present_days=db.query(func.count(StaffAttendance.id)).filter(
            StaffAttendance.staff_course_id ==  staff_course_id,
            StaffAttendance.status == AttendanceStatus.PRESENT,
            StaffAttendance.date.between(start_date,end_date)
        ).scalar()

        present_days= present_days or 0

        if present_days >= 4:
            total_salary=staff_course.monthly_salary
        else:
            salary_perday=staff_course.monthly_salary / 4
            total_salary=salary_perday * present_days
    
        return{
            "from":start_date,
            "to":end_date,
            "present_days":present_days,
            "this_month_salary":total_salary,
            "acc_details":{
                "acc_number":account_details.account_number,
                "ifsc":account_details.ifsc
            }
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


def salary_pay_completed(db,staff_course_id,current_admin):
    try:
        staff_course=db.query(StaffCourse).filter(
            StaffCourse.id == staff_course_id
        ).first()

        if not staff_course:
            raise HTTPException(status_code=404,detail="staff Course not found")
        
        salary_data=calculate_staff_salary(db,staff_course_id,current_admin)

        payment=SalaryPayment(
            staff_id=staff_course.staff_id,
            staff_course_id=staff_course_id,
            amount=salary_data["this_month_salary"],
            status=SalarySatus.SUCCESS,
            transaction_id=str(uuid.uuid4()),
            created_at=today()
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
        "payment_id": payment.id,
        "amount": payment.amount,
        "present_days": salary_data["present_days"],
        "start_date": salary_data["from"],
        "end_date": salary_data["to"]
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))