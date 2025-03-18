from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "email", "email_verified", "first_name", "last_name", "gender", "date_of_birth", "picture_url", "degree_id", "year_of_study", "grad_date", "tags", "created_at", "updated_at", "rank")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    DEGREE_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    GRAD_DATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    id: int
    email: str
    email_verified: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: str
    picture_url: str
    degree_id: int
    year_of_study: int
    grad_date: str
    tags: _containers.RepeatedScalarFieldContainer[int]
    created_at: int
    updated_at: int
    rank: str
    def __init__(self, id: _Optional[int] = ..., email: _Optional[str] = ..., email_verified: _Optional[int] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., gender: _Optional[str] = ..., date_of_birth: _Optional[str] = ..., picture_url: _Optional[str] = ..., degree_id: _Optional[int] = ..., year_of_study: _Optional[int] = ..., grad_date: _Optional[str] = ..., tags: _Optional[_Iterable[int]] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., rank: _Optional[str] = ...) -> None: ...

class RegistrationRequest(_message.Message):
    __slots__ = ("email", "password", "first_name", "last_name", "date_of_birth", "gender", "degree_id", "year_of_study", "grad_date", "tags", "skip_email", "rank")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    DEGREE_ID_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    GRAD_DATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SKIP_EMAIL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    degree_id: int
    year_of_study: int
    grad_date: str
    tags: _containers.RepeatedScalarFieldContainer[int]
    skip_email: bool
    rank: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., date_of_birth: _Optional[str] = ..., gender: _Optional[str] = ..., degree_id: _Optional[int] = ..., year_of_study: _Optional[int] = ..., grad_date: _Optional[str] = ..., tags: _Optional[_Iterable[int]] = ..., skip_email: bool = ..., rank: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("email", "password", "skip_email", "otp")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SKIP_EMAIL_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    skip_email: bool
    otp: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., skip_email: bool = ..., otp: _Optional[str] = ...) -> None: ...

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
    user_id: int
    user: User
    otp_required: bool
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ..., otp_required: bool = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ("user_id", "email", "first_name", "last_name", "email_verified", "age_from", "age_to", "degree_id", "tag_id", "gender", "year_of_study", "page", "limit")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    AGE_FROM_FIELD_NUMBER: _ClassVar[int]
    AGE_TO_FIELD_NUMBER: _ClassVar[int]
    DEGREE_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    YEAR_OF_STUDY_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    email: str
    first_name: str
    last_name: str
    email_verified: int
    age_from: int
    age_to: int
    degree_id: int
    tag_id: int
    gender: str
    year_of_study: int
    page: int
    limit: int
    def __init__(self, user_id: _Optional[int] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email_verified: _Optional[int] = ..., age_from: _Optional[int] = ..., age_to: _Optional[int] = ..., degree_id: _Optional[int] = ..., tag_id: _Optional[int] = ..., gender: _Optional[str] = ..., year_of_study: _Optional[int] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("users", "total", "success", "http_status", "error_message")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    total: int
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., total: _Optional[int] = ..., success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("user", "is_self", "otp", "skip_email", "password", "new_password")
    USER_FIELD_NUMBER: _ClassVar[int]
    IS_SELF_FIELD_NUMBER: _ClassVar[int]
    OTP_FIELD_NUMBER: _ClassVar[int]
    SKIP_EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user: User
    is_self: bool
    otp: str
    skip_email: bool
    password: str
    new_password: str
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., is_self: bool = ..., otp: _Optional[str] = ..., skip_email: bool = ..., password: _Optional[str] = ..., new_password: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "otp_required")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OTP_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    otp_required: bool
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., otp_required: bool = ...) -> None: ...
