from sqlalchemy.orm import Session
from app.models.payment import Payment
from datetime import datetime

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def confirm_payment(self, order_id: str, payment_id: str):
        """Standardized logic to confirm a payment in the DB."""
        payment_record = self.db.query(Payment).filter(
            Payment.razorpay_order_id == order_id
        ).first()

        if not payment_record:
            return None
        
        if payment_record.status == "PAID":
            return payment_record

        payment_record.status = "PAID"
        payment_record.razorpay_payment_id = payment_id
        payment_record.payment_date = datetime.utcnow().date()

        schedule = payment_record.schedule
        if schedule:
            total_paid = sum(p.amount_paid for p in schedule.payments if p.status == "PAID")
            
            if total_paid >= schedule.amount:
                schedule.status = "paid"
            elif total_paid > 0:
                schedule.status = "partial"

        self.db.commit()
        self.db.refresh(payment_record)
        return payment_record

    def mark_as_failed(self, order_id: str):
        """Standardized logic to mark a payment as failed in the DB."""
        payment_record = self.db.query(Payment).filter(
            Payment.razorpay_order_id == order_id
        ).first()

        if payment_record and payment_record.status != "PAID":
            payment_record.status = "FAILED"
            self.db.commit()
            self.db.refresh(payment_record)
        
        return payment_record