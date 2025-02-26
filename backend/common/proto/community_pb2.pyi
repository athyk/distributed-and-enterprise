from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommunityCreateRequest(_message.Message):
    __slots__ = ("name", "description", "public", "tags", "degrees", "user_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    public: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    degrees: _containers.RepeatedScalarFieldContainer[str]
    user_id: int
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., public: bool = ..., tags: _Optional[_Iterable[str]] = ..., degrees: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommunityUpdateRequest(_message.Message):
    __slots__ = ("id", "name", "description", "public", "tags", "degrees", "user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    public: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    degrees: _containers.RepeatedScalarFieldContainer[str]
    user_id: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., public: bool = ..., tags: _Optional[_Iterable[str]] = ..., degrees: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommunityViewRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CommunityDeleteRequest(_message.Message):
    __slots__ = ("id", "user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_id: int
    def __init__(self, id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class BasicCommunityResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityIDResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    id: int
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., id: _Optional[int] = ...) -> None: ...

class CommunityDataResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "id", "name", "description", "public", "tags", "degrees")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    id: int
    name: str
    description: str
    public: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    degrees: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., public: bool = ..., tags: _Optional[_Iterable[str]] = ..., degrees: _Optional[_Iterable[str]] = ...) -> None: ...
