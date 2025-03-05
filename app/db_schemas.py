from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.utcnow)
    modified_at = Column(DateTime, default=func.utcnow, onupdate=func.utcnow)

    blogs = relationship("Blog", back_populates="author", cascade="all, delete")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String(500), nullable=True)  # Increased length for URLs
    created_at = Column(DateTime, default=func.utcnow)
    modified_at = Column(DateTime, default=func.utcnow, onupdate=func.utcnow)

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="blogs")
