from urllib.parse import urlparse, parse_qs

from starline.sources import Source
from starline.sources.common.booru import BooruDataClient
from starline.model import Post, PostFile, PostMeta
from utils import prepare_logger

log = prepare_logger(__name__)


class GelbooruDataClient(BooruDataClient):
    DOMAIN = 'gelbooru.com'
    _POST_URL = '/index.php?page=post&s=view&id={}'
    _POST_API_URL = '/index.php?page=dapi&s=post&q=index&id={}'
    _SEARCH_API_URL = '/index.php?page=dapi&s=post&q=index&tags={}'
    _LOGIN_URL = '/index.php?page=account&s=login&code=00'

    def __init__(self, login: str, password: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._login = login
        self._password = password

    def get_post_id(self, url):
        url_obj = urlparse(url)
        return parse_qs(url_obj.query)[b'id'][0]

    def login(self):
        headers = {'user-agent': 'OhaioPoster'}
        data = {'user': self._login,
                'pass': self._password,
                'commit': 'Log in'}
        self.session.post(self.get_full_url(self._LOGIN_URL), headers=headers, json=data)


class Gelbooru(Source):
    ALIAS = 'Gel'
    DATA_CLIENT = GelbooruDataClient

    def get_post(self, post_id):
        post_data = super().get_post(post_id)
        pic = self.wrap_picture(post_data)
        return pic

    def wrap_picture(self, picture_info: dict):
        # TODO
        return Post(
            file=PostFile(
                name=f"{self.ALIAS}-{picture_info['id']}.{picture_info['file_ext']}",
                extension=picture_info['file_ext'],
                url=picture_info['file_url'],
            ),
            meta=PostMeta(
                source=self.ALIAS,
                post_id=picture_info['id'],
                url=self.data_client.get_post_url(picture_info['id']),
                authors=set(picture_info['tag_string_artist'].split()),
                characters=set(picture_info['tag_string_character'].split()),
                copyright=set(picture_info['tag_string_copyright'].replace('_(series)', '').split()),
                height=picture_info['image_height'],
                width=picture_info['image_width'],
            )
        )
