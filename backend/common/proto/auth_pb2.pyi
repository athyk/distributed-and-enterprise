from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "email", "email_verified", "full_name", "first_name", "last_name", "nickname", "gender", "dob", "picture_url", "degree_id", "year_of_study", "grad_date", "tags", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    DOB_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    DEGREE_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    GRAD_DATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    email_verified: int
    full_name: str
    first_name: str
    last_name: str
    nickname: str
    gender: str
    dob: int
    picture_url: str
    degree_id: str
    year_of_study: int
    grad_date: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_at: int
    updated_at: int
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., email_verified: _Optional[int] = ..., full_name: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., nickname: _Optional[str] = ..., gender: _Optional[str] = ..., dob: _Optional[int] = ..., picture_url: _Optional[str] = ..., degree_id: _Optional[str] = ..., year_of_study: _Optional[int] = ..., grad_date: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...

class RegistrationRequest(_message.Message):
    __slots__ = ("email", "password", "first_name", "last_name", "nickname", "dob", "gender", "degree", "year_of_study", "grad_date", "tags")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    DOB_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    DEGREE_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    GRAD_DATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    first_name: str
    last_name: str
    nickname: str
    dob: int
    gender: str
    degree: str
    year_of_study: int
    grad_date: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., nickname: _Optional[str] = ..., dob: _Optional[int] = ..., gender: _Optional[str] = ..., degree: _Optional[str] = ..., year_of_study: _Optional[int] = ..., grad_date: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("email", "password", "skip_email")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SKIP_EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    skip_email: bool
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., skip_email: bool = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "user_id", "user", "otp_required")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    OTP_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    user_id: str
    user: User
    otp_required: bool
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., user_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., otp_required: bool = ...) -> None: ...

class LoginVerificationRequest(_message.Message):
    __slots__ = ("user_id", "otp")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    otp: str
    def __init__(self, user_id: _Optional[str] = ..., otp: _Optional[str] = ...) -> None: ...

class LoginVerificationResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "user")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    user: User
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("id", "email", "nickname", "first_name", "last_name", "email_verified", "page", "limit")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    nickname: str
    first_name: str
    last_name: str
    email_verified: int
    page: str
    limit: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., nickname: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email_verified: _Optional[int] = ..., page: _Optional[str] = ..., limit: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("users", "total")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    total: int
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("user", "is_self", "otp")
    USER_FIELD_NUMBER: _ClassVar[int]
    IS_SELF_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    user: User
    is_self: bool
    otp: str
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., is_self: bool = ..., otp: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("id", "is_self", "otp")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_SELF_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    id: str
    is_self: bool
    otp: str
    def __init__(self, id: _Optional[str] = ..., is_self: bool = ..., otp: _Optional[str] = ...) -> None: ...
