from starline.model import TelegramMessage
from .. import MessageInterface


class TelegramInterface(MessageInterface):
    def send_message(self, tg_message: TelegramMessage):
        print(f'Message for: {tg_message.chat}', f'Message: {tg_message.msg}', sep='\n')

