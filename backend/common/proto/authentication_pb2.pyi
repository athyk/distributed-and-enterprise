from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegistrationRequest(_message.Message):
    __slots__ = ("email", "password", "first_name", "last_name", "dob", "gender", "degree", "year_of_study", "grad_year", "tag")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    DOB_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    DEGREE_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    GRAD_YEAR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    first_name: str
    last_name: str
    dob: str
    gender: str
    degree: str
    year_of_study: int
    grad_year: str
    tag: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., dob: _Optional[str] = ..., gender: _Optional[str] = ..., degree: _Optional[str] = ..., year_of_study: _Optional[int] = ..., grad_year: _Optional[str] = ..., tag: _Optional[_Iterable[str]] = ...) -> None: ...

class AuthenticationResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "user_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    user_id: int
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class EmailAuthRequest(_message.Message):
    __slots__ = ("email", "skip")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    email: str
    skip: bool
    def __init__(self, email: _Optional[str] = ..., skip: bool = ...) -> None: ...

class EmailAuthSent(_message.Message):
    __slots__ = ("sent", "error_message")
    SENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sent: bool
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, sent: bool = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class EmailAuthVerify(_message.Message):
    __slots__ = ("email", "otp", "id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    otp: int
    id: str
    def __init__(self, email: _Optional[str] = ..., otp: _Optional[int] = ..., id: _Optional[str] = ...) -> None: ...

class EmailVerifiedResponse(_message.Message):
    __slots__ = ("verified", "error_message")
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    verified: bool
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, verified: bool = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...
