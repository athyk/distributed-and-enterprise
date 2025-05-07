from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberActionResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class UserRequest(_message.Message):
    __slots__ = ("community_id", "user_id", "action_user_id")
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_USER_ID_FIELD_NUMBER: _ClassVar[int]
    community_id: int
    user_id: int
    action_user_id: int
    def __init__(self, community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., action_user_id: _Optional[int] = ...) -> None: ...

class Entry(_message.Message):
    __slots__ = ("user_id", "status")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    status: str
    def __init__(self, user_id: _Optional[int] = ..., status: _Optional[str] = ...) -> None: ...

class AllUsers(_message.Message):
    __slots__ = ("community_id", "user_id", "action_user_id", "users")
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    community_id: int
    user_id: int
    action_user_id: int
    users: _containers.RepeatedCompositeFieldContainer[Entry]
    def __init__(self, community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., action_user_id: _Optional[int] = ..., users: _Optional[_Iterable[_Union[Entry, _Mapping]]] = ...) -> None: ...
