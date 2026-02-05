from starlette import status

from app.database import get_db
from app.schemas.book_loan_schemas import BookLoanResponse
from app.services.book_loan_service import BookLoanService
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter()

def get_book_service(db: Session = Depends(get_db)) -> BookLoanService:
    return BookLoanService(db)

@router.post("/", response_model=BookLoanResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(member_id: int, book_id: int, service: BookLoanService = Depends(get_book_service)):
    return service.borrow_book(member_id, book_id)

@router.post("/{loan_id}/return", response_model=BookLoanResponse, status_code=status.HTTP_201_CREATED)
def return_book(loan_id: int, service: BookLoanService = Depends(get_book_service)):
    return service.return_book(loan_id)
