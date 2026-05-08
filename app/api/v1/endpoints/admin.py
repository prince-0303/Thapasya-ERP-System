from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.core.dependencies import get_current_admin
from app.services.admin_service import student_list,get_student_details,get_dashborad_data,get_monthly_revenue,get_staff_service,get_staff_details_service,get_branch_service,get_staff_basedbranch_service,staff_attedence_service,staff_attendance_log

from app.schemas.admin import StaffAttendanceCreate

router=APIRouter(prefix='/admin',tags=["Admin Apis"])

@router.get('/all-students')
def get_all_students(db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return student_list(db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@router.get('/student-details')
def student_details(student_id : int, db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return get_student_details(student_id,db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@router.get('/dashboard-data')
def dashboard_data(db : Session=Depends(get_db),current_admin =Depends(get_current_admin)):
    try:
        return get_dashborad_data(db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@router.get('/monthly-revenue')
def monthly_revenue(db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        data=get_monthly_revenue(db,current_admin)
        return[
            {
                "year":int (row.year) if row.year else 0,
                "month":int (row.month) if row.month else 0,
                "total":float(row.total) if row.total else 0
            }
            for row in data
        ]
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
   
    
@router.get('/get-staffs')
def get_staff(db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return get_staff_service(db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.get('/staff-details')
def get(staff_id : int ,db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        staff_data=get_staff_details_service(db,current_admin,staff_id)
        attendance_log=staff_attendance_log(db,current_admin,staff_id)

        return {
            "staff":staff_data,
            "attendance":attendance_log
        }
    
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
    

@router.get('/get-branch')
def get_branch(db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return get_branch_service(db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
 
    
@router.get('/get-staff-branchbased')
def get_staff_branchbased(branch_id : int,db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return get_staff_basedbranch_service(db,current_admin,branch_id)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.post('/staff-attendance')
def mark_staff_attendance(data : StaffAttendanceCreate ,db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return staff_attedence_service(data,db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))