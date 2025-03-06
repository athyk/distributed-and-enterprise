from sqlalchemy import Column, String, Boolean, DateTime, Date, Text, ForeignKey, Integer
from backend.auth.database.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    two_fa_secret = Column(Text, nullable=True)
    account_verified = Column(Boolean, default=False, nullable=False)

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, default=lambda: datetime.utcnow().date(), nullable=False)
    picture_url = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, nullable=True)

    degree = Column(Integer, ForeignKey('degree.id'), nullable=False)

    year_of_study = Column(Integer, nullable=False)
    grad_year = Column(Date, default=lambda: datetime.utcnow().date(), nullable=False)


class Degree(Base):
    __tablename__ = "degree"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)


class UserTag(Base):
    __tablename__ = "user_tag"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
