from fastapi import APIRouter, Depends
from controller import BlogManagement
from models import UserCreate
from db_connection import pg_session
from sqlalchemy.orm import session


router = APIRouter()


@router.post("/user-create/")
def register_user(usermodel: UserCreate, db: session = Depends(pg_session)):
    return BlogManagement.create_user(db, **usermodel.dict())
