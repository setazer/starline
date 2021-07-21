from dataclasses import dataclass, field
from typing import Any

from utils import prepare_logger

log = prepare_logger(__name__)


@dataclass
class PostFile:
    name: str = None
    extension: str = None
    url: str = None
    valid: bool = True
    hash: str = None


@dataclass
class PostMeta:
    source: str
    post_id: str
    url: str = None
    authors: set[str] = field(default_factory=set)
    characters: set[str] = field(default_factory=set)
    copyright: set[str] = field(default_factory=set)
    height: int = 0
    width: int = 0


@dataclass
class Post:
    meta: PostMeta
    file: PostFile = PostFile()

    def __repr__(self):
        return f"Post [{self.meta.source}:{self.meta.post_id}] ({self.meta.width}x{self.meta.height})"

    def __eq__(self, other):
        return (self.file.hash and self.file.hash == other.file.hash
                or self.meta.source == other.meta.source and self.meta.post_id == other.meta.post_id)

    def __hash__(self):
        return hash((self.meta.source, self.meta.post_id))


@dataclass
class Message:
    msg: str


@dataclass
class TelegramMessage(Message):
    chat: int = None
    sender: int = None

    @classmethod
    def from_telegram(cls, message):
        return cls(chat=message.chat.id, sender=message.from_user, msg=message.text)


@dataclass
class LoggingMessage(Message):
    level: int


@dataclass
class PublishResult:
    success: bool
    extra: Any = None


@dataclass
class QueueItem:
    post: Post
    lock: bool = False
