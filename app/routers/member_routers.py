from starlette import status
from app.database import get_db
from app.schemas.member_schemas import MemberResponse, AddMember
from app.services.member_service import MemberService
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    return MemberService(db)

@router.get("/", response_model=List[MemberResponse], status_code=status.HTTP_200_OK)
def get_members(service: MemberService = Depends(get_member_service)):
    return service.get_members()

@router.get("/{member_id}", response_model=MemberResponse, status_code=status.HTTP_200_OK)
def get_member(member_id: int, service: MemberService = Depends(get_member_service)):
    return service.get_member_by_id(member_id)

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: AddMember, service: MemberService = Depends(get_member_service)):
    return service.add_member(member)