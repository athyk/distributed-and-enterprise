from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityData(_message.Message):
    __slots__ = ("id", "name", "description", "public_community", "member_count", "tags", "degrees")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    public_community: int
    member_count: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    degrees: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., public_community: _Optional[int] = ..., member_count: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., degrees: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityFilter(_message.Message):
    __slots__ = ("status", "communities")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMUNITIES_FIELD_NUMBER: _ClassVar[int]
    status: RequestResponse
    communities: _containers.RepeatedCompositeFieldContainer[CommunityData]
    def __init__(self, status: _Optional[_Union[RequestResponse, _Mapping]] = ..., communities: _Optional[_Iterable[_Union[CommunityData, _Mapping]]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("user_id", "is_with", "name", "public", "minimum_members", "tags", "degrees", "offset", "limit")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_WITH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEGREES_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    is_with: int
    name: str
    public: int
    minimum_members: int
    tags: _containers.RepeatedScalarFieldContainer[int]
    degrees: _containers.RepeatedScalarFieldContainer[int]
    offset: int
    limit: int
    def __init__(self, user_id: _Optional[int] = ..., is_with: _Optional[int] = ..., name: _Optional[str] = ..., public: _Optional[int] = ..., minimum_members: _Optional[int] = ..., tags: _Optional[_Iterable[int]] = ..., degrees: _Optional[_Iterable[int]] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...
