from interfaces import PublishInterface
from model import PublishResult
from utils import prepare_logger

log = prepare_logger(__name__)


class Channel:

    @property
    def enabled(self):
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def __init__(self, enabled, publish_interface: PublishInterface):
        self._enabled = enabled
        self.interface = publish_interface

    def publish(self, post) -> PublishResult:
        self.preprocess(post)
        result = self.process(post)
        self.postprocess(post, result)
        return result

    def preprocess(self, post):
        pass

    def process(self, post) -> PublishResult:
        log.debug(f'Posting {post} via {self.__class__.__name__}')
        result: PublishResult = self.interface.publish(post)
        log.debug(f'Posted {post} via {self.__class__.__name__}')
        return result

    def postprocess(self, post, result):
        pass
