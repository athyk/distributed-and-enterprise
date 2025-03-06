from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataListResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    data: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., data: _Optional[_Iterable[str]] = ...) -> None: ...
