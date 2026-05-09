import json
from datetime import datetime
import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.student import Student
from app.models.fee import FeeSchedule
from app.repositories.payment import PaymentRepository
from app.services.payment_service import payment_service
from app.schemas.payment import OrderCreate, PaymentVerify
from app.core.dependencies import get_current_user
from app.models.payment import Payment

router = APIRouter()

@router.post("/create-order", status_code=status.HTTP_201_CREATED)
async def create_new_payment_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    schedule = db.query(FeeSchedule).filter(FeeSchedule.id == order_data.fee_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Fee schedule not found")

    if schedule.status == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This fee has already been paid. No further action required."
        )

    if not current_user.student_profile or schedule.student_id != current_user.student_profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Unauthorized: You can only pay your own fees."
        )

    student = schedule.student
    branch_name = student.branch.name if (student and student.branch) else "Main"

    try:
        order = payment_service.create_order(
            amount=schedule.amount,
            fee_id=str(schedule.id),
            student_name=student.name if student else "Student",
            branch=branch_name
        )

        new_payment = Payment(
            schedule_id=schedule.id,
            amount_paid=schedule.amount,
            razorpay_order_id=order["id"],
            status="PENDING"
        )
        db.add(new_payment)
        db.commit()
        
        return order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Order Creation Failed: {str(e)}")

@router.post("/verify-payment")
async def verify_payment_completion(
    verify_data: PaymentVerify, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        is_valid = payment_service.verify_payment_signature(verify_data.model_dump())
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid payment signature")

        repo = PaymentRepository(db)
        payment = repo.confirm_payment(
            order_id=verify_data.razorpay_order_id, 
            payment_id=verify_data.razorpay_payment_id
        )

        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found")

        return {"status": "success", "message": "Payment verified and recorded"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    webhook_body = await request.body()
    webhook_signature = request.headers.get("X-Razorpay-Signature")
    webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    if not webhook_signature or not webhook_secret:
        return {"status": "error", "message": "Missing security credentials"}

    try:
        payment_service.client.utility.verify_webhook_signature(
            webhook_body, 
            webhook_signature, 
            webhook_secret
        )
        
        data = json.loads(webhook_body)
        event = data.get('event')
        repo = PaymentRepository(db)

        if event == "order.paid":
            order_id = data['payload']['order']['entity']['id']
            payment_id = data['payload'].get('payment', {}).get('entity', {}).get('id', 'WH_CONFIRMED')
            
            repo.confirm_payment(order_id=order_id, payment_id=payment_id)

        elif event == "payment.failed":
            payment_entity = data['payload']['payment']['entity']
            order_id = payment_entity.get('order_id')
            error_msg = payment_entity.get('error_description', 'Payment failed')
            repo.mark_as_failed(order_id=order_id)
            
        return {"status": "ok"}

    except Exception as e:
        return {"status": "error"}