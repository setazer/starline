import logging

from PIL import Image, UnidentifiedImageError
from imagehash import dhash

from exceptions import InvalidImage


def get_image_hash(image, size=8):
    try:
        image_fh = Image.open(image)
    except (UnidentifiedImageError, AttributeError):
        raise InvalidImage
    return image_fh, dhash(image_fh, hash_size=size)


def prepare_logger(name):
    logger = logging.getLogger(name)
    # logger.propagate = False
    con = logging.StreamHandler()
    con.setFormatter(logging.Formatter("%(asctime)s  %(levelname)s  %(name)s\t\t%(message)s"))
    logger.addHandler(con)
    return logger


class NamedSingleton(type):
    _instances = {}

    def __call__(cls, name: str, *args, **kwargs):
        if name not in cls._instances:
            cls._instances[name] = super(NamedSingleton, cls).__call__(name, *args, **kwargs)
        return cls._instances[name]
