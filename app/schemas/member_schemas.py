
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class AddMember(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=80)
    mobile: str = Field(min_length=10, max_length=10)

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}