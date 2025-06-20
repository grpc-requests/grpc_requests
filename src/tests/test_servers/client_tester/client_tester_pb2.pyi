from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestRequest(_message.Message):
    __slots__ = ("factor", "readings", "uuid", "sample_flag", "request_name", "meta_data")
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    READINGS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FLAG_FIELD_NUMBER: _ClassVar[int]
    REQUEST_NAME_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    factor: int
    readings: _containers.RepeatedScalarFieldContainer[float]
    uuid: int
    sample_flag: bool
    request_name: str
    meta_data: _containers.RepeatedCompositeFieldContainer[Metadata]
    def __init__(self, factor: _Optional[int] = ..., readings: _Optional[_Iterable[float]] = ..., uuid: _Optional[int] = ..., sample_flag: bool = ..., request_name: _Optional[str] = ..., meta_data: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("key", "data")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    key: str
    data: bytes
    def __init__(self, key: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class TestResponse(_message.Message):
    __slots__ = ("average", "feedback")
    AVERAGE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    average: float
    feedback: str
    def __init__(self, average: _Optional[float] = ..., feedback: _Optional[str] = ...) -> None: ...
