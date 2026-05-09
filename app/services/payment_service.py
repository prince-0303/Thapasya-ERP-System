import os
import razorpay
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

class PaymentService:
    def __init__(self):
        self.key_id = os.getenv("RAZORPAY_KEY_ID")
        self.key_secret = os.getenv("RAZORPAY_KEY_SECRET")

        if not self.key_id or not self.key_secret:
            raise ValueError("Razorpay keys not found in environment variables")
        
        try:
            self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
        except Exception as e:
            print(f"Error initializing Razorpay Client: {e}")

    def create_order(self, amount: float, fee_id: str, student_name: str, branch: str):
        """Creates a Razorpay Order for Student Fees."""
        try:
            # Convert to paise
            amount_in_paise = int(amount * 100)

            data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"rcpt_{fee_id}",
                "notes": {
                    "student_name": student_name,
                    "branch": branch,
                    "fee_schedule_id": fee_id,
                    "purpose": "Monthly Fee Receipt"
                }
            }

            return self.client.order.create(data=data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Razorpay Order Creation Failed: {str(e)}")
    
    def verify_payment_signature(self, params_dict: dict):
        """Verifies the signature received from the mobile app."""
        try:
            return self.client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Signature verification error: {str(e)}")
        
payment_service = PaymentService()