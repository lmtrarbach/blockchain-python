from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Block(_message.Message):
    __slots__ = ["hash", "nonce", "previous_hash", "timestamp", "transactions"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_HASH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    hash: str
    nonce: int
    previous_hash: str
    timestamp: str
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, hash: _Optional[str] = ..., previous_hash: _Optional[str] = ..., transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ..., timestamp: _Optional[str] = ..., nonce: _Optional[int] = ...) -> None: ...

class SyncRequest(_message.Message):
    __slots__ = ["blocks"]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    blocks: _containers.RepeatedCompositeFieldContainer[Block]
    def __init__(self, blocks: _Optional[_Iterable[_Union[Block, _Mapping]]] = ...) -> None: ...

class SyncResponse(_message.Message):
    __slots__ = ["blocks"]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    blocks: _containers.RepeatedCompositeFieldContainer[Block]
    def __init__(self, blocks: _Optional[_Iterable[_Union[Block, _Mapping]]] = ...) -> None: ...

class Transaction(_message.Message):
    __slots__ = ["amount", "recipient", "sender"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    amount: int
    recipient: str
    sender: str
    def __init__(self, sender: _Optional[str] = ..., recipient: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...
