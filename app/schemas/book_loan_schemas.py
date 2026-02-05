from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookLoanResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}