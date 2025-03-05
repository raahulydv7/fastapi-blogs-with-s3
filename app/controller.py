from sqlalchemy.exc import SQLAlchemyError
from app.db_schemas import User
from app.utils import hash_password
from fastapi import HTTPException, status

class BlogManagement:
    def __init__(self):
        pass

    @classmethod
    def create_user(cls, db, **usermodel):
        try:
            username = usermodel.get('username')
            email = usermodel.get('email')
            password = usermodel.get('password')

            
            existing_user = db.query(User).filter(User.email == email).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {email} already exists"
                )

            
            existing_username = db.query(User).filter(User.username == username).first()

            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username {username} already exists"
                )

            
            hashed_password = hash_password(password)

            
            new_user = User(
                username=username,
                email=email,
                password=hashed_password
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return new_user
        
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while creating user"
            )

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating user"
            )
