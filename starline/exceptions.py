
class InvalidImage(Exception):
    """Невалидное изображение"""


class NoPostsProvided(ValueError):
    """Не передан список постов для загрузки"""


class InvalidImageSource(ValueError):
    """Невалидный источник картинки"""


class InvalidLogic(Exception):
    """Логика вернула неверный результат"""
