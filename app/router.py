from fastapi import APIRouter, Depends
from app.controller import BlogManagement
from app.models import UserCreate, UserLogin
from app.db_connection import pg_session
from sqlalchemy.orm import Session


routes = APIRouter()


@routes.post("/user-create/")
def register_user(usermodel: UserCreate, db: Session = Depends(pg_session)):
    return BlogManagement.create_user(db, **usermodel.dict())


@routes.post("/login")
def login_user(userlogin: UserLogin, db: Session = Depends(pg_session)):
    return BlogManagement.login_user(db, **userlogin.dict())
