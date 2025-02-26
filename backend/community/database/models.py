from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from backend.community.database.database import Base
from datetime import datetime



class Community(Base):
    __tablename__ = 'community'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(511))
    public = Column(Boolean, default=True)


class Degree(Base):
    __tablename__ = 'degree'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


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
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    edit_datetime = Column(DateTime, default=datetime.utcnow, nullable=True)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_edited_user_id = Column(String(50), nullable=True)


class CommunityDegree(Base):
    __tablename__ = 'community_degree'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    degree_id = Column(Integer, ForeignKey('degree.id'), nullable=False)


class CommunityTag(Base):
    __tablename__ = 'community_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)


class EventTag(Base):
    __tablename__ = 'event_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)


class AnnouncementTag(Base):
    __tablename__ = 'announcement_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('announcement.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)


class Event(Base):
    __tablename__ = 'event'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    community_id = Column(Integer, ForeignKey('announcement.id'), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    location = Column(String(200), nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration = Column(String(2), nullable=False)

