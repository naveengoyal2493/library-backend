from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book_loan_model import BookLoan
from app.models.book_model import Book
from app.schemas.book_schemas import AddBook
from typing import List, Optional

class BookRepository():

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Book]:
        stmt = select(Book).where(Book.id == id)
        return self.db.scalar(stmt)

    def get_books(self) -> List[Book]:
        stmt = select(Book).order_by(Book.created_at.desc())
        return self.db.scalars(stmt).all()

    def get_borrowed_books(self) -> List[Book]:
        stmt = (
            select(Book)
            .join(BookLoan, BookLoan.book_id == Book.id)
            .where(BookLoan.book_id == Book.id)
        )
        return self.db.scalars(stmt).all()

    def get_by_id_for_update(self, id: int) -> Optional[Book]:
        stmt = select(Book).where(Book.id == id).with_for_update()
        return self.db.scalar(stmt)

    def add_book(self, book: AddBook) -> Book:
        new_book = Book(**book.model_dump())
        self.db.add(new_book)
        return new_book

    def delete_book(self, book: Book) -> None:
        self.db.delete(book)