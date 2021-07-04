import logging

from interfaces import MessageInterface
from starline.exceptions import InvalidLogic
from starline.loader import Loader
from starline.logic import Logic
from starline.model import TelegramMessage, LoggingMessage, Post

log = logging.getLogger(__name__)


class Client:
    def __init__(self, context):
        self.context = context
        self.loader: Loader = context.loader
        self.logic: Logic = context.logic
        self.output: MessageInterface = context.message_interface

    def got_message(self, message: TelegramMessage):
        result_posts = []

        for return_event in self.logic.parse_input(message):
            result = return_event
            if isinstance(result, TelegramMessage):
                self.output.send_message(result)
            elif isinstance(result, LoggingMessage):
                logging.log(result.level, result.msg)
            elif isinstance(result, Post):
                result_posts.append(result)
            else:
                raise InvalidLogic

        loaded_posts = []
        for post in result_posts:
            loaded_post = self.loader.load(post)
            if loaded_post.file.valid:
                loaded_posts.append(loaded_post)



