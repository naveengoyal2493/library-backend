from app.repositories.book_repository import BookRepository
from app.schemas.book_schemas import BookResponse, AddBook
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

class BookService:

    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)

    def get_book(self, book_id: int) -> BookResponse:
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookResponse.model_validate(book)

    def get_books(self) -> List[BookResponse]:
        books = self.book_repo.get_books()
        if books is None:
            raise HTTPException(status_code=404, detail="No Books found")
        return [BookResponse.model_validate(book) for book in books]

    def get_borrowed_books(self) -> List[BookResponse]:
        books = self.book_repo.get_borrowed_books()
        if books is None:
            raise HTTPException(status_code=404, detail="No borrowed books found")
        return [BookResponse.model_validate(book) for book in books]

    def add_book(self, book: AddBook) -> BookResponse:
        try:
            new_book = self.book_repo.add_book(book)
            self.db.commit()
            self.db.refresh(new_book)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Book already exists"
            )

        return BookResponse.model_validate(new_book)

    def delete_book(self, book_id: int) -> None:
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        try:
            self.db.delete(book)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cannot delete book because it has loan records."
            )