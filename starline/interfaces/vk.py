import requests
import vk_requests

from interfaces import PublishInterface
from model import PublishResult, Post


class VkDataClient:
    def __init__(self, token):
        self.api = vk_requests.create_api(service_token=token, api_version=5.131)

    def publish_post(self, filename, message, group, album):
        with open(filename, 'rb') as pic:
            upload_url = self.api.photos.getUploadServer(group_id=group, album_id=album)['upload_url']
            img = {'file1': (filename.name, pic)}
            response = requests.post(upload_url, files=img)
            result = response.json()
            result['server'] = int(result['server'])
            uploaded_photo = self.api.photos.save(group_id=group, album_id=album, caption=message, **result)
            photo_link = 'photo' + str(uploaded_photo[0]['owner_id']) + '_' + str(uploaded_photo[0]['id'])
            wall_post = self.api.wall.post(message=message, owner_id='-' + group, attachments=(photo_link,))
        return wall_post

    def get_albums(self, group, album_ids=()):
        return self.api.photos.getAlbums(owner_id='-' + group, album_ids=album_ids)['items']

    def create_album(self, group, name):
        new_album = self.api.photos.createAlbum(title=name, group_id=group,
                                                upload_by_admins_only=1, comments_disabled=1)
        return new_album


class VKClient(PublishInterface):
    def __init__(self, token: str, group_id: str, *args, album: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_client = VkDataClient(token)
        self.group_id = group_id
        self._album = album

    @property
    def album(self):
        if self._album is None:
            self._album = self.get_current_album()
        return self._album

    def publish(self, post: Post) -> PublishResult:
        msg = self.get_message(post)
        # Загрузка картинки на сервер
        wall_post = self.data_client.publish_post(post.file.name, msg, self.group_id, self.album)
        return PublishResult(success=True, extra={'wall_id': wall_post['post_id']})

    def get_current_album(self):
        albums = self.data_client.get_albums(self.group_id)
        latest_album = next((album for album in albums
                             if (album['title'].startswith('Feed #') and album['size'] < 10000)
                             ), None)
        if not latest_album:
            latest_feed_album = next((album for album in albums if (album['title'].startswith('Feed #'))), None)
            if not latest_feed_album:
                next_number = 1
            else:
                next_number = int(latest_feed_album['title'].replace("Feed #", "")) + 1
            latest_album = self.data_client.create_album(self.group_id, f"Feed #{next_number:03}")
        return str(latest_album['id'])

    def get_message(self, post):
        lines = []
        if post.meta.authors:
            lines.append("Автор(ы): " + ' '.join([f"#{author}" for author in post.meta.authors]))
        if post.meta.characters:
            lines.append("Персонаж(и): " + ' '.join([f"#{x}@ohaio" for x in post.meta.characters]))
        if post.meta.copyright:
            lines.append("Копирайт: " + ' '.join([f"#{x}@ohaio" for x in post.meta.copyright]))
        if not lines:
            lines.append("#ohaioposter")
        lines.append("Оригинал: " + post.meta.url)
        return '\n'.join(lines)
