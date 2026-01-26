from pydantic import BaseModel, EmailStr
from datetime import datetime, date, time

class SignUpWithEmailSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    
class UserSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    resume_id: str | None = None
    is_subscribed: bool = False
    super_id: str
    created_at: datetime | None = None
    
class LogiSchema(BaseModel):
    email: EmailStr
    password: str