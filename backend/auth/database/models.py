from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    tablename = "users"

    id = Column(String, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    two_fa_secret = Column(Text, nullable=True)
    account_verified = Column(Boolean, default=False, nullable=False)

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    nickname = Column(String(50), nullable=True)

    gender = Column(String(20), nullable=True)
    picture_url = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    degree = Column(Integer, ForeignKey('degree.id'), nullable=False)


class Degree(Base):
    tablename = "degree"

    id = Column(String, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class Tag(Base):
    tablename = "tag"

    id = Column(String, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class UserTag(Base):
    tablename = "user_tag"

    id = Column(String, primary_key=True)
    degree_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
