from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.core.dependencies import get_current_admin
from app.services.admin_service import student_list,get_student_details,get_dashborad_data,get_monthly_revenue


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