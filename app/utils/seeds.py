from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password
from app.core.config import ADMIN_EMAIL,ADMIN_PASSWORD,ADMIN_USERNAME

import pytz
from datetime import datetime

def create_default_admin(db):
    admin_role=db.query(Role).filter(Role.name=="admin").first()

    if not admin_role:
        admin_role=Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    existing_admin=db.query(User).filter(User.username == ADMIN_USERNAME ).first()
    if existing_admin:
        return 
    
    admin=User(
        username=ADMIN_USERNAME,
        email = ADMIN_EMAIL,
        password=hash_password(ADMIN_PASSWORD),
        role_id=admin_role.id,
        is_active=True
    )

    db.add(admin)
    db.commit()

def today():
    IST=pytz.timezone("Asia/Kolkata")
    return datetime.now(IST).date()