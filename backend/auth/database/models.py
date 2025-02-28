from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    tablename = "users"  # Match PostgreSQL table name

    id = Column(String, primary_key=True)  # Assuming Django's default UUID or AutoField
    email = Column(Text, unique=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    password = Column(Text, nullable=False)
    two_fa_secret = Column(Text, nullable=True)

    full_name = Column(Text, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    nickname = Column(String(50), nullable=True)

    gender = Column(String(20), nullable=True)
    picture_url = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
