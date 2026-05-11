from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.daily_log import DailyLog
from app.models.staff import Staff
from app.models.user import User
from datetime import date
from app.core.dependencies import check_admin_role,check_user_role


def create_daily_log_service(data, db : Session ,current_user):

    role = check_user_role(db,current_user)

    if role != "staff":
        raise HTTPException(status_code=403,detail="Not a staff")
    
    staff = db.query(Staff).filter(
        Staff.user_id == current_user.id
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")


    existing = db.query(DailyLog).filter(
        DailyLog.date == date.today(),
        DailyLog.course_id == data.course_id,
        DailyLog.staff_id == staff.id).first()

    if existing:
        raise HTTPException(400, "Log already exists for this class today")
    
    log= DailyLog(
        staff_id=staff.id,
        course_id=data.course_id,
        class_summary=data.class_summary,
        topics_covered=data.topics_covered,
        next_class_topic=data.next_class_topic,
        date = date.today()
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_all_logs_service(staff_id, db : Session, current_user):

    role= check_admin_role(db,current_user)
    if role != "admin" or role != "staff":
        raise HTTPException(status_code=403,detail="Admin only can access")
    
    log = db.query(DailyLog).filter(
        DailyLog.staff_id == staff_id
    ).all()

    if not log:
        return {
            "message":"No log from the staff"
        }

    return log
