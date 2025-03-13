from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tag(_message.Message):
    __slots__ = ("id", "name", "created_at", "updated_at", "count")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    created_at: int
    updated_at: int
    count: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class TagCreateRequest(_message.Message):
    __slots__ = ("name", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: int
    def __init__(self, name: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class TagCreateResponse(_message.Message):
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

class TagDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class TagDeleteResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class TagGetRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class TagGetResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "tag")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    tag: Tag
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., tag: _Optional[_Union[Tag, _Mapping]] = ...) -> None: ...

class TagListRequest(_message.Message):
    __slots__ = ("page", "limit", "name")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    page: int
    limit: int
    name: str
    def __init__(self, page: _Optional[int] = ..., limit: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class TagListResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "tags")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...
