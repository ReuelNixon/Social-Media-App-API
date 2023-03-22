from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    uid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # is_active = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    uid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user = relationship("User")
    pid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post = relationship("Post")