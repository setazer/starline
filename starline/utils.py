from pathlib import Path

from PIL import Image, UnidentifiedImageError
from imagehash import dhash

from exceptions import InvalidImage


def get_image_hash(image, size=8):
    try:
        image_fh = Image.open(image)
    except (UnidentifiedImageError, AttributeError):
        raise InvalidImage
    return image_fh, dhash(image_fh, hash_size=size)


class Context:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)