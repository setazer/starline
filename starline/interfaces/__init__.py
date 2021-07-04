from model import Message


class MessageInterface:
    def send_message(self, msg: Message):
        raise NotImplementedError
