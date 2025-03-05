from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommunityAnnouncementCreateRequest(_message.Message):
    __slots__ = ("community_id", "user_id", "title", "description", "tags")
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    community_id: int
    user_id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityAnnouncementUpdateRequest(_message.Message):
    __slots__ = ("announcement_id", "community_id", "user_id", "title", "description", "tags")
    ANNOUNCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    announcement_id: int
    community_id: int
    user_id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, announcement_id: _Optional[int] = ..., community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityAnnouncementViewSelectRequest(_message.Message):
    __slots__ = ("community_id", "user_id", "offset", "limit")
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    community_id: int
    user_id: int
    offset: int
    limit: int
    def __init__(self, community_id: _Optional[int] = ..., user_id: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class CommunityAnnouncementGlobalRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class CommunityAnnouncementViewSelectOneRequest(_message.Message):
    __slots__ = ("announcement_id", "community_id", "user_id")
    ANNOUNCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    announcement_id: int
    community_id: int
    user_id: int
    def __init__(self, announcement_id: _Optional[int] = ..., community_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommunityAnnouncementDeleteRequest(_message.Message):
    __slots__ = ("announcement_id", "community_id", "user_id")
    ANNOUNCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    announcement_id: int
    community_id: int
    user_id: int
    def __init__(self, announcement_id: _Optional[int] = ..., community_id: _Optional[int] = ..., user_id: _Optional[int] = ...) -> None: ...

class CommunityAnnouncementResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ...) -> None: ...

class CommunityAnnouncementData(_message.Message):
    __slots__ = ("id", "title", "description", "tags", "user_id", "uploaded", "edit_user_id", "edit_uploaded")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_FIELD_NUMBER: _ClassVar[int]
    EDIT_USER_ID_FIELD_NUMBER: _ClassVar[int]
    EDIT_UPLOADED_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    user_id: int
    uploaded: str
    edit_user_id: int
    edit_uploaded: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ..., uploaded: _Optional[str] = ..., edit_user_id: _Optional[int] = ..., edit_uploaded: _Optional[str] = ...) -> None: ...

class SingleCommunityAnnouncementResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "announcement")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    announcement: CommunityAnnouncementData
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., announcement: _Optional[_Union[CommunityAnnouncementData, _Mapping]] = ...) -> None: ...

class AllCommunityAnnouncementResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "announcements")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    announcements: _containers.RepeatedCompositeFieldContainer[CommunityAnnouncementData]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., announcements: _Optional[_Iterable[_Union[CommunityAnnouncementData, _Mapping]]] = ...) -> None: ...

class GlobalCommunityAnnouncementData(_message.Message):
    __slots__ = ("id", "community_id", "title", "description", "tags", "user_id", "uploaded", "edit_user_id", "edit_uploaded")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_FIELD_NUMBER: _ClassVar[int]
    EDIT_USER_ID_FIELD_NUMBER: _ClassVar[int]
    EDIT_UPLOADED_FIELD_NUMBER: _ClassVar[int]
    id: int
    community_id: int
    title: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    user_id: int
    uploaded: str
    edit_user_id: int
    edit_uploaded: str
    def __init__(self, id: _Optional[int] = ..., community_id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., user_id: _Optional[int] = ..., uploaded: _Optional[str] = ..., edit_user_id: _Optional[int] = ..., edit_uploaded: _Optional[str] = ...) -> None: ...

class GlobalCommunityAnnouncementResponse(_message.Message):
    __slots__ = ("success", "http_status", "error_message", "global_announcements")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTTP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    http_status: int
    error_message: _containers.RepeatedScalarFieldContainer[str]
    global_announcements: _containers.RepeatedCompositeFieldContainer[GlobalCommunityAnnouncementData]
    def __init__(self, success: bool = ..., http_status: _Optional[int] = ..., error_message: _Optional[_Iterable[str]] = ..., global_announcements: _Optional[_Iterable[_Union[GlobalCommunityAnnouncementData, _Mapping]]] = ...) -> None: ...
