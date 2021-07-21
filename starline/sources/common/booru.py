from urllib.parse import quote

from starline.sources import DataClient


class BooruDataClient(DataClient):

    def __init__(self, excluded_tags: set[str] = None):
        super().__init__()
        self._excluded_tags = excluded_tags or set()

    def get_post_url(self, post_id):
        return self.get_full_url(self._POST_API_URL.format(post_id))

    def get_post(self, post_id):
        response = self.session.get(self.get_post_url(post_id))
        return response

    def get_post_id(self, url):
        raise NotImplementedError

    def _search(self, query):
        response = self.session.get(self._SEARCH_API_URL.format(query))
        return response

    def search(self, tags: str):
        tag_list = [quote(tag) for tag in tags.split()]
        for excluded_tag in self._excluded_tags:
            tag_list.append(f'-{excluded_tag}')
        search_query = '+'.join(tag_list)
        return self._search(search_query)
