from sqlalchemy import Column, String, Boolean, DateTime, Date, Text, Integer, ForeignKey
from backend.accounts.database.database import Base, get_db
from datetime import datetime, UTC


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    two_fa_secret = Column(Text, nullable=True)
    # email_verified is a boolean to check if the user has verified their email.
    email_verified = Column(Boolean, default=False, nullable=False)

    # rank is a string representing a static global rank, like "user", or "admin"
    # this is done instead of a permissions system and custom rank system to provide simplicity
    rank = Column(String, default="user", nullable=False)

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, default=lambda: datetime.now(UTC), nullable=False)
    # picture_url is a link to the user's profile picture.
    picture_url = Column(Text, nullable=True)

    # degree_id is the id of the main degree that the user is studying.
    degree_id = Column(Integer, nullable=False)

    year_of_study = Column(Integer, nullable=False)
    grad_date = Column(Date, default=lambda: datetime.now(UTC), nullable=False)

    # created_at stores the time a user was made. Intended to be the final fields in the class.
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    # updated_at stores the time a user was last updated. This is set when the user is created too.
    # It's updated everytime a field is modified.
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    def get_tags(self, session):
        """
        Get all the tags that the user has.
        """
        return session.query(UserTag).filter(UserTag.user_id == self.id).all()

    def to_dict(self) -> dict:
        """
        Converts the User object to the User object in the proto file.
        """
        td = self.__dict__
        # Remove the _sa_instance_state key since this causes a Protocol message User has no "_sa_instance_state" field.
        td.pop('_sa_instance_state', None)
        # Convert the datetime objects to timestamps (unix time).
        td['created_at'] = int(td['created_at'].timestamp())
        td['updated_at'] = int(td['updated_at'].timestamp())
        # Convert the date objects to strings.
        td['date_of_birth'] = str(td['date_of_birth'])
        td['grad_date'] = str(td['grad_date'])

        td["picture_url"] = td["picture_url"] if td["picture_url"] else ""

        # Get rid of password and 2fa as it should never be revealed in a dictionary
        td.pop('password', None)
        td.pop('two_fa_secret', None)

        with get_db() as session:  # Get the tags for the user, display as a list of tag ids
            tags = self.get_tags(session)
            td['tags'] = [tag.tag_id for tag in tags]
            # Could always convert the tag ids to tag names here if needed or do a dictionary.

        return td


class UserTag(Base):
    __tablename__ = "user_tag"

    id = Column(Integer, primary_key=True, nullable=False)
    tag_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    # user_id is not a foreign key to allow the post to be kept if the user is deleted.
    # as well as to allow Post to be easily moved to another service.
    user_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    def get_tags(self, session):
        """
        Get all the tags that the post has.
        """
        return session.query(PostTag).filter(PostTag.post_id == self.id).all()

    def get_images(self, session):
        """
        Get all the images that the post has.
        """
        return session.query(PostImage).filter(PostImage.post_id == self.id).all()

    def to_dict(self) -> dict:
        """
        Converts the Post object to the Post object in the proto file.
        """
        td = self.__dict__
        # Remove the _sa_instance_state key since this causes a Protocol message Post has no "_sa_instance_state" field.
        td.pop('_sa_instance_state', None)
        # Convert the datetime objects to timestamps (unix time).
        td['created_at'] = int(td['created_at'].timestamp())
        td['updated_at'] = int(td['updated_at'].timestamp())

        with get_db() as session:  # Get the tags and images for the post, display as a list of tag ids and image urls
            tags = self.get_tags(session)
            td['tags'] = [tag.tag_id for tag in tags]
            # Could always convert the tag ids to tag names here if needed or do a dictionary.
            images = self.get_images(session)
            td['images'] = [image.image_url for image in images]

        return td


class PostTag(Base):
    __tablename__ = "post_tag"
    id = Column(Integer, primary_key=True, nullable=False)
    tag_id = Column(Integer, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)


class PostImage(Base):
    __tablename__ = "post_image"
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    image_url = Column(Text, nullable=False)
