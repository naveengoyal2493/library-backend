from fastapi import APIRouter
from app.routers.book_routers import router as book_router
from app.routers.member_routers import router as member_router
from app.routers.book_loan_routers import router as loan_router

api_router = APIRouter()

api_router.include_router(book_router, prefix="/books", tags=["Books"])
api_router.include_router(loan_router, prefix="/loans", tags=["Loans"])
api_router.include_router(member_router, prefix="/members", tags=["Members"])