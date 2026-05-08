from fastapi import HTTPException,APIRouter,Depends
from app.db.session import get_db
from app.core.dependencies import get_current_admin 
from sqlalchemy.orm import Session

from app.services.salary_service import calculate_staff_salary,salary_pay_completed


router=APIRouter(prefix='/staff-salary',tags=["Salary management"])

@router.get('/calculate-salary')
def calculate_salary(staff_course_id : int ,db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return calculate_staff_salary(db,staff_course_id,current_admin)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.post('/payment-completed')
def payment_completed(staff_course_id : int ,db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    try:
        return salary_pay_completed(db ,staff_course_id,current_admin)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))