from urllib.parse import urlparse

from starline.sources import Source
from starline.sources.common.booru import BooruDataClient
from starline.model import Post, PostFile, PostMeta
from utils import prepare_logger

log = prepare_logger(__name__)


class DanbooruDataClient(BooruDataClient):
    DOMAIN = 'danbooru.donmai.us'
    _POST_URL = '/posts/{}'
    _POST_API_URL = '/posts/{}.json'
    _SEARCH_API_URL = '/posts.json?tags={}'
    _LOGIN_URL = '/session/new'

    def __init__(self, login: str, api_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._login = login
        self._api_key = api_key

    def get_post_id(self, url: str):
        url_obj = urlparse(url)
        return url_obj.path.rpartition('/')[-1]

    def get_post(self, post_id: str):
        response = super().get_post(post_id)
        return self._get_json(response)

    def login(self):
        headers = {'user-agent': 'OhaioPoster'}
        data = {'user': self._login,
                'api_key': self._api_key,
                'commit': 'Submit'}
        self.session.post(self.get_full_url(self._LOGIN_URL), headers=headers, json=data)


class Danbooru(Source):
    ALIAS = 'dan'
    DATA_CLIENT = DanbooruDataClient

    def get_post(self, post_id: str):
        post_data = super().get_post(post_id)
        pic = self.wrap_picture(post_data)
        return pic

    def wrap_picture(self, picture_info: dict):
        return Post(
            file=PostFile(
                name=f"{self.ALIAS}-{picture_info['id']}.{picture_info['file_ext']}",
                extension=picture_info['file_ext'],
                url=picture_info['file_url'],
            ),
            meta=PostMeta(
                source=self.ALIAS,
                post_id=str(picture_info['id']),
                url=self.data_client.get_post_url(picture_info['id']),
                authors=set(picture_info['tag_string_artist'].split()),
                characters=set(picture_info['tag_string_character'].split()),
                copyright=set(picture_info['tag_string_copyright'].replace('_(series)', '').split()),
                height=picture_info['image_height'],
                width=picture_info['image_width'],
            )
        )
