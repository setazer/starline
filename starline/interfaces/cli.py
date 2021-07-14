import config
from model import Message, TelegramMessage, PublishResult, Post
from . import MessageInterface, PublishInterface


class Printer(MessageInterface):
    def send_message(self, msg: Message):
        print('Message:', msg.msg)


class TelegramPrinter(Printer):
    def __init__(self):
        super().__init__()
        self.bot_chat = config.TELEGRAM_BOT_CHAT

    def send_message(self, tg_msg: TelegramMessage):
        if tg_msg.chat is None:
            tg_msg.chat = self.bot_chat
        print('Chat:', tg_msg.chat, end=', ')
        print('Sender:', tg_msg.sender, end=', ')
        super().send_message(tg_msg)


class CliPublisher(PublishInterface):
    def publish(self, post: Post) -> PublishResult:
        print(post, 'published!', sep=' ')
        return PublishResult(success=True, extra=None)
