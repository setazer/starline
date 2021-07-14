import collections

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

    def pop(self):
        raise NotImplementedError


class MemoryStack(QueueProvider, metaclass=NamedSingleton):

    def __init__(self, name):
        self._name = name
        super().__init__(collections.deque())

    def put(self, data):
        self._queue.appendleft(data)

    def pop(self):
        try:
            return self._queue.pop()
        except IndexError:
            return None
