from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRequest(_message.Message):
    __slots__ = ("message", "is_bot")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_BOT_FIELD_NUMBER: _ClassVar[int]
    message: str
    is_bot: bool
    def __init__(self, message: _Optional[str] = ..., is_bot: bool = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("success", "error", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    message: str
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
