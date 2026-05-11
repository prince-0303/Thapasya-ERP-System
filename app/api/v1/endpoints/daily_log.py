from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.daily_log import DailyLogCreate
from app.core.dependencies import get_current_user,get_current_admin
from app.services.daily_log_service import create_daily_log_service,get_all_logs_service


router = APIRouter(prefix="/daily_log",tags=["DailyLog"])

@router.post("/")
def create_daily_log(data : DailyLogCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return create_daily_log_service(data ,db ,current_user)

@router.get('/get_log')
def get_specific_log(staff_id : int ,db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return get_all_logs_service(staff_id, db, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    