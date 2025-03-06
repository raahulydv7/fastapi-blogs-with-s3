from fastapi import APIRouter, Depends, Form, UploadFile, File
from app.controller import BlogManagement
from app.models import UserCreate, BlogCreate
from app.db_connection import pg_session
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


routes = APIRouter()


@routes.post("/users/")
def register_user(usermodel: UserCreate, db: Session = Depends(pg_session)):
    return BlogManagement.create_user(db, **usermodel.dict())


@routes.post("/token/")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(pg_session)
):
    return BlogManagement.login_user(db, form_data.username, form_data.password)


from fastapi import Request


@routes.post("/blogs/upload/")
async def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(pg_session),
    token: str = Depends(oauth2_scheme),
):
    form_data = await request.form()
    print("Request Form Data:", form_data)
    blog_data = {"title": title, "content": content}
    return BlogManagement.create_blog(db, token, file, **blog_data)


@routes.get("/blogs")
def get_all_blog(
    db: Session = Depends(pg_session),
    token: str = Depends(oauth2_scheme),
):
    return BlogManagement.get_blogs(db, token)


@routes.get("/blogs/{blog_id}")
def get_blog(
    blog_id: int,
    db: Session = Depends(pg_session),
    token: str = Depends(oauth2_scheme),
):
    return BlogManagement.get_blog(db, token, blog_id)


@routes.put("/blogs/{blog_id}")
def update_blog(blog_id: int,
    blog:BlogCreate,
    db: Session = Depends(pg_session),
    token: str = Depends(oauth2_scheme)):
    return BlogManagement.update_blog(db, blog_id,token, **blog.dict())
    

@routes.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(pg_session),
    token: str = Depends(oauth2_scheme),
):
    return BlogManagement.delete_blog(db, token, blog_id)