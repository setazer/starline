import json
import logging
from dataclasses import dataclass
from urllib.parse import urlparse

import requests as requests

from starline.model import Post

log = logging.getLogger(__name__)


class Source:
    ALIAS = None
    DATA_CLIENT = None

    def __init__(self, *args, **kwargs):
        self.data_client = self.DATA_CLIENT(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __contains__(self, item):
        if isinstance(Post, item):
            return item.meta.source == self.ALIAS
        raise ValueError

    def post_belongs(self, post: Post):
        return post.meta.source == self.ALIAS

    def get_post(self, post_id):
        return self.data_client.get_post(post_id)


class DataClient:
    DOMAIN: str = None
    _POST_URL: str = None
    _POST_API_URL: str = None
    _SEARCH_API_URL: str = None
    _LOGIN_URL: str = None

    def __init__(self):
        self._session = None

    def get_full_url(self, path: str):
        parsed_url = urlparse(path)._replace(scheme='https')
        if not parsed_url.netloc:
            parsed_url = parsed_url._replace(netloc=self.DOMAIN)
        return parsed_url.geturl()

    @property
    def session(self):
        if self._session is None:
            self.switch_session()
        return self._session

    def switch_session(self):
        self._session = requests.Session()
        if self._LOGIN_URL:
            self.login()

    def stream_file(self, url, **kwargs):
        return self.session.get(url, stream=True, **kwargs)

    def login(self):
        raise NotImplemented

    def get_post(self, item_id):
        raise NotImplemented

    def search_items(self, query):
        raise NotImplemented

    @staticmethod
    def _get_json(response):
        try:
            data = response.json()
        except json.JSONDecodeError:
            log.error("Couldn't decode json response", exc_info=True)
            return None
        return data


@dataclass
class SourceCollection:
    sources: set[Source]

    def get_source_by_alias(self, alias):
        return next((source for source in self.sources if source.ALIAS == alias), None)

    def get_post_source(self, post: Post):
        return self.get_source_by_alias(post.meta.source)

    def get_source_by_url(self, url):
        return next((source for source in self.sources if source.data_client.DOMAIN in url), None)
