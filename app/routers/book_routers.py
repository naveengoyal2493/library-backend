from starlette import status
from app.database import get_db
from app.schemas.book_schemas import BookResponse, AddBook
from app.services.book_service import BookService
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.get_book(book_id)

@router.get("/", response_model=List[BookResponse])
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_books()

@router.get("/borrowed/", response_model=List[BookResponse])
def get_borrowed_books(service: BookService = Depends(get_book_service)):
    return service.get_borrowed_books()

@router.post("/", response_model=BookResponse)
def create_book(book: AddBook, service: BookService = Depends(get_book_service)):
    return service.add_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.delete_book(book_id)
