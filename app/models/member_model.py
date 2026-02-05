from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class Member(Base):
    __tablename__ = "tbl_member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    mobile = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True, index=True)