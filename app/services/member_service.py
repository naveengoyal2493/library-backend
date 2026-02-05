from app.schemas.member_schemas import AddMember, MemberResponse
from app.repositories.member_repository import MemberRepository
from fastapi import HTTPException, status
from typing import List

class MemberService:

    def __init__(self, db):
        self.db = db
        self.member_repo = MemberRepository(db)

    def get_member_by_id(self, member_id: int) -> MemberResponse:
        new_member = self.member_repo.get_by_id(member_id)
        if new_member is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        return MemberResponse.model_validate(new_member)

    def get_members(self) -> List[MemberResponse]:
        members = self.member_repo.get_members()
        if not members:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No members found")
        return [MemberResponse.model_validate(member) for member in members]

    def add_member(self, member: AddMember) -> MemberResponse:
        new_member = self.member_repo.add_member(member)
        self.db.commit()
        return MemberResponse.model_validate(new_member)