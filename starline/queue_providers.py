from model import QueueItem, Post
from utils import NamedSingleton


class QueueProvider:
    def __init__(self, queue):
        self._queue = queue

    def __bool__(self):
        return bool(self._queue)

    def __len__(self):
        return len(self._queue)

    def __contains__(self, item):
        return item in self._queue

    def __iter__(self):
        return iter(self._queue)

    def put(self, item):
        raise NotImplementedError

    def get_item(self):
        raise NotImplementedError

    def remove(self, item):
        raise NotImplementedError


class MemoryQueue(QueueProvider, metaclass=NamedSingleton):
    def __init__(self, name):
        self._name = name
        super().__init__(list())

    def __contains__(self, item: Post):
        return next((queue_item for queue_item in self._queue if queue_item.post == item), None)

    def put(self, item):
        self._queue.append(QueueItem(post=item))

    def get_item(self):
        item: QueueItem = next((item for item in self._queue if not item.lock), None)
        return item

    def remove(self, item: QueueItem):
        self._queue.remove(item)
