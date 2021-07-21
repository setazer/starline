from starline.exceptions import InvalidLogic
from starline.interfaces import MessageInterface
from starline.loader import Loader
from starline.logic import Logic
from starline.model import TelegramMessage, LoggingMessage, Post
from starline.queue_providers import QueueProvider
from starline.storage_providers import StorageProvider
from starline.utils import prepare_logger

log = prepare_logger(__name__)


class Client:
    def __init__(self, logic: Logic, loader: Loader, queue_provider: QueueProvider, history_provider: StorageProvider,
                 message_interface: MessageInterface):
        self.loader = loader
        self.logic = logic
        self.queue = queue_provider
        self.history = history_provider
        self.output = message_interface

    def got_message(self, message: TelegramMessage):
        log.debug(f"Got message: {message}")
        result_posts = self._parse_message(message)
        loaded_posts = self._load_posts(result_posts)
        self._add_posts_to_queue(loaded_posts)

    def _parse_message(self, message):
        result_posts = []
        for return_event in self.logic.parse_raw_message(message):
            result = return_event
            if isinstance(result, TelegramMessage):
                self.output.send_message(result)
            elif isinstance(result, LoggingMessage):
                log.log(result.level, result.msg)
            elif isinstance(result, Post):
                if self._check_post(result):
                    continue
                result_posts.append(result)
            else:
                raise InvalidLogic
        return result_posts

    def _load_posts(self, result_posts):
        loaded_posts = []
        for post in result_posts:
            loaded_post = self.loader.load(post)
            if loaded_post.file.valid:
                self.output.send_message(TelegramMessage(msg=f"Пост {post.meta.post_id} скачан"))
                loaded_posts.append(loaded_post)
        return loaded_posts

    def _add_posts_to_queue(self, loaded_posts):
        for post in loaded_posts:
            self.queue.put(post)
            self.output.send_message(TelegramMessage(msg=f"Пост {post.meta.post_id} добавлен в очередь"))

    def _check_post(self, result):
        if result in self.queue:
            msg = TelegramMessage(msg=f'Пост {result} уже в очереди!')
            self.output.send_message(msg)
            return True

        if result in self.history:
            msg = TelegramMessage(msg=f'Пост {result} уже был!')
            self.output.send_message(msg)
            return True
        return False
