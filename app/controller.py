from sqlalchemy.exc import SQLAlchemyError
from app.db_schemas import User, Blog
from app.utils import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)
from fastapi import HTTPException, status
from app.s3_service import s3_service


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


class BlogManagement:
    def __init__(self):
        pass

    @classmethod
    def create_user(cls, db, **usermodel):
        try:
            username = usermodel.get("username")
            email = usermodel.get("email")
            password = usermodel.get("password")

            existing_user = db.query(User).filter(User.email == email).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {email} already exists",
                )

            existing_username = db.query(User).filter(User.username == username).first()

            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username {username} already exists",
                )

            hashed_password = hash_password(password)

            new_user = User(username=username, email=email, password=hashed_password)

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while creating user",
            )

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating user",
            )

    @classmethod
    def login_user(cls, db, username, password):
        try:
            if not username or not password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username and password are required",
                )

            user_exist = db.query(User).filter(User.username == username).first()
            if not user_exist:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            if not verify_password(password, user_exist.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                )

            token = create_access_token(
                data={"user_id": user_exist.id, "username": user_exist.username}
            )
            return {
                "access_token": token,
                "token_type": "bearer",
                "user_id": user_exist.id,
                "sub": user_exist.username,
            }
        except Exception as e:
            print(f"Login error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during authentication",
            )

    @classmethod
    def create_blog(cls, db, token, file, **blog):
        try:

            payload = verify_access_token(token)
            user = get_user_by_username(db, username=payload["username"])
            title = blog.get("title")
            content = blog.get("content")
            image_url = None
            if file:
                print("calling")
                image_url = s3_service.upload_image(file, user.id)
            print(image_url)
            new_blog = Blog(
                title=title, content=content, author_id=user.id, image_url=image_url
            )
            db.add(new_blog)
            db.commit()
            db.refresh(new_blog)
            return new_blog
        except Exception as e:
            print(f"Create blog error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during blog creation",
            )

    @classmethod
    def get_blogs(cls, db, token):
        try:
            payload = verify_access_token(token)
            user = get_user_by_username(db, username=payload["username"])
            user_all_blogs = db.query(Blog).filter(Blog.author_id == user.id).all()
            if not user_all_blogs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No blogs found for this user",
                )
            return user_all_blogs
        except Exception as e:
            print(f"Create blog error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during blog creation",
            )

    @classmethod
    def get_blog(cls, db, token, blog_id):
        try:
            payload = verify_access_token(token)
            user = get_user_by_username(db, username=payload["username"])
            user_blog = db.query(Blog).filter(Blog.id == blog_id).first()
            if not user_blog:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Blog not found",
                )
            if user_blog.author_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not the author of this blog",
                )
            return user_blog
        except Exception as e:
            print(f"Create blog error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during blog creation",
            )

    @classmethod
    def update_blog(cls, db, blog_id, token, **blog):
        try:
            payload = verify_access_token(token)
            user = get_user_by_username(db, username=payload["username"])

            update_blog = db.query(Blog).filter(Blog.id == blog_id).first()
            if not update_blog:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Blog not found",
                )

            if update_blog.author_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not the author of this blog",
                )
            for key, value in blog.items():
                setattr(update_blog, key, value)

            db.commit()
            db.refresh(update_blog)
            return update_blog
        except Exception as e:
            print(f"Update blog error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during blog update",
            )

    @classmethod
    def delete_blog(cls, db, token, blog_id):
        try:
            payload = verify_access_token(token)
            user = get_user_by_username(db, username=payload["username"])

            delete_blog = db.query(Blog).filter(Blog.id == blog_id).first()
            if not delete_blog:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Blog not found",
                )

            if delete_blog.author_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not the author of this blog",
                )

            image_url = delete_blog.image_url
            db.delete(delete_blog)
            db.commit()

            if image_url:
                s3_service.delete_image(image_url)
            return {"message": "Blog deleted successfully"}
        except Exception as e:
            print(f"Delete blog error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during blog deletion",
            )
