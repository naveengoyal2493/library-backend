from app.database import Base
from sqlalchemy import Column, DateTime, func, Integer, String


class Book(Base):
    __tablename__ = 'tbl_book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    copies = Column(Integer, nullable=False, index=True, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True),  onupdate=func.now(), nullable=True, index=True)