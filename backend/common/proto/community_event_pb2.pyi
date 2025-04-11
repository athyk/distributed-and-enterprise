from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventDataRequest(_message.Message):
    __slots__ = ("user_id", "community_id", "title", "description", "location", "datetime", "duration", "tags", "lat_lng")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LAT_LNG_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    community_id: int
    title: str
    description: str
    location: str
    datetime: str
    duration: int
    tags: _containers.RepeatedScalarFieldContainer[int]
    lat_lng: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, user_id: _Optional[int] = ..., community_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., location: _Optional[str] = ..., datetime: _Optional[str] = ..., duration: _Optional[int] = ..., tags: _Optional[_Iterable[int]] = ..., lat_lng: _Optional[_Iterable[float]] = ...) -> None: ...

class EventResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateResponse(_message.Message):
    __slots__ = ("status", "event_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    status: EventResponse
    event_id: int
    def __init__(self, status: _Optional[_Union[EventResponse, _Mapping]] = ..., event_id: _Optional[int] = ...) -> None: ...

class ViewEvent(_message.Message):
    __slots__ = ("id", "community_id", "title", "description", "location", "datetime", "duration", "tags", "latitude", "longitude")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    id: int
    community_id: int
    title: str
    description: str
    location: str
    datetime: str
    duration: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    latitude: float
    longitude: float
    def __init__(self, id: _Optional[int] = ..., community_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., location: _Optional[str] = ..., datetime: _Optional[str] = ..., duration: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class ViewOneRequest(_message.Message):
    __slots__ = ("user_id", "community_id", "event_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    community_id: int
    event_id: int
    def __init__(self, user_id: _Optional[int] = ..., community_id: _Optional[int] = ..., event_id: _Optional[int] = ...) -> None: ...

class ViewRequest(_message.Message):
    __slots__ = ("community_id", "user_id", "offset", "limit")
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    community_id: int
    user_id: int
    offset: int
    limit: int
    def __init__(self, community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ViewGlobalRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ViewResponse(_message.Message):
    __slots__ = ("status", "event")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    status: EventResponse
    event: _containers.RepeatedCompositeFieldContainer[ViewEvent]
    def __init__(self, status: _Optional[_Union[EventResponse, _Mapping]] = ..., event: _Optional[_Iterable[_Union[ViewEvent, _Mapping]]] = ...) -> None: ...

class EditEventRequest(_message.Message):
    __slots__ = ("event_id", "event_data")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    event_data: EventDataRequest
    def __init__(self, event_id: _Optional[int] = ..., event_data: _Optional[_Union[EventDataRequest, _Mapping]] = ...) -> None: ...

class DeleteEventRequest(_message.Message):
    __slots__ = ("user_id", "community_id", "event_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    community_id: int
    event_id: int
    def __init__(self, user_id: _Optional[int] = ..., community_id: _Optional[int] = ..., event_id: _Optional[int] = ...) -> None: ...
