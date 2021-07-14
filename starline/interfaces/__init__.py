from model import Message, Post, PublishResult


class MessageInterface:
    def send_message(self, msg: Message):
        raise NotImplementedError


class PublishInterface:
    def publish(self, post: Post) -> PublishResult:
        raise NotImplementedError

