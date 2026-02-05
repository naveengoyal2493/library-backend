from app.models.member_model import Member
from app.schemas.member_schemas import AddMember
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List


class MemberRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, member_id: int) -> Optional[Member]:
        stmt = select(Member).where(Member.id == member_id)
        return self.db.scalar(stmt)

    def get_members(self) -> List[Member]:
        stmt = select(Member).order_by(Member.name.asc())
        return self.db.scalars(stmt).all()

    def add_member(self, member: AddMember) -> Member:
        new_member = Member(**member.model_dump())
        self.db.add(new_member)
        return new_member
