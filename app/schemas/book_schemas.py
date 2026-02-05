from pydantic import BaseModel, Field

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    copies: int

    model_config = {"from_attributes": True}

class AddBook(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=50)
    copies: int