from app.database import Base
from sqlalchemy import Column, CheckConstraint, Integer, DateTime, func, ForeignKey, Index

class BookLoan(Base):
    __tablename__ = "tbl_book_loan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('tbl_book.id', ondelete='RESTRICT'), nullable=False)
    member_id = Column(Integer, ForeignKey('tbl_member.id', ondelete='RESTRICT'), nullable=False, index=True)
    borrowed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index(
            "uq_active_book_loan",
            "book_id",
            unique=True,
            postgresql_where=(returned_at.is_(None))
        ),
        Index(
            "idx_member_active_loans",
            "member_id",
            postgresql_where=(returned_at.is_(None))
        ),
        Index(
            "idx_member_loan_history",
            "member_id",
            "borrowed_at"
        ),
        CheckConstraint(
            "returned_at IS NULL OR returned_at >= borrowed_at",
            name="ck_return_after_borrow"
        ),
        CheckConstraint(
            "due_at >= borrowed_at",
            name="ck_due_after_borrow"
    )
    )