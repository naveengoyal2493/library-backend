from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.book_loan_model import BookLoan


class BookLoanRepository():

    def __init__(self, db: Session):
        self.db = db

    def get_by_loan_id_for_update(self, loan_id: int) -> Optional[BookLoan]:
        stmt = select(BookLoan).where(BookLoan.id == loan_id).with_for_update(skip_locked=True)
        return self.db.scalar(stmt)

    def get_loans_by_member_id(self, member_id: int) -> List[BookLoan]:
        stmt = select(BookLoan).where(BookLoan.member_id == member_id)
        return self.db.scalars(stmt).all()

    def get_loans_by_book_id(self, book_id: int) -> List[BookLoan]:
        stmt = select(BookLoan).where(BookLoan.book_id == book_id)
        return self.db.scalars(stmt).all()

    def get_active_loan_for_book_for_update(self, book_id: int) -> Optional[BookLoan]:
        stmt = (
            select(BookLoan)
            .where(
                BookLoan.book_id == book_id,
                BookLoan.returned_at.is_(None)
            ).with_for_update()
        )
        return self.db.scalar(stmt)

    def get_overdue_loans(self) -> List[BookLoan]:
        stmt = select(BookLoan).where(
            BookLoan.returned_at.is_(None),
            BookLoan.due_at < func.now()
        )
        return self.db.scalars(stmt).all()

    def add_loan(self, member_id: int, book_id: int, due_at) -> BookLoan:
        loan = BookLoan(
            member_id=member_id,
            book_id=book_id,
            due_at=due_at,
        )
        self.db.add(loan)
        self.db.flush()
        return loan
