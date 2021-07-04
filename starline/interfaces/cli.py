from model import Message, TelegramMessage
from . import MessageInterface


class Printer(MessageInterface):
    def send_message(self, msg: Message):
        print('Message:', msg.msg)


class TelegramPrinter(Printer):
    def send_message(self, tg_msg: TelegramMessage):
        print('Chat:', tg_msg.chat)
        print('Sender:', tg_msg.sender)
        super().send_message(tg_msg)
