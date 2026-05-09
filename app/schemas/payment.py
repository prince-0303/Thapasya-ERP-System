from pydantic import BaseModel

class OrderCreate(BaseModel):
    fee_id: int

class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str