from pydantic import BaseModel, EmailStr
from typing import Optional

class BookingData(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    check_in: str
    check_out: str
    room_type: str
    num_guests: int
    special_requests: Optional[str] = ""