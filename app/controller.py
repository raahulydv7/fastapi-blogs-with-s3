from sqlalchemy.exc import SQLAlchemyError
from app.db_schemas import User
from app.utils import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


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
    def login_user(cls, db, **userlogin):
        try:
            username = userlogin.get("username")
            password = userlogin.get("password")

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
                data={"user_id": user_exist.id, "username": user_exist.username} )
            return {
            "access_token": token, 
            "token_type": "bearer",
            "user_id": user_exist.id,
            "username": user_exist.username
            }
        except Exception as e:
            print(f"Login error: {str(e)}")
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )
