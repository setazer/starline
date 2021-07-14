from typing import Callable

from model import Post
from utils import prepare_logger, NamedSingleton

log = prepare_logger(__name__)


class StorageProvider:
    def __init__(self, storage, *args, **kwargs):
        self._storage = storage

    def __iter__(self):
        return iter(self._storage)

    def __contains__(self, item: Post):
        return item in self._storage

    def write(self, data):
        raise NotImplementedError

    def search(self, filter_=None):
        raise NotImplementedError

    def remove(self, filter_: Callable):
        raise NotImplementedError


class MemoryStorage(StorageProvider, metaclass=NamedSingleton):
    def __init__(self, name):
        self._name = name
        super().__init__(storage=set())

    def __iter__(self):
        return iter(self._storage)

    def __repr__(self):
        return "MemoryStorage({})".format(self._storage)

    def write(self, data):
        self._storage.add(data)
        log.info(f'stored {data} to {self._name}')

    def search(self, filter_=None):
        if filter_ is None:
            return self._storage.copy()
        return set(filter(filter_,  self._storage))

    def remove(self, filter_: callable):
        for item in self._storage.copy():
            if filter_(item):
                self._storage.remove(item)
