from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

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
