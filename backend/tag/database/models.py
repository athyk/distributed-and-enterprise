from sqlalchemy import Column, DateTime, Text, Integer
from backend.tag.database.database import Base
from datetime import datetime, UTC


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, unique=True, nullable=False, index=True)
    count = Column(Integer, default=0, nullable=False, index=True)
    # created_at stores the time a user was made. Intended to be the final fields in the class.
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    # updated_at stores the time a user was last updated. This is set when the user is created too.
    # It's updated everytime a field is modified.
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    def to_dict(self) -> dict:
        """
        Converts the Tag object to the Tag object in the proto file.
        """
        td = self.__dict__
        # Remove the _sa_instance_state key since this causes a Protocol message Tag has no "_sa_instance_state" field.
        td.pop('_sa_instance_state', None)
        # Convert the datetime objects to timestamps (unix time).
        td['created_at'] = int(td['created_at'].timestamp())
        td['updated_at'] = int(td['updated_at'].timestamp())

        return td
