from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from backend.auth.database.database import Base
from datetime import datetime, UTC


class User(Base):
    __tablename__ = "user"
    # id is the user's unique id, nullable and primary key for performance optimisations.
    id = Column(String, primary_key=True, nullable=False)
    # email is unique and not nullable, as it is the primary way to identify a user.
    email = Column(Text, unique=True, nullable=False)
    # password is a hashed passwords.
    password = Column(Text, nullable=False)
    # email_verified is a boolean to check if the user has verified their email.
    email_verified = Column(Boolean, default=False, nullable=False)

    # full_name is the full name of the user, not nullable. This includes first and last name.
    # Intended for performance, as it does not require a join to get the full name.
    #
    # Takes at least 16.68 ns/op to combine first and last name. 0.31 ns/op to get the full name.
    # TODO: Maybe reconsider?
    full_name = Column(Text, nullable=False)
    # first_name is the user's first real name.
    first_name = Column(Text, nullable=False)
    # last_name is the user's last real name.
    last_name = Column(Text, nullable=False)
    # nickname is the user's display name.
    nickname = Column(Text, nullable=False)

    # Gender has no length restraint, must be validated before storing.
    gender = Column(String, nullable=True)
    # date_of_birth is a date object, not nullable.
    date_of_birth = Column(DateTime, nullable=False)
    # picture_url is a link to the user's profile picture.
    picture_url = Column(Text, nullable=True)

    # degree is the degreeID of the user. This assumes it was pre-validated.
    degree = Column(String, nullable=False)
    # year_of_study is the year of study of the user, for example 1 is first year, 2 is second year.
    year_of_study = Column(Integer, nullable=False)
    # grad_date is the date when the user is expected to graduate, for example 11th of May 2025.
    grad_date = Column(DateTime, default=lambda: datetime.now(UTC).date(), nullable=False)

    # created_at stores the time a user was made. Intended to be the final fields in the class.
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    # updated_at stores the time a user was last updated. This is set when the user is created too.
    # It's updated everytime a field is modified.
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    def to_dict(self):
        """
        Converts the User object to the User object in the proto file.
        """

        td = self.__dict__

        # Remove the _sa_instance_state key since this causes a Protocol message User has no "_sa_instance_state" field.
        td.pop('_sa_instance_state', None)

        # Convert the datetime objects to timestamps (unix time).
        td['created_at'] = int(td['created_at'].timestamp())
        td['updated_at'] = int(td['updated_at'].timestamp())
        td['grad_date'] = int(td['grad_date'].timestamp())
        td['dob'] = int(td['date_of_birth'].timestamp())

        # Get rid of fields that don't exist within the user object,
        # that's specified in the proto file.
        td.pop('date_of_birth', None)
        td['degree_id'] = td['degree']
        td.pop('degree', None)

        # Get rid of password as it should never be revealed in a dictionary
        td.pop('password', None)

        return td


class UserTag(Base):
    """
    This table specifies all Tags a User is interested in.
    """
    __tablename__ = "user_tag"

    # id is the unique id of the user_tag.
    id = Column(String, primary_key=True, nullable=False)
    # tag_id is the id of the tag. This assumes it was pre-validated.
    tag_id = Column(String, nullable=False)
    # user_id is the id of the user. This does reference the user table.La
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
