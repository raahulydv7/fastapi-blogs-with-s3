from fastapi import APIRouter, Depends
from app.controller import BlogManagement
from app.models import UserCreate
from app.db_connection import pg_session
from sqlalchemy.orm import session


routes = APIRouter()


@routes.post("/user-create/")
def register_user(usermodel: UserCreate, db: session = Depends(pg_session)):
    return BlogManagement.create_user(db, **usermodel.dict())
