import logging
from dataclasses import dataclass, field


log = logging.getLogger(__name__)


@dataclass
class PostFile:
    name: str
    extension: str
    url: str
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
    file: PostFile = None

    def __repr__(self):
        return f"Image [{self.meta.source}:{self.meta.post_id}] ({self.meta.width}x{self.meta.height})"


@dataclass(frozen=True)
class Message:
    msg: str


@dataclass(frozen=True)
class TelegramMessage(Message):
    chat: int
    sender: int = None

    @classmethod
    def from_telegram(cls, message):
        return cls(chat=message.chat.id, sender=message.from_user, msg=message.text)


@dataclass(frozen=True)
class LoggingMessage(Message):
    level: int
