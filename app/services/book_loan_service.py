from app.repositories.book_repository import BookRepository
from app.repositories.book_loan_repository import BookLoanRepository
from app.repositories.member_repository import MemberRepository
from app.schemas.book_loan_schemas import BookLoanResponse
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class BookLoanService:

    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)
        self.book_loan_repo = BookLoanRepository(db)
        self.member_repo = MemberRepository(db)

    def borrow_book(self, member_id: int, book_id: int) -> BookLoanResponse:
        book = self.book_repo.get_by_id_for_update(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        member = self.member_repo.get_by_id(member_id)
        if member is None:
            raise HTTPException(status_code=404, detail="Member not found")

        try:
            loan = self.book_loan_repo.add_loan(
                member_id=member_id,
                book_id=book_id,
                due_at=datetime.now(timezone.utc) + timedelta(days=14),
            )
            book.copies -= 1
            self.db.commit()
            self.db.refresh(loan)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Book is already borrowed"
            )
        return BookLoanResponse.model_validate(loan)

    def return_book(self, loan_id: int) -> BookLoanResponse:
        loan = self.book_loan_repo.get_by_loan_id_for_update(loan_id)

        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.returned_at is not None:
            raise HTTPException(status_code=409, detail="Book already returned")

        book = self.book_repo.get_by_id(loan.book_id)

        loan.returned_at = datetime.now(timezone.utc)
        book.copies += 1
        self.db.commit()
        self.db.refresh(loan)
        return BookLoanResponse.model_validate(loan)
