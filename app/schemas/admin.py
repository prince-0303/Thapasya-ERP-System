from pydantic import BaseModel
from app.models.staff_attendance import AttendanceStatus

class StaffAttendanceCreate(BaseModel):
    staff_course_id : int
    status : AttendanceStatus