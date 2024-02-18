import dependency2_pb2 as _dependency2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dependency1(_message.Message):
    __slots__ = ("field1", "field2")
    FIELD1_FIELD_NUMBER: _ClassVar[int]
    FIELD2_FIELD_NUMBER: _ClassVar[int]
    field1: str
    field2: _dependency2_pb2.Dependency2
    def __init__(self, field1: _Optional[str] = ..., field2: _Optional[_Union[_dependency2_pb2.Dependency2, _Mapping]] = ...) -> None: ...
