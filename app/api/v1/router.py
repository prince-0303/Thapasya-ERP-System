from fastapi import APIRouter
from app.api.v1.endpoints import enquiry, course, booking

from app.api.v1.endpoints.student import router as student_router
from app.api.v1.endpoints.staff import router as staff_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.role import router as role_router
from app.api.v1.endpoints.branch import router as branch_router
from app.api.v1.endpoints.daily_log import router as daily_log_router
from app.api.v1.endpoints.staff_course_togle import router as my_courses
from app.api.v1.endpoints.schedules import router as class_schedule
from app.api.v1.endpoints.profile import router as user_profile
from app.api.v1.endpoints.fee import router as fee_router
from app.api.v1.endpoints.notification import router as notification_router
from app.api.v1.endpoints.admin import router as admin_routes
from app.api.v1.endpoints.payment import router as payment_router

api_router = APIRouter()

# Application routes

api_router.include_router(notification_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(payment_router, prefix="/payments", tags=["payments"])
api_router.include_router(student_router, prefix="/student", tags=["Students"])
api_router.include_router(staff_router, prefix="/staff", tags=["Staff"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(role_router)   
api_router.include_router(branch_router)
api_router.include_router(daily_log_router)
api_router.include_router(my_courses)
api_router.include_router(class_schedule)
api_router.include_router(user_profile)
api_router.include_router(fee_router)
api_router.include_router(admin_routes)

# Website routes

api_router.include_router(enquiry.router, prefix="/enquiries", tags=["Enquiries"])
api_router.include_router(course.router, prefix="/courses", tags=["Courses"])
api_router.include_router(booking.router, prefix="/bookings", tags=["Bookings"])