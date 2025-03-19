from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from backend.community.database.database import Base
from datetime import datetime


class Community(Base):
    __tablename__ = 'community'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512))
    public = Column(Boolean, default=True)


class CommunityUser(Base):
    __tablename__ = 'community_users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)


class Announcement(Base):
    __tablename__ = 'announcement'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    datetime = Column(DateTime, default=lambda: datetime(1970, 1, 1), nullable=False)

    title = Column(String(128), nullable=False)
    description = Column(String(2048), nullable=False)
    
    last_edited_user_id = Column(Integer, nullable=True)
    edit_datetime = Column(DateTime, default=lambda: datetime(1970, 1, 1), nullable=True)



class CommunityDegree(Base):
    __tablename__ = 'community_degree'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    degree_id = Column(Integer, nullable=False)


class CommunityTag(Base):
    __tablename__ = 'community_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    tag_id = Column(Integer, nullable=False)


class EventTag(Base):
    __tablename__ = 'event_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    tag_id = Column(Integer, nullable=False)


class AnnouncementTag(Base):
    __tablename__ = 'announcement_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    announcement_id = Column(Integer, ForeignKey('announcement.id'), nullable=False)
    tag_id = Column(Integer, nullable=False)


class Event(Base):
    __tablename__ = 'event'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(1024), nullable=False)
    location = Column(String(200), nullable=False)
    datetime = Column(DateTime, default=lambda: datetime(1970, 1, 1), nullable=False)
    duration = Column(String(2), nullable=False)

