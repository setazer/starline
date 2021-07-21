from pathlib import Path

from starline.sources import SourceCollection
from starline.exceptions import InvalidImage
from starline.model import Post
from starline.utils import get_image_hash, prepare_logger

log = prepare_logger(__name__)


class Loader:

    def __init__(self, images_path: Path, sources: SourceCollection):
        self.images_path = images_path
        self.sources: SourceCollection = sources
        self.images_path.mkdir(exist_ok=True)

    def load(self, post: Post):
        source = self.sources.get_post_source(post)
        if not source:
            raise ValueError
        post = source.get_post(post.meta.post_id)
        try:
            stream = source.data_client.stream_file(post.file.url)
            img, post.file.hash = get_image_hash(stream.raw)
            post.file.name = Path(self.images_path) / post.file.name
            img.save(post.file.name)
        except InvalidImage:
            post.file.valid = False
            log.error("Error loading image", exc_info=True)
        return post
