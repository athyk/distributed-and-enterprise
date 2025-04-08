from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageChannel(_message.Message):
    __slots__ = ("id", "owner_id", "ids", "name", "is_group")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_GROUP_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: int
    ids: _containers.RepeatedScalarFieldContainer[int]
    name: str
    is_group: bool
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[int] = ..., ids: _Optional[_Iterable[int]] = ..., name: _Optional[str] = ..., is_group: bool = ...) -> None: ...

class MessageChannelCreateRequest(_message.Message):
    __slots__ = ("ids", "owner_id")
    IDS_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    owner_id: int
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., owner_id: _Optional[int] = ...) -> None: ...

class MessageChannelUpdateRequest(_message.Message):
    __slots__ = ("id", "name", "member_to_remove", "member_to_add", "member_to_be_owner", "delete", "requesting_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    MEMBER_TO_BE_OWNER_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    member_to_remove: int
    member_to_add: int
    member_to_be_owner: int
    delete: bool
    requesting_user_id: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., member_to_remove: _Optional[int] = ..., member_to_add: _Optional[int] = ..., member_to_be_owner: _Optional[int] = ..., delete: bool = ..., requesting_user_id: _Optional[int] = ...) -> None: ...

class MessageChannelResponse(_message.Message):
    __slots__ = ("success", "error", "channel")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    channel: MessageChannel
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., channel: _Optional[_Union[MessageChannel, _Mapping]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("id", "channel_id", "user_id", "content", "edited", "is_bot", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EDITED_FIELD_NUMBER: _ClassVar[int]
    IS_BOT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    channel_id: str
    user_id: int
    content: str
    edited: bool
    is_bot: bool
    created_at: int
    updated_at: int
    def __init__(self, id: _Optional[str] = ..., channel_id: _Optional[str] = ..., user_id: _Optional[int] = ..., content: _Optional[str] = ..., edited: bool = ..., is_bot: bool = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...

class MessageRequest(_message.Message):
    __slots__ = ("message", "is_bot", "channel_id", "user_id")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_BOT_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    message: str
    is_bot: bool
    channel_id: str
    user_id: int
    def __init__(self, message: _Optional[str] = ..., is_bot: bool = ..., channel_id: _Optional[str] = ..., user_id: _Optional[int] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("success", "error", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    message: Message
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., message: _Optional[_Union[Message, _Mapping]] = ...) -> None: ...

class MessageGetRequest(_message.Message):
    __slots__ = ("id", "requesting_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    requesting_user_id: int
    def __init__(self, id: _Optional[str] = ..., requesting_user_id: _Optional[int] = ...) -> None: ...

class MessageUpdateRequest(_message.Message):
    __slots__ = ("id", "message", "requesting_user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUESTING_USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    requesting_user_id: int
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ..., requesting_user_id: _Optional[int] = ...) -> None: ...

class MessageListRequest(_message.Message):
    __slots__ = ("channel_id", "user_id", "content", "limit", "offset")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    user_id: int
    content: str
    limit: int
    offset: int
    def __init__(self, channel_id: _Optional[str] = ..., user_id: _Optional[int] = ..., content: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class MessageListResponse(_message.Message):
    __slots__ = ("success", "error", "messages")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ...) -> None: ...

class MessageChannelListRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class MessageChannelListResponse(_message.Message):
    __slots__ = ("success", "error", "channels")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    channels: _containers.RepeatedCompositeFieldContainer[MessageChannel]
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[MessageChannel, _Mapping]]] = ...) -> None: ...
