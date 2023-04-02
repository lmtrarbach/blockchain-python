from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Peer(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class Peers(_message.Message):
    __slots__ = ["peers"]
    PEERS_FIELD_NUMBER: _ClassVar[int]
    peers: _containers.RepeatedCompositeFieldContainer[Peer]
    def __init__(self, peers: _Optional[_Iterable[_Union[Peer, _Mapping]]] = ...) -> None: ...
