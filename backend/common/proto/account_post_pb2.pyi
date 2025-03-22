from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountPost(_message.Message):
    __slots__ = ("id", "title", "description", "tags", "user_id", "created_at", "updated_at", "images")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[int]
    user_id: int
    created_at: int
    updated_at: int
    images: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[int]] = ..., user_id: _Optional[int] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., images: _Optional[_Iterable[str]] = ...) -> None: ...

class AccountPostCreateRequest(_message.Message):
    __slots__ = ("user_id", "title", "description", "tags", "images")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[int]
    images: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, user_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[int]] = ..., images: _Optional[_Iterable[str]] = ...) -> None: ...

class AccountPostUpdateRequest(_message.Message):
    __slots__ = ("post_id", "user_id", "title", "description", "tags", "images")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    user_id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[int]
    images: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, post_id: _Optional[int] = ..., user_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[int]] = ..., images: _Optional[_Iterable[str]] = ...) -> None: ...

class AccountPostGetRequest(_message.Message):
    __slots__ = ("post_id", "user_id")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    user_id: int
    def __init__(self, post_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class AccountPostListRequest(_message.Message):
    __slots__ = ("user_id", "tag_id", "title", "description", "offset", "limit")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    tag_id: int
    title: str
    description: str
    offset: int
    limit: int
    def __init__(self, user_id: _Optional[int] = ..., tag_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class AccountPostResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "post")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    post: AccountPost
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., post: _Optional[_Union[AccountPost, _Mapping]] = ...) -> None: ...

class AccountPostListResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "posts")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    posts: _containers.RepeatedCompositeFieldContainer[AccountPost]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., posts: _Optional[_Iterable[_Union[AccountPost, _Mapping]]] = ...) -> None: ...
